"""Flat-file "databases" for the simulated Jira and Confluence.

Three JSON files under data/, each a plain list. No ORM, no schema migration:
a learner can open any of these files directly and see exactly what the app
sees. Seeded once, on first import, so a fresh clone starts from a known
scenario (one vague requirement page, one open ticket linking to it).
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

DATA_DIR = Path(__file__).parent / "data"
PAGES_PATH = DATA_DIR / "pages.json"
TICKETS_PATH = DATA_DIR / "tickets.json"
RUNS_PATH = DATA_DIR / "analysis_runs.json"

REQUIREMENT_PAGE_ID = "page-req-upload"
BOT_AUTHOR = "Requirements Analysis Agent (bot)"

# A fixed cast so ticket creation and page edits pick a name rather than type
# free text. Real Jira/Confluence pull this from account directory, not a
# text box.
PEOPLE = [
    "Dana (Product Manager)",
    "Jordan (Eng Lead)",
    "Priya (QA Lead)",
    "Sam (Backend Engineer)",
    "Morgan (Frontend Engineer)",
]


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _load(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    return json.loads(path.read_text())


def _save(path: Path, items: List[Dict[str, Any]]) -> None:
    path.write_text(json.dumps(items, indent=2))


def seed_if_missing() -> None:
    """Create the starting scenario the lesson is built around.

    One Confluence requirement page, deliberately vague, and one open Jira
    ticket that already links to it. This is the same "User Profile File
    Upload" requirement used in Lessons 2-4, so the ambiguities a learner
    sees the agent find here are ones they have already seen analyzed.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not PAGES_PATH.exists():
        _save(PAGES_PATH, [
            {
                "id": REQUIREMENT_PAGE_ID,
                "kind": "requirement",
                "title": "User Profile File Upload — Requirements",
                "linked_ticket": None,
                "versions": [
                    {
                        "n": 1,
                        "author": "Dana (Product Manager)",
                        "timestamp": now(),
                        "body": (
                            "Users shall be able to upload files to their profile.\n\n"
                            "Uploaded files should be stored securely.\n\n"
                            "The system should support common file types."
                        ),
                    }
                ],
            }
        ])

    if not TICKETS_PATH.exists():
        _save(TICKETS_PATH, [
            {
                "key": "REQ-104",
                "title": "Review requirements: User Profile File Upload",
                "description": (
                    "Please review the attached requirements doc for ambiguity "
                    "before implementation kicks off."
                ),
                "linked_page_id": REQUIREMENT_PAGE_ID,
                "assignee": "Jordan (Eng Lead)",
                "status": "Open",
                "comments": [],
                "created_at": now(),
                "last_analyzed_version": None,
                "last_run_id": None,
            }
        ])

    if not RUNS_PATH.exists():
        _save(RUNS_PATH, [])


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def load_pages() -> List[Dict[str, Any]]:
    return _load(PAGES_PATH)


def save_pages(pages: List[Dict[str, Any]]) -> None:
    _save(PAGES_PATH, pages)


def get_page(page_id: str) -> Optional[Dict[str, Any]]:
    return next((p for p in load_pages() if p["id"] == page_id), None)


def page_body(page: Dict[str, Any], version: Optional[int] = None) -> str:
    versions = page["versions"]
    if version is None:
        return versions[-1]["body"]
    return next(v["body"] for v in versions if v["n"] == version)


def add_page_version(page_id: str, body: str, author: str) -> int:
    pages = load_pages()
    page = next(p for p in pages if p["id"] == page_id)
    next_n = page["versions"][-1]["n"] + 1 if page["versions"] else 1
    page["versions"].append({
        "n": next_n, "author": author, "timestamp": now(), "body": body,
    })
    save_pages(pages)
    return next_n


def next_page_id(title: str) -> str:
    slug = "".join(c if c.isalnum() else "-" for c in title.lower()).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    base = f"page-{slug}" or "page"
    pages = {p["id"] for p in load_pages()}
    candidate, n = base, 2
    while candidate in pages:
        candidate = f"{base}-{n}"
        n += 1
    return candidate


def create_requirement_page(title: str, body: str, author: str) -> Dict[str, Any]:
    pages = load_pages()
    page = {
        "id": next_page_id(title),
        "kind": "requirement",
        "title": title,
        "linked_ticket": None,
        "versions": [{"n": 1, "author": author, "timestamp": now(), "body": body}],
    }
    pages.append(page)
    save_pages(pages)
    return page


def get_or_create_report_page(ticket_key: str, title: str) -> Dict[str, Any]:
    pages = load_pages()
    page = next(
        (p for p in pages if p["kind"] == "analysis_report" and p["linked_ticket"] == ticket_key),
        None,
    )
    if page:
        return page
    page = {
        "id": f"page-analysis-{ticket_key.lower()}",
        "kind": "analysis_report",
        "title": title,
        "linked_ticket": ticket_key,
        "versions": [],
    }
    pages.append(page)
    save_pages(pages)
    return page


# ---------------------------------------------------------------------------
# Tickets
# ---------------------------------------------------------------------------

def load_tickets() -> List[Dict[str, Any]]:
    return _load(TICKETS_PATH)


def save_tickets(tickets: List[Dict[str, Any]]) -> None:
    _save(TICKETS_PATH, tickets)


def get_ticket(key: str) -> Optional[Dict[str, Any]]:
    return next((t for t in load_tickets() if t["key"] == key), None)


def next_ticket_key() -> str:
    tickets = load_tickets()
    nums = [int(t["key"].split("-")[1]) for t in tickets if "-" in t["key"]]
    return f"REQ-{(max(nums) + 1) if nums else 100}"


def add_ticket(title: str, description: str, linked_page_id: str, assignee: str) -> Dict[str, Any]:
    tickets = load_tickets()
    ticket = {
        "key": next_ticket_key(),
        "title": title,
        "description": description,
        "linked_page_id": linked_page_id,
        "assignee": assignee or "Unassigned",
        "status": "Open",
        "comments": [],
        "created_at": now(),
        "last_analyzed_version": None,
        "last_run_id": None,
    }
    tickets.append(ticket)
    save_tickets(tickets)
    return ticket


def update_ticket(key: str, **fields: Any) -> None:
    tickets = load_tickets()
    ticket = next(t for t in tickets if t["key"] == key)
    ticket.update(fields)
    save_tickets(tickets)


def add_comment(key: str, author: str, text: str) -> None:
    tickets = load_tickets()
    ticket = next(t for t in tickets if t["key"] == key)
    ticket["comments"].append({"author": author, "text": text, "timestamp": now()})
    save_tickets(tickets)


def open_tickets_linked_to(page_id: str) -> List[Dict[str, Any]]:
    return [t for t in load_tickets() if t["linked_page_id"] == page_id and t["status"] != "Done"]


# ---------------------------------------------------------------------------
# Analysis runs (one entry per automation trigger)
# ---------------------------------------------------------------------------

def load_runs() -> List[Dict[str, Any]]:
    return _load(RUNS_PATH)


def get_run(run_id: str) -> Optional[Dict[str, Any]]:
    return next((r for r in load_runs() if r["id"] == run_id), None)


def runs_for_ticket(ticket_key: str) -> List[Dict[str, Any]]:
    return [r for r in load_runs() if r["ticket_key"] == ticket_key]


def find_run_by_report_version(report_page_id: str, report_version: int) -> Optional[Dict[str, Any]]:
    return next(
        (r for r in load_runs()
         if r["report_page_id"] == report_page_id and r["report_version"] == report_version),
        None,
    )


def add_run(run: Dict[str, Any]) -> None:
    runs = load_runs()
    runs.append(run)
    _save(RUNS_PATH, runs)
