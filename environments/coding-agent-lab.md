# environment.md — The AI Coding Lab, for lab authors and their coding agents

This document describes the **AI Coding Lab** (the `agentic-chat-ide` product) from the
point of view of someone building a *new lab* to run inside it. It is written to be
handed to a coding agent (Claude Code, OpenCode, Codex, …) at the start of a lab-authoring
session, so that the agent makes choices that fit this environment and writes those
choices into its own spec. It complements, and does not replace, the [README](README.md)
"Authoring a lab" section, which is the field-level reference for the file formats.

If you are the agent building a lab: read this whole file before drafting anything.
Section 10 is a checklist of what your lab spec must decide.

---

## 1. What the lab is

The AI Coding Lab is a browser IDE in which a **learner talks to a coding agent** that
builds software for them inside a sandboxed workspace. There is no terminal and no
notebook. The learner's only instrument is the chat; the agent does all reading, writing,
running and testing. The IDE is deployed one container per learner on DeepLearning.AI's
platform (Pantheon) and opened from a course page, on anything from a desktop browser to
a phone.

A lab is **content dropped into a generic image**, not a fork of the app:

| Piece | Where it lands | What it does |
|---|---|---|
| **Instruction artifact** (zip) | `/assignment` | `instructions.md` (the learner brief), optional `rubric.json` (grading), optional `resources.json` + `resources/` (visual aids) |
| **Workspace artifact** (zip) | `/workspace` | Starter code, datasets, step specs — anything the agent should find on disk |

Both zips are uploaded as course items and downloaded by an init container at sandbox
start. Zip the *contents* (files at the archive root, not nested in a folder). No image
rebuild is needed unless the lab needs heavy system dependencies (see §9).

The learner's experience, in order:

1. The IDE opens on an empty chat that says "Welcome to AI coding lab! Click on the button
   in the top left to open your instructions." (On phones a hint dot points at the
   Instructions tab.) **`instructions.md` is the front door of the lab.**
2. The learner reads the brief, copies a kickoff prompt from it, and sends it to the agent.
3. The agent asks design questions (rendered as clickable answer buttons), builds the app,
   serves it on port 4000, and the IDE's preview pane shows it live.
4. Optionally, the learner submits the workspace for grading and gets a rubric-scored
   report in the chat.

---

## 2. The three surfaces

**Sidebar** (left) has three tabs:

- **History** — the learner's chats. A learner can have many chats; each is an independent
  agent session (see §4).
- **Files** — the workspace tree. Clicking a file opens it in the artifact pane. Learners
  can create, rename, delete, and edit files, and download the project as a zip.
  Dependency and build directories (`node_modules`, `.venv`, `__pycache__`, `dist`, …) are
  filtered out; IDE-internal entries (`.chats`, `.git`, `.env`, `.agentic-chat-ide`) are
  never shown.
- **Instructions** — `instructions.md`, rendered as markdown. Static; it has no live state.

**Chat** (center): the thread. Assistant messages are markdown with syntax highlighting.
Tool calls (bash, read, write, edit, search, webfetch, …) render as collapsible cards.
Special constructs — answer buttons, "Learn more" chips, "Dive deeper" cards — are
described in §5. The header shows the model and running cost.

**Artifact pane** (right): shows one of

- a workspace file in CodeMirror (read-only by default, Edit toggle, Cmd/Ctrl+S saves;
  markdown gets a rendered preview), auto-opened on the first file the agent touches;
- a **learning resource** (an HTML page or image from the assignment) — see §5.3;
- the **live app preview** — an iframe of whatever is listening on port 4000 — see §6.

**Phones and tablets.** Below 1024px the sidebar becomes a drawer; below 768px the IDE is a
chat-first stack where files, resources and the app preview open as full-screen layers
with a Back button. Everything a lab ships (brief, resources, questions, preview) is used
on a 390px phone by real learners. See [MOBILE-SPEC.md](MOBILE-SPEC.md) for the details.

---

## 3. The assignment directory (`/assignment`)

Only these files are read. Anything else in the directory is ignored.

### 3.1 `instructions.md` (required)

Ordinary markdown, rendered in the Instructions tab and handed verbatim to the grader.
Three things make it more than a static page:

- **Copy pills on code blocks.** Every fenced code block gets a **Copy** button. On a phone
  the tap also closes the drawer and drops the text into the chat composer (creating a
  new chat if none is open). **Put the lab's kickoff prompt in the first code fence**, and
  one fence per step for multi-step labs, so the learner's action is one tap.
- **Resource markers** (`[phrase](resource:<id>)`, `[phrase](resource-inline:<id>)`) work
  here exactly as in chat (§5.3), so the brief can open a visual before the learner ever
  talks to the agent.
- **Images and other assets.** Anything under `/assignment` (dotfiles excluded) is served
  at `/api/instructions/assets/<relative path>`, so `![pet](/api/instructions/assets/imgs/pet.png)`
  works. Put images in a subfolder and include it in the zip.

Do **not** put a ` ```choices ` fence in `instructions.md`: the fence is parsed only in
assistant chat messages. In the brief it renders as a code block with a copy pill.

A good brief tells the learner: what they will build, roughly how long it takes, how the
lab is structured (steps and what each produces), the exact prompt(s) to send, the reminder
that the app must be served on **port 4000** to preview it, and how the work is evaluated.

### 3.2 `rubric.json` (optional)

```json
{
  "subject": "Memory service · spec + implementation",
  "emphasis": "One-line steer the grader reads before the dimensions (optional).",
  "dimensions": [
    { "name": "Spec completeness", "guide": "What the grader checks, in free text." },
    { "name": "Internal consistency", "guide": "…" }
  ]
}
```

Up to 8 dimensions; each is scored 0–10 by an LLM grader that explores the workspace
itself (§8). Missing or malformed ⇒ a generic four-dimension *spec-quality* rubric
(completeness, clarity, consistency, testability). Write `guide` as instructions to a
grader that will read the learner's files, not as a description for the learner.

### 3.3 `resources.json` + `resources/` (optional)

Registry of visual aids the IDE can open beside the chat:

```json
{ "resources": [
  { "id": "memory-types", "title": "The seven kinds of memory",
    "file": "resources/memory-types.html", "kind": "on-mention",
    "topics": ["the seven types of memory"] },
  { "id": "step1-toolbox-memory", "title": "Toolbox memory: SQL vs vector store",
    "file": "resources/step1-toolbox-memory.html", "kind": "dive-deeper",
    "topics": ["toolbox memory"] } ] }
```

- `id`: slug (`[a-z0-9_-]`), unique. Markers reference it.
- `file`: relative to `/assignment`; `.html`/`.htm` (fully self-contained) or
  `.png/.jpg/.gif/.webp/.svg`. Max 20 entries. Entries with a bad id, duplicate id,
  missing file, or unsupported extension are **silently dropped** — check
  `GET /api/resources` to see what registered.
- `kind`: `on-mention` (default) or `dive-deeper` — decides the affordance (§5.3).
- `topics`: phrases that tell the **agent** when to surface the resource. Entries with
  topics are listed in the agent's standing instructions; entries without topics are
  only ever opened from markers you write yourself.

**Building a resource page.** It is viewed in a same-origin iframe at anything from 320px
to a desktop pane, with no network access beyond the IDE origin. So: one file, inline CSS
and JS, no CDN or font fetches, a viewport meta tag, fluid layout with no horizontal
overflow at 320/480/800px, text ≥11px rendered, touch targets ≥44×44px, accessible names
and states on every control, keyboard reachable. Prefer one shared worked example that the
page reworks under each option over abstract prose — the page opens *next to a question*
and should show the learner how each answer plays out. `e2e/helpers/audit.js` exports
`assertWidgetAudit(page, id, width)` for checking these rules in Playwright.

---

## 4. The agent the learner talks to

**Engine.** OpenCode CLI (pinned, currently 1.15.x), run once per learner turn as
`opencode run --format json --session <id> --model <provider/model> "<message>"`.
The IDE is the only client; the learner never sees OpenCode's own UI.

**Models.** On the platform: OpenAI `gpt-5.6-luna` (default), `gpt-5.6-terra`, Anthropic
`claude-sonnet-5`, `claude-sonnet-4-6`, all through DeepLearning.AI's proxy with a
platform-injected token. Google is not available there. The learner can pick a model per
conversation from a picker. **Write specs that work on all four**, or say in the brief
which model the lab assumes. Locking the picker to one model is an image change (§9).

**Tools and permissions.** The agent has bash, file read/write/edit, glob/grep/list,
webfetch, websearch, todo, and skills. **Every tool is auto-allowed.** `opencode run` is
non-interactive: there are no permission prompts, and nothing pauses for approval. Assume
the agent will run whatever it decides to run.

**Standing instructions.** OpenCode reads `/workspace/AGENTS.md` at every turn. The IDE
**writes this file itself on every boot** from a fixed template plus a generated appendix
listing your topic-bearing resources. It tells the agent to:

- build only inside `/workspace` and never touch the IDE's own tree at `/app`;
- serve the app on **port 4000** bound to `0.0.0.0`, frontend and API from **one** server,
  long-running servers in the background;
- follow the user's persistence spec literally (in-memory means in-memory);
- reuse the preinstalled stack (§9) and create venvs with `--system-site-packages`;
- use the ` ```choices ` fence for every fixed-choice question, one question per message,
  fence last, then stop and wait (§5.1);
- mark the first substantive mention of each registered topic with a resource marker
  (§5.3).

Because the IDE rewrites `AGENTS.md`, **a workspace zip must not ship its own
`AGENTS.md`** — it will be overwritten. Lab-specific agent guidance goes into spec files
seeded into the workspace (§7) and into the kickoff prompt that tells the agent to read
them.

**What the agent cannot see.** `/assignment` is outside the workspace and is not readable
by the agent. If the agent needs the brief, the rubric, or any lab text, seed a copy into
the workspace.

**Sessions and memory.** One chat = one OpenCode session; context carries across turns in
that chat and survives the learner navigating away and back, page reloads, and container
restarts. A **new chat starts with no memory of earlier chats**. The only state that
crosses chats is what is on disk in the workspace. Design multi-step labs so that each
step can begin from the files alone (the memory lab's Step 2 spec opens with "read Step
1's configuration before asking anything; do not re-ask it").

**Resilience.** A turn that dies on a transient API error, or streams nothing for 180s, is
auto-retried in the same session up to 5 times. Long silent builds (a large `pip install`,
a model download) count as "nothing streamed" only if the agent emits no events at all;
in practice tool calls keep the turn alive.

**Shell containment.** `kill`/`pkill`/`killall`/`fuser` are shimmed so the agent cannot
kill the IDE's own processes. The agent runs as the non-root `learner` user.

---

## 5. Chat rendering features a lab should design around

These are the affordances that make a lab feel guided rather than free-form. A lab spec
should say explicitly where each is used.

### 5.1 The `choices` fence — clickable answers

An assistant message containing

````markdown
**Question 1 of 2 — Toolbox memory**

How should the agent find a tool it can't name? …explanation…

```choices
SQL table (SQLite)
Vector store (Chroma)
```
````

renders the fence as answer buttons. Exact behaviour, from the parser:

- The opening line is three backticks immediately followed by `choices`; the block ends at
  the next three backticks. One option per line; leading `-`, `*`, or `1.`/`1)` prefixes
  are stripped; blank lines are dropped. A fence with no options renders nothing.
- A click sends the option line **verbatim** as an ordinary user message. The learner may
  type a free-form answer instead. Specs must accept both ("a typed answer that names an
  option counts the same as a click").
- Buttons are enabled only on the **latest** assistant message while no turn is streaming.
  Older questions become inert, so the agent must not rely on the learner revisiting them.
- A line matching `**Question N of M …**` before the fence draws a **question box** around
  everything from that label through the buttons (and a following Dive-deeper card). Use
  the label to make multi-question sequences trackable; the count is how learner and
  agent both know nothing was skipped.
- The base `AGENTS.md` already tells the agent to use the fence for any fixed-choice
  question and to ask one question per message. A spec that says "use the interactive
  structured-question tool" maps onto this fence; the memory lab's specs spell out the
  fence explicitly anyway, which is more robust.

Design guidance: put explanation in prose *above* the fence, keep option labels short
(suffixes like "(course default)" / "(Recommended)" are fine), one decision per message,
and tell the agent what to do after each answer ("acknowledge and record — no
correction"). Explanations, considerations and trade-offs belong in the spec so the agent
has them to paraphrase.

### 5.2 Tool cards and file touches

Every tool call the agent makes is visible as a collapsible card. Writing a file also
opens it in the artifact pane on first touch. Nothing here needs authoring, but it means
the learner *sees* the agent read spec files and run tests — a lab can lean on that
("watch the agent run the Step 1 tests before it asks the next question").

### 5.3 Resource markers — "Learn more" and "Dive deeper"

A marker is a markdown link whose destination is a registered resource id:

| Marker | Resource `kind` | Renders as |
|---|---|---|
| `[phrase](resource:<id>)` | `on-mention` | The phrase as prose plus a small **Learn more** chip after it |
| `[phrase](resource:<id>)` | `dive-deeper` | The phrase as plain prose; a **Dive deeper** card (title + "See how this choice plays out") **below the answer buttons** of the last `choices` fence, or at the end of the message if there is none |
| `[phrase](resource-inline:<id>)` | any | A **Dive deeper** card **in place of the phrase**, at that position — put it on a line of its own |

Rules: unregistered ids degrade to plain text (a typo never breaks a message); markers are
ignored inside code blocks; the agent is told to use only listed ids, at most one marker
per resource per message, never inside a `choices` fence, heading, or code block, and
never to mention the syntax to the learner. Dive-deeper cards stay clickable on old
messages; Learn-more chips too.

Who writes markers: **you**, in `instructions.md` and in seeded spec files that quote the
exact marker for a specific message; **the agent**, for any resource with `topics`,
whenever it substantively discusses that topic. If a resource must appear at one precise
moment (e.g. a "why these are settled" card under a settled-architecture list), don't
rely on topic matching — put the literal marker in the step spec with a table of
"where → marker", as the memory lab does.

Where it opens: desktop and tablet in the artifact pane (replacing whatever file or
preview was there); phone as a full-screen layer with Back returning to the chat or the
Instructions tab with scroll position preserved.

### 5.4 Grading report

When a grading run finishes, a report card (overall score, verdict, per-dimension scores,
"what's working", "push further") renders at the bottom of every chat. See §8.

---

## 6. The app preview (port 4000)

The artifact pane can show the learner's running app. The rules are strict and the agent
is told them, but a lab's *starter code and spec* must obey them too:

- **One server, port 4000, bound to 0.0.0.0.** The IDE polls port 4000 every 3s and
  auto-reveals the preview when something starts listening. Nothing else is previewable.
  The default shape is a backend (FastAPI/uvicorn or Express) serving static files plus
  API routes. The agent is told to run a second process only if asked.
- **The preview is reverse-proxied**, not loaded from `localhost:4000`. The iframe (and
  "open in new tab") loads `/app-preview/` on the IDE's own origin, and the server forwards
  it to `127.0.0.1:4000`. Consequences:
  - **All URLs in the learner's app must be relative.** `<script src="static/app.js">` and
    `fetch("api/chat")`, never `/static/app.js` or `/api/chat` — a root-absolute path
    resolves against the IDE, where `/api/*` is the IDE's own API. The memory lab's starter
    app computes a base from `location.pathname` and prefixes every request with it. Put
    this rule in your spec and in any starter code.
  - **HTTP only.** WebSocket upgrades are not proxied. Streaming responses (SSE, chunked)
    are piped through and work; a Vite dev server with HMR does not.
  - The app is served under a path prefix; frameworks that assume they own `/` (client-side
    routers with absolute routes, absolute redirects) need configuring.
- A static site is fine (`python3 -m http.server 4000` serves an `index.html`), as long as
  it uses relative asset paths.
- On a phone the preview is a full-screen layer; on desktop it shares the artifact pane
  with files and resources. There is a reload button; the iframe also reloads when the
  server transitions from down to up.
- Port 8000 is also exposed by the local Docker image but the preview never loads it.

---

## 7. The workspace (`/workspace`)

- A persistent, learner-owned directory that the IDE git-inits as OpenCode's project
  root. It survives container restarts.
- **Seed files** from the workspace artifact (or the image's `data/` → `/workspace-seed`)
  are copied in with `cp -rn` on every start: **missing files are added, existing files are
  never overwritten.** A learner's edits persist; a lab update to a seeded file does not
  reach learners who already started.
- `.gitignore` gets IDE entries appended (`.opencode/`, `.chats/`, `.uploads/`,
  `.agentic-chat-ide/`, `.ide-state.json`). Don't fight this; a learner may add their own
  entries.
- Don't ship: `AGENTS.md` (overwritten, §4), `.env` (hidden from the file browser and a
  secrets hazard), `node_modules`/`.venv` (filtered from the tree and heavy in a zip).
- **Starter apps.** If the lab ships one, the kickoff prompt or a seeded spec must tell the
  agent it exists and that it is the thing to extend; otherwise the agent scaffolds a new
  app. Starter apps must already follow §6 (port 4000, relative URLs, one server).
- **Step specs.** The proven pattern for a multi-step lab is one markdown spec per step in
  the workspace root (`step-1-….md`, `step-2-….md`), each self-contained: context, what
  earlier steps already provide (reuse, don't re-create), the blocking questions with
  their exact fence text and resource markers, scope in/out, deliverables, component
  specs, tests, and a completion report. The brief's kickoff prompt for each step is
  "Read `step-N-….md` and follow it." Specs are addressed to the *implementation agent*,
  not the learner.
- **Skills.** The Customize panel lists workspace skills at
  `.opencode/skills/<name>/SKILL.md` (also `.claude/` and `.agents/`). A lab can seed a
  skill the agent should use; it is a lightweight alternative to a long spec for
  reusable procedure.

---

## 8. Grading

`POST /api/grading/submit` runs OpenCode once over the workspace with a grading prompt
built from the rubric, and stores a report at `/workspace/.agentic-chat-ide/grade.json`.
The grader is told to explore the workspace itself, read spec/markdown docs and app
source, ignore IDE files (`AGENTS.md`, dotfiles), and return JSON: `overall` 0–100, a
verdict (Strong ≥80, Solid ≥65, Developing ≥50, else Needs work), per-dimension 0–10
scores in rubric order, 2–4 "working" points, 2–4 "push further" points. The report
renders at the bottom of every chat; on a phone a toast announces it.

Things to know when designing for grading:

- The grader sees **the workspace and `instructions.md`**, nothing else. Decisions the
  learner made only in chat are invisible unless the agent recorded them in a file. Have
  the spec require a written record (a config module, a `DECISIONS.md`, a completion
  report) — this is also what lets later steps start from disk.
- The **in-UI "Submit for grading" button is currently disabled** (`GRADING_CTA_ENABLED`
  is `false` in `client/src/App.jsx`). Don't promise learners a button unless the lab's
  deployment flips it; grading can still be triggered via the API.
- Only one grading run at a time (a second submit returns 409); a run takes a minute or
  two.

---

## 9. The container

- Debian, non-root `learner` user, Node 22, Python 3 with pip and venv, sqlite3, git, curl,
  build-essential.
- **Preinstalled** (assume these, and say so in specs): Python `fastapi`, `uvicorn`,
  `python-dotenv`, `openai`, `anthropic`; Node globals `express`, `cors`,
  `better-sqlite3`, `vite`, `nodemon`. Nothing else — no torch, no vector stores, no
  embedding models — in the generic image.
- **Outbound network is available** (pip/npm installs work; the agent has webfetch), but
  each install costs the learner wall-clock time inside the lab. A dependency the agent
  will need on turn one should be preinstalled (image change) or the brief should warn
  about the wait.
- **Provider access from the learner's app.** The agent's environment — and therefore any
  app it starts — carries `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` and the matching
  `OPENAI_BASE_URL` / `ANTHROPIC_BASE_URL` pointing at the platform proxy. Apps that use
  the official SDKs with default env handling work unchanged; apps that hard-code
  `api.openai.com` or a model outside the platform's set fail. Tell the spec: read keys and
  base URLs from the environment, use one of the platform models, never ask the learner
  for a key.
- **Resources** (CPU/memory) are set per sandbox in the platform builder; the defaults
  suit a small Python/Node web app. Heavier stacks need more, and a memory-hungry step
  (loading an embedding model while running tests) can OOM-kill the agent's process.
- **Lab-specific image changes** (Pathway 2): heavy dependencies, a restricted or
  different model picker, a different default model, extra guidance in the base
  `AGENTS.md`. Each is a change to this repo plus an image rebuild, kept in sync across
  `Dockerfile` and `Dockerfile.pantheon` — see the README.

---

## 10. What a lab spec must decide (checklist for the authoring agent)

When you draft a lab for this environment, your spec should state each of these
explicitly. Defaults in brackets are the environment's conventions.

**Shape**
- [ ] What the learner builds, the number of steps, and what each step leaves on disk.
- [ ] Whether there is a starter app in the workspace zip [none], and if so its stack and
      how the agent is told about it.
- [ ] Stack for the built app [FastAPI or Express serving static + API on port 4000].
- [ ] Which platform model(s) the specs are validated against [all four; default gpt-5.6-luna].
- [ ] Any dependency beyond the preinstalled set, and whether it is installed live or
      requires an image change.

**Brief (`instructions.md`)**
- [ ] The kickoff prompt(s), one per step, each in its own fenced code block; the first
      fence is the first thing the learner copies.
- [ ] The port-4000 reminder and a one-line description of the preview.
- [ ] What resources the brief itself links, with markers.
- [ ] Images, placed under `/assignment` and referenced via `/api/instructions/assets/…`.
- [ ] Checked at 390px as well as desktop.

**Questions**
- [ ] Every fixed-choice decision the agent will ask, with the exact `**Question N of M —**`
      label, the prose considerations, and the fence text — one per message.
- [ ] What counts as settled (presented as information, no fence) versus asked.
- [ ] What the agent does after each answer, on pushback, and on a free-typed answer.
- [ ] Where answers are recorded on disk so later steps and the grader can see them.

**Resources**
- [ ] The registry: ids, titles, kinds, topics; which markers are author-placed (with a
      "where → marker" table in the step spec) and which are topic-triggered.
- [ ] Each page self-contained, tested at 320/480/800px, with a worked example that
      changes under each option.

**Agent guidance**
- [ ] Nothing in a workspace `AGENTS.md` (it is overwritten). Guidance lives in step specs
      and the kickoff prompt.
- [ ] Each step spec self-contained: context, what earlier steps provide, questions, scope
      in/out, deliverables, component specs, tests, completion report.
- [ ] Relative URLs and single-server rule restated for the built app.

**Grading**
- [ ] `rubric.json` with ≤8 dimensions whose guides tell the grader what to look for on
      disk.
- [ ] Whether the deployment has the grading button enabled; the brief's wording matches.

---

## 11. Pitfalls seen in real labs

- **Absolute URLs in the app.** Works when the agent tests with `curl localhost:4000`,
  breaks in the preview iframe. Put the rule in the starter code and the spec.
- **Shipping `AGENTS.md` in the workspace zip.** Silently replaced at boot; the guidance
  never reaches the agent.
- **Assuming the agent can read `/assignment`.** It cannot. Copy what it needs into the
  workspace.
- **Options outside the fence.** A list of choices in plain prose renders as prose; the
  learner has to type. The base `AGENTS.md` pushes hard on this, but specs should still
  show the fence literally.
- **Relying on old answer buttons.** Only the latest message's buttons are live; a "go
  back and change your Step 1 answer" flow must be a new question.
- **Topic-triggered markers for moment-specific cards.** Topic matching is fuzzy; if a
  card must appear under a particular paragraph, write the literal marker into the spec.
- **Resources that fetch anything.** A CDN script or web font makes the page blank inside
  the sandboxed iframe. Inline everything.
- **Silently dropped resource entries.** A bad id or missing file drops the entry with no
  error; markers then render as plain text. Check `GET /api/resources` after packaging.
- **Seeded files that need updating.** `cp -rn` never overwrites, so a fix to a seeded
  spec does not reach learners with an existing workspace. Version step specs by
  filename if you expect to iterate after launch.
- **Decisions that live only in chat.** New chats and the grader cannot see them. Require
  the agent to write them down.
- **First-turn installs.** A `pip install torch` on the first message can outlast the
  learner's patience and the idle timeout. Preinstall or warn.

---

## 12. Testing a lab before shipping

Locally (`npm run dev`, IDE at `http://localhost:5173`):

- Point `ASSIGNMENT_DIR` at your instruction artifact's contents (or replace
  `assignment/`), and copy your workspace artifact's contents into `workspace/`
  (local dev runs no seed step).
- `curl -s localhost:3000/api/resources` — confirm every resource registered.
- `curl -s localhost:3000/api/instructions` — confirm the brief loads.
- Run the lab end to end as a learner: kickoff prompt, every question via buttons *and* via
  a typed answer, preview appears on port 4000, resources open from both the brief and the
  chat, then `POST /api/grading/submit` and read the report.
- Resize to 390px and repeat the brief, one question, one resource, and the preview.
- `npx playwright test e2e/tests/shell-responsive.spec.js` covers the shell; add a spec
  that loops your registry through `assertWidgetAudit` at 320/480/800.

On the platform: build the two zips (files at the archive root), create a sandbox from
the prebuilt **Agentic Chat IDE** image with the Instruction Artifact URL and Workspace
Artifact URL set, size the resources, and run the same pass in the real container —
including one model other than the default.
