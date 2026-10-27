# Pattern card: Multi AI Agent Systems with crewAI

*Confirmed by the owner on 2026-10-27.*
*Drafted by a fresh general-purpose agent on Opus 5.5 (claude-opus-5-5) with guide v2.6, as `pattern-proposed.md`; each item reviewed with the owner one at a time.*
*Changes from the proposal:*
- *Program sentence: "returns the finished outcome" changed to "returns the finished results", because the final crew (Lesson 16) writes two separate results. Suggested by Claude (the orchestrator) and accepted by the owner.*
- *Item 1: the Lesson 7 quote was a paraphrase; replaced with the transcript's exact words. Suggested by Claude (the orchestrator) and accepted by the owner.*
- *Item 3: "and the run ends with one final outcome" changed to "The run finishes when every task is done", because Lessons 12 and 16 each produce two separate results; the Lesson 3 quote that supported only the removed part was dropped. Suggested by Claude (the orchestrator) and accepted by the owner.*
- *Offered from other lessons: memory and the QA reviewer agent. The owner's own choice from candidates Claude listed; the situation lines were suggested by Claude (the orchestrator) and accepted by the owner.*

*Lesson numbers are transcript numbers.*

*Reconfirmed by the owner, 2026-10-27, before the v2.7 regeneration: no changes.*

*Reconfirmed by the owner, 2026-10-27, before the v2.8 regeneration: no changes.*

**The one kind of program:** A program that takes a few named inputs for one job, runs a team of specialised AI agents through a set of defined tasks, passes each task's result on to the tasks that depend on it, and returns the finished results.

## What every build keeps

1. **The work is split across several specialised agents, and each agent has its own role, goal and backstory.** No single agent does the whole job.
   - Lesson 3: "you can have each agent be customized to do one single thing and do it well. You can have one agent, for example, being a researcher and another agent being a writer."
   - Lesson 5: "You shouldn't rely on one agent to do it all, but instead many agents that work better together."
   - Lesson 4: "When creating that instance, there are a few attributes that you really care about, namely the role, the go, and the backstory." and "agents perform better with role playing."
   - Lesson 7: "What are the actual people that you would hire to do this? And then once that you have those people in mind, think about what would be their goals. What would be their roles? What would be their backstories?"

2. **Every piece of work is a task with a clear description and a stated expected output, and each task is assigned to an agent.**
   - Lesson 4: "In the task expect at least three attributes. The description, the expected output, and the agent."
   - Lesson 11: "crewAI makes sure that it's mandatory for you to share at least two attributes on every task that you create. The description and the expected outcome."
   - Lesson 13: "we should be very much thinking about what are the clear descriptions and what is the clear expected output that we want to get for each and every one of them."

3. **Results move between agents: a task works from the outputs of the tasks it depends on and does not start until they are done. The run finishes when every task is done.**
   - Lesson 4: "the output of one task is going to be sent as part of the input for the next. So you really want to make sure that you get that right."
   - Lesson 16: "the resume strategy task is going to wait until both of those tasks finishes before it can actually move on and use those context in order to come up with a new strategy for your resume."
   - Lesson 15 (hierarchical run): "everything that the previous agents learned, is now being sent to this new agent. And all of that is being coordinated by this crew manager"

4. **One team definition serves any instance of the job: each run takes its named inputs and puts them in place wherever the agents and tasks use them.**
   - Lesson 4: "passing an input dictionary into the kickoff method. In this input we have all the variables that you interpolated throughout your tasks and agents."
   - Lesson 9: "these inputs are going to be used into any place in the tasks descriptions or the agents definitions."
   - Lesson 15: "Bring your stocks, the stocks that you care about. Play around with the initial capital. ... see how these agents behave differently, given the different inputs"

## Offered from other lessons

- **Memory (Lessons 5, 6, 9):** for a learner who wants the agents to remember earlier steps and past runs, so the crew improves with use.
- **QA reviewer agent (Lesson 6):** for a learner whose output reaches someone else, such as a customer, and should be fact-checked before it goes out.
