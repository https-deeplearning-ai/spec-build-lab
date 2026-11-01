# Pattern card: Agent Memory: Building Memory-Aware Agents

*Confirmed by the owner, 2026-10-23. Drafted by a clean-room generator (guide v2.4) from the materials, as 7 items. Claude (the orchestrator) suggested reducing it to the two items below, and the owner accepted each change:*
- *Dropped: separate memory kinds beyond the chat log (it would block the course's own chat-memory stage).*
- *Dropped: automatic per-conversation write-back with timestamps (item 1 covers its point).*
- *Dropped: labelled memory sections in the prompt.*
- *Dropped: at least one agent-chosen memory tool (it would block a "program does everything" option).*
- *Dropped: "shrinking never silently loses memory". (Corrected 2026-10-23: lossy summarizing is not excluded. The course states its cost, "we will always lose a little bit of information", but never shows it failing; its Lesson 6 demo shows the summarize-keep-expand method working. So lossy summarizing is offered, with that cost in its "pick this when".)*
- *Reworded: "the program reads memory automatically" became item 2 below, so agent-driven reading stays an option, with its cost.*

*All dropped items stay rules of the recommended build. Lesson numbers follow the transcripts.*


*Reconfirmed by the owner, 2026-10-31, before the v2.9 regeneration: no changes.*
**The one kind of program:** a tool-using agent whose memory lives outside the model, so it carries on across turns and sessions.

## What every build keeps

1. **Memory lives outside the model and survives the session.** What the agent learns in one turn or session is stored in persistent storage and is available to later turns and new sessions; nothing depends on the model or the process remembering it.
   - L1: "You need memory engineering, treating long-term memory as first-class infrastructure, external to the model, persistent and structured."
   - L2: "Turn 1 and 2 in a Memory-Augmented Agent would have been stored in an external memory source such as a database."
   - L2: "if a user was to interact with an agent and then leave and come back or start a new session, the information as to the user would be lost" (the stateless failure this prevents).

2. **Before the model answers, the memory relevant to the request reaches its context.**
   - L6: "At a start condition, when we are about to enter the Agent Loop, we typically would have memory operations that read from memory. This is because we're assembling context for our LLMs."
   - L2: "we reduce the amount of information we have to pass into the context window and only pass in one that are relevant to the interaction that have been stored in an external memory store."
