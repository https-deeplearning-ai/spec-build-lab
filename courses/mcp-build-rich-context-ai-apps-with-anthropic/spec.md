# Spec: MCP Research Chatbot — Standalone Takeaway

> **Self-contained spec.** Everything the building agent needs is in this file.
> Course material is condensed into the **Course Context Pack** below; the
> spec body never references "the course" or external lesson pages. `(CTX-X)`
> anchors mark course-derived knowledge; `[bracketed]` values are learner
> intake. **Provenance:** generated from the supplied notebook dump
> (`materials/notebooks/mcp-build-rich-context-ai-apps-with-anthropic-context.md`)
> and transcripts
> (`materials/transcripts/mcp-build-rich-context-ai-apps-with-anthropic-transcripts.md`)
> on 2026-06-29. Transcript lesson numbering is authoritative (CTX-E).

## Complete before handoff

The build is designed to work with neutral defaults. The following slots are
**[learner intake]** placeholders; the agent should keep them as written or
replace them in a single pass before building. None are load-bearing for the
acceptance criteria, but they sharpen the audience.

- `[learner project]` — what the learner is building this into (default: a
  standalone CLI research chatbot).
- `[learner data]` — additional MCP servers the learner wants connected
  beyond `filesystem`, `fetch`, and the in-repo `research` server (default:
  none).
- `[learner deploy target]` — where the optional SSE remote server is hosted
  (default: local-only; render.com configuration is included but not
  required to pass acceptance).

---

## 1. Objective

Build a **CLI MCP host** that connects to multiple MCP servers via a
declarative JSON config, then drives a conversational chatbot whose tools,
read-only resources, and prompt templates are discovered from those servers
at runtime — including an in-repo `research` MCP server exposing arXiv
paper search/lookup tools, two paper-data resources, and one search prompt
template (pattern: CTX-A).

### Not Included    ★

Out of scope for this build:

- **No web UI, no Claude Desktop integration as part of the deliverable.**
  Claude Desktop is a known *consumer* of the same `research` server (the
  config file format is identical), but the host/client we ship is the CLI
  chatbot, not Claude Desktop.
- **No OAuth 2.1, no roots, no sampling.** These are mentioned in the
  course as roadmap items; the build must not fake them.
- **No registry-API server discovery.** Servers are listed explicitly in
  `server_config.json`.
- **No vector store, no embeddings, no RAG.** Retrieval here means "an MCP
  tool returns paper metadata from arXiv"; do not confuse with vector
  retrieval.
- **No persistent conversation memory across CLI sessions.** Within a
  single `chat_loop()` run, prior turns are passed back to the model (R5);
  across runs, state is whatever the servers persisted to disk
  (`papers/*/papers_info.json`).
- **No tool-name collision resolution beyond detection.** If two servers
  expose the same tool name, fail loudly at startup (R6) rather than
  silently picking one.
- **No streaming UI for the LLM response.** Stdout-print the full response
  per turn.

---

## 2. Tech Stack & Versions

| Component | Pinned choice | Note |
| --- | --- | --- |
| Python | `>=3.10,<3.13` | the notebooks declared `python 3.11.11` in `runtime.txt` for the deploy step; 3.10+ is fine locally. |
| Package manager (local dev) | `uv` ≥ 0.4 | the materials use `uv init` / `uv venv` / `uv add` / `uv run` throughout. Treat `pip` + `venv` as a supported fallback; do not require `uv`. |
| Package manager (deploy) | `pip` | `render.com` does not support `uv` at the time of the materials; deploy uses `requirements.txt` (CTX-D). |
| MCP SDK (Python) | `mcp` (the official SDK) | unpinned in the notebooks. State plainly: the notebooks ran with whatever version `uv add mcp` resolved to at recording time; pin a recent stable version when building, and call out the unpinned origin in `requirements.txt` as a comment. |
| LLM client | `anthropic` (the official Python SDK) | unpinned in the notebooks. |
| Chatbot model | `claude-sonnet-4-6` | (CTX-D) the notebooks were *updated* from `claude-3-7-sonnet-20250219` after that model was deprecated. Use `claude-sonnet-4-6` as the default; allow override via env. |
| `max_tokens` per call | `2024` | exact value from every `client.messages.create(...)` in the notebooks. Honest note: this is almost certainly a typo for `2048`, but it's what the materials use; treat the magnitude as the load-bearing constraint, not the exact integer. |
| arXiv client | `arxiv` (Python SDK) | unpinned in the notebooks. |
| `.env` loader | `python-dotenv` | required for `ANTHROPIC_API_KEY`. |
| Async-in-Jupyter shim | `nest_asyncio` | required by the notebooks because they run async code in Jupyter; a pure-CLI build *can* drop it. Keep it as an optional import for parity. |
| Reference server: `filesystem` | `npx -y @modelcontextprotocol/server-filesystem .` | Node-based reference server, launched on demand by `npx`. Argument `.` scopes file ops to cwd (CTX-B2). |
| Reference server: `fetch` | `uvx mcp-server-fetch` | Python-based reference server, launched on demand by `uvx`. |
| Inspector (manual test only, not a build dep) | `npx @modelcontextprotocol/inspector` | used to hand-test the in-repo server. Not invoked from code. |
| Transport (local) | `stdio` | server launched as a subprocess of the client; the standard choice for local dev (CTX-C2). |
| Transport (remote, optional) | `sse` | `mcp.run(transport='sse')`, port `8001` from `FastMCP("research", port=8001)`. `streamable-http` is the forward direction; flag it in CTX-D and keep `sse` as the build default. |
| Secrets | `.env` for `ANTHROPIC_API_KEY` only | **never** committed; `.gitignore` MUST include `.env`. CI/deploy uses environment-variable injection (CTX-C1). |

---

## 3. Input/Output Contracts    ★

Three machine-readable contracts pin the build's surfaces. Agents
hallucinate shapes from prose; these are JSON-Schema-style and load-bearing.

### 3.1 `server_config.json` — multi-server registry

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "MCPServerConfig",
  "type": "object",
  "required": ["mcpServers"],
  "additionalProperties": false,
  "properties": {
    "mcpServers": {
      "type": "object",
      "minProperties": 1,
      "patternProperties": {
        "^[a-zA-Z0-9_\\-]+$": {
          "type": "object",
          "required": ["command", "args"],
          "additionalProperties": false,
          "properties": {
            "command": { "type": "string", "minLength": 1 },
            "args":    { "type": "array", "items": { "type": "string" } },
            "env":     { "type": "object", "additionalProperties": { "type": "string" } }
          }
        }
      },
      "additionalProperties": false
    }
  }
}
```

Notes:
- Each entry maps a *server name* to a `StdioServerParameters`-shaped
  dictionary (CTX-A step 3). Names MUST be unique within the file (object
  keys enforce that).
- The build's default `server_config.json` MUST contain three entries:
  `research`, `filesystem`, `fetch`, with the commands listed in §2.
- `filesystem`'s arg-list MUST include a directory path; in the default
  file it is `"."` (current working directory), which is a deliberate
  least-privilege choice (CTX-B2).

### 3.2 `papers_info.json` — per-topic arXiv cache

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PapersInfo",
  "description": "Stored at papers/<topic-snake>/papers_info.json. Keyed by arXiv short id.",
  "type": "object",
  "additionalProperties": {
    "type": "object",
    "required": ["title", "authors", "summary", "pdf_url", "published"],
    "additionalProperties": false,
    "properties": {
      "title":     { "type": "string", "minLength": 1 },
      "authors":   { "type": "array", "items": { "type": "string" }, "minItems": 1 },
      "summary":   { "type": "string", "minLength": 1 },
      "pdf_url":   { "type": "string", "format": "uri" },
      "published": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" }
    }
  }
}
```

The directory path is **deterministic and lowercased-with-underscores**:
`papers/<topic.lower().replace(" ", "_")>/papers_info.json` (R2). Multiple
topics → multiple folders, each with one `papers_info.json`.

### 3.3 The MCP surface exposed by the `research` server

The `research` server MUST expose **exactly** this surface. Names and arg
shapes are machine-checkable via `session.list_tools()`, `list_resources()`,
`list_resource_templates()`, `list_prompts()`.

```json
{
  "tools": [
    {
      "name": "search_papers",
      "input_schema": {
        "type": "object",
        "required": ["topic"],
        "properties": {
          "topic":       { "type": "string", "minLength": 1 },
          "max_results": { "type": "integer", "minimum": 1, "default": 5 }
        }
      },
      "returns": "array<string>  // arXiv short ids"
    },
    {
      "name": "extract_info",
      "input_schema": {
        "type": "object",
        "required": ["paper_id"],
        "properties": { "paper_id": { "type": "string", "minLength": 1 } }
      },
      "returns": "string  // JSON-stringified paper record OR a 'no saved info' message"
    }
  ],
  "resources": [
    { "uri": "papers://folders", "kind": "static",
      "returns": "markdown listing topic folders" }
  ],
  "resource_templates": [
    { "uri_template": "papers://{topic}", "kind": "dynamic",
      "returns": "markdown listing papers under the topic folder" }
  ],
  "prompts": [
    {
      "name": "generate_search_prompt",
      "arguments": [
        { "name": "topic",      "type": "string",  "required": true  },
        { "name": "num_papers", "type": "integer", "required": false, "default": 5 }
      ],
      "returns": "string  // a single user-message template instructing search_papers + summarize"
    }
  ]
}
```

### 3.4 The chatbot CLI command grammar

Inside `chat_loop()`, the user's input line is matched in this order:

```
quit                                  → exit
@folders                              → read resource papers://folders
@<topic>                              → read resource papers://<topic>
/prompts                              → list every server's prompts (name, args)
/prompt <name> [k=v]...               → invoke prompt <name> with kwargs, then send to LLM
<anything else>                       → ordinary chat turn (LLM may call tools)
```

Argument parsing: `/prompt name k1=v1 k2=v2`; whitespace-separated; the
first token after `/prompt` is the prompt name; remaining tokens are
`key=value` pairs (R3). Quoting is not required by the contract.

---

## 4. Business Rules

Each rule pins a behavior + the failure it prevents + AC mapping. Provenance:
*course-demonstrated* unless tagged *project hardening*.

- **R1 — The host discovers capabilities at runtime, never hardcodes them.**
  After `session.initialize()` on each connection, the host MUST call
  `list_tools`, `list_resources`, `list_resource_templates`, and
  `list_prompts`. Tool definitions passed to the model are built from the
  server's reply, not from a Python literal. (CTX-A step 4; CTX-B1.) → AC1, AC4.

- **R2 — `search_papers` writes a deterministic directory layout.**
  Given a topic string `T`, the tool MUST create
  `papers/<T.lower().replace(" ", "_")>/papers_info.json`, and MUST upsert
  records into the existing file rather than overwriting it. Each record
  has the shape from §3.2 and is keyed by `paper.get_short_id()`.
  → AC2.

- **R3 — Slash-prompts and at-resources are routed locally.**
  The chatbot CLI MUST recognise `@<x>` and `/prompts` / `/prompt …`
  *before* dispatching to the LLM. `@folders` → `read_resource("papers://folders")`.
  `@<topic>` → `read_resource("papers://<topic>")`. `/prompts` enumerates
  every connected server's prompts. `/prompt <name> [k=v]...` calls
  `get_prompt(name, args)`, takes the rendered text, sends it to the LLM
  as a user message, and prints the response. → AC6.

- **R4 — Tool calls are routed through the originating session.**
  The host maintains a `tool_to_session` map populated during connect; when
  the model emits a `tool_use` block, the host MUST look up the session
  for that tool name and call `session.call_tool(name, arguments=args)` —
  never the wrong session, never a direct in-process Python call. (CTX-A
  step 4; CTX-B3.) → AC4, AC5.

- **R5 — Multi-turn within a single CLI run preserves message history.**
  `process_query` MUST thread the running `messages` list through every
  `messages.create` call. Across `chat_loop()` iterations, the history
  resets — this is by design (Not Included). → AC7.

- **R6 — Tool-name collisions across servers are a startup failure.**
  *Project hardening.* If two connected servers each expose a tool with
  the same name, the host MUST print a clear error naming both servers
  and the conflicting tool, then exit non-zero before entering
  `chat_loop`. The course flagged this risk verbally (CTX-B5) but did not
  resolve it; the build's rule is to fail loudly rather than silently
  shadow one. → AC8.

- **R7 — Connections are torn down deterministically.**
  All client sessions and transports MUST be managed via a single
  `contextlib.AsyncExitStack`; `main()` MUST call `await stack.aclose()`
  in a `finally:` block, regardless of how `chat_loop()` exited. (CTX-A
  step 6.) → AC4 (implicit — no hung subprocesses).

- **R8 — `ANTHROPIC_API_KEY` is never hardcoded and never committed.**
  Key load order: real `os.environ` first, `.env` via `python-dotenv`
  second. `.gitignore` MUST contain `.env` and `papers/`. Code MUST NOT
  contain a string literal that looks like an API key. (CTX-C1.) → AC9.

- **R9 — Remote SSE is opt-in.**
  *Project hardening on top of course-demonstrated.* The `research` server
  ships with a single source file that supports both transports. The
  transport is selected by an environment variable, defaulting to `stdio`;
  `sse` activates port `8001` and `mcp.run(transport='sse')`. The local
  CLI host MUST work without ever starting the SSE variant. → AC10.

---

## 5. Acceptance Criteria    ★

### 5.1 Fixture corpus (the agent MUST author these before writing code)

Real arXiv calls require network. The acceptance suite MUST stub the
`arxiv.Client.results(...)` call so tests are deterministic. Fixture
content:

- **`tests/fixtures/papers/llm_reasoning/papers_info.json`** — pre-seeded
  by `conftest.py` for resource-read tests. Contains exactly two records
  keyed `2401.00001v1` and `2401.00002v1`, each conforming to §3.2.
- **`tests/fixtures/papers/ai_interpretability/papers_info.json`** — same
  shape, two records keyed `2402.00001v1` and `2402.00002v1`.
- **`tests/fixtures/server_config.fixture.json`** — references only the
  in-repo `research` server (no `fetch`, no `filesystem`) to keep the test
  matrix self-contained. Two-server collision tests synthesize a second
  fake server inline.
- **`tests/fixtures/arxiv_stub.py`** — replaces `arxiv.Client` with a fake
  whose `.results(...)` yields a hand-authored list of paper-shaped
  objects. Used to exercise `search_papers` end-to-end without network.

The build MUST NOT modify a fixture file to make a test pass; if a test
fails because the fixture lacks a record, the build is wrong, not the
fixture (CTX-B4).

### 5.2 Given / When / Then

| # | Given | When | Then |
|---|---|---|---|
| **AC1** | The `research` server is launched over stdio. | An MCP `Inspector`-style client initializes the session and calls `list_tools`, `list_resources`, `list_resource_templates`, `list_prompts`. | The returned names are *exactly* `{search_papers, extract_info}` for tools, `{papers://folders}` for resources, `{papers://{topic}}` for resource templates, `{generate_search_prompt}` for prompts; arg schemas match §3.3 byte-for-byte on `required` and `properties` keys. |
| **AC2** | `papers/` is empty; `arxiv.Client.results` is stubbed to yield two records. | `search_papers(topic="LLM Reasoning")` is invoked. | A file `papers/llm_reasoning/papers_info.json` exists; it parses as JSON; it contains both records; each record has `title`, `authors`, `summary`, `pdf_url`, `published`; `published` matches `^\d{4}-\d{2}-\d{2}$`. |
| **AC3** | `papers/llm_reasoning/papers_info.json` contains paper id `2401.00001v1`; `papers/ai_interpretability/papers_info.json` contains id `2402.00001v1`. | `extract_info("2402.00001v1")` is called. | Returns a JSON-stringified record whose `title` matches the `ai_interpretability` record; for a nonexistent id, returns a string starting with `There's no saved information related to paper `. |
| **AC4** | A `server_config.json` listing the `research` server only. | The host starts. | Stdout contains `Connected to research with tools: ['search_papers', 'extract_info']`; the host's `available_tools` has length 2; `tool_to_session['search_papers']` and `tool_to_session['extract_info']` reference the same `ClientSession` instance. |
| **AC5** | A user query "search for 2 papers on LLM reasoning" is sent to a host connected to the `research` server. | The LLM emits a `tool_use` block for `search_papers` with `topic="LLM reasoning"`, `max_results=2`. | The host invokes `session.call_tool("search_papers", arguments={"topic": "LLM reasoning", "max_results": 2})` on the *research* session — not via a direct Python call to the function. The returned content is appended to `messages` as a `tool_result` block with the matching `tool_use_id`. |
| **AC6** | The host is connected; `papers/llm_reasoning/papers_info.json` exists. | The user types `@folders` then `@llm_reasoning` then `/prompts` then `/prompt generate_search_prompt topic=physics num_papers=3`. | (i) `@folders` prints the markdown content of `papers://folders` including the line `- llm_reasoning`; (ii) `@llm_reasoning` prints the markdown content of `papers://llm_reasoning` including paper id `2401.00001v1`; (iii) `/prompts` lists `generate_search_prompt` with its two args; (iv) `/prompt …` fetches the rendered prompt text and dispatches it to the LLM (a single `messages.create` call observed). |
| **AC7** | The host has just answered "what is the title of paper 2401.00001v1?". | The user asks "and the authors?" without restating the paper id. | The follow-up `messages.create` call's `messages` parameter contains both turns of the prior exchange (assistant text + tool results from turn 1) plus the new user turn. |
| **AC8** | A `server_config.json` with two servers, both exposing a tool named `search_papers`. | The host starts. | The host writes a clear error (containing both server names and the conflicting tool name) to stderr and exits non-zero **before** `chat_loop()` is entered. Hangs and silent precedence are failures. |
| **AC9** | The repo as built. | `git check-ignore .env` and a regex scan of all tracked files for `sk-ant-` and `ANTHROPIC_API_KEY=` (followed by a value) are run. | `.env` is git-ignored; no tracked file contains an API key literal; `.env.example` contains the variable name but no value. |
| **AC10** | `CWYD_MCP_TRANSPORT=sse` env-var is set; the `research` server is started in a separate process. | A `sse_client` opens a session to `http://localhost:8001/sse` and calls `list_tools`. | The returned tool names are identical to AC1's stdio result. |

Each AC maps back to ≥1 rule (R1↔AC1,4; R2↔AC2; R3↔AC6; R4↔AC4,5; R5↔AC7;
R6↔AC8; R7↔AC4 implicit; R8↔AC9; R9↔AC10). Every rule has ≥1 AC.

---

## 6. Boundaries

### Always

- Always run capability discovery before exposing tools to the LLM (R1).
- Always reach a server's tool through the session that produced its
  definition; never call the tool's Python implementation directly from
  the host code path (R4).
- Always teardown sessions through `AsyncExitStack` (R7).
- Always load `ANTHROPIC_API_KEY` from environment, falling back to
  `.env`; reject startup with a clear error if neither is present (R8).
- Always preserve the conversation history within a single
  `chat_loop()` (R5).

### Ask First

These are course-demonstrated trade-offs that the materials flagged as
laterals or worse — they require an explicit human decision before
proceeding:

- **Use `streamable-http` instead of `sse`** for the remote transport.
  The materials state the Python SDK didn't support `streamable-http`
  at recording time (CTX-D); a build using it is forward-looking. Ask
  before switching.
- **Run real arXiv calls in tests.** The acceptance suite stubs
  `arxiv.Client`; running unstubbed tests adds network flakiness and
  rate-limit risk. Ask before un-stubbing.
- **Add a fourth MCP server** beyond `research`/`filesystem`/`fetch`.
  Each new server changes the tool surface the LLM sees and risks tool
  name collision (R6). Ask, and verify R6 still holds.
- **Persist conversation memory across CLI sessions.** The Not-Included
  boundary names this explicitly. Ask before adding it; if added, do not
  let it shadow the per-server `papers_info.json` files.
- **Drop `nest_asyncio`.** It exists for parity with the notebooks'
  Jupyter origin. Dropping it is safe in a pure-CLI build but should be
  an explicit decision.

### Never

- **Never** fabricate tool, resource, or prompt names in the `research`
  server beyond what §3.3 lists. The acceptance test asserts exact
  equality.
- **Never** silently resolve a tool-name collision by picking one. R6
  requires a hard error.
- **Never** commit `.env`, `papers/`, or anything else containing live
  API keys (R8).
- **Never** modify a fixture file to make a test pass. (§5.1.)
- **Never** hardcode tool definitions in the host. They MUST come from
  `list_tools` (R1). The notebook's pre-MCP "Chatbot Example"
  (L4 transcripts) hardcoded them — that is the *before* picture, not
  the target.
- **Never** strip the `tool_use_id` when appending a `tool_result` to
  `messages`. The Anthropic API requires the id to match.

---

## 7. Test Plan & Self-Verification

Run these commands top-to-bottom; report PASS/FAIL per AC with cited
evidence (stdout, file paths, exit code). "Should pass" / "looks correct"
are failures — they mean the step wasn't run.

```bash
# 0. One-time setup
cp .env.example .env                       # then fill in ANTHROPIC_API_KEY
uv venv && source .venv/bin/activate       # or python -m venv .venv && ...
uv pip install -r requirements.txt         # or pip install -r requirements.txt

# 1. Unit + integration test suite (all ACs except AC10 SSE)
pytest -q tests/                           # → expect 0 failed, ≥9 passed/skipped

# 2. Server surface check (AC1) — manual, requires Node
npx @modelcontextprotocol/inspector uv run research_server.py
# In the inspector UI: list tools/resources/prompts; compare against §3.3.

# 3. Host smoke test (AC4, AC5, AC6, AC7) — requires ANTHROPIC_API_KEY
uv run mcp_chatbot.py
#  > search for 2 papers on LLM reasoning
#  > @folders
#  > @llm_reasoning
#  > /prompts
#  > /prompt generate_search_prompt topic=physics num_papers=2
#  > quit
# Expect: tool calls fire on the research server; @ and / commands resolve locally; quit cleans up subprocesses.

# 4. Collision detection (AC8)
cp server_config.json server_config.bak
jq '.mcpServers += {"research_dup": .mcpServers.research}' server_config.bak > server_config.json
uv run mcp_chatbot.py ; echo "exit=$?"     # → nonzero exit; stderr mentions both servers and the conflicting tool name
mv server_config.bak server_config.json

# 5. Secret hygiene (AC9)
git check-ignore .env                      # → exit 0 (ignored)
grep -RnE 'sk-ant-[A-Za-z0-9_-]{8,}' --include='*.py' --include='*.json' --include='*.md' . && exit 1 || true
grep -RnE 'ANTHROPIC_API_KEY\s*=\s*[A-Za-z0-9]' --include='*.py' --include='*.md' . && exit 1 || true

# 6. SSE remote variant (AC10) — optional
CWYD_MCP_TRANSPORT=sse uv run research_server.py &
SERVER_PID=$!
sleep 1
pytest -q tests/test_sse_transport.py
kill $SERVER_PID
```

The build agent MUST cite, for each AC, the exact stdout line / file
content / exit code that proves PASS or FAIL.

---

## Course Context Pack (embedded — agent-readable)

Concepts only — no notebook code copied. Anchors are stable; insertion of
optional sections never breaks them.

### CTX-A. The pattern

A **rich-context AI app** uses MCP as the wiring between an LLM-driven
**host** and one or more **servers** that expose capabilities. The host
holds **clients**, each in a 1:1 connection with one server. The pipeline:

1. **Describe** capabilities on the server. The server author decorates
   pure Python functions to mark them as **tools** (callable side-effects
   or computations the LLM may invoke), **resources** (read-only data
   identified by a URI scheme, static or templated, that the application
   may inject into context without calling an LLM), and **prompts**
   (parameterised user-controlled message templates curated by the server
   so end-users don't have to write prompt-engineered queries from
   scratch). Each stage exists because LLMs need three different shapes
   of context: *act-on-the-world*, *look-something-up*, *use-a-canned-
   workflow*.
2. **Run** the server. Local servers communicate over the **stdio
   transport**: the client launches the server as a subprocess and
   exchanges JSON messages over stdin/stdout. Remote servers
   communicate over **HTTP+SSE** or the newer **Streamable HTTP**, the
   latter unifying stateful and stateless connections on top of plain
   HTTP POST/GET. The transport is a detail of the **how**, never the
   **what**: the same server file should be able to publish over
   stdio or sse.
3. **Configure** the host. A single JSON file lists every server the host
   should connect to, each entry naming the *command* and *args* used to
   launch it (or — for remote servers — the URL to dial). This is the
   "build once, use everywhere" tier: identical config schema is consumed
   by hand-rolled CLI hosts and by ready-made hosts like Claude Desktop
   or IDE-integrated agents.
4. **Discover** at runtime. For each configured server, the host opens a
   `ClientSession`, performs an `initialize` handshake, then calls
   `list_tools` / `list_resources` / `list_resource_templates` /
   `list_prompts`. Discovery is non-negotiable: hardcoding tools defeats
   the protocol's whole point of substitutability.
5. **Route** at call time. The host maps each discovered tool name to
   the session that produced it (`tool_to_session`). When the LLM emits a
   `tool_use` block, the host looks up the session and invokes
   `session.call_tool(name, arguments)`. Resource reads and prompt
   invocations are similarly per-session. Same shape, different
   primitive.
6. **Tear down** through a `contextlib.AsyncExitStack`. Multiple
   subprocesses + multiple async sessions = nested context managers; the
   exit stack registers them in connect order and closes them in reverse
   in a single `aclose()` call. Without it, signal handling and
   exception paths leak processes.

### CTX-B. Failure-mode catalog

The course planted fewer hard "failure → fix" pairs than a typical
RAG course; the protocol is the *removal* of an integration failure
mode. The catalogued items below are each demonstrated or explicitly
warned about in the materials.

- **CTX-B1 — Hardcoded tool schemas drift from the server.** The "Chatbot
  Example" lesson (L4 in transcripts) hand-writes a Python list of tool
  definitions matching the in-process functions; the next lesson moves
  the implementation behind MCP. If you copy the hardcoded shape into the
  MCP host, two sources of truth diverge the moment the server changes
  its surface. *Fix:* always derive `available_tools` from
  `session.list_tools()` (R1). *Enforced by* R1, AC1, AC4.

- **CTX-B2 — Filesystem server with no path scope = the world.** The
  `filesystem` reference server takes one or more directory paths as
  arguments; without them, an LLM-driven agent can read or write
  anywhere the host process can. *Fix:* always pass an explicit
  least-privilege directory (`.` for "this project only"). *Enforced
  by* the default `server_config.json` in §3.1.

- **CTX-B3 — Multi-server hosts pick the wrong session.** With multiple
  servers and dozens of tools, the LLM emits a `tool_use` with just a
  name; the host has to know which session owns that name. A naive
  "first session found" lookup silently routes calls to the wrong
  process. *Fix:* maintain an explicit `tool_to_session` map built
  during connect, queried on every tool call (R4). *Enforced by* R4,
  AC4, AC5.

- **CTX-B4 — Prompt mis-steering from generic terms.** The course
  demonstrates a query for "multi-concept pretraining" resolving to a
  different acronym than the user expected ("MCP" the protocol vs.
  "MCP" the ML technique); the lesson is *prompt engineering remains
  necessary even with rich context*. *Fix:* the prompt templates the
  server exposes should narrow the search frame; the host should pass
  rendered prompts through unchanged. *Enforced by* the prompt-template
  surface in §3.3 and AC6.

- **CTX-B5 — Tool-name collisions across servers.** Explicitly raised in
  the course's "Conclusion" / roadmap discussion: generic names like
  `fetch_users` may collide when multiple servers are connected. The
  course did *not* prescribe a resolution. This spec's R6 chooses
  hard-fail; CTX-D notes that namespacing is on the roadmap.

### CTX-C. Decision guides

- **CTX-C1 — Secrets handling.** `.env` + `python-dotenv` for local;
  platform env vars for deploy. `ANTHROPIC_API_KEY` is the only secret
  this build needs. Reference servers may need their own (`fetch` and
  `filesystem` do not).

- **CTX-C2 — Choosing a transport.** For local development, stdio is
  the default for one reason: the client owns the server's lifecycle
  via subprocess management. For multi-tenant or hosted deployments,
  the server is its own process and SSE / Streamable HTTP is required.
  Streamable HTTP is the forward direction; SSE remains the working
  baseline in the materials.

- **CTX-C3 — Multi-server hosts vs. a single per-app server.** The
  course recommends connecting to existing reference / community
  servers wherever possible (`filesystem`, `fetch`, etc.) rather than
  re-implementing their surfaces inside a custom server. Build the
  smallest server that wraps *your* data, and compose with the rest.

- **CTX-C4 — Resources vs. tools.** Use a resource when the data is
  read-only, addressable by a stable URI, and small enough to drop
  directly into context without a tool call. Use a tool when the
  operation is parameterised, mutates state, or wraps an external API
  call whose schema benefits from validation. The course uses
  *both* over the same data (papers): `extract_info` (tool) is the
  computational path; `papers://{topic}` (resource template) is the
  zero-LLM-call path.

- **CTX-C5 — `FastMCP` vs. the low-level server API.** The course uses
  `FastMCP` exclusively. The low-level API gives more control over
  `ListToolsRequest` / `CallToolRequest` handling at the cost of
  boilerplate. Default to `FastMCP`; do not reach for the low-level
  API unless a specific request shape is required.

### CTX-D. Perishable assumptions

Treat the names below as **search keywords against current docs**, not
guaranteed imports. The concepts in CTX-A…CTX-C are durable; only these
are perishable.

- `claude-3-7-sonnet-20250219` — the *original* model in the notebooks;
  deprecated in February 2026 per the notebooks' own deprecation
  banner; replaced by `claude-sonnet-4-6`. Re-check Anthropic's current
  model list before adopting either literal.
- `claude-sonnet-4-6` — the current default in the materials; verify
  against the Anthropic API model catalog at build time.
- `max_tokens = 2024` — almost certainly a typo for `2048`, present
  verbatim in every `messages.create(...)` call in the notebooks.
- `mcp` Python SDK — unpinned in the notebooks; expect API churn around
  `ClientSession`, `StdioServerParameters`, `stdio_client`,
  `sse_client`, `streamablehttp_client`, `FastMCP`.
- `mcp.client.sse.sse_client` — the SSE client used by the materials.
- `mcp.client.streamable_http.streamablehttp_client` — the
  forward-looking equivalent; the SDK didn't fully support it at
  recording time per the materials.
- `npx @modelcontextprotocol/inspector` — the manual-test inspector; the
  exact package name should be reverified.
- `@modelcontextprotocol/server-filesystem` (Node), `mcp-server-fetch`
  (Python, via `uvx`) — the two reference servers used; names mirror
  the org's GitHub package registry at recording time.
- `FastMCP("research", port=8001)` — the constructor used; the `port`
  kwarg is SSE-only.
- `mcp.run(transport='stdio' | 'sse' | 'streamable-http')` — the
  three transports the materials reference.
- `Streamable HTTP transport` — flagged as the recommended direction;
  the materials use SSE as a working substitute.
- `OAuth 2.1` for remote-server auth, `roots` (URI scoping that the
  client suggests to the server), `sampling` (server requests
  inference back through the client) — all flagged as roadmap, not
  built in this spec.
- `render.com` Python runtime needing `requirements.txt` + `runtime.txt`,
  no native `uv` support — the deploy story may shift.
- arXiv SDK calls: `arxiv.Client()`, `arxiv.Search(query=..., max_results=...,
  sort_by=arxiv.SortCriterion.Relevance)`, `paper.get_short_id()`,
  `paper.pdf_url`, `paper.published` — versioning unpinned; recheck
  before trusting field names.

**Nothing in CTX-A through CTX-C requires platform access; the spec is
self-contained.**

### CTX-E. Provenance map

Lesson titles in transcript numbering (transcripts are authoritative;
the notebook bundle's `Lesson Map` header is off-by-some due to a
"trap #1: lesson-numbering drift" — notebook `L3.ipynb` corresponds to
transcript Lesson 4, not Lesson 6 as the bundle's map claims).

| Transcript lesson | Title | Sourced into |
|---|---|---|
| L1 | Introduction | (framing only) |
| L2 | Why MCP | CTX-A intro; §1 Not Included |
| L3 | MCP Architecture | CTX-A.1, CTX-A.2, CTX-C2, CTX-C4 |
| L4 | Chatbot Example | CTX-B1 (the before-picture); §3.2; §3.3 tool surfaces |
| L5 | Creating an MCP Server | CTX-A.1, CTX-C5; §3.3 tool surfaces |
| L6 | Creating an MCP Client | CTX-A.4, CTX-A.5; R1, R4; AC1, AC4, AC5 |
| L7 | Connecting the MCP Chatbot to Reference Servers | CTX-A.3, CTX-A.5, CTX-A.6, CTX-B2, CTX-B3, CTX-C3; R4, R7; §3.1 |
| L8 | Adding Prompt and Resource Features | CTX-A.1 (resources/prompts), CTX-C4; R3; §3.3 resources/prompts; AC6 |
| L9 | Configuring Servers for Claude Desktop | §1 Not Included (we ship CLI, not Claude Desktop); §3.1 (same config schema is reused by Claude Desktop) |
| L10 | Creating and Deploying Remote Servers | CTX-A.2 (sse vs streamable-http); R9; CTX-D (transports, port 8001); AC10 |
| L11 | Conclusion | CTX-B5; CTX-D (OAuth, roots, sampling, registry as roadmap) |

---

## 8. Closing — Infra/Structure Diagram

The build is complete when the implementing agent emits the
infra/structure diagram of the running app, followed by the line:

> *This is the infra/structure diagram of this app.*

Suggested form: a text or mermaid diagram that names the host process,
each connected MCP server, the transport between each pair, the location
of `papers/`, and where `ANTHROPIC_API_KEY` enters the system. Anything
clearer is fine; the closing sentence is what `/extract-build-log` uses
as the default closing bookend when slicing the conversation.

---

### Status

- **Version:** 1.0 — generated 2026-06-29.
- **Course:** MCP — Build Rich-Context AI Apps with Anthropic.
- **Learner project:** `[learner project]` (default: standalone CLI MCP
  research chatbot).
- **Living document.** If the building agent produces something this
  spec did not anticipate — a contract that's too loose, an AC that
  doesn't catch the failure it was designed for, a CTX-D entry that has
  already gone stale — add the missing constraint here and regenerate.
  Specs are revised, not annotated.
