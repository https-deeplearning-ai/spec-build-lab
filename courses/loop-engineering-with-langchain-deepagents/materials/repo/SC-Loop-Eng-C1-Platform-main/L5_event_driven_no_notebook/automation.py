"""The automation bridge: the thing a real Jira/Confluence webhook would call.

This is the only place this lesson adds new agent-facing logic. Everything it
calls into (`run_verification_loop_live`, the rubric, the agent itself) is the
same execution + evaluation loop built in Lessons 3-4. What's new here is
wiring a trigger (a ticket created, or a linked page edited) to that loop, and
writing the result back as a Confluence page the agent owns rather than the
requirement page itself.
"""

import shutil
import sys
from dataclasses import asdict
from pathlib import Path
from uuid import uuid4

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import deepagent_helpers as dh  # noqa: E402

import data_store as store  # noqa: E402

RUN_WORKSPACE_ROOT = Path(__file__).parent / ".run_workspace"
AGENTS_BASELINE = REPO_ROOT / "workspace" / "memories" / "AGENTS.md"

MAX_RUBRIC_ITERATIONS = 2


def _fresh_workspace() -> Path:
    """One throwaway workspace per run, seeded with the tracked AGENTS.md.

    `build_review_agent` requires memories/AGENTS.md to already exist in the
    workspace it is given (`require_agents_file`), and a fresh directory per
    run means two tickets analyzed back to back never see each other's
    leftover /analysis.md.
    """
    run_dir = RUN_WORKSPACE_ROOT / uuid4().hex[:8]
    (run_dir / "memories").mkdir(parents=True, exist_ok=True)
    shutil.copy(AGENTS_BASELINE, run_dir / "memories" / "AGENTS.md")
    return run_dir


def _report_body(run: "dh.VerificationRun", ticket_key: str, requirement_version: int) -> str:
    banner = (
        f"> Generated automatically from {ticket_key} on {store.now()}.\n"
        f"> Source requirement: version {requirement_version}.\n"
        f"> Verification status: **{run.status or 'unknown'}** "
        f"after {len(run.grading)} grading pass(es).\n\n"
    )
    return banner + run.analysis_markdown


def run_automation(ticket_key: str) -> str:
    """Fetch the linked page, run the loop, write the report, update the ticket.

    Returns the new run's id. Raises if the ticket or its linked page is
    missing — there is no silent partial state to produce here.
    """
    ticket = store.get_ticket(ticket_key)
    if ticket is None:
        raise ValueError(f"No ticket {ticket_key}")
    page = store.get_page(ticket["linked_page_id"])
    if page is None:
        raise ValueError(f"Ticket {ticket_key} links to a missing page")

    requirement_version = page["versions"][-1]["n"]
    requirement_body = store.page_body(page)

    run_dir = _fresh_workspace()
    try:
        agent = dh.build_review_agent(
            rubric_iterations=MAX_RUBRIC_ITERATIONS,
            max_turns=40,  # several verification passes cost more turns than one review
            workspace_dir=str(run_dir),
        )
        result = dh.run_verification_loop_live(
            agent,
            requirement_doc=requirement_body,
            rubric=dh.DEFAULT_RUBRIC,
            workspace_dir=str(run_dir),
        )
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)

    report_page = store.get_or_create_report_page(
        ticket_key, title=f"Analysis Report — {ticket_key}"
    )
    report_body = _report_body(result, ticket_key, requirement_version)
    report_version = store.add_page_version(report_page["id"], report_body, store.BOT_AUTHOR)

    run_id = uuid4().hex[:8]
    store.add_run({
        "id": run_id,
        "ticket_key": ticket_key,
        "requirement_page_id": page["id"],
        "requirement_version": requirement_version,
        "report_page_id": report_page["id"],
        "report_version": report_version,
        "status": result.status,
        "turns": result.turns,
        "counts": result.counts,
        "trace": [asdict(step) for step in result.trace],
        "grading": [asdict(pass_) for pass_ in result.grading],
        "timestamp": store.now(),
    })

    store.update_ticket(
        ticket_key,
        status="Analysis Ready",
        last_analyzed_version=requirement_version,
        last_run_id=run_id,
    )
    store.add_comment(
        ticket_key,
        store.BOT_AUTHOR,
        f"Analysis complete ({result.status or 'unknown'}), requirement version "
        f"{requirement_version}. See {report_page['title']} in Confluence.",
    )
    return run_id
