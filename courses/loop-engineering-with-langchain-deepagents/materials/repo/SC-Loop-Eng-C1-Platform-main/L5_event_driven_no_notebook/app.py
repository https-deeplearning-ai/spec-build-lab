"""Lesson 5: the Automation Loop, played out across two simulated tools.

Run with `python app.py`, then open http://localhost:5050.

This app is two small surfaces sharing one JSON data store:

- /jira        a stand-in for a Jira project: tickets, statuses, comments.
- /confluence  a stand-in for a Confluence space: pages and their version
               history.

Creating a ticket, or editing a requirement page that an open ticket already
points at, calls `automation.run_automation`, which is the only place this
lesson adds logic: it fetches the linked page's current content, runs the
same execution + evaluation loop from Lessons 3-4, and writes the result back
as a new version of a Confluence page the agent owns. See automation.py and
data_store.py for the two moving pieces; this file is only routes.
"""

import difflib

from flask import Flask, flash, redirect, render_template, request, url_for

import automation
import data_store as store

app = Flask(__name__)
app.secret_key = "lesson-5-automation-loop"  # local demo only, never deployed

store.seed_if_missing()


# ---------------------------------------------------------------------------
# Landing page
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


# ---------------------------------------------------------------------------
# Jira
# ---------------------------------------------------------------------------

@app.route("/jira")
def jira_board():
    tickets = store.load_tickets()
    pages = [p for p in store.load_pages() if p["kind"] == "requirement"]
    return render_template("jira_board.html", tickets=tickets, pages=pages, people=store.PEOPLE)


@app.route("/jira/tickets", methods=["POST"])
def jira_create_ticket():
    ticket = store.add_ticket(
        title=request.form["title"].strip(),
        description=request.form.get("description", "").strip(),
        linked_page_id=request.form["linked_page_id"],
        assignee=request.form.get("assignee", "").strip(),
    )
    flash(f"{ticket['key']} created. Running the requirements agent now — this takes under a minute.")
    automation.run_automation(ticket["key"])
    return redirect(url_for("jira_ticket", key=ticket["key"]))


@app.route("/jira/<key>")
def jira_ticket(key):
    ticket = store.get_ticket(key)
    if ticket is None:
        return "Ticket not found", 404
    page = store.get_page(ticket["linked_page_id"])
    report_page = next(
        (p for p in store.load_pages() if p["kind"] == "analysis_report" and p["linked_ticket"] == key),
        None,
    )
    runs = sorted(store.runs_for_ticket(key), key=lambda r: r["timestamp"])
    latest_run = runs[-1] if runs else None
    return render_template(
        "jira_ticket.html",
        ticket=ticket, page=page, report_page=report_page,
        runs=runs, latest_run=latest_run,
    )


@app.route("/jira/<key>/rerun", methods=["POST"])
def jira_rerun(key):
    automation.run_automation(key)
    flash(f"{key} re-analyzed against the current requirement version.")
    return redirect(url_for("jira_ticket", key=key))


@app.route("/jira/<key>/close", methods=["POST"])
def jira_close(key):
    store.update_ticket(key, status="Done")
    flash(f"{key} marked Done by a human reviewer.")
    return redirect(url_for("jira_ticket", key=key))


@app.route("/jira/<key>/run/<run_id>")
def jira_run_detail(key, run_id):
    ticket = store.get_ticket(key)
    run = store.get_run(run_id)
    if ticket is None or run is None:
        return "Run not found", 404
    return render_template("jira_run_detail.html", ticket=ticket, run=run)


# ---------------------------------------------------------------------------
# Confluence
# ---------------------------------------------------------------------------

@app.route("/confluence")
def confluence_list():
    pages = store.load_pages()
    requirement_pages = [p for p in pages if p["kind"] == "requirement"]
    report_pages = [p for p in pages if p["kind"] == "analysis_report"]
    return render_template(
        "confluence_list.html",
        requirement_pages=requirement_pages, report_pages=report_pages, people=store.PEOPLE,
    )


@app.route("/confluence/pages", methods=["POST"])
def confluence_create_page():
    title = request.form["title"].strip()
    body = request.form["body"].strip()
    author = request.form.get("author") or store.PEOPLE[0]
    page = store.create_requirement_page(title, body, author)
    flash(f'"{page["title"]}" created. Link a Jira ticket to it to run the agent against it.')
    return redirect(url_for("confluence_page", page_id=page["id"]))


@app.route("/confluence/<page_id>")
def confluence_page(page_id):
    page = store.get_page(page_id)
    if page is None:
        return "Page not found", 404
    linked_ticket = None
    if page["kind"] == "analysis_report":
        linked_ticket = store.get_ticket(page["linked_ticket"])
    return render_template(
        "confluence_page.html", page=page, linked_ticket=linked_ticket, people=store.PEOPLE,
    )


@app.route("/confluence/<page_id>/save", methods=["POST"])
def confluence_save(page_id):
    page = store.get_page(page_id)
    if page is None or page["kind"] != "requirement":
        return "Only requirement pages can be edited here", 400

    body = request.form["body"]
    author = request.form.get("author") or store.PEOPLE[0]
    store.add_page_version(page_id, body, author)

    retriggered = []
    for ticket in store.open_tickets_linked_to(page_id):
        automation.run_automation(ticket["key"])
        retriggered.append(ticket["key"])

    if retriggered:
        flash(
            "Page saved. This page has an open linked ticket, so the automation "
            f"loop re-ran automatically for: {', '.join(retriggered)}."
        )
    else:
        flash("Page saved. No open ticket links here, so nothing was re-triggered.")
    return redirect(url_for("confluence_page", page_id=page_id))


@app.route("/confluence/<page_id>/compare")
def confluence_compare(page_id):
    page = store.get_page(page_id)
    if page is None:
        return "Page not found", 404
    a = int(request.args.get("a", page["versions"][0]["n"]))
    b = int(request.args.get("b", page["versions"][-1]["n"]))
    body_a = store.page_body(page, a)
    body_b = store.page_body(page, b)
    diff = list(difflib.unified_diff(
        body_a.splitlines(), body_b.splitlines(),
        fromfile=f"version {a}", tofile=f"version {b}", lineterm="",
    ))

    # For an agent-authored report, the bullet counts and verification status
    # recorded on the two runs behind these versions tell the "did anything
    # really change" story more clearly than scanning a text diff does.
    run_a = run_b = None
    if page["kind"] == "analysis_report":
        run_a = store.find_run_by_report_version(page_id, a)
        run_b = store.find_run_by_report_version(page_id, b)

    return render_template(
        "confluence_compare.html", page=page, a=a, b=b, diff=diff, run_a=run_a, run_b=run_b,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5050)
