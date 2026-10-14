# Diff analysis — clean-room regen (guide b03ddc9) vs shipped spec

- **NEW** = `experiments/agent-memory/regen-main-b03ddc9/spec.md` (this run).
- **SHIP** = `courses/agent-memory-building-memory-aware-agents/spec.md` (generated at guide `a7de8ef`, then hand-evolved; SHIP L7).
- Line numbers are written `N:<line>` and `S:<line>`.

## 1. Decision Ledger side by side

Rows are aligned by subject. Δ means the default or the option set differs.

| Subject | NEW row (category) | SHIP row (category) | Default NEW / SHIP | Options in brief NEW / SHIP | Δ |
|---|---|---|---|---|---|
| Project | L1 learner (N:68) | D1 learner (S:70) | same: research-assistant chat over the course's example shape | own domain + free text / own project | — |
| Data | L2 learner (N:69) | D2 learner (S:71) | same: synthetic fixtures | NEW names the course's 100-record dataset as the course option; SHIP names live arXiv ingestion | option wording |
| Goal | L3 learner (N:70) | D3 learner (S:72) | same idea: cross-turn recall, restart recall, expand after summary | — | — |
| Model/provider | L4 learner (N:71) | D4 learner (S:73) | NEW: OpenAI Chat Completions, "the specific model is chosen at gate time". SHIP: "`gpt-5-mini` for the agent loop + `gpt-5` for background memory operations" | NEW: OpenAI or any tool-calling provider. SHIP: also lists OpenAI-compatible endpoints | **Δ default** (SHIP pins course model names) |
| Environment | L5 learner (N:72) | D5 learner (S:74) | NEW: local, Python 3.10+ (§2). SHIP: "Python ≥ 3.11" | NEW: local / shared service. SHIP: local / container / server | Δ options |
| Scope boundary | L6 learner (N:73) | D6 learner (S:75) | same: keep as-is | same two paths | — |
| Store topology | D1 **design-structural** (N:74) | D7 **design-argued** (S:76) | same: seven per-type stores | NEW: seven stores / one similarity store with a type field. SHIP: seven types / "**conversational-memory-only** (the course's Lesson-2 baseline …)" / "any subset in between" | **Δ category and options** |
| Tool-description augmentation | D2 design-argued (N:75) | D10 design-argued (S:79) | same: augmented | same: augmented / raw | — |
| Who triggers each memory operation | D3 **design-argued** (N:76) | D8 **design-structural** (S:77) | NEW: the Lesson 6 app's split, with toolbox search harness-only. SHIP: the app's split **plus `read_toolbox` as an agent tool** | NEW: app split / also expose toolbox search / the Lesson 3 table's split. SHIP: app split / move operations | **Δ category, default and options** |
| Context reduction | D4 design-argued (N:77) | D9 design-argued (S:78) | same: recoverable compaction | NEW: compaction / lossy. SHIP adds a third: "pure compaction (offload raw content under an ID + description, no summary)" | Δ options |
| Persistent store | RR1 realization (N:78) | D11 realization (S:80) | same: stdlib SQLite, brute-force cosine, tier 1 | same: Oracle (course default) / tier 2 / tier 3 | — |
| Model the test suite runs against | **RR2 realization (N:79)** | **none**. SHIP declares the stubs as "[H] … project hardening" (S:460) | NEW: scripted stand-in | NEW: scripted / live course model | **only in NEW** |
| Web search (Tavily) | RR3 realization (N:80) | D12 realization (S:81) | same: omit | same three options: Tavily / stand-in / omit | — |
| Summary scope | C1 contradicted (N:81) | D13 contradicted (S:83) | same: thread-scoped | same: thread-scoped / global | — |

**Totals.** Both Ledgers have 14 rows. NEW has 13 subject rows in common with SHIP plus RR2. SHIP's extra 14th "subject" is the conversation-only option on its D7. Both specs have a topology row, so this is not a separate row; the difference is SHIP's category and options for it.

## 2. Not Included

- **NEW, 14 items (N:91–104).** Tag counts:
  - *named, never built*: 7 — hybrid search, re-ranking, graph traversal, semantic cache, forget/decay/merge, a tool-log reader, fine-tuning.
  - *owned by another row*: 4 — Tavily → RR3; Oracle and index → RR1; course dataset → L2; toolbox-as-agent-tool → D3.
  - *restorable*: 2 — web/GUI; multi-user/auth.
  - *unavailable*: 1 — integrating into an existing codebase.
- **SHIP, 10 items (S:105–114).**
  - named, never built: 5 (hybrid, reranking, semantic cache, decay/merge, fine-tuning).
  - owned: 3 (Tavily → D12; IVF/HNSW/Oracle → D11; bulk dataset → D2).
  - restorable: 1, a combined item: "Multi-user auth, concurrency, or a web/GUI frontend" (S:113).
  - unavailable: 1.
- **Present only in NEW:**
  - Graph traversal (N:93).
  - Tool-log reader (N:96). SHIP instead bakes in "Tool logs are **not** preloaded … (JIT-only by default)" (S:371) without listing a reader as excluded.
  - Toolbox search as an agent tool (N:101).
- **Moved between Ledger and list:**
  - *Toolbox search as an agent tool* is a Ledger option plus an *owned* list item in NEW (N:76, N:101). SHIP bakes it in as rule R10 (S:362–364) and lists it in D8's default (S:77).
  - *Conversation-only memory* is a Ledger option in SHIP (S:76). In NEW it is in neither the Ledger nor the list; it is a narrative line in the trade-off table (N:488).

## 3. Trade-off dispositions

SHIP has no mined trade-off table. Its CTX-C is background prose, and CTX-C12 "Instructor heuristics" (S:607) lists some subjects with no disposition. The table below compares NEW's table (N:487–507) with how SHIP handled each subject.

| NEW line | NEW disposition | SHIP handling | Same? | Guide rule that decided NEW's reading |
|---|---|---|---|---|
| T1 maturity ladder | narrative | CTX-A framing (S:574–578) | yes | — |
| T2 conversation-only vs multi-type | narrative (N:488) | **row option on D7** (S:76) | **no** | "`narrative` is reserved for subjects step (c) already excludes — framing, taxonomy, a maturity story". SHIP's reading rests on "an alternative the course demonstrates working at reduced scope and then **moves beyond** … remains a legitimate reduced-scope choice". |
| T3, T4 taxonomies | narrative | framing (S:574–577) | yes | — |
| T5 exact-key vs similarity for conversation | bake-in into D1's Invariant | in D11's Invariant (S:597) | yes | — |
| T6 deterministic vs agent-triggered | row D3, design-argued | row D8, **design-structural** | category differs | "When several routes apply, Category records the highest-precedence one: `design-argued > design-structural`". SHIP's own Trade-off cell says "argued in Lessons 3 and 6" (S:77). |
| T7 all tools vs retrieved | bake-in R6 | bake-in R9, plus AF4 "the course demonstrated" (S:516) | yes | Same outcome. NEW also records "A limit value that removes a component is a component choice". |
| T8 toolset size k | lever R6, k=5 | lever R9, k=5, branch 2 (S:358–361) | yes | — |
| T9 augmentation | row D2 | row D10 | yes | — |
| T10 local vs third-party tools | narrative (presentation only) | absent | no (SHIP silent) | "A subject the course argued that appears nowhere in this table is a defect". NEW judged it presented, not argued. |
| T11 lossy vs compaction | row D4 | row D9 (3 options) | yes (options differ) | — |
| T12 chars/token | lever R10 (spoken) | lever, but listed among "single-valued" values (S:437–438; AF5 S:517) | partly | "A trade-off about a value is a lever". NEW records it as a spoken two-value trade-off. |
| T13 summary prompt wording | narrative | CTX-C12 heuristic (S:607) | yes | — |
| T14 full tool output vs logged excerpt | bake-in R9 | bake-in R11 | yes | — |
| T15 route paper through the model vs store it | bake-in R20 | bake-in R17 (S:416–418) | yes | — |
| T16 HNSW vs IVF | bake-in inside RR1's course option | inside D11's Options (S:596) | yes | — |
| T17 workflow reuse | narrative | CTX-C12 heuristic | yes | — |
| T18 summary scope | row C1 | row D13 | yes | — |
| T19 cosine vs Euclidean | lever, branch 1 | lever, branch 1 (S:404–415) | yes | — |
| T20 chunk overlap | lever R20 | "single-valued" (S:438) | partly | "A trade-off about a value is a lever". |
| T21 same embedding model at ingest and query | bake-in R18 | R16 rule (S:404–406) | yes | — |
| (not a T-line) toolbox search as an agent tool | D3 option; default harness-only | **bake-in R10** (S:362–364) | **no** | The end-to-end app wins over the Lesson 4 notebook: "When both exist, the app config is the recommended starting point". SHIP applied that test to the entity and summary operations (S:599) but not to toolbox search. |
| (not a T-line) the model as keyed dependency | row RR2 | stubs labelled "[H] … project hardening" (S:460); six `live` ACs | **no** | "In standalone mode this is a `realization` row … scripted stand-in as Default". |

## 4. Rules and criteria

- **Counts:**
  - NEW: 23 rules, 34 ACs (AC32–AC34 `live`, so 31 offline).
  - SHIP: 18 rules, 25 ACs. Six are `live` (AC4, AC9, AC19, AC21, AC22, AC24, per S:540), so 19 are offline.
- **Rules only in NEW:**
  - R4's most-recent-10 window (project hardening) (N:306).
  - R16 harness supplies the thread id to `summarize_and_store` (N:318).
  - R19 seed-record ingestion (N:321).
  - R21 system prompt as a tested rule (N:323).
  - R22 arXiv candidate search as its own rule (N:324).
  - R23 the live model drives the same loop (N:325).
- **Rules only in SHIP:**
  - R10 toolbox search is agent-callable (S:362).
  - R15 grounding and abstention, a separate rule with live AC22 (S:399–403). NEW folds this into R21 (N:323) and the Never list.
  - R11's generalized hidden-thread-id injection, labelled "[H — constraint added 2026-09-09 …]" (S:371–380). NEW's R16 covers one tool only.
- **Criteria coverage.** NEW's scripted model gives the full Lesson 6 demo arc an offline oracle: summarize-by-tool (AC21) and "What was my first question?" (AC25). It also covers:
  - the exact 80.0 vs 80.1 threshold boundary (AC18);
  - thread isolation of summaries (AC20);
  - the generic-label fallback text (AC22);
  - an unknown tool name (AC16);
  - entity types reached by fixtures (AC27).

  In SHIP, entity extraction (AC19), grounding (AC22), conversational follow-up (AC4) and the end-to-end demo (AC21) are `live` only, so a key-less build never checks them. SHIP covers a few things NEW does not:
  - a write/read round-trip for every memory type across a restart (AC2, S:471);
  - a paraphrase retrieval check (AC23, S:492);
  - read_toolbox's registration (AC16, S:485).

## 5. What the three newest guide rules changed for this course

- **"three dispositions and no fourth" (§5.5).**
  - Subject touched: conversation-only vs multi-type memory (T2). The rule's exclusion of "a maturity story" put it at narrative in NEW. SHIP made the same subject a row option (S:76).
  - It also forced every argued subject into a table line with a named deciding test (N:487–507). SHIP has no such table to check against.
- **"a limit value that removes a component is a component choice" (§5.5).**
  - Subject touched: toolset size. "All tools in the prompt" is the setting that removes the retrieval stage.
  - The outcome did not change: it is a bake-in in both specs. NEW only records the branch (N:308, N:493).
- **"omission means leaving out the keyed tool, never the taught behavior" (§3).**
  - Subject touched: Tavily web search. Omission keeps search-and-store through the keyless arXiv fetch tool (N:80). SHIP already read it this way (S:81), so nothing changed.
  - The same clause also kept "omit" out of RR2's options (N:79), a row SHIP lacks.

## 6. Assessment

NEW differs in kind more than in quality: it makes the same core decisions (seven stores, SQLite substitution, compaction, thread scope, Tavily omitted, cosine, k=5). Its main structural gain for a learner is RR2. The scripted model turns the course's closing demo — summarize, then "What was my first question?" — into an offline test that passes or fails without a key, where SHIP tests it only live. Its main risk is the opposite reading of conversation-only memory (narrative here, a Ledger option in SHIP). On that subject the guide's two phrases, "maturity story" and "moves beyond … legitimate reduced-scope choice", still point in different directions. The owner should look first at T2 vs SHIP D7, because whether a learner is offered a conversation-only build depends on which of the guide's two phrases a generation reads as governing.
