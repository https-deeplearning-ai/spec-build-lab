# Lesson 5: The Automation Loop

A simulated Jira + Confluence, so this lesson runs with no Atlassian account
and no API tokens. The agent is the same Requirements Analysis Agent built in
Lessons 3-4 (`deepagent_helpers.py` at the repo root); the only new code here
is the automation trigger and the two small web UIs.

## What it demonstrates

- **Confluence** holds the requirement document. It is the source of truth;
  the agent only ever reads it, never edits it.
- **Jira** holds the ticket. Creating a ticket — or editing the linked
  requirement page while a ticket is still open — triggers the agent
  automatically.
- The agent writes its findings to a separate, agent-authored Confluence page
  (never into the requirement page itself), so Confluence's own version
  history shows every past analysis, who (or what) wrote it, and a diff
  between any two versions.
- A human, not the agent, decides when a ticket is actually Done.

## Running it

From the repo root, with the project's virtual environment active and
`OPENAI_API_KEY` set in `.env` (see the root README):

```bash
source venv/bin/activate        # or: venv/bin/python app.py below, without activating
cd lesson_5_event_driven
python app.py
```

Then open **http://localhost:5050**.

Each automation run makes live calls to the model (it is the Lesson 3-4
execution + evaluation loop under the hood), so creating a ticket or saving a
requirement edit takes under a minute, not instant. The UI tells you when a
run is in progress.

## A walkthrough to show learners

1. Open **Jira → Board**. There's one open ticket, `REQ-104`, linked to a
   vague requirement page.
2. Click into it. It's `Open` with no analysis yet.
3. Open the linked Confluence page in another tab. Read the requirement —
   three vague sentences about file upload.
4. Back in Jira, click **Create ticket** instead (or just wait — `REQ-104`
   was already created against this seed, so for a live first trigger, use
   **Re-run analysis now** on it). Watch the status move to `Analysis Ready`
   and a new "Analysis Report" Confluence page appear, authored by
   `Requirements Analysis Agent (bot)`.
5. Open that report page. Note the banner at the top: which ticket generated
   it, which requirement version it analyzed, and the verification status.
6. Go back to the Confluence requirement page and edit it — add a concrete
   file-size limit, say. Save.
7. Because `REQ-104` is still open and linked to this page, the agent reruns
   automatically. Go back to the ticket: a **"What changed since the previous
   run"** table shows the verification status and bullet counts side by side,
   a second run appears in **Run history**, and the report page now has a v2
   you can diff against v1 from its version history.
8. Note the bullet counts often look similar before and after (the agent
   finds roughly as many ambiguities either way) — the content changed
   completely even though the shape didn't. That's the point of showing both
   the counts table and the full text diff together, not just one or the
   other.
9. Only now does a human click **Mark Done** on the ticket — the agent never
   closes its own work.

Two more things to try: the **Create a new requirement page** form at the
bottom of `/confluence` (so you're not limited to the seeded scenario), and
the **Assignee** / **Written by** dropdowns, which pick from a small fixed
cast of people rather than free text.

## Files

- `app.py` — Flask routes for both simulated tools. No business logic lives
  here.
- `automation.py` — the trigger: what a real Jira/Confluence webhook would
  call. Fetches the linked page, runs the agent, writes the report back.
- `data_store.py` — the JSON "database" (`data/tickets.json`,
  `data/pages.json`, `data/analysis_runs.json`) and the seed scenario.
- `templates/`, `static/` — the two UIs, styled distinctly so they read as
  two different tools rather than two tabs of one app.

## Next step (not built here)

The same `automation.run_automation` function is the seam for a real
integration: swap `data_store`'s page/ticket lookups for the Confluence and
Jira REST APIs (the repo's `.env.example` already has placeholders for
`ATLASSIAN_EMAIL` / `ATLASSIAN_API_TOKEN` / `ATLASSIAN_SITE_URL`) and call it
from an actual webhook endpoint instead of a Flask form submit. Nothing about
the agent or the loop changes.
