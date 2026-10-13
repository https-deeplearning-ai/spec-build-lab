# Slide descriptions: Loop Engineering with LangChain DeepAgents
Source decks: ../repo/slides/Loop-Eng_Slides – Wide (Overview of Loop Engineering).pdf (13 slides), ../repo/slides/Loop-Eng_Slides – Tall (Lessons with Jupyternotbook).pdf (18 slides), ../repo/slides/new_lesson.pdf (4 slides, wide format, the Event-Driven Loop lesson)
Instructors: Sydney Runkle (LangChain) and Esmaeil Gargari (DeepLearning.AI)

Rich text descriptions of the course slides, organized by lesson in the same order and with the
same lesson titles as the transcripts in `../transcripts/`. Each entry gives the deck and original
slide number, the evidence that ties the slide to a lesson (a verbatim transcript passage, or a
note that none exists), every word visible on the slide, a description of the visual, and what it
teaches.

## How to read this file

- **Lesson assignment rests on transcript content, not video frames.** No lesson videos were
  available, so no slide was matched to a video by frame sampling and there are no timestamps.
  Each slide was placed in the lesson whose narration describes what the slide shows. The decks
  were rendered to one PNG per slide and read alongside their extracted text layer.
- **Evidence field.** "Narrated" means a transcript passage clearly describes what the slide shows;
  the passage is quoted verbatim. "Deck-only" means no transcript passage matches. "Narrated" is
  the best available proxy for "shown in the video", but it is a proxy: a narrated slide may have
  been on screen for a different span than the quote, or replaced by a notebook or the instructor.
- **Lesson numbering comes from the transcripts:** 1 Introduction, 2 Overview of Loop Engineering,
  3 Deep Agent Primer, 4 Agent Loop, 5 Verification Loop, 6 Event-Driven Loop, 7 Learning loop,
  8 Conclusion. The decks carry no lesson numbers. Their title cards map onto the transcript
  lessons as follows: Wide deck subtitle "Overview of Loop Engineering" = Lesson 2; Tall deck title
  cards "Deep Agent Primer" = Lesson 3, "Agent Loop" = Lesson 4, "Verification Loop" = Lesson 5,
  "Event driven loop" = Lesson 6, "Learning loop" = Lesson 7; the third deck (`new_lesson.pdf`,
  subtitle "Event-Driven Loop") = Lesson 6. Lesson 6 therefore has six slides: the third deck's
  four and the Tall deck's title card (slide 15) and diagram (slide 16). Transcripts win wherever
  the decks disagree.
- **Slide numbering** is `Lesson.Order` in deck order within the lesson. The deck and original
  slide number follow in parentheses so each entry can be traced back to the PDF.
- **Text on slide** is transcribed verbatim from the extracted text layer, with labels inside
  diagrams read from the page images (the extractor skipped text embedded in diagram images). Items
  are separated by " · ". Code blocks are reproduced as code.
- **Animations cannot be known** from a PDF, so no entry claims a build order. Where a slide
  carries callout marks (block arrows, highlight rectangles) they are described as drawn.
- **Lessons 1 and 8 have no slides** in any deck. They are listed with a note so the file still
  has one section per lesson. All 35 slides are accounted for.
- Course-wide visual conventions: every content slide has the LangChain logo top left and the
  DeepLearning.AI logo top right, a centered black title in a light sans face, and a coral-red
  wave along the bottom edge. Title cards have the course title in coral red, the lesson title in
  slate grey, and both logos near the bottom, with no wave. Wide-deck loop diagrams share a color
  code: lavender for the model and tools (the agent loop), green for the grader (the verification
  loop), blue for the event loop and its system update, orange-red for the engine analysis and
  "harness improvements", and a pink dashed frame around the element the current slide introduces.
  Tall-deck lesson diagrams use a pink dashed box for the incoming requirement (with a blue square
  app icon matching the Jira ticket the narration mentions), a dark navy box for the requirements
  analysis agent, light-blue rows for its output sections, a dark green box for the grader, a
  yellow box for feedback, and dark-red block arrows as callouts.

---

## Lesson 1: Introduction
Transcript: `## Lesson 1: Introduction` in transcripts/loop-engineering-with-langchain-deepagents-transcripts.md

No slide in any deck belongs to this lesson. The narration previews the four loops and the
requirement review agent, but every slide covering those topics is narrated in detail in Lessons
2 to 7 and is placed there.

---

## Lesson 2: Overview of Loop Engineering
Transcript: `## Lesson 2: Overview of Loop Engineering` in transcripts/loop-engineering-with-langchain-deepagents-transcripts.md

All 13 slides of the Wide deck belong here; the deck's subtitle is this lesson's title and the
narration walks through them in deck order: where loop engineering sits among prompt, context and
harness engineering; why loops matter; the four loops each with a concept slide and a "docs writer
agent" example slide; human oversight; and a summary table.

### Slide 2.1 — Title card: Overview of Loop Engineering (Wide deck, slide 1)
**Evidence:** Deck-only (title card; its subtitle is this lesson's title)
**Text on slide:** Loop Engineering with LangChain DeepAgents · Overview of Loop Engineering
**Visual description:** White title card. The course title in coral red on two lines, centered;
below it the subtitle in slate grey. The LangChain wordmark sits bottom left of center and the
DeepLearning.AI logo (red concentric mark over the name) bottom right of center. No wave.
**What it teaches:** Names the course and the lesson. "DeepAgents" is written as one word here.

### Slide 2.2 — Prompt, Context, Harness, and Loop Engineering (Wide deck, slide 2)
**Evidence:** Narrated — "The first was prompt engineering, which focuses on optimizing the instructions sent to a model. Closely related is context engineering. The prompt is part of the context, but the context also includes tool descriptions and results, human and AI messages, retrieved documents, memory, and many other types of information. Context engineering focuses on ensuring that the right information is available to the LLM at the right time. Harness engineering is broader and can encompass context engineering."
**Text on slide:** Prompt, Context, Harness, and Loop Engineering · Prompt Engineering · Shapes what you ask the model — the instructions that guide its behavior and output. · Context Engineering · Shapes what the model knows at each step — selecting and organizing the right information, memory, and tool results. · Harness Engineering · Shapes the system around the model: tools, middleware, permissions, workflows, and other infrastructure that determines how the agent operates. · Loop Engineering · Shapes how the system repeatedly acts, evaluates, and improves: designing feedback loops that enable agents to complete work, verify results, and improve over time.
**Visual description:** A 2×2 grid of pale-pink rounded boxes with coral borders: Prompt (top
left), Context (top right), Harness (bottom left), Loop (bottom right). In each heading the first
word is bold black and "Engineering" is grey; a one- or two-sentence definition follows in dark
grey. (The extracted text layer lists Loop before Harness; on the page Harness is bottom left.)
**What it teaches:** Four named disciplines of agent engineering, each defined by what it shapes:
the prompt, the model's per-step context, the system around the model, and the feedback loops.
Loop engineering is the course's focus: acting, evaluating and improving repeatedly.

### Slide 2.3 — Why loops matter (Wide deck, slide 3)
**Evidence:** Narrated — "I've identified four levels of loops, which we'll explore in more detail in the coming slides. First, you have the Agent loop, the basic model calling tools loop which most agents are based. The second is the Verification loop, which checks the agent's final output against a given rubric. Third is the event-driven loop, which connects the agent to an application and invokes it in response to real-world events. And the fourth, and maybe most exciting, is the hill-climbing loop, which uses what happens during each run to improve the agent over time."
**Text on slide:** Why loops matter · Why loops? · One model call is rarely enough for complex work · Agents need to act → observe → decide → act again · Repeated execution creates opportunities for feedback and improvement · Continuous improvement · Every run produces rich execution outcomes and traces · Outcomes directly transition into actionable feedback · Feedback loops continuously refine and improve future behavior · Four levels of loops · 1) Agent loop · Automate fundamental workflows · 2) Verification loop · Improve end-to-end reliability · 3) Event-driven loop · Automate work in real-world systems · 4) Hill-climbing loop · Optimize and improve the agent itself
**Visual description:** Three light-grey panels with coral headings. Left column: "Why loops?"
(three bullets; the arrows in "act → observe → decide → act again" are coral) above "Continuous
improvement" (three bullets), joined by a hollow grey down-arrow. A hollow grey right-arrow leads
from the lower panel to a taller right panel "Four levels of loops" listing 1) to 4), each a bold
name over a grey one-line purpose.
**What it teaches:** Why one call is not enough, how repeated runs produce traces that become
feedback, and the course's four-level taxonomy of loops with a one-line purpose each.

### Slide 2.4 — Loop 1: The Agent Loop (Wide deck, slide 4)
**Evidence:** Narrated — "The first loop is the core Agent loop. First, a model receives context for a given task. Then it calls tools to complete work for that task. Tools return observations, and then the model continues in that core loop until it's done with the given task. And so when we talk about loop engineering here, It means that you're selecting the right model."
**Text on slide:** Loop 1: The Agent Loop · A basic agent loop: A model repeatedly interacts with tools until it can complete a request. · Execution steps · Task + context · Model reasons about next action · Model calls a tool · Tool returns an observation · Model chooses next action · Repeat until done · request · model · action · observation · tools · repeat until done · result · What can we engineer? · Model selection: Choose the right capability · Tool selection: Provide relevant capabilities · Tool descriptions: Optimize definitions
**Visual description:** A one-line definition under the title with "A basic agent loop:" in bold.
Left: a panel with a coral top rule, "Execution steps", six bullets. Center: a beige "request"
pill with an arrow down into a pink dashed rounded frame holding two lavender boxes, "model" and
"tools", joined by dashed arrows labelled "action" (model to tools, above) and "observation"
(tools to model, below). An arrow drops from "model" labelled "repeat until done" to a beige
"result" box. A red bracket line runs from the right edge of the pink frame down to a panel at
bottom right, "What can we engineer?", with three bold-labelled bullets.
**What it teaches:** The agent loop is model-calls-tools-observes-repeats until done. What loop
engineering changes at this level: which model, which tools, and how the tools are described.

### Slide 2.5 — Agent Loop - Example (Wide deck, slide 5)
**Evidence:** Narrated — "This is our docs improvement agent. So we'll start with the very basic infrastructure here. We send a docs improvement request, the model plans and drafts changes, and then we give it tools to clone the docs repository, read existing docs, write new docs, and then open a pull request with an appropriate diff and description."
**Text on slide:** Agent Loop - Example · DOCS WRITER AGENT LOOP · docs improvement request · model · plan + draft changes · action · observation · sandbox tools · clone · read · write · repeat until done · pull request · diff + description
**Visual description:** The Slide 2.4 diagram with the generic labels replaced. Small-caps caption
"DOCS WRITER AGENT LOOP". A beige "docs improvement request" pill feeds a pink dashed frame with
a lavender "model / plan + draft changes" box and a lavender "sandbox tools / clone · read ·
write" box, dashed arrows "action" and "observation" between them. "repeat until done" leads to a
beige "pull request / diff + description" box. A faint vertical rule sits at the right third.
**What it teaches:** A concrete agent loop: the request is a docs improvement, the tools are a
sandbox that can clone, read and write, and the finished result is a pull request with a diff
and description.

### Slide 2.6 — Level 2: Verification loop (Wide deck, slide 6)
**Evidence:** Narrated — "You can see outlined in purple here, I have the core agent loop. But now we have this green grader. You send a request to that core loop and it returns a result. So that's a cycle of the core agent loop. That gets fed into our grader agent, which decides if the task is actually complete. The grader scores the result against a given set of criteria. If those criteria are not met, we feed it back into the core agent loop. Otherwise, we move to complete."
**Text on slide:** Level 2: Verification loop · Verification Flow · Request: Initial system input. · Agent Attempt: Executes the task. · Grader Evaluation: Result sent to grader. · Feedback Loop: Fail feedback retry. · Done: Pass finished. · Why verification helps · Explicit quality criteria · Higher reliability · Fewer incomplete results · Can make cheaper models viable for harder tasks · Grader checks the agent's output against a rubric and, if it fails, sends the result back with feedback. · Type: Graders can either be deterministic or agentic (LLM as a judge is a classic example, here). · request · agent loop · model · action · observation · tools · result · retry with feedback · grader · rubric / eval · pass · done
**Visual description:** Left: two light panels, "Verification Flow" (five bullets with bold
labels) and "Why verification helps" (a bullet with two sub-bullets, then a bold bullet). Right
top: the "Grader checks..." sentence with "Grader" bold, and a smaller "Type:" line. Right: a
beige "request" pill feeds a lavender dashed frame labelled "agent loop" containing "model" and
"tools" (lavender, dashed action/observation arrows) and a beige "result" box under the model.
An arrow drops from "result" into a pink dashed frame holding a grey-green "grader" box with the
green sublabel "rubric / eval"; an arrow right labelled "pass" reaches a "done" pill. A green
curved arrow from the grader back up to the model is labelled "retry with feedback".
**What it teaches:** The verification loop wraps the agent loop: a grader scores the result against
a rubric, passes to done, or sends feedback for a retry. Graders can be deterministic or an LLM
judge. Explicit criteria raise reliability and let cheaper models handle harder tasks.

### Slide 2.7 — Level 2: Verification loop – Example (Wide deck, slide 7)
**Evidence:** Narrated — "So, what does this look like for our docs agent? We have the docs improvement request coming in, the core agent loop opens a pull request, and then the grader agent ensures that all links resolve and that CI passes, before an actual complete notification, right?"
**Text on slide:** Level 2: Verification loop – Example · Verification Flow · Request: Initial system input. · Agent Attempt: Executes the task. · Grader Evaluation: Result sent to grader. · Feedback Loop: Fail feedback retry. · Done: Pass finished. · Why verification helps · Explicit quality criteria · Higher reliability · Fewer incomplete results · Can make cheaper models viable for harder tasks · docs improvement request · agent loop · model · plan + draft changes · action · observation · sandbox tools · clone · read · write · pull request · diff + description · retry with feedback · grader · links resolve · CI passes · pass · done
**Visual description:** Near-duplicate of Slide 2.6. The two left panels are identical. The
"Grader checks..." and "Type:" text is gone, and the diagram is the docs-writer version: "docs
improvement request" in its own pink dashed frame; a pink-tinted "agent loop" frame holding
"model / plan + draft changes", "sandbox tools / clone · read · write" and "pull request / diff
+ description"; a grader box reading "links resolve · CI passes" in a pink dashed frame; "pass"
to a small "done" circle; the green "retry with feedback" arrow back to the model.
**What it teaches:** For the docs agent the rubric is mechanical: links must resolve and CI must
pass before the pull request counts as done.

### Slide 2.8 — Level 3: Event driven loop (Wide deck, slide 8)
**Evidence:** Narrated — "You can see in the diagram, we have the event trigger, then our nested verification loop, the nested core agent loop, and then also a system update. I'll also note in these diagrams, I'm doing the Russian doll thing of nesting every loop inside of another. You don't necessarily have to do that for all four loops."
**Text on slide:** Level 3: Event driven loop · The event-driven loop connects your agent to your ecosystem. · An event fires · A new document lands · A schedule triggers · A webhook arrives · event trigger · verification loop · agent loop · model · action · observation · tools · result · retry with feedback · grader · rubric / eval · new events · system update · service improves
**Visual description:** Left: the sentence "The event-driven loop connects your agent to your
ecosystem." and four bullets. Right: a tan "event trigger" pill inside a pink dashed frame at the
top. An arrow drops into a green dashed frame labelled "verification loop", which contains the
lavender dashed "agent loop" frame (model, tools, action/observation, result) and a green "grader
/ rubric / eval" box, with the green "retry with feedback" arrow. An arrow leaves the verification
frame into a pink dashed frame holding a grey-lavender "system update" box with the blue sublabel
"service improves". A thin curved arrow climbs the right side from "system update" back to "event
trigger", labelled "new events".
**What it teaches:** The event-driven loop is the outer trigger: an event (a document, a schedule,
a webhook) starts the nested verification and agent loops, the system is updated, and the updated
system produces new events. Loops nest like Russian dolls.

### Slide 2.9 — Level 3: Event driven loop – Example (Wide deck, slide 9)
**Evidence:** Narrated — "So at LangChain, we have a Slack channel called docs-plz. I can send it a Slack message and say, "Hey, can you please update our DeepAgents docs to showcase the value of verification loops?" Then the core agent runs and drafts a PR. The verification loop decides if links resolve and CI passes, we actually go ahead and send a Slack notification back that's like, "Hey Sydney, here's your PR, please review." After I approve and merge, we now have this live and discoverable docs enhancement."
**Text on slide:** Level 3: Event driven loop – Example · Slack message · #docs-plz · verification loop · agent loop · model · plan + draft changes · action · observation · sandbox tools · clone · read · write · pull request · diff + description · retry with feedback · grader · links resolve · CI passes · new request · docs enhancement · merged · live · discoverable
**Visual description:** The Slide 2.8 diagram, centered and relabelled, with no left text. The
trigger is a tan "Slack message / #docs-plz" pill in a pink dashed frame. The green "verification
loop" frame holds the lavender "agent loop" frame (model plan + draft changes, sandbox tools
clone · read · write, pull request diff + description) and the grader "links resolve · CI
passes". Below, a pink dashed frame holds "docs enhancement / merged · live · discoverable". The
curved arrow back to the Slack message is labelled "new request".
**What it teaches:** A Slack message in a channel is the event; the result is a merged, live,
discoverable docs change; new requests keep the loop going.

### Slide 2.10 — Level 4: Learning / hill climbing loop (Wide deck, slide 10)
**Evidence:** Narrated — "This loop automates agent improvement by finding signal in traces, which are records of every step an agent took for a given task." and "So the first category of things that you can do with the hill climbing loop is improve those base procedural things, such as tool descriptions and prompts. I would even say skills are pretty procedural. The second category is focused more on memory type information, that's persisted across runs."
**Text on slide:** Level 4: Learning / hill climbing loop · Trace: a record of what the model did, the tools it called, grader feedback, etc. · The hill climbing loop: · improve base procedural things · more memory information · event trigger · event loop · verification loop · agent loop · model · action · observation · tools · result · retry with feedback · grader · rubric / eval · new events · system update · service improves · harness improvements · traces · engine analysis · agent over traces
**Visual description:** Left: a definition with "Trace:" in bold, then "The hill climbing loop:"
in bold with two bullets. Right: the full nest. A beige "event trigger" pill at top feeds a blue
dashed frame "event loop", which contains the green dashed "verification loop", which contains
the lavender dashed "agent loop" (model, tools, result); below them the green grader and a blue
"system update / service improves" box; "new events" curves back to the trigger. A dashed arrow
labelled "traces" drops out of the event loop into a pink dashed frame holding a salmon "engine
analysis" box with the dark-red sublabel "agent over traces". An orange-red curved arrow labelled
"harness improvements" climbs from the engine analysis up the right side to the "tools" box in
the agent loop. A large dark-red block arrow points left at the "traces" label as a callout.
**What it teaches:** The fourth loop runs an analysis agent over the traces of past runs and feeds
"harness improvements" back into the inner loops. A trace records what the model did, the tools
it called and grader feedback. Improvements fall into two kinds: procedural things (prompts, tool
descriptions, skills) and memory.

### Slide 2.11 — Level 4: Learning / Hill Climbing Loop - Example (Wide deck, slide 11)
**Evidence:** Narrated — "At LangChain, we built an agent called Engine for this continual improvement loop. So we run Engine over the docs agent traces, and then we can update all the things that you just learned about on that last slide."
**Text on slide:** Level 4: Learning / Hill Climbing Loop-  Example · DOCS WRITER HILL CLIMBING LOOP · Slack message · #docs-plz · event loop · verification loop · agent loop · model · plan + draft changes · action · observation · sandbox tools · clone · read · write · pull request · diff + description · retry with feedback · grader · links resolve · CI passes · new request · docs enhancement · merged · live · discoverable · harness improvements · traces · engine analysis · detects issues across traces · files prompt or tool change
**Visual description:** The Slide 2.10 nest in its docs-writer form, with the small-caps caption
"DOCS WRITER HILL CLIMBING LOOP" and no left text. Slack message #docs-plz at top; blue "event
loop" frame containing the green "verification loop" frame containing the lavender "agent loop"
(model plan + draft changes, sandbox tools clone · read · write, pull request diff +
description), the grader "links resolve · CI passes", and a blue "docs enhancement / merged ·
live · discoverable" box; "new request" curves back to the Slack message. A dashed "traces" arrow
drops to a peach "engine analysis" box whose sublabel reads "detects issues across traces · files
prompt or tool change"; an orange-red "harness improvements" arrow climbs back to "sandbox tools".
No callout arrow on this slide.
**What it teaches:** The docs writer's learning loop: an engine agent reads traces across runs,
detects recurring issues, and files a prompt or tool change back into the harness.

### Slide 2.12 — Human oversight and expertise (Wide deck, slide 12)
**Evidence:** Narrated — "One really important note that I'll add here is that while we talk about automating things, human input is still really important. Let's talk about this at each loop level. So let's go back to that email assistant. if there is a send email tool, I probably want human approval in that cycle. So you can still add human approval at important or sensitive tool calls in that core loop. The second is that you can add a human to the grader or verifier cycle, basically plugging in some form of human approval in the grader stage. The third case is human approval on agent artifacts or results. So in our docs writer example, we always have human approval on those PRs before they merge. And then the fourth case is approving harness and code changes to your core agent."
**Text on slide:** Human oversight and expertise · 1. AGENT LOOP · Require human input before executing sensitive tools or final actions. · 2. VERIFICATION LOOP · A human acts as the grader to audit and score sensitive automated workflows. · 3. APPLICATION LOOP · Human-in-the-loop approves raw outputs before final delivery to users. · 4. HILL CLIMBING LOOP (System-level Optimization) · Harness and evaluation improvements must flow through systematic human review before final system deployment.
**Visual description:** Three equal boxes in a row, each with a grey header strip carrying a
colored dot and an upper-case name: blue dot "1. AGENT LOOP", orange dot "2. VERIFICATION LOOP",
teal dot "3. APPLICATION LOOP"; thin arrows run 1 → 2 → 3. A connector drops from box 3, turns
left, and enters a wider fourth box centered under boxes 2 and 3 with an amber dot, "4. HILL
CLIMBING LOOP (System-level Optimization)"; its body text is set in amber-orange rather than grey.
**What it teaches:** Where a human belongs at each level: approving sensitive tool calls, acting as
grader, approving outputs before delivery, and reviewing harness changes before deployment. Note
the third loop is labelled "APPLICATION LOOP" here, not "Event-driven loop".

### Slide 2.13 — Putting it all together (Wide deck, slide 13)
**Evidence:** Narrated — "So, for a quick recap of all the loops you just learned about, the first, the core agent loop, does the work. The model calls tools, allow the agent to take action, and the fact that this is done in a loop makes it pretty powerful. The verification loop improves quality, especially in cases where models aren't as individually powerful. The event-driven loop helps scale execution and makes sure that agents are actually getting used. And then the fourth, my favorite, is the hill-climbing loop. Call it the learning loop or the self-improvement loop. This improves your agent system over time."
**Text on slide:** Putting it all together · Loop · What is looping? · Core idea · Result · 1. Agent loop · Model ↔ tools · Act, observe, act again · Task completed · 2. Verification loop · Agent run ↔ evaluator · Evaluate the result and retry with feedback · Better-quality task result · 3. Event-driven loop · Event ↔ agent execution · Run agents whenever something happens · Ongoing automation · 4. Hill-climbing loop · Production traces ↔ harness · Learn from many runs and improve the system · Better agent itself
**Visual description:** A four-column table with a grey header row. Each of the four body rows is
tinted pink and outlined in coral, with the loop name in bold in a slightly darker first cell, and
a dark-red block arrow in the left margin pointing at the row.
**What it teaches:** One-line summary of each loop: what pair cycles (model and tools; agent run
and evaluator; event and execution; traces and harness), the core idea, and the result it buys.

---

## Lesson 3: Deep Agent Primer
Transcript: `## Lesson 3: Deep Agent Primer` in transcripts/loop-engineering-with-langchain-deepagents-transcripts.md

Tall-deck slides 1 to 5: a title card, the base `create_agent` loop, middleware hook points, the
four pillars behind `create_deep_agent()`, and a `create_deep_agent` code example. The rest of the
lesson narrates a Jupyter notebook (a poet agent with skills) and a LangSmith trace, with no deck
slides.

### Slide 3.1 — Title card: Deep Agent Primer (Tall deck, slide 1)
**Evidence:** Deck-only (title card; its subtitle is this lesson's title)
**Text on slide:** Loop Engineering with LangChain Deep Agents · Deep Agent Primer
**Visual description:** Tall-format title card: course title in coral red on two lines, "Deep
Agent Primer" in slate grey, the LangChain wordmark and DeepLearning.AI logo side by side near the
bottom. "Deep Agents" is two words on every Tall-deck title card.
**What it teaches:** Names the lesson.

### Slide 3.2 — create_agent (Tall deck, slide 2)
**Evidence:** Narrated — "LangChain has a base ReAct agent in the LangChain library. This is shown here, and it's simply a model calling tools in a loop. You can create an agent like this, providing the model, tools, system prompt, and you invoke it like this, including a request in the invocation."
**Text on slide:** create_agent · request · model · result · tools
```
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-5.5",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content":
"What's the weather in San Francisco?"}]}
)
```
**Visual description:** Upper half: a compact loop diagram. A black "request" pill with an arrow
down to a black "model" box; from "model" two dashed blue arrows fan down-left to a light-blue
"result" pill and down-right to a black "tools" box; a solid blue line runs from "tools" up and
back into the arrow entering "model", closing the loop. Lower half: a grey code box with
syntax-colored Python (keywords purple, strings green, argument names orange).
**What it teaches:** The base agent is a model that either calls a tool and loops back or returns a
result. It is built with `create_agent(model, tools, system_prompt)` and run with `invoke` on a
messages list.

### Slide 3.3 — middleware (Tall deck, slide 3)
**Evidence:** Narrated — "That agent can be enhanced by adding code at critical points in the loop. This is called middleware. You can add code before and after the agent, before and after the model, and before and after tools."
**Text on slide:** middleware · request · model · result · tools · before_agent, after_agent · before_model, after_model · wrap_model_call, wrap_tool_call
**Visual description:** The Slide 3.2 loop diagram with hook markers added: a blue dot on the
arrow just below "request" and another blue dot on the dashed arrow to "result"; a purple dot on
the arrow just above "model" and another just below it; light-blue rounded outlines drawn around
the "model" box and the "tools" box. A legend below maps blue dot to `before_agent, after_agent`,
purple dot to `before_model, after_model`, and the light-blue outline to `wrap_model_call,
wrap_tool_call`. No code block.
**What it teaches:** Middleware inserts code at fixed points in the loop: around the whole agent
run, around each model call, and as wrappers around the model call and each tool call.

### Slide 3.4 — create_deep_agent() (Tall deck, slide 4)
**Evidence:** Narrated — "LangChain offers a create_deep_agent primitive that adds middleware to enable the list of features you see here. There are four core pillars of a deep agent. First, it has an execution environment. This includes tools, which allow the agent to take actions in the real world; a file system, which is the backbone of a deep agent, and option- optionally a code interpreter or sandbox that allows the agent to execute code. The second pillar is Delegation. A Deep Agent can plan for complex tasks and dispatch smaller units of work to subagents. At the core of a Deep Agent is this third pillar, Context Management. It has built-in support for memory and skills. Under the hood, it uses summarization and context offloading, which enable long-running interactions. Finally, deep agents enable prompt caching by default, no matter the model provider you're using. The final pillar of a deep agent is the steering pillar. Deep agents support first-class human-in-the-loop, and as we'll discuss in more depth later, they also support grading rubrics for giving feedback to a core agent."
**Text on slide:** create_deep_agent() · request · model · result · tools · Execution Environment · Tools · Filesystem · Code Interpreter · Sandbox · Delegation · Planning · Subagents · Context Management · Memory: Agent.md · Skills · Summarization · Context Offloading · Prompt Caching · Steering · Human-in-the-loop · Grading Rubrics
**Visual description:** Left: the middleware loop diagram from Slide 3.3 (with its dots and
outlines, no legend), smaller. Right: four bold headings each followed by a bullet list:
Execution Environment (4), Delegation (2), Context Management (5), Steering (2). "Agent.md" is
rendered as a teal underlined hyperlink.
**What it teaches:** `create_deep_agent()` is the middleware-equipped agent with four pillars: an
execution environment, delegation, context management, and steering. Memory via an Agent.md
file, skills, and grading rubrics are the features the rest of the course relies on.

### Slide 3.5 — create_deep_agent (Tall deck, slide 5)
**Evidence:** Narrated — "Here's a quick example that creates a deep agent with a model, tools, prompts, memory, and an additional middleware. As you can see here, we're invoking the agent with a query."
**Text on slide:** create_deep_agent · request · model · result · tools
```
backend = FilesystemBackend(root_dir="workspace", virtual_mode=True)

agent = create_deep_agent(
   model="openai:gpt-5.4-mini",
   tools=[fetch_requirement_from_jira],
   system_prompt="Follow the instructions in /memories/AGENTS.md.",
   memory=["/memories/AGENTS.md"],           # loaded on every run
   backend=backend,
   middleware=[ModelCallLimitMiddleware(run_limit=12, exit_behavior="end")],
)

result = agent.invoke({"messages": [{"role": "user", "content":
   "The requirement document is tracked in Jira as ticket AUTH-142. "
   "Fetch it to begin."}]})
```
**Visual description:** Upper half: the middleware loop diagram (request, model, result, tools with
blue and purple dots and light-blue outlines). Lower half: a full-width grey code box. The code is
rendered in very pale, low-contrast syntax colors (light blue identifiers, pale green strings,
pale orange argument names) so it reads faint against the grey; the text layer above is the
reliable source. The comment `# loaded on every run` is only faintly visible on the page.
**What it teaches:** A deep agent for the course's requirement task: a filesystem backend rooted
at a workspace, a Jira fetch tool, a system prompt that defers to `/memories/AGENTS.md`, that file
loaded as memory on every run, and a model-call limit of 12 that ends the run when hit. The
invocation names a Jira ticket.

---

## Lesson 4: Agent Loop
Transcript: `## Lesson 4: Agent Loop` in transcripts/loop-engineering-with-langchain-deepagents-transcripts.md

Tall-deck slides 6 to 10: a title card, the agent-loop diagram, what a requirements analysis agent
does, a worked example on the file-upload requirement, and the agent's tools plus the three loops
to be added later. The rest of the lesson narrates the notebook.

### Slide 4.1 — Title card: Agent Loop (Tall deck, slide 6)
**Evidence:** Deck-only (title card; its subtitle is this lesson's title)
**Text on slide:** Loop Engineering with LangChain Deep Agents · Agent Loop
**Visual description:** Tall title card as in Slide 3.1; the course title wraps to three lines
here ("Loop Engineering / with LangChain Deep / Agents"). Subtitle "Agent Loop".
**What it teaches:** Names the lesson.

### Slide 4.2 — Agent Loop (Tall deck, slide 7)
**Evidence:** Narrated — "As you learned in lesson one, in the agent loop, the model repeatedly interacts with tools until the task is complete. It takes an action, sees what happens, and then decides what to do next. The loop continues until the agent has finished the work."
**Text on slide:** Agent Loop · request · model · action · observation · tools · repeat until done · result
**Visual description:** The Wide-deck agent loop redrawn for the tall page. A beige "request" pill
with an arrow down into a single wide lavender bar split into "model" (left) and "tools" (right);
in the middle of the bar, dashed arrows "action" (rightward, above) and "observation" (leftward,
below) sit inside a translucent pink-red highlight rectangle. A grey arrow drops from "model",
labelled "repeat until done", to a beige "result" box; this arrow is covered by a translucent
pink-red vertical highlight bar. The two highlights are callouts, not loop frames.
**What it teaches:** The two things to notice in the agent loop: the action/observation exchange
between model and tools, and the exit to a result once the model decides it is done.

### Slide 4.3 — Requirements Analysis Agent: what it does (Tall deck, slide 8)
**Evidence:** Narrated — "A product manager or another stakeholder might share a new requirement document describing what they want to build. This might be a Jira ticket or a Confluence page. The engineering team usually needs to make sure the requirements are clear and complete. So someone on the team needs to go through it carefully and figure out: Is anything missing? Is anything unclear? Are there questions we should answer before we build?"
**Text on slide:** Requirements Analysis Agent · NEW REQUIREMENT · Requirements Analysis · Is anything missing? · Is anything unclear? · Are there questions we should answer before we start building?
**Visual description:** A vertical flow. A pink dashed box "NEW REQUIREMENT" in bold caps with a
blue square app icon (white angular mark) at its right end; an arrow down to a dark navy rounded
box "Requirements Analysis" in white bold; an arrow down to a light-blue dashed box with three
bulleted questions.
**What it teaches:** The job the course's agent automates: take a new requirement and ask what is
missing, what is unclear, and what must be answered before building.

### Slide 4.4 — Requirements Analysis Agent: worked example (Tall deck, slide 9)
**Evidence:** Narrated — "Say the engineering team receives this new requirement to build a feature that enables users to upload files to their profile. The requirement description asks for the uploaded files to be stored securely and also the need for supporting common file types. Our agent will analyze this requirement and will return a list of facts, ambiguities, clarification questions, and assumptions. For example, the agent finds out that the phrase "common file types" in the requirement description has ambiguities and adds a specific clarification question related to this ambiguity."
**Text on slide:** Requirements Analysis Agent · REQUIREMENT: User Profile File Upload · "Users shall be able to upload files to their profile. Uploaded files should be stored securely. The system should support common file types." · Requirements analysis agent · 1 · Facts: Users can upload files to their profile. · 2 · Ambiguities: "Common file types" is undefined. "Stored securely" doesn't specify a security standard. · 3 · Clarification Questions: What does "secure" require? Which file types must be supported (PDF, JPG, PNG, …)? · 4 · Assumptions: Assume a 10MB max file size and encryption at rest, until confirmed otherwise.
**Visual description:** Top: a pink dashed box headed "REQUIREMENT:" in red caps and "User Profile
File Upload" in bold, with the blue app icon at right, containing the quoted requirement in
italics; "Users shall be able to upload files to their profile." is bold, and "securely" and
"common file types" are bold with thick dark-red underline bars. An arrow drops to the navy
"Requirements analysis agent" box. Below, four rows: a blue numbered square (1 to 4) on the left
of each light-blue row, labelled in bold Facts, Ambiguities, Clarification Questions,
Assumptions. A dark-red line runs from the underlined "common file types" down the left margin
to a dark-red block arrow pointing at row 2; a second dark-red block arrow points at row 3.
**What it teaches:** The agent's output has four sections. The example shows how one vague phrase
("common file types") becomes an ambiguity and then a clarification question, and how the agent
records explicit assumptions until confirmed.

### Slide 4.5 — Agent Tools (Tall deck, slide 10)
**Evidence:** Narrated — "The agent first uses fetch_requirement tool to get the requirement. Then, as it analyzes the requirement, it has two general file tools: write_file, which lets it create a new file, or overwrite an existing one, or overwrite an existing one, and edit_file, which lets it make specific changes inside a file. The agent uses these tools to build up its analysis and produce the structured report you saw on the previous slide, with confirmed facts, ambiguities, clarification questions, and assumptions." and "From this agent loop in this lesson to verification, then event-driven, and finally, the hill-climbing or learning loop in the next lessons."
**Text on slide:** Agent Tools · REQUIREMENT: User Profile File Upload · Model · fetch_requirement · write_file · edit_file · Structured report · 1) Facts · 2) Ambiguities · 3) Questions · 4) Assumptions · + · Verification Loop · Event-driven Loop · Hill-climbing / learning loop
**Visual description:** Top: the pink dashed "REQUIREMENT: User Profile File Upload" box with the
blue app icon. An arrow drops into a large mauve rounded container. Inside it, a blue panel holds
a dark grey "Model" box on the left and three light monospace boxes on the right
(`fetch_requirement`, `write_file`, `edit_file`) with arrows from Model to each. Below the panel,
still inside the container, a light-blue dashed box "Structured report" lists 1) to 4) in two
columns. Under the container a mauve "+" sign, then three mauve boxes in a row: "Verification
Loop", "Event-driven Loop", "Hill-climbing / learning loop".
**What it teaches:** The agent loop's tools are one fetch tool and two file tools, and its product is
a structured four-part report. The three boxes below name the loops that later lessons add around
this agent.

---

## Lesson 5: Verification Loop
Transcript: `## Lesson 5: Verification Loop` in transcripts/loop-engineering-with-langchain-deepagents-transcripts.md

Tall-deck slides 11 to 14: a title card, the verification-loop diagram with the question it
answers, the three rubric criteria and the pass/fail flow, and a worked grader-feedback example.
The rest of the lesson narrates the notebook, which uses a different requirement (a real-time
notification system).

### Slide 5.1 — Title card: Verification Loop (Tall deck, slide 11)
**Evidence:** Deck-only (title card; its subtitle is this lesson's title)
**Text on slide:** Loop Engineering with LangChain Deep Agents · Verification Loop
**Visual description:** Tall title card, course title on three lines, subtitle "Verification Loop".
**What it teaches:** Names the lesson.

### Slide 5.2 — Verification Loop (Tall deck, slide 12)
**Evidence:** Narrated — "But just because the agent says it is done, is the analysis actually good enough? In the agent loop, nothing is checking for this. So in this lesson, we are going to add another loop around it, which is the Verification Loop. Once the agent finishes, a grader looks at what it produced and checks it against a rubric, which is basically our definition of what a good analysis looks like. If everything passes, we are done. If something fails, the grader gives the agent specific feedback, and the agent goes back and tries again."
**Text on slide:** Verification Loop · Verification grades the output of a run of your agent and can retry the run with added feedback. · request · agent loop · model · action · observation · tools · result · retry with feedback · is the analysis actually good enough? · grader · rubric / eval · pass · done
**Visual description:** A two-line definition under the title. Below, the Wide-deck verification
diagram (Slide 2.6) with callouts: "request" pill; a pink-tinted dashed "agent loop" frame
holding lavender "model" and "tools" with action/observation arrows and a pinkish "result" box;
the green "retry with feedback" arrow on the left; a green "grader / rubric / eval" box; "pass"
to a beige "done" box. A translucent yellow highlight covers the left side and the grader row. A
dark-red dot on the arrow from "result" to "grader" has a dashed dark-red leader to the red
italic caption "is the analysis actually good enough?". Three dark-red block arrows point up at
the retry arrow, at the grader, and at "done".
**What it teaches:** The agent loop ends when the agent says it is done; the verification loop asks
whether the result is actually good enough, grading against a rubric and retrying with feedback.

### Slide 5.3 — Rubric criteria and pass/fail flow (Tall deck, slide 13)
**Evidence:** Narrated — "In this lesson, we will use a rubric with three criteria to evaluate the quality of the output. First is completeness, where we check to see if the analysis covers every part of the requirement. Second is clarity. Here, for each ambiguity, we check to see if it says what specific information would resolve it. And third is Depth, where we ask if the result explains what could go wrong if that ambiguity isn't resolved. Each criterion is either pass or fail, and if all three criteria pass, the final output is accepted. And if any of the three criteria fails, the evaluation feedback is sent back to the agent to fix in the next iteration."
**Text on slide:** Agent Tools · REQUIREMENT: User Profile File Upload · Requirements analysis agent · 1) Facts, 2) Ambiguities, 3) Questions, 4)  Assumptions · Rubric criteria · 1 · Completeness: Did the analysis cover every part of the requirement? · 2 · Clarity: For each ambiguity, does it say what specific information would resolve it? · 3 · Depth: does it explain what could go wrong if that ambiguity isn't resolved? · Pass? · NO · YES · End
**Visual description:** The slide title reads "Agent Tools" (the same title as Slide 4.5) although
the content is the rubric. Top: the pink dashed requirement box with the blue app icon; an arrow
to the navy "Requirements analysis agent"; under it a small line "1) Facts, 2) Ambiguities, 3)
Questions, 4)  Assumptions". A line leaves the agent down the left to three light-green rows,
each with a green numbered square (1 to 3) and a bold label: Completeness, Clarity, Depth; the
rotated label "Rubric criteria" runs up the left margin. Arrows from the three rows converge on an
orange diamond "Pass?". From the diamond, "NO" (red) leads up the right side back into the agent
box, and "YES" (green) leads down to a grey "End" box.
**What it teaches:** The grader's rubric has three pass/fail criteria. All three must pass to end;
any failure sends the agent back for another attempt.

### Slide 5.4 — Grader feedback example (Tall deck, slide 14)
**Evidence:** Narrated — "In the first attempt, the agent identifies the ambiguity in the term common files and explains why it is unclear, but it doesn't say what information would resolve it, or what could go wrong if we leave it unresolved. The grader then reads this finished report and gives the agent specific feedback by telling the agent what is missing. The agent then gets this feedback and goes back and revises the report, such that in the second attempt, it adds the missing information."
**Text on slide:** Requirements Analysis Agent · REQUIREMENT: User Profile File Upload · "Users shall be able to upload files to their profile. Uploaded files should be stored securely. The system should support common file types." · Requirements analysis agent · Ambiguities: "Common file types" is undefined. · Grader · Clarity and depth failed. · Feedback: we need a specific fact that would resolve this ambiguity, and we need to explain the potential production failure.
**Visual description:** The Slide 4.4 requirement box at top (only "common file types" carries the
dark-red underline this time). An arrow to the navy "Requirements analysis agent"; an arrow to a
single light-blue box "Ambiguities: "Common file types" is undefined."; an arrow to a dark green
"Grader" box; an arrow to a yellow box whose header reads "Clarity and depth failed." in bold with
the body "Feedback: ..." below. A line leaves the yellow header, runs up the right side, and
re-enters the agent box, closing the loop.
**What it teaches:** A concrete failed grade: the ambiguity was found but lacked a resolving fact
and a consequence, so clarity and depth fail and the feedback names exactly what to add.

---

## Lesson 6: Event-Driven Loop
Transcript: `## Lesson 6: Event-Driven Loop` in transcripts/loop-engineering-with-langchain-deepagents-transcripts.md

The third deck (`new_lesson.pdf`, four wide-format slides in the Wide deck's style): a title card,
the event-driven loop diagram, why the loop matters, and the lesson's three-part plan. The Tall
deck's "Event driven loop" title card (slide 15) and diagram (slide 16) also belong here. The rest
of the lesson is screen recording, not slides: the Slack direct-message and team-channel demos,
the Jira and Confluence automation demos, and the setup steps for running the integrations
(cloning the repo, the environment file, creating a Slack app and its two tokens, Atlassian API
credentials, an ngrok tunnel, Jira and Confluence Automation rules). No slide carries those
steps.

### Slide 6.1 — Title card: Event-Driven Loop (third deck, slide 1)
**Evidence:** Deck-only (title card; its subtitle is this lesson's title)
**Text on slide:** Loop Engineering with LangChain Deep Agents · Event-Driven Loop
**Visual description:** Wide-format title card: the course title in coral red on two lines,
"Event-Driven Loop" in slate grey below it, the LangChain wordmark and the DeepLearning.AI logo side
by side near the bottom. No wave. "Deep Agents" is two words, as on the Tall-deck title cards.
**What it teaches:** Names the lesson.

### Slide 6.2 — Event driven loop (third deck, slide 2)
**Evidence:** Narrated — "In this lesson, we are going to add the event-driven loop. In this loop, an external event like a Slack message will trigger the agent to review a requirements report and return the result as a Slack message to the user."
**Text on slide:** Event driven loop · event trigger · verification loop · agent loop · model · action · observation · tools · result · retry with feedback · grader · rubric / eval · new events · system update · service improves
**Visual description:** The Wide deck's Slide 2.8 diagram, centered, with no left-hand text. A tan
"event trigger" pill in a pink dashed frame at the top; an arrow down into a green dashed frame
"verification loop" holding the lavender dashed "agent loop" (model and tools joined by dashed
"action" and "observation" arrows, "result" below the model) and the green "grader / rubric /
eval" box, with the green "retry with feedback" arrow climbing the left side from the grader back
to the model; below, a pink dashed frame holding a grey-lavender "system update / service
improves" box; a thin curved arrow labelled "new events" climbs the right side from "system
update" back to "event trigger".
**What it teaches:** The event-driven loop is the outer trigger: an event starts the nested
verification and agent loops, the system is updated, and the updated system produces new events.

### Slide 6.3 — Why event driven loop? (third deck, slide 3)
**Evidence:** Narrated — "Event-driven loop makes our agents easier to use by connecting them to the tools where the work is already happening, like Slack, GitHub, or Jira. This reduces friction. Say you want to review a requirement. If you have to open a separate agent, copy the requirement, paste it, and ask for a review, that's several extra steps. Even if the review is useful, you might not do it every time. But if the agent is available right where the conversation is happening, using it becomes a natural part of the workflow. Or, the agent can be automatically triggered when a requirement changes, so it responds when it's needed."
**Text on slide:** Why event driven loop? · Less friction: No manual copying, pasting, or switching tools · In the flow of work: Agents available where work happens · Timely action: Events trigger agents when needed
**Visual description:** Three stacked white cards with a thin grey border and a coral-red bar down
the left edge, centered on the page. In each, a bold dark label ("Less friction:", "In the flow of
work:", "Timely action:") is followed by one grey sentence.
**What it teaches:** Three reasons for the loop: no copying between tools, the agent lives where
the conversation already is, and a change in the source can trigger the agent by itself.

### Slide 6.4 — In this lesson (third deck, slide 4)
**Evidence:** Narrated — "In this lesson, first, we will see the event driven loop in action, using it in Slack, Jira, and Confluence, and we'll see how events in these tools trigger our agent. ... In the next step, you will learn how to run the agent loop yourself on your local machine by cloning the repo. and setting up the integrations on your end. Finally, we will look at how to build your own event-driven loop using the verification loop of Lesson 4 as the start point, and the specifications you can give to a coding agent, like Claude Code, to build the same event-driven loop built in this lesson."
**Text on slide:** In this lesson · 1 · See the event loop in action · Event-driven agents in Slack, Jira, and Confluence · 2 · Run the evel loop yourself · Clone the repo and set up the integrations · 3 · Build your own · Extend the verification loop into an event-driven agent using specs and a coding agent
**Visual description:** Three stacked cards joined by a coral-red bracket line on the left, each
with a numbered circle (1 to 3) in a pale pink disc, a bold title and a grey one-line subtitle.
**What it teaches:** The lesson's three parts: watch the loop work in Slack, Jira and Confluence;
run it yourself by cloning the repo and setting up the integrations; and build your own by
extending the verification loop with a spec handed to a coding agent. The deck writes "evel loop"
where the narration says the event loop.

### Slide 6.5 — Title card: Event driven loop (Tall deck, slide 15)
**Evidence:** Deck-only (title card; its subtitle is this lesson's subject)
**Text on slide:** Loop Engineering with LangChain Deep Agents · Event driven loop
**Visual description:** Tall title card, course title on two lines, subtitle "Event driven loop".
**What it teaches:** Names the lesson in the Tall deck.

### Slide 6.6 — Event-driven loop diagram (Tall deck, slide 16)
**Evidence:** Narrated by the same passage as Slide 6.2 (the diagram is the same); which of the two
decks was on screen cannot be known from the materials.
**Text on slide:** (no title; the extracted text layer is empty) · event trigger · verification loop · agent loop · model · action · observation · tools · result · retry with feedback · grader · rubric / eval · new events · system update · service improves
**Visual description:** Near-duplicate of the diagram on Slide 2.8 (Wide deck, slide 8) and Slide
6.2, with no title and no left-hand text: the upper half of the page is blank and the diagram sits
in the lower half. Same elements and colors. All labels here are read from the image because the
text layer is empty.
**What it teaches:** The same as Slide 6.2.

---

## Lesson 7: Learning loop
Transcript: `## Lesson 7: Learning loop` in transcripts/loop-engineering-with-langchain-deepagents-transcripts.md

Tall-deck slides 17 and 18: a title card and one diagram showing many runs feeding one grader
whose feedback is mined across runs. The rest of the lesson narrates the notebook (five
requirements, an analyst agent, a proposal file, and a re-run).

### Slide 7.1 — Title card: Learning loop (Tall deck, slide 17)
**Evidence:** Deck-only (title card; its subtitle is this lesson's title)
**Text on slide:** Loop Engineering with LangChain Deep Agents · Learning loop
**Visual description:** Tall title card, course title on two lines, subtitle "Learning loop".
**What it teaches:** Names the lesson. The deck calls this loop "Learning loop"; the Wide deck
calls it "Learning / hill climbing loop" and "Hill-climbing loop".

### Slide 7.2 — Learning Loop (Tall deck, slide 18)
**Evidence:** Narrated — "Instead of looking at just one run, we are going to look across the traces from many completed runs and ask what does this agent keep getting wrong? If we see the same correction coming up across completely different documents, we will use those findings to make the agent better for future runs."
**Text on slide:** Learning Loop · REQUIREMENT 1: · REQUIREMENT 2: · Requirements analysis agent · Grader · Feedback · Look across many runs · Find recurring corrections · Improve the agent for future runs
**Visual description:** Two pink dashed boxes side by side at the top, "REQUIREMENT 1:" and
"REQUIREMENT 2:" in dark-red caps, each over a dashed placeholder line. Arrows from both converge
on the navy "Requirements analysis agent"; an arrow down to the dark green "Grader"; an arrow
down to a yellow "Feedback" box. A line leaves "Feedback", climbs the right side, and re-enters
the agent box. Three grey bullets below.
**What it teaches:** The learning loop reuses the verification loop's feedback across many runs:
different requirements go through the same agent and grader, recurring corrections are found, and
the agent is improved for future runs.

---

## Lesson 8: Conclusion
Transcript: `## Lesson 8: Conclusion` in transcripts/loop-engineering-with-langchain-deepagents-transcripts.md

No slide in any deck belongs to this lesson. The transcript is three sentences recapping the
loops that were added.

---

## Discrepancies

Facts only; each item names the slide(s) and the transcript passage that differ.

1. **The event-driven lesson's slides are split across two decks, and most of the lesson has no
   slide.** The third deck (`new_lesson.pdf`) carries four slides for Lesson 6; the Tall deck
   carries a title card (slide 15) and a diagram (slide 16) for the same lesson, the diagram a copy
   of the third deck's slide 2 and the Wide deck's slide 8. The Slack, Jira and Confluence demos
   and every setup step the narration walks through ("create a Slack app by going through these
   six steps", "get Atlassian API credentials by going here", the tunneling service, the Jira and
   Confluence automation steps) are on screen as recordings, not slides. The third deck's slide 4
   writes "Run the evel loop yourself" where the narration says the event loop.
2. **"Loop" versus "Level" numbering in the Wide deck.** Slide 4 is titled "Loop 1: The Agent
   Loop"; slides 6, 8 and 10 are titled "Level 2", "Level 3", "Level 4". Slide 3 says "Four levels
   of loops"; slides 12 and 13 number them "1." to "4.". The Lesson 2 narration says "four levels of
   loops" and also "We consider Loop 3 to be a loop".
3. **Third loop named "APPLICATION LOOP" on Wide slide 12.** Everywhere else in both decks and in
   the transcripts the third loop is "Event-driven loop" / "Event driven loop". The matching
   narration describes the third human-oversight case as "human approval on agent artifacts or
   results" without naming the loop.
4. **Fourth loop has several names.** Wide slide 3 and slide 13: "Hill-climbing loop"; Wide slides
   10 and 11: "Learning / hill climbing loop"; Wide slide 12: "HILL CLIMBING LOOP (System-level
   Optimization)"; Tall slide 10: "Hill-climbing / learning loop"; Tall slide 17: "Learning loop".
   Transcripts: Lesson 1 and Lesson 2 say "hill-climbing loop", Lesson 2 also "self-improvement
   loop" and "learning loop", Lesson 7's heading is "Learning loop" and its narration says "the
   hill climbing or learning loop".
5. **Course title spelling.** Wide slide 1 and the transcript file heading write "LangChain
   DeepAgents" (one word); every Tall-deck title card writes "LangChain Deep Agents" (two words).
   The Lesson 1 narration says "DeepAgents"; Lesson 3 says "LangChain Deep Agents".
6. **Tall slide 13 is titled "Agent Tools"** (the same title as Tall slide 10) but shows the
   rubric criteria and pass/fail flow, not tools.
7. **Requirement wording differs.** Tall slides 9 and 14 quote "Users shall be able to upload files
   to their profile. Uploaded files should be stored securely. The system should support common
   file types." The Lesson 4 narration quotes it as "Users should be able to upload files to their
   profile. Their files should be stored securely, and this feature should support all common
   files."
8. **Memory file name.** Tall slide 4 lists "Memory: Agent.md"; Tall slide 5 and the Lesson 4
   narration use "AGENTS.md". The Lesson 3 narration uses both ("the Agent.md files" and
   "AGENTS.md").
9. **Model in the code samples.** Tall slide 2 uses `model="openai:gpt-5.5"`; Tall slide 5 uses
   `"openai:gpt-5.4-mini"`. The Lesson 3 narration says "The model we'll be using is GPT-5.4-mini"
   for the notebook; Lesson 7 uses gpt-5.5 only for the analyst agent.
10. **Count of runs in the learning loop.** Tall slide 18 shows two placeholders ("REQUIREMENT 1:",
    "REQUIREMENT 2:"). The Lesson 7 narration first says "four different documents:
    Authentication, Notifications, Payments, and Alerting" and then "these five different
    requirements"; the notebook runs five.
11. **Lesson 5's notebook uses a different requirement than its slides.** Tall slides 12 to 14
    illustrate the verification loop on "User Profile File Upload"; the Lesson 5 narration runs
    the notebook on "a Real-time Notification System" requirement. The narration itself also uses
    the file-upload example before switching to the notebook.
