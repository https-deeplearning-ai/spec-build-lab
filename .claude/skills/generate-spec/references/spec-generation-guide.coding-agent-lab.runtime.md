# Spec Generation Guide — `coding-agent-lab` runtime facts

**Companion to `spec-generation-guide.coding-agent-lab.md`.** Do not open this file until
**OVERRIDE 2 Phase 1 is complete** — every one of the six learner-context dimensions derived from
the course materials and written down. The rules file says when; this separation is why that
ordering is real rather than a request.

Everything here is `[environment]` provenance: contributed by the environment, never by the
course, and never co-labelled course-demonstrated.

Source: `environments/coding-agent-lab.md` §4, §5.1, §6, §9.

---

### The question mechanism — feeds base §6.0 unchanged

Base §6.0 already requires a structured question tool "if you have one". This environment has
one, so **this is an input to that rule, not an override of it.** The mechanism is a fenced
` ```choices ` block:

- Explanation in prose *above* the fence; the fence is **last** in the message; one option per
  line; the turn ends there.
- A line `**Question N of M — <decision>**` before the fence renders a question box. Use it, so
  learner and agent can both see nothing was skipped.
- A click sends the option line verbatim; a typed answer naming an option counts identically.
  The generated spec must say so.
- Only the **latest** assistant message's buttons stay live. A spec must never ask anyone to go
  back and change an earlier answer — re-ask as a new question.
- Never put a `choices` fence inside the spec's own examples in a way that implies the learner
  brief carries one; the fence is parsed only in assistant chat messages.

### The container — feeds spec §2

Debian, non-root user, Node 22, Python 3 with venv, sqlite3, git, build tooling.
**Preinstalled:** `fastapi`, `uvicorn`, `python-dotenv`, `openai`, `anthropic`; Node `express`,
`cors`, `better-sqlite3`, `vite`, `nodemon`. **Nothing else** — no vector stores, no embedding
models, no ML frameworks.

Outbound network works, so installs and one-time model downloads succeed, but each costs the
learner wall-clock time inside the session. A spec whose stack needs anything beyond the
preinstalled set must say so in §2 and tell the build agent to batch the install early and
announce its cost. Create venvs with `--system-site-packages` so the preinstalled stack is
reusable.

Memory is finite and shared with the agent's own process. A spec whose pipeline can hold several
models resident at once must carry a business rule releasing one before loading the next.

### Model / provider — facts only; the resolution is decided in ADD 1

**What this environment actually fixes:** the model *the coding agent itself* runs on. The learner
picks it per conversation from the platform's set, so a spec must work across all of them, or say
in its own text which it assumes. **Never bake a "current best" model name into the spec** — base
§6.0's gate-time "(Recommended)" flag already owns model currency.

**What it supplies:** the container exports provider API keys and their base URLs. If the built
app needs an LLM, the spec says: read keys and base URLs from the environment, use a platform
model, **never ask the learner for a key**.

**What it does NOT fix:** any model the course's own pipeline uses — embedding, speech, vision.
Those remain a genuine decision with a real invariant and a real switching cost. If the course's
pipeline needs no LLM, say so plainly, add a rule that the ambient keys are not to be read, and
**keep the model/provider Ledger row** — see ADD 1's conditional test, which is the authority
here. Do not read this section as licence to resolve that row CONSTRAINED by default.

### The app preview — feeds spec §4 business rules

- **One server, port 4000, bound to `0.0.0.0`**, serving both the page and the API. Nothing
  else is previewable.
- **Every URL inside the page must be relative** (`api/thing`, never `/api/thing`). The preview
  is reverse-proxied under a path prefix, so a root-absolute path resolves against the IDE.
  This is the single most common way a working app appears broken; it belongs in the spec as a
  numbered business rule with an acceptance criterion, not as a note.
- HTTP only — WebSocket upgrades are not proxied. Streaming responses work.

### The workspace — feeds spec §6 permissions

- **The workspace is the record.** A new chat starts with no memory of an earlier one, and the
  grader sees only what is on disk. Decisions, resolved values and results must be written to
  files, not left in chat. Base §6.0 already requires `resolved-decisions.md`; state *why* it is
  load-bearing here.
- **Never author `AGENTS.md`** in the workspace — the IDE rewrites it at every boot, so guidance
  placed there is silently lost. This belongs in the spec's **Never** tier.
- Every tool call is visible to the learner, and long-running servers run in the background.

---
