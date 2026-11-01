# Pattern card: Evaluating AI Agents

*Confirmed by the owner on 2026-11-01.*
*Drafted by a fresh general-purpose agent on Opus 5.5 (claude-opus-5-5) with guide v2.9, as `pattern-proposed.md`; every quote checked against `materials/` by grep (all 15 found verbatim, each in the lesson claimed); the program scope and each item reviewed with the owner.*
*Changes from the proposal:*
- *Items 1 to 4 and the program sentence: kept as proposed. The owner's decision.*
- *"LLM judges return a label, never a numeric score" (Lesson 7): left off the card, as the proposal had it; it remains a rule of the recommended build, since the course forbids the alternative. Suggested by Claude (the orchestrator), accepted by the owner.*
- *Offered from other lessons: human labels (Lessons 7, 14). The owner's own choice from the candidates Claude listed (judge the judge, human labels, monitoring and CI gates); the situation line was suggested by Claude (the orchestrator).*

*Scope decision recorded for the generator: the program is the evaluation setup, and the course's sales-data agent is the sample instance. A learner may bring a different router-and-skills agent; the sales-data agent and its tools are rules of the recommended build, not essence. Framed by Claude (the orchestrator) and decided by the owner.*

*Lesson numbers are transcript numbers. Notebook quotes name the lab's transcript lesson.*

**The one kind of program:** A program that runs a tool-using agent (a router that picks among skills) over a fixed set of test questions, records every step of each run, scores the router's decisions, each skill's output and the path taken with separate evaluators, and shows the scores per agent version so that changes can be compared.

## What every build keeps

1. **The agent is judged part by part, not only by its final answer.** The router's choice of tool, the arguments it passes to that tool, and each skill's output each get their own evaluator, so a failure points to the part that caused it.
   - Lesson 1: "You'll then learn how to evaluate each tool in your agent workflow using different types of evaluators. You also evaluate if the router chooses the right tool based on the user's query, and if it extracts the right parameters to execute the tool"
   - Lesson 2: "you need to evaluate not just the LLMs raw output, but also how the agent decides on each action along the way."
   - Lesson 7: "Routers are typically evaluated in two different ways. First, you'll evaluate the function calling choice [...] The second kind of thing that gets evaluated in routers is typically the parameter extraction."
   - Lesson 8: "So at this point, you now have at least one evaluator set up for each main part of your agent."

2. **Every run leaves a record of its steps, and the evaluators score that record.** For each run the record holds the question, each router decision, each tool call with its arguments and result, the final answer and the number of steps; evaluators read the parts they judge from it.
   - Lesson 5: "these traces will become the bedrock that is used to run evaluation."
   - Lesson 8: "the pattern of evaluation in Phoenix typically involves exporting spans from your Phoenix instance, either using LLM as-a-Judge or a code-based eval to add labels to each row of those spans"
   - Lesson 12 (notebook, Lab 5): the task's output "is a dictionary that organizes the messages into these keys: "tool_calls", "tool_responses", "final_output", "unchanged_messages" and "path_length"."

3. **The path the agent takes is measured, not only what it outputs.** Similar questions are run through the agent, the steps of each run are counted, and each run is compared with the shortest path seen for that kind of question.
   - Lesson 1: "you can also evaluate the path taken by the agent to ensure it doesn't get stuck in a loop or repeat steps unnecessarily."
   - Lesson 9: "Convergence as a measurement for how closely your agent follows an optimal path for a given query."
   - Lesson 9: "you run each of these queries through your agent and record the number of steps taken for each of those queries, and then find the length of the optimal path taken. In this case, that's the minimum number of steps that your agent took"

4. **One fixed set of test cases is run through every version of the agent, and the scores are compared side by side.** A change to the agent (a prompt, a tool description, the model, the logic) is judged by re-running the same test set through all the evaluators and comparing the new version's scores with the old one's.
   - Lesson 2: "you want a consistent set of tests covering different user cases that get run every time you make a change."
   - Lesson 11: "Those evaluators will give you a set of scores that you can then use to compare the different iterations of your agent on an apples to apples basis."
   - Lesson 12: "you might want actually change this experiment name to say V2 [...] And then you can run that experiment again and you'll get a comparable line."

## Offered from other lessons

- **Human labels (Lessons 7, 14):** for a learner whose evaluators cannot settle a case alone, so a person reviews a queue of recorded runs and attaches a label or feedback that sits beside the evaluators' scores.
  - Lesson 7: "The third evaluation technique that you can use is using annotations or human labels. The idea here is that you can use tools like Phoenix or other observability platforms to construct a queue of lots of runs of your application to construct an annotation queue, and then have human labelers work their way through that queue and attach feedback, or judge the responses of your application."
  - Lesson 14: "You can take real usage data, for example, every user query or interaction, and attach human-labeled annotations to highlight issues or successes."
