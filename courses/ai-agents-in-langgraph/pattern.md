# Pattern card — AI Agents in LangGraph

*Confirmed by the owner on 2026-11-03.*
*Drafted on 2026-11-02 by a clean-room general-purpose agent on Claude Opus 5.5 from the card prompt (`pattern-proposed.md`). Every transcript quote was checked against `materials/` by grep before the owner saw it; all were present and read as claimed.*
*Changes from the proposal:*
*- The program: the owner chose the Lesson 7 essay writer over the Lessons 2–6 tool-calling research assistant (the generator's recommendation, agreed by the owner).*
*- Item 3: "Web research grounds the writing" reworded to "Research grounds the writing", so a learner path that researches from their own documents still keeps the card; suggested by Claude (the orchestrator) and accepted by the owner.*
*- All seven items kept as proposed; the orchestrator suggested folding them to four and the owner chose to keep seven ("if more items can frame the spec better, we can do it"): the owner's own edit.*
*- "Offered from other lessons": the agentic research node and approval before each search were suggested by Claude (the orchestrator) and accepted by the owner; streaming output was the owner's own edit.*

**The one kind of program:** A program that produces a written piece on a topic the user gives (the course's example: a short essay) by passing it through separate LLM roles in a fixed, looping flow: plan, research the web, draft, critique, research again, redraft. It stops at a revision limit and saves every step, so a person can pause the run, edit it, and go back to an earlier step.

## What every build keeps

**1. Fixed flow with one decision point, through separate roles that share one record.**
Every run follows the same order: plan → research → draft → decide. If the run continues, the order is critique → research → draft → decide again. The only branch is the decision after each draft: finish, or go round again. Each step is its own LLM role with its own instructions (planner, researcher, writer, critic). The roles pass work to each other only through one shared record of the run: task, plan, research, draft, critique and revision count.
- L7: "So after the generation step we're either going to finish or we're going to go into this critique loop."
- L7: "So we're going to want to keep track of a bunch of different things. First, we're going to keep track of the task. This is the human input. This is what we're trying to write an essay about."
- L9: "A multi-agent architecture is when multiple different agents work on the same shared state. And so these agents could be just a prompt and a language model as they were in the writer."
- L3: "Crucially, it allows for really controlled flows."

**2. A plan is made once, before any research or drafting, and every draft follows it.**
- L7: "So first we're going to generate a plan for the essay. This is going to happen once upfront."
- L7: "We're going to follow the plan using the documents that we researched. And we're going to write the essay."
- Notebook, L7 cell 14: the writer's input is the task followed by "Here is my plan:" and the plan.

**3. Research grounds the writing, and the research only grows.**
Before the first draft, and again after every critique, the program writes a few search queries, runs them, and adds the results to the research gathered so far. Earlier research is never dropped. Every draft is written with all the research gathered so far.
- L7: "Then based on that plan we're going to do some research. This involves calling Tavily and getting back some documents."
- L7: "Then based on that critique, we're going to do another research step with Tavily, and get another set of documents. We're going to append those to the existing set of documents"
- L4: "First, the data on this is dynamic. So we couldn't, for instance, ask about the scores from the game last night."
- Notebook, L7 cells 13, 14, 16: queries are generated as a list, each is searched, and the result contents are appended to `content`. The writer's instructions include all of `content`.

**4. Critique drives each revision.**
After a draft, if the run continues, a critic role writes a critique of that draft. The next draft is written only after that critique has been turned into new research.
- L7: "If we continue, we're going to go into a reflect node where we're going to generate a critique of the current essay."
- L7: "…go all the way back to the generate step, where we're going to once again try to write this essay."
- L1: "Reflection, which refers to iteratively improve a result, possibly with multiple LLMs critiquing and making useful suggestions to drive that type of editing cycle."

**5. The loop is bounded by a revision count kept in the record.**
Each draft adds one to the revision count. After each draft, the program compares that count with the maximum given for the run, then ends or goes round again. Every run ends.
- L7: "So revision number, which is going to keep track of the number of revisions we've made and max revisions, which is keeping track of the maximum revisions that we want to make."
- L7: "This is going to look at the revision number. And if it's greater than the number of max revisions, we're going to end. If not, we're going to go on to reflect."
- L7: "And we've only told it to do two drafts. So this is the final one. It ends after this."

**6. Every step is saved, per thread.**
The record is saved after every step under a thread id. Continuing a thread resumes it with its full history. A different thread is a separate piece of work with no shared history.
- L5: "A check pointer basically checkpoints the state after and between every node."
- L5: "That's because it doesn't have access to any history. And that's because we're using a separate thread ID."
- L7: "Now you'll notice that we have two different threads to choose from. We have thread zero which is a pizza shop, and then one which is the New England IPA topic."

**7. A person can stop, inspect, edit and rewind the run.**
The run can stop after any step the person chooses. The person can then view the current record, change a field (for example the plan), and continue from the changed record. They can also pick an earlier step's saved record and continue from there. An edit or a rewind adds a new latest record and never erases the history.
- L7: "So when we're compiling the graph, we have "interrupt after set" for each of the states. after each state it'll stop."
- L7: "you can now update the state if you hit this modify button, that will run the update state command that we had seen earlier."
- L7: "So maybe we want to go back to the beginning. So with this update state from Tab, you can go back to the original planner state."
- L6: "So when we modify the state, we actually created a new state. And that became the new state."
- L6: "It allows you to go back to a previous point in time, and by editing, it allows you to correct what it has done."

## Offered from other lessons

- **Agentic research node (Lessons 2 and 3):** the research step becomes an LLM that decides its own searches until it has enough, capped by a turn limit, instead of a fixed list of queries. For a learner whose topics need follow-up searches that cannot be planned in advance.
- **Approve before each search (Lesson 6):** the research step stops between generating the queries and running them, so a person can see, edit or drop queries before any search fires. For a learner whose searches cost money or quota, or whose topics need the queries vetted.
- **Streaming output (Lesson 5):** steps or tokens are shown as they happen. For a learner who wants to watch a long run in progress rather than wait for it to finish.
