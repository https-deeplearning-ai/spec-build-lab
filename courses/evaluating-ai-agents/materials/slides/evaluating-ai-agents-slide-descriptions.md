# Slide descriptions: Evaluating AI Agents
Source decks (all under `../repo/slides/`, all wide 16:9): `Copy of Arize_short course wide slides.pdf` (7 slides), `Copy of ArizeDLAICourse-Lesson-1.pdf` (19), `-Lesson-2a.pdf` (11), `-Lesson-2b.pdf` (9), `-Lesson-3.pdf` (20), `-Lesson-4.pdf` (14), `-Lesson-5a.pdf` (15), `-Lesson-5b.pdf` (8), `-Lesson-6.pdf` (13). 116 slides in all.
Instructors: John Gilhuly and Aman Khan (Arize AI)

Rich text descriptions of the course slides, organized by lesson in the same order and with the
same lesson titles as the transcripts in `../transcripts/`. Each entry gives the deck and original
slide number, the evidence that ties the slide to a lesson (a verbatim transcript passage, or a
note that none exists), every word visible on the slide, a description of the visual, and what it
teaches.

## How to read this file

- **Lesson assignment rests on transcript content, not video frames.** No lesson videos were
  available, so no slide was matched to a video by frame sampling and there are no timestamps.
  Each slide was placed in the lesson whose narration describes what the slide shows. The decks
  were read page by page as images alongside their extracted text layer; words inside diagrams
  and screenshots were read from the images.
- **Evidence field.** "Narrated" means a transcript passage clearly describes what the slide shows;
  the passage is quoted verbatim. The transcript wraps lines mid-sentence, so quotes read its line
  breaks as single spaces; "[...]" or " … " marks a cut between two exact passages. Transcript
  typos are kept as printed. "Deck-only" means no transcript passage matches. "Narrated" is the
  best available proxy for "shown in the video", but it is a proxy.
- **Lesson numbering comes from the transcripts:** 1 Introduction, 2 Evaluation in the time of
  LLMs, 3 Decomposing agents, 4 Lab 1: Building your agent, 5 Tracing agents, 6 Lab 2: Tracing
  your agent, 7 Adding router and skill evaluations, 8 Lab 3: Adding router and skill evaluations,
  9 Adding trajectory evaluations, 10 Lab 4: Adding trajectory evaluations, 11 Adding structure to
  your evaluations, 12 Lab 5: Adding structure to your evaluations, 13 Improving your
  LLM-as-a-judge, 14 Monitoring agents, 15 Conclusion. **The deck file names use their own
  numbering** and must not be read as transcript lesson numbers. The decks map onto the
  transcript lessons by their title cards, and each deck covers exactly one lesson:
  - deck "course-wide" (title card "Evaluating AI Agents", no subtitle; instructor card, course
    outline, acknowledgments) = Lesson 1;
  - deck "Lesson-1" ("Evaluation in the Time of LLMs") = Lesson 2;
  - deck "Lesson-2a" ("Decomposing Agents") = Lesson 3;
  - deck "Lesson-2b" ("Observing Agents") = Lesson 5 "Tracing agents" (title differs, content
    matches);
  - deck "Lesson-3" ("Adding Router & Skill Evaluations") = Lesson 7;
  - deck "Lesson-4" ("Adding Trajectory Evaluations") = Lesson 9;
  - deck "Lesson-5a" ("Adding Structure to your Evaluations") = Lesson 11;
  - deck "Lesson-5b" ("Improving your LLM-as-a-Judge") = Lesson 13;
  - deck "Lesson-6" ("Monitoring Agents") = Lesson 14.

  Transcripts win wherever the decks disagree.
- **Lessons with no slides.** The five labs (Lessons 4, 6, 8, 10, 12) are notebook walkthroughs;
  their code is in `../notebooks/from-repo/evaluating-ai-agents-context.md`. Lesson 15
  (Conclusion) has no deck. Each has a short stub section below.
- **Cross-references in the narration use their own numbering.** Lesson 2 calls itself "this
  first lesson"; Lesson 13 calls itself "a bonus lesson" and refers to Lesson 11 as "the previous
  slides lesson"; Lesson 10 refers back to "the previous slides" (Lesson 9).
- **Production slides.** Slide 2 of most decks is a pale "Talking Head" placeholder marking where
  the instructor is on camera, and course-wide slide 2 is a note to the video editor
  ("Meta-slide: The next section is about the intro slide"). They carry no teaching content and
  are listed as Deck-only so every page is accounted for.
- **Hidden text layer.** Every lesson deck's title card has the text "[Your Logo Here]" in its
  text layer, not visible on the page. It is left out of the slide text.
- **Animations cannot be known from a PDF.** Where consecutive slides look like stages of one
  build (the same diagram or table with more filled in), that is a reading of the drawings.
- **Visual conventions shared by all decks.** Content slides have the arize wordmark (pink caret
  mark, black "arize") top left, the DeepLearning.AI logo (coral concentric mark and name) top
  right, a centered black title, grey body text, and a coral-red wave along the bottom edge. Title
  cards are white with "Evaluating AI Agents" in coral red, the lesson title in slate grey below,
  and the two logos side by side near the bottom, with no wave. Agent diagrams are in a
  hand-drawn (Excalidraw-style) look: blue "User" ellipses, red rounded "Router" boxes,
  black-outlined tool boxes, red text for LLM-call steps and green text for pure-code steps.

## Where slides and narration differ

Listed so a reader can weigh them; the transcript wins in each case.

- **Slide 1.4:** "update the prompt" is drawn at the Plan step; the narration asks whether to
  "update a prompt at the last step".
- **Slide 2.8** lists "Summarization performance" and "Code writing correctness and readability";
  the narration says "overall performance" and does not mention code writing.
- **Slide 2.12** "Popular Agent Frameworks" (three DeepLearning.AI course banners) is never
  narrated.
- **Slide 2.18** says "PLAYGROUND ON DATA"; the narration says "a prompt playground".
- **Router model label:** "GPT-4o-mini w/ function calling" on most diagrams (Slides 7.17–7.18,
  most of Lesson 9, Slides 14.10 and 14.12), but "GPT-4o w/ function calling" on Slide 7.19, in
  the "Agent 1" box of Slide 9.8, and on Slide 14.5. No narration names the router model.
- **Slide 7.18** lists "SQL gen correctness" twice under Tool #1, once as code-based and once as
  LLM-as-a-Judge; Slide 7.19 keeps only the code-based one. The narration explains both. Slide
  7.19 has no title.
- **Slide 9.7** says "Plot daily sales volume over time"; the narration says "plot sales data
  volume over time".
- **Slide 11.5** says "25+ examples of inputs to your agent"; the narration says "You don't need
  to have hundreds and hundreds of examples", asks for "1 or 2 examples from each of the different
  types of inputs", and never says 25.
- **Tool names:** the agent diagram on Slide 11.8 says "Look Up Sales Data Tool", "Data Analysis
  Tool" and "Data Visualization Tool"; the table on Slides 11.9–11.12 says "Database lookup tool"
  and "Database analysis tool" and has no row for the visualization tool.
- **Slide 14.3** (agenda) promises "Adding experiments to a CI/CD pipeline"; the narration covers
  it only as concepts, with no pipeline shown.
- **Slides 14.8–14.9** show screenshots of a LlamaIndex RAG demo app (`demo_llama_index`), not the
  course's own agent; Slide 14.11 shows a dataset scored by the course's kind of evaluators.

## Repeated slides

- The "LLM-based Application" diagram appears on both Slide 2.5 and Slide 2.9 with different
  titles and bullets.
- The sales-agent diagram appears on Slide 14.5 (third panel), Slide 14.10, and, extended with a
  "Self Improvement" box, Slide 14.12.
- Slide 13.3 repeats the Router row of Slide 11.9, with an asterisk added after "LLM-as-a-Judge".
- The course-wide deck repeats no slide from deck "Lesson-1". It was not compared against the
  later decks.

---

## Lesson 1: Introduction
Transcript: `## Lesson 1: Introduction` in transcripts/evaluating-ai-agents-transcripts.md

All 7 slides of deck "course-wide" belong here, in deck order: the course title card, a
production note, the instructor card, two evaluation-driven-development diagrams (a coding agent,
then a research agent), the course outline with the data analyzer agent diagram, and the
acknowledgments.

### Slide 1.1 — Title card: Evaluating AI Agents (deck "course-wide", slide 1)
**Evidence:** Deck-only (course title card)
**Text on slide:** Evaluating AI Agents
**Visual description:** Wide white title card. "Evaluating AI Agents" in coral red, centered in the
upper half. Below it, side by side, the arize logo (pink caret mark, black "arize") on the left and
the DeepLearning.AI logo (coral concentric-circle mark above the coral name) on the right. No
subtitle, no wave.
**What it teaches:** Names the course and its two partners.

### Slide 1.2 — Meta-slide: The next section is about the intro slide (deck "course-wide", slide 2)
**Evidence:** Deck-only (production note to the video editor)
**Text on slide:** Meta-slide: The next section is about the intro slide
**Visual description:** A content-slide frame with only the DeepLearning.AI logo top right (no
arize logo), the one-line title at the top, an empty white body, and the coral wave at the bottom.
**What it teaches:** Nothing for the learner; it marks a section break in the source deck.

### Slide 1.3 — Title card: Evaluating AI Agents, John Gilhuly, Aman Khan (deck "course-wide", slide 3)
**Evidence:** Narrated — "The instructors of this course are John Gilhuly, whose head of developer relations and Aman Khan, who is director of product at Arize AI."
**Text on slide:** Evaluating AI Agents · John Gilhuly, Aman Khan
**Visual description:** White title card. "Evaluating AI Agents" in coral red at the top, the arize
logo alone in the middle, and the two instructor names in grey-blue below. No DeepLearning.AI logo,
no wave.
**What it teaches:** Introduces the two instructors.

### Slide 1.4 — Evaluation-driven Development: AI coding agent (deck "course-wide", slide 4)
**Evidence:** Narrated — "Say you're building an AI coding agent, you might have to carry out a lot of steps to generate good code such as plan, use tools, reflect, and so on. And using an evaluation driven development process would make your development much more efficient." Also — "So if you're asking yourself questions like should you update a prompt at the last step, or should you update the logic of the workflow, or should you change the large language model you're using?"
**Text on slide:** Evaluation-driven Development · AI Coding Agent · User · Plan · Use Tools · Reflect · User · update the prompt · update the LLM · update the logic · Observability
**Visual description:** A hand-sketched flow. A light-blue "User" circle on the left points into a
dashed rounded box labelled "AI Coding Agent". Inside, three white boxes with thick orange borders,
"Plan" → "Use Tools" → "Reflect", with a grey arrow looping from after "Reflect" back to "Plan".
An arrow leaves the box to a second light-blue "User" circle on the right. Red handwritten notes
with small red arrows: "update the prompt" points at "Plan", "update the LLM" points at "Reflect",
and "update the logic" points at the dashed box edge. Below the dashed box, a wide peach rounded
bar reads "Observability" in orange.
**What it teaches:** An agent is a multi-step loop (plan, use tools, reflect) between a user's
request and its answer. Three kinds of change are possible (the prompt, the model, the workflow
logic), and observability under the whole agent is what lets you decide which to make,
systematically rather than by trial and error.

### Slide 1.5 — Evaluation-driven Development: evaluate the quality of each step's output (deck "course-wide", slide 5)
**Evidence:** Narrated — "Say you're building a research agent that searches the web, identifies sources, collects content, summarizes findings, and then maybe iterates if it identifies any weaknesses as an output. When you're building this complex system, you need to evaluate the quality of each step's output. For example, for source selection, you might create a test set that comprises research topics and the corresponding set of expected sources, and then measure the percentage of times that the agent chooses to correct sources. Or for open ended tasks like summarization, you can prompt a separate large language model or apply what we call large language model as judge."
**Text on slide:** Evaluation-driven Development · Evaluate the quality of each step’s output · AI Research Agent · User · Search the Web · Identify sources · Collect content · Summarize · Review Summary · User · Test set: research topics + expected sources · Measure: percentage of times the agent chooses the correct sources · Use LLM-as-a-judge to evaluate the quality of the summary.
**Visual description:** Same hand-sketched style as Slide 1.4, with the subtitle in grey-blue under
the title. A "User" circle points into a dashed box labelled "AI Research Agent" holding five boxes
in a row: "Search the Web" → "Identify sources" → "Collect content" → "Summarize" → "Review
Summary", with a grey arrow looping from "Review Summary" back to "Search the Web", and an exit
arrow to a second "User" circle. "Identify sources" and "Summarize" have thick orange borders.
Under "Identify sources", blue handwriting "Test set: research topics + expected sources" and
orange handwriting "Measure: percentage of times the agent chooses the correct sources". Under
"Summarize", blue handwriting "Use LLM-as-a-judge to evaluate the quality of the summary."
**What it teaches:** Evaluate each step of an agent separately, choosing the method to fit the
step: a step with a known right answer (source selection) gets a labelled test set and an accuracy
percentage; an open-ended step (summarization) gets an LLM-as-a-judge.

### Slide 1.6 — Course Outline (deck "course-wide", slide 6)
**Evidence:** Narrated — "You'll do this by creating a code based agent that operates as a data analyzer. The agent will have access to a set of tools that allow it to connect to a database and perform analysis. A router that identifies what tool to use, and a memory that keeps track of the chat history. You'll collect and evaluate traces of the steps taken by your agent to process a query and visualize the collected data. You'll then learn how to evaluate each tool in your agent workflow using different types of evaluators. You also evaluate if the router chooses the right tool based on the user's query, and if it extracts the right parameters to execute the tool and assess the trajectory taken by the agent. Finally, you put all of your evaluators into a structured experiment that you can use to iterate on and improve your agent."
**Text on slide:** Course Outline · Create a code-based agent · Collect traces of the agent’s steps · Evaluate each tool · Evaluate the router: · Choice of right tool · Extraction of the right parameters · Assess the trajectory · Run structured experiments to iterate on the agent · Data Analyzer Agent · User · Router · Tool 1 · Tool 2 · Tool 3 · Memory
**Visual description:** Left, a grey bulleted list with two indented sub-bullets under "Evaluate the
router:". Right, a hand-sketched dashed box labelled "Data Analyzer Agent". A light-blue "User"
circle outside it has a pair of opposite arrows to and from a pink "Router" box (red text) inside.
Three arrows fan out from "Router" to white boxes "Tool 1", "Tool 2", "Tool 3". Along the bottom of
the dashed box, a wide lavender bar reads "Memory" in purple.
**What it teaches:** The course's running example and its order of work: build a data analyzer
agent made of a router, tools and memory; trace it; evaluate each tool; evaluate the router on both
tool choice and parameter extraction; assess the trajectory; then wrap the evaluators in
structured experiments to iterate.

### Slide 1.7 — Acknowledgments (deck "course-wide", slide 7)
**Evidence:** Narrated — "I'd like to thank Mikyo King, Xander Song, and Aparna Dhinakaran from Arize AI. And from DeepLearning.AI Hawraa Salami has also contributed to this course."
**Text on slide:** Acknowledgments · Mikyo King · Arize AI · Xander Song · Arize AI · Aparna Dhinakaran · Arize AI · Hawraa Salami · DeepLearning.AI
**Visual description:** Four circular headshots with name and organization captions: three in a
top row (Mikyo King, shown as an illustrated portrait in a cap; Xander Song; Aparna Dhinakaran),
one centered in a second row (Hawraa Salami).
**What it teaches:** Credits the contributors.

---

## Lesson 2: Evaluation in the time of LLMs
Transcript: `## Lesson 2: Evaluation in the time of LLMs` in transcripts/evaluating-ai-agents-transcripts.md

All 19 slides of deck "Lesson-1" belong here; the deck's title card subtitle is this lesson's
title and the narration follows the deck order. Two slides are not narrated: the "Talking Head"
placeholder (2.2) and "Popular Agent Frameworks" (2.12).

### Slide 2.1 — Title card: Evaluation in the Time of LLMs (deck "Lesson-1", slide 1)
**Evidence:** Deck-only (title card; its subtitle is this lesson's title)
**Text on slide:** Evaluating AI Agents · Evaluation in the Time of LLMs
**Visual description:** Wide white title card. The course title in coral red, the subtitle in
grey-blue below it, then the arize logo bottom left of center and the DeepLearning.AI logo bottom
right of center. No wave.
**What it teaches:** Names the course and the lesson.

### Slide 2.2 — Talking Head (deck "Lesson-1", slide 2)
**Evidence:** Deck-only (production placeholder; the video shows the instructor here)
**Text on slide:** Talking Head
**Visual description:** A plain cream-yellow slide with "Talking Head" in bold dark grey in the
middle. No logos, no wave.
**What it teaches:** Nothing for the learner; it marks where the instructor appears on camera.

### Slide 2.3 — In this lesson (deck "Lesson-1", slide 3)
**Evidence:** Narrated — "In this first lesson, you'll learn how evaluating LLM-based systems differs from traditional software testing. We'll then examine what agents mean and discuss what you need to consider when evaluating agents."
**Text on slide:** In this lesson: · LLM model evaluation vs LLM system evaluation · Similarities and differences to software development testing · Agent use cases and why you should evaluate agents · Agent testing and iteration tools
**Visual description:** A plain bulleted list of four grey items under the title.
**What it teaches:** The lesson's four topics.

### Slide 2.4 — Scope of evaluation (deck "Lesson-1", slide 4)
**Evidence:** Narrated — "When you think about evaluation in general, there are typically two layers. On the left-hand side, you have LLM model evaluation. This focuses on how well a large language model performs a specific task. You might have seen benchmarks like MMLU for questions spanning math, philosophy, medicine and more, or human eval for code generation tasks. Providers often use these benchmarks to showcase how their foundation models stack up. On the right-hand side, you have an LLM system or application evaluation. This zeroes in on how well your overall application, of which the LLM is just a part of, performs. Here, the data sets being used for evaluation are created either manually, automatically, or synthetically, using real-world data."
**Text on slide:** Scope of evaluation · LLM Model Evaluation · Measure the general language understanding of the foundational models. · Benchmark Datasets · LLM · Example of Benchmark Datasets: · MMLU (multiple-choice questions covering math, philosophy, medicine…) · HumanEval (code generation) · LLM System Evaluation · Evaluate how well the entire application, including the LLM, performs (meeting business requirements). · LLM-based Application · Testing Datasets · LLM · Testing Datasets can be manually created, synthesized, or curated from the application · i.e. real world data
**Visual description:** Two columns split by a thin grey vertical line, each with a bold grey
heading. Left: a bullet, then a small diagram where "Benchmark Datasets" has an arrow into a grey
"LLM" box, then a bullet with two sub-bullets. Right: a bullet, then a small diagram where
"Testing Datasets" has an arrow into a dashed box labelled "LLM-based Application" with a grey
"LLM" box inside it, then a bullet with one sub-bullet.
**What it teaches:** Two layers of evaluation: model evaluation scores a bare LLM on public
benchmarks; system evaluation scores the whole application (the LLM plus everything around it)
against its business requirements, on test datasets built by hand, synthesized, or curated from
real application data. The course is about the second layer.

### Slide 2.5 — LLM-based applications (deck "Lesson-1", slide 5)
**Evidence:** Narrated — "When you incorporate an LLM into a broader system or product, you'll want to understand if the entire system including the prompts, tools, memory, and routing components are delivering the results that you expect."
**Text on slide:** LLM-based applications · Input: user’s query · LLM-based Application · prompt · LLM · memory · tools · data sources · Output / Response · Examples: Agents, RAG Systems
**Visual description:** "Input: user's query" on the left with an arrow into a dashed box labelled
"LLM-based Application". Inside it a grey "LLM" box, surrounded by light-grey words "prompt"
(left), "memory" (right), "tools" and "data sources" (below). An arrow leads out to "Output /
Response" on the right. One bullet below the diagram.
**What it teaches:** An LLM application wraps the model in a prompt, tools, memory and data
sources, between a user's query and the response; agents and RAG systems are examples.

### Slide 2.6 — A paradigm shift from traditional software testing: train and city traffic (deck "Lesson-1", slide 6)
**Evidence:** Narrated — "You may have experience with traditional software testing, where systems are largely deterministic. You can picture that like a train on a track. There's usually a well-defined start and end, and it's often straightforward to check whether each piece, the train or the track is working correctly. LLM-based systems, on the other hand, can feel more like driving a car through a busy city. The environment is variable and the system is non-deterministic."
**Text on slide:** A paradigm shift from traditional software testing
**Visual description:** Two photographs split by a grey vertical line. Left: a white bullet train
on a track through green countryside. Right: a crowded city street between tall buildings, with a
yellow taxi, a black car, pedestrians crossing and traffic lights.
**What it teaches:** The metaphor for the shift: traditional software is a train on fixed rails
(deterministic, easy to check piece by piece); an LLM system is a car in city traffic (variable
environment, non-deterministic behaviour).

### Slide 2.7 — A paradigm shift from traditional software testing (deck "Lesson-1", slide 7)
**Evidence:** Narrated — "With software testing, you rely on unit tests to check individual parts of the system and integration tests to make sure they fit together as intended. And the results are usually pretty deterministic. Unlike traditional software testing, when you give the same prompt to an LLM multiple times, you might see slightly different responses. Just like how drivers can behave differently in city traffic. You're often dealing with more qualitative or open-ended metrics, like the relevance or coherence of the output, which might not fit neatly into a strict pass/fail test model."
**Text on slide:** A paradigm shift from traditional software testing · Traditional software testing: · Unit testing: testing individual component of the software application · Integration testing: testing how different components work together · Testing in the time of LLMs: · Non-deterministic nature of LLMs: outputs can vary even with the same inputs · Focus on testing the application’s ability to respond to users’ specific tasks · Examine the output quality (relevance, coherence)
**Visual description:** Two top-level bullets, each with indented hollow-circle sub-bullets, in
grey text. No diagram.
**What it teaches:** Unit and integration tests assume deterministic outputs. LLM testing must
handle outputs that vary for the same input, focus on whether the application does the user's
task, and judge qualitative output properties such as relevance and coherence.

### Slide 2.8 — Common Types of Evaluations for LLM Systems (deck "Lesson-1", slide 8)
**Evidence:** Narrated — "There are a number of common evaluation types for LLM systems. We have hallucination. Is the LLM accurately using provided context or as in making things up? Retrieval relevance. If the system retrieves documents or context, are they actually relevant to the query? Question answering accuracy. Does the response match the ground truth the user needs? Toxicity. Is the LLM outputting harmful or undesirable language? And overall performance. How well is the system performing at its goal?"
**Text on slide:** Common Types of Evaluations for LLM Systems · Hallucinations · Retrieval relevance · Q&A on retrieved data · Toxicity · Summarization performance · Code writing correctness and readability
**Visual description:** A plain bulleted list of six grey items.
**What it teaches:** A catalogue of standard LLM-system evaluations. The narration adds the
question each one asks; it names "overall performance" where the slide has "Summarization
performance" and does not mention the last bullet.

### Slide 2.9 — LLM-based applications: agents (deck "Lesson-1", slide 9)
**Evidence:** Narrated — "As soon as you move from an LLM-based app to an agent, you're adding an extra layer of complexity. Agents use LLMs for reasoning, but they also take actions on your behalf by choosing among tools, APIs, or other capabilities."
**Text on slide:** LLM-based applications: agents · Input: user’s query · LLM-based Application · prompt · LLM · memory · tools · data sources · Output / Response · What are agents? · What could go wrong with agent-based systems?
**Visual description:** The same diagram as Slide 2.5, shifted slightly left, with two question
bullets below it in place of the examples bullet.
**What it teaches:** Agents are a kind of LLM application; the two questions set up the next
slides (what an agent is, and how it can fail).

### Slide 2.10 — What are agents? (deck "Lesson-1", slide 10)
**Evidence:** Narrated — "an agent as a software-based system that can take actions on behalf of a user utilizing reasoning. An agent typically has three main components. We have reasoning, which is powered by the LLM. Routing, which is deciding which tool or skill to use. And the action, which is executing the tool call, API call, or code."
**Text on slide:** What are agents? · Agents are software based systems that can take actions on behalf of a user utilizing reasoning · Reasoning: powered by AI (LLMs) · Routing: interpreting request and determining the correct tool · Action: executing code/tools (utilizing APIs, making LLM call)
**Visual description:** One bullet with three indented hollow-circle sub-bullets, in grey text.
**What it teaches:** The definition of an agent and its three components: reasoning (the LLM),
routing (choosing the tool for a request) and action (running the code, tool or API call).

### Slide 2.11 — Agent use cases (deck "Lesson-1", slide 11)
**Evidence:** Narrated — "You may have already seen examples of agent use cases, like personal assistant agents that help you take notes or transcribe information for you. Desktop or browser-based agents that help automate repetitive tasks. Agents for data scraping and summarization and agents that can conduct search and compile research."
**Text on slide:** Agent use cases · Personal assistants · Desktop or Browser agents · Automated scraping and summarization · Research assistant
**Visual description:** A plain bulleted list of four grey items.
**What it teaches:** Typical kinds of agents.

### Slide 2.12 — Popular Agent Frameworks (deck "Lesson-1", slide 12)
**Evidence:** Deck-only (no passage in Lesson 2 mentions agent frameworks or these courses)
**Text on slide:** Popular Agent Frameworks · All Courses › Short Courses › AI Agents in LangGraph · Short Course · Intermediate · 1 Hour 25 Minutes · AI Agents in LangGraph · Instructors: Harrison Chase, Rotem Weiss · LangChain · Tavily · Enroll for Free · All Courses › Short Courses › Building Agentic RAG with LlamaIndex · Short Course · Beginner · 46 Minutes · Building Agentic RAG with LlamaIndex · Instructor: Jerry Liu · LlamaIndex · Enroll for Free · All Courses › Short Courses › Practical Multi AI Agents and Advanced Use Cases with crewAI · Short Course · Beginner · 2 Hours 43 Minutes · Practical Multi AI Agents and Advanced Use Cases with crewAI · Instructor: João Moura · crewAI · Enroll for Free · Building Agentic RAG with Llamaindex · Practical Multi AI Agents and Advanced Use Cases with crewAI
**Visual description:** Three overlapping screenshots of DeepLearning.AI course page banners,
cascading from top left to bottom right: a dark green "AI Agents in LangGraph" banner with the
LangChain and Tavily logos and two instructors on video; a purple-pink "Building Agentic RAG with
LlamaIndex" banner with the LlamaIndex llama logo and one instructor; a beige "Practical Multi AI
Agents and Advanced Use Cases with crewAI" banner with the crewAI logo and one instructor in front
of a monitor showing the course title. Each banner has a breadcrumb, level and duration tags, a
white "Enroll for Free" button and a play button on the video. The last two lines of the text list
are the small titles on the monitors inside the second and third screenshots.
**What it teaches:** Points to three agent frameworks (LangGraph, LlamaIndex, crewAI) and the
DeepLearning.AI courses that teach them.

### Slide 2.13 — Anatomy of an Agent (deck "Lesson-1", slide 13)
**Evidence:** Narrated — "Suppose you want an agent to book a trip to San Francisco. There's a lot going on behind the scenes. First, the agent has to figure out which tool or API it should call based on your request. It needs to understand what you're really asking for and which resources will help. Next, it might call a search API to check available flights or hotels, and it could decide to ask you follow-up questions or refine how it constructs the request for that tool. Finally, you wanted to return a friendly and accurate response, ideally with the correct trip details."
**Text on slide:** Anatomy of an Agent · Trip planning · i.e. Book me a trip to San Francisco · Figure out which tool to call · Search API · Use context · Construct a response · Overall correctness
**Visual description:** A three-level grey list: a round bullet, a hollow-circle sub-bullet ending
in a small Golden Gate Bridge in fog emoji, and five square third-level bullets.
**What it teaches:** Breaks one agent request into its steps: pick the tool, call the search API,
use context, build the response, and be correct overall.

### Slide 2.14 — Agent Evaluation Example (deck "Lesson-1", slide 14)
**Evidence:** Narrated — "Now, let's think about how you'd evaluate the step by step. Did the agent pick the right tool in the first place? When it forms a search or booking request that it call the correct function with the right parameters? Is it using your contacts, for instance, the dates, preferences, and location accurately? How does the final response look? Does it have the right tone and is it factually correct?"
**Text on slide:** Agent Evaluation Example · Trip planning · i.e. Book me a trip to San Francisco · Figure out which tool to call (tool selection evaluation or eval) · Search API (function calling eval) · Use context (RAG eval) · Construct a response (tone eval) · Overall correctness (correctness eval)
**Visual description:** The same list as Slide 2.13 with an evaluation name in parentheses added
to each third-level bullet.
**What it teaches:** Each step of the agent gets its own evaluation: tool selection, function
calling (right function, right parameters), RAG (use of context), tone, and overall correctness.

### Slide 2.15 — What could go wrong? (deck "Lesson-1", slide 15)
**Evidence:** Narrated — "Maybe the agent returns flights to San Diego instead of San Francisco. That might work for some people. Then those folks would be unhappy if they wanted San Francisco and ended up with San Diego. This highlights why you need to evaluate not just the LLMs raw output, but also how the agent decides on each action along the way. You might see issues like the agent calling the wrong tool, misusing context, or even adopting a snarky or inappropriate tone. Sometimes users also try to jailbreak the system, which can create even more unexpected outputs. To evaluate each of these factors. You can use human feedback or human in the loop or in less an LLM itself as a judge to assess whether the agent's final response is truly fulfilling your requirements."
**Text on slide:** What could go wrong? · Trip planning · i.e. Book me a trip to San Francisco San Diego · Figure out which tool to call (tool selection eval) → Calls the wrong tool · Search API (function calling eval) → Constructs search incorrectly · Use context (RAG eval) · Construct a response (tone eval) → Could be jailbroken, or inappropriate · Overall correctness (correctness eval) → Unhappy user · LLM-as-a-judge · Results in poor business outcomes and unhappy users!
**Visual description:** The list from Slide 2.14, with "San Francisco" struck through and followed
by "San Diego" and a beach-umbrella emoji. Four steps end in an arrow and a failure in red: "Calls
the wrong tool", "Constructs search incorrectly", "Could be jailbroken, or inappropriate", "Unhappy
user" with a frowning-face emoji. Pink stars sit to the left of three steps (tool selection, use
context, construct a response). Bottom left, a legend: a pink star = "LLM-as-a-judge". Bottom
right, larger grey text: "Results in poor business outcomes and unhappy users!"
**What it teaches:** How each step can fail (wrong tool, malformed search, jailbroken or
inappropriate response, wrong destination for the user), that the failures cost the business, and
which of these steps can be checked with an LLM-as-a-judge (the starred ones: tool selection, use
of context, response tone).

### Slide 2.16 — Even Small Changes Can Cause Performance Regressions (deck "Lesson-1", slide 16)
**Evidence:** Narrated — "Finally, remember that even small changes to your prompts or code can have unexpected ripple effects. For instance, adding a simple line in like "remember to respond politely" might help you improve on a number of use cases, but can also cause a regression in test cases that you may not expect. That's why you want to maintain a representative set of test cases or data sets that reflect your critical use cases."
**Text on slide:** Even Small Changes Can Cause Performance Regressions · LGTM! · system prompt: · You are an assistant debugging RAG, investigate the retrieved results · + Remember to respond politely · Reality of AI Engineering: · Change a prompt or model, break a use case. Repeat.
**Visual description:** Hand-sketched. Left, a person-at-laptop emoji with a thought cloud "LGTM!".
An arrow points to a handwritten system prompt; its added last line "Remember to respond politely"
is highlighted in a green box with a green "+" (a diff addition). Three arrows fan out from the
prompt to three rounded boxes: two green with a check-mark emoji, one red with a prohibited-sign
emoji. Below, "Reality of AI Engineering:" in regular weight, then "Change a prompt or model, break
a use case. Repeat." in large bold black.
**What it teaches:** A one-line prompt change that looks fine can fix some cases and break
another; this is why you keep a representative test set and rerun it after every change to catch
regressions.

### Slide 2.17 — Software Testing vs Agent Evals (deck "Lesson-1", slide 17)
**Evidence:** Narrated — "Just like you do with traditional software. You want to iterate on an agent's performance. However, you can't rely on purely deterministic checks. Agents themselves are non-deterministic, and take multiple paths, and might regress in one scenario even as they improve in another. To handle this, you want a consistent set of tests covering different user cases that get run every time you make a change. These tests often loop back from production data, like real-world queries and real user interactions."
**Text on slide:** Software Testing vs Agent Evals · Software is deterministic · Unit tests are deterministic · Integration tests rely on existing codebase and documentation · LLM Agents are non deterministic · LLM Agents can have multiple paths · Improving agents relies on data
**Visual description:** Two bulleted columns in grey with no headings. Bold words: "deterministic"
(three times), "multiple paths". Left column is software, right column is agents.
**What it teaches:** Contrasts software testing with agent evaluation: software and its tests are
deterministic, agents are not and can take several paths, so improving an agent depends on data
(a test set, fed back from production) rather than on fixed checks.

### Slide 2.18 — Tools you will use to evaluate agents (deck "Lesson-1", slide 18)
**Evidence:** Narrated — "A few of the tools that we're going to be covering in this course are: trace instrumentation to understand what's happening with your agent underneath the hood, an eval runner which contains LLM as a judge, data sets which you can use to rerun experiments, human feedback that allow you to capture human annotations and production, and a prompt playground you can use for your data for iterating on your data."
**Text on slide:** Tools you will use to evaluate agents · PHOENIX · TRACE INSTRUMENTATION · EVAL RUNNER · DATASETS · HUMAN FEEDBACK · PLAYGROUND ON DATA · DEVELOPMENT · Curate dev datasets · TRACE · Evaluate experiments · EVALUATE · ITERATE · Run experiment on app/eval templates, model, retriever, etc. · PRODUCTION · Online evals · EVALUATE · Performance analytics & dashboards · MONITOR · TRACE · Production app traces
**Visual description:** Center, a dotted teal column headed by the Phoenix bird logo and
"PHOENIX", holding five stacked teal-outlined boxes (the five tool names). Teal arrows run from
each box both left to a "DEVELOPMENT" cycle and right to a "PRODUCTION" cycle. Each cycle is a ring
of three colored arcs with small grey arrows between them. Development ring: pink "TRACE" (note
"Curate dev datasets"), navy "ITERATE" (note "Run experiment on app/eval templates, model,
retriever, etc."), orange "EVALUATE" (note "Evaluate experiments"). Production ring: pink "MONITOR"
(note "Performance analytics & dashboards"), navy "TRACE" (note "Production app traces"), orange
"EVALUATE" (note "Online evals").
**What it teaches:** The toolset used in the course (Arize Phoenix): trace instrumentation, an eval
runner, datasets, human feedback, and a playground. The same tools serve two loops, development
(trace, evaluate, iterate) and production (trace, evaluate, monitor), with data flowing between
them.

### Slide 2.19 — What you've learned (deck "Lesson-1", slide 19)
**Evidence:** Narrated — "In this lesson, you took a broad look at how LLM model evaluation compares to system evaluation, why LLM-based apps require different testing approaches than traditional software, the extra complexity that agents bring with reasoning, routing, and action. Common pitfalls with agents like wrong tool selection for context usage and the importance of iterative testing using a single set of tools for development to production."
**Text on slide:** What you’ve learned: · Scope of LLM evaluation · How AI Agents can be used to perform tasks · Similarities and differences between evaluating software and AI agents · Tools that are used to evaluate agents
**Visual description:** A numbered list (1 to 4) in grey under the title.
**What it teaches:** Recap of the lesson's four topics.

---

## Lesson 3: Decomposing agents
Transcript: `## Lesson 3: Decomposing agents` in transcripts/evaluating-ai-agents-transcripts.md

All 11 slides of deck "2a" belong here, in deck order.

### Slide 3.1 — Title card: Decomposing Agents (deck "2a", slide 1)
**Evidence:** Deck-only (title card; its subtitle is this lesson's title)
**Text on slide:** Evaluating AI Agents · Decomposing Agents
**Visual description:** Wide white title card. "Evaluating AI Agents" in coral red, centered;
"Decomposing Agents" in slate grey below; the arize logo bottom left of center and the
DeepLearning.AI logo (concentric coral-red mark over the name) bottom right of center.
**What it teaches:** Names the course and the lesson.

### Slide 3.2 — Talking Head (deck "2a", slide 2)
**Evidence:** Deck-only (production placeholder for the instructor on camera)
**Text on slide:** Talking Head
**Visual description:** Plain pale yellow page with "Talking Head" in bold dark grey, centered.
No logos, no wave.
**What it teaches:** Nothing; it marks where the video cuts to the instructor.

### Slide 3.3 — In this lesson (deck "2a", slide 3)
**Evidence:** Narrated — "In this lesson, we'll dive into the details of this agent structure and then go through an agent example that can perform data analysis."
**Text on slide:** In this lesson: · Understanding the basic structure of agents · Examining an example agent
**Visual description:** Standard content slide with the title and two grey bullets near the top;
the rest of the page is empty.
**What it teaches:** The lesson's two goals: the general structure of agents, and the example
agent built in the course.

### Slide 3.4 — The Main Components (deck "2a", slide 4)
**Evidence:** Narrated — "Agents are typically made up of three main types of components: a router, skills, and then memory and state. The image on the right here shows an example of an agent with a router in black, the state as the dark purple at the bottom, and then a set of three different skills that that agent can call in this case track package, look up item, and answer a question. Each of those different components can interact with the state, and the router is responsible for handling user input and then output back to the user."
**Text on slide:** The Main Components · A Router · Skills · Memory and State · User Input · Router · Track package · Lookup item · Answer question · State
**Visual description:** Left, a numbered list of the three components (1. A Router, 2. Skills,
3. Memory and State). Right, a diagram on a lavender-to-light-blue gradient panel: an arrow
labelled "User Input" enters a black "Router" box; three solid arrows fan out from the router to
three magenta boxes ("Track package", "Lookup item", "Answer question"). A wide dark purple
"State" bar runs along the bottom; dotted two-headed arrows connect the router and each of the
three skill boxes to the State bar.
**What it teaches:** An agent has three parts: a router that takes user input and picks a skill,
a set of skills, and a shared state that every part reads and writes.

### Slide 3.5 — Router (deck "2a", slide 5)
**Evidence:** Narrated — "Looking first at the router, the router is the main planner of the agent. Sort of the agent's brain in a way. The router is responsible for deciding which skill or function the agent will call to answer a user's question. [...] Routers can take a few different forms. They can either be an LLM equipped with function calling, as we'll use in this course, or a more simple NLP classifier, or even just a rules-based code. [...] Some agents, instead of using a single router step, will distribute that logic throughout the agent."
**Text on slide:** Router · The main planner of the agent · Decides which skill or function to call to answer the user's question · Can take the form of an LLM, an NLP classifier, or even rules-based code · Some agents distribute router logic throughout the agent, instead of having a single router unit · User input · Router · Skills
**Visual description:** Four grey bullets, then a simple diagram across the bottom: a thick
slate-blue arrow labelled "User input" points into a rounded slate-blue box labelled "Router" in
bold white; two arrows leave it to the right, diverging, with the label "Skills".
**What it teaches:** The router decides which skill to call. It can be an LLM, an NLP classifier
or rules-based code, and in some agents the routing logic is spread through the agent. The
narration adds the trade-off: simpler routers are more consistent but less capable, and the
course uses an LLM with function calling.

### Slide 3.6 — Skills (deck "2a", slide 6)
**Evidence:** Narrated — "Skills are made up of individual steps. LLM calls, application code, API calls, or really any other code that you want to use there. One example of a skill that's very common is a RAG skill. So in this case, you could have a retrieval augmented generation capability within your agent that would handle everything from embeddings to looking up data from a vector database to making an LLM call with retrieved context."
**Text on slide:** Skills · A skill is a chain of individual logic blocks that can complete a task · Each agent will have one or more skills · Made up of individual steps · LLM calls · Application code · API calls · etc. · A RAG Skill · Embed input query · Vector DB lookup · LLM call w/ retrieved context
**Visual description:** A one-sentence definition, two bullets, and four sub-bullets in grey.
Bottom, a light grey rounded panel captioned "A RAG Skill" at its top right, holding three dark
red boxes in a row joined by arrows: "Embed input query" → "Vector DB lookup" → "LLM call w/
retrieved context".
**What it teaches:** A skill is a chain of steps (LLM calls, application code, API calls) that
completes a task; every agent has at least one. A RAG pipeline is one example of a whole skill.

### Slide 3.7 — Memory and State (deck "2a", slide 7)
**Evidence:** Narrated — "Typically, memory and state are used to store things like retrieved-context, configuration variables, or very commonly, a log of previous agent execution steps. This last one is probably the most common that you'll see. Many LLM APIs actually rely on being passed in a whole dictionary or list of messages about what the agent has done previously, before choosing the next step to call."
**Text on slide:** Memory and State · Shared state that can be accessed by each component in the agent · Used to store: · Retrieved context · Configuration variables · Previous agent execution steps · Many LLM APIs rely on receiving each agent step to decide on the next step. Your list of previous steps is often stored in memory.
```
messages = []
messages.append({"role": "system", "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user."})
messages.append({"role": "user", "content": "Hi, can you tell me the delivery date for my order?"})
messages.append({"role": "assistant", "content": "Hi there! I can help with that. Can you please provide your order ID?"})
messages.append({"role": "user", "content": "i think it is order_12345"})
```
**Visual description:** Left, two bullets with three sub-bullets. Right, a light grey rounded
callout with the black explanatory sentence on top and the code below in a monospace face (keys
in black, string values in green). A slate arrow points from the callout to the "Previous agent
execution steps" sub-bullet.
**What it teaches:** Memory and state are shared by every component; the most common use is the
running list of messages (previous steps) that the LLM API receives to decide the next step.

### Slide 3.8 — Your Example Agent: use case and skills (deck "2a", slide 8)
**Evidence:** Narrated — "The example agent that you're going to create is a data analysis assistant that can help you understand and ask questions over a sales database that you have. That agent has a few different skills. It has a data lookup skill that can query information from that attached database. It has a data analysis skill that can draw conclusions from that data, spot trends and make calculations. And then finally, it has a data visualization skill that can generate Python code and create graphs through that code and visualizations."
**Text on slide:** Your Example Agent · Use case: a data analysis assistant that can help you understand sales data from each of your stores · Skills: · A data lookup skill to query from your attached database · A data analysis skill to draw conclusions from your data · A data visualization skill to generate graphs and visualizations about your data
**Visual description:** Text only: a bold "Use case:" line, a bold "Skills:" heading and three
grey bullets.
**What it teaches:** The course's example agent: a sales-data analysis assistant with three
skills (data lookup, data analysis, data visualization).

### Slide 3.9 — Your Example Agent: router and tools (deck "2a", slide 9)
**Evidence:** Narrated — "Looking at your example agent visually here you see you have a user who's sending in queries to a router in this case GPT-4o-mini call with function calling. And then that router will call one of three different tools here, the lookup sales data tool, data analysis tool or data visualization tool. And then those tools will return back to the router, which then decides to either return to the user or call another tool from there."
**Text on slide:** Your Example Agent · User · Router (GPT-4o-mini w/ function calling) · Look Up Sales Data Tool · Data Analysis Tool · Data Visualization Tool
**Visual description:** A hand-drawn style diagram. A light blue "User" circle on the left with
arrows to and from a pink, red-outlined "Router (GPT-4o-mini w/ function calling)" box. Three
solid arrows fan from the router to three white rounded boxes: "Look Up Sales Data Tool", "Data
Analysis Tool", "Data Visualization Tool". Dashed lines from each tool join a dashed path that
loops over the top back into the router.
**What it teaches:** The agent's control flow: user ↔ router; the router calls one of three
tools; each tool returns to the router, which either answers the user or calls another tool. The
narration explains "tool" is the word GPT-4o-mini expects and is the same as a skill.

### Slide 3.10 — Your Example Agent: steps inside each tool (deck "2a", slide 10)
**Evidence:** Narrated — "The Lookup sales data tool, for example, first prepares a database so it loads in a local database and make sure that it's ready to query that database. Then it will generate SQL using another LLM call to query that database, and then finally execute that SQL and return the result all the way back to the router. Similarly, the data analysis tool makes a single call to generate an analysis. [...] And finally, the data visualization tool actually makes two sequential LLM calls. First, to generate a chart config and then to generate Python code based on that config."
**Text on slide:** Your Example Agent · User · Router (GPT-4o-mini w/ function calling) · Look Up Sales Data Tool · Prepare database · Generate SQL · Execute SQL · Data Analysis Tool · Generate Analysis · Data Visualization Tool · Generate chart config · Generate python code based on config · Key · LLM Call · Pure code
**Visual description:** The Slide 3.9 diagram, shifted left, with each tool's steps drawn to its
right and colour-coded by the key at bottom left (a dashed box: "LLM Call" in red, "Pure code"
in green). Look Up Sales Data Tool → "Prepare database" (green) → "Generate SQL" (red) →
"Execute SQL" (green). Data Analysis Tool → "Generate Analysis" (red). Data Visualization Tool →
"Generate chart config" (red) → "Generate python code based on config" (red). The router is red
(an LLM call). Dashed lines from the last step of each chain loop back over the top into the
router.
**What it teaches:** Which steps of each skill are LLM calls and which are plain code: lookup is
code, LLM SQL generation, code execution; analysis is one LLM call; visualization is two LLM
calls (chart config, then Python code). The narration gives the reason for the two-step
visualization: splitting one hard task into two simpler ones gives more reliable output.

### Slide 3.11 — What you've learned (deck "2a", slide 11)
**Evidence:** Narrated — "In this lesson, you've learned about the major components of agents, routers, skills, and memory, and you've examined the example agent that you're going to build."
**Text on slide:** What you've learned: · The major components of agents: Routers, Skills, Memory · Your example agent
**Visual description:** Standard content slide with the title and a two-item numbered list near
the top; the rest is empty.
**What it teaches:** Recap of the lesson.

---

## Lesson 4: Lab 1: Building your agent
Transcript: `## Lesson 4: Lab 1: Building your agent` in transcripts/evaluating-ai-agents-transcripts.md

No slide in decks "2a" or "2b" belongs to this lesson. It is a notebook lesson that sits between
the two decks.

---

## Lesson 5: Tracing agents
Transcript: `## Lesson 5: Tracing agents` in transcripts/evaluating-ai-agents-transcripts.md

All 9 slides of deck "2b" belong here, in deck order. The deck's title card says "Observing
Agents"; the transcript title is "Tracing agents".

### Slide 5.1 — Title card: Observing Agents (deck "2b", slide 1)
**Evidence:** Deck-only (title card; subtitle "Observing Agents" matches this lesson's content, not its exact title)
**Text on slide:** Evaluating AI Agents · Observing Agents
**Visual description:** Same layout as Slide 3.1: "Evaluating AI Agents" in coral red, "Observing
Agents" in slate grey below, the arize and DeepLearning.AI logos near the bottom.
**What it teaches:** Names the course and the lesson.

### Slide 5.2 — Talking Head (deck "2b", slide 2)
**Evidence:** Deck-only (production placeholder for the instructor on camera)
**Text on slide:** Talking Head
**Visual description:** Same as Slide 3.2: pale yellow page, "Talking Head" in bold dark grey.
**What it teaches:** Nothing; it marks where the video cuts to the instructor.

### Slide 5.3 — In this lesson (deck "2b", slide 3)
**Evidence:** Narrated — "Now that you understand your agent example, the next step is to add observability to your agent code."
**Text on slide:** In this lesson: · Adding tracing and observability to an agent
**Visual description:** Standard content slide with the title and one grey bullet; the rest is
empty.
**What it teaches:** The lesson's goal: add tracing and observability to the agent.

### Slide 5.4 — Observing your Agent (deck "2b", slide 4)
**Evidence:** Narrated — "Observability is a general software concept that refers to having complete visibility into every layer of your application. In the context of LLM applications, that's often tracking things like the prompt, the response, token usage, and then any calls that happen around the calls that you're making to LLMs. Observability is typically made up of traces and spans. Traces refer to full run through of your application, so a single trace would be one and end run of your application from an input all the way through to an output. And then traces are comprised of multiple spans."
**Text on slide:** Observing your Agent · Observability - complete visibility into every layer of an LLM-based software system: the application, the prompt, and the response. · Traces: · A trace records the paths taken by requests (made by an application or end-user) as they propagate through multiple steps. · Spans: · Data captured on individual steps in an LLM app or pipeline. · Trace 1 · Trace 2 · LLM Spans (runs) · Chain · Retriever · Embedding · Chain · LLM · Tool
**Visual description:** Top, the bold-headed definition of observability. Bottom left, "Traces:"
and "Spans:" with one bullet each. Bottom right, an image of two dark-framed panels side by
side, "Trace 1" and "Trace 2" in purple. Each holds a staircase of indented bars: "Chain";
"Retriever" and "Embedding" side by side; "Chain"; "LLM"; "Tool". The left panel's bars are
lavender; the right panel's are pink. A label "LLM Spans (runs)" on the left points arrows at the
first two rows.
**What it teaches:** Observability means seeing every layer of an LLM app. A trace is one full
request through the app; it is made of spans, one per step, nested to show which step runs
inside which. Span kinds include chain, retriever, embedding, LLM and tool.

### Slide 5.5 — OpenTelemetry (OTEL) (deck "2b", slide 5)
**Evidence:** Narrated — "Traces and spans come from a framework called OpenTelemetry. OpenTelemetry is often abbreviated to OTEL, and it's one of the most widely used standards for application observability, even outside of LLMs and AI agents. [...] And then OpenTelemetry also includes the concept of collectors and processors to receive those traces and spans, and then enumerate them in a platform that allows you to visualize those traces and run later evaluation on them. Throughout this course, you're going to use a tool called Arize Phoenix, which serves as one of those collectors to allow you to receive, visualize, and evaluate traces."
**Text on slide:** OpenTelemetry (OTEL) · "OTEL" is one of the most widely-used standards for application observability · LLM APPLICATION · INSTRUMENTATION · EXPORTER · OpenTelemetry · OPEN INFERENCE · OTEL PROCESSOR · COLLECTOR · PHOENIX SERVER · COLLECTOR
**Visual description:** One sentence of grey text, then an architecture diagram. Left, a pale
teal "LLM APPLICATION" panel holding four hexagon icons (library logos, unlabelled; one is the
OpenAI mark, one a llama), with two vertical strips at its right edge labelled "INSTRUMENTATION"
and "EXPORTER". From the exporter, two curved arrows go right: one to a mauve "OTEL PROCESSOR"
panel (a "COLLECTOR" strip and a dark pink hexagon), one to a pale blue "PHOENIX SERVER" panel
(a "COLLECTOR" strip and a blue hexagon with the Phoenix bird mark). Above the arrows, the
OpenTelemetry and OPEN INFERENCE logos.
**What it teaches:** Traces are produced by instrumentation inside the app and sent by an
exporter, using the OpenTelemetry / OpenInference standards, to a collector: any OTEL processor,
or a Phoenix server, which the course uses to receive, view and evaluate traces.

### Slide 5.6 — An Example Trace in Arize Phoenix (deck "2b", slide 6)
**Evidence:** Narrated — "But you'll notice there's one trace here of Agent Run in the image that's made up of multiple spans. You have an LLM span in orange. You have your chain spans in blue. And then your tool spans in yellow."
**Text on slide:** An Example Trace in Arize Phoenix · projects > · Total Traces 2 · Traces · Trace Details · Trace Status OK · Latency 6.30s · AgentRun 6.30s · router_call 3.12s · ChatCompletion 190 1.58s · tool_calls 1.45s · tool_call_lookup_sales_data 1.41s · ChatCompletion 156 1.30s · router_call 3.09s · ChatCompletion 967 3.04s · agent · AgentRun · Playground · Code · Add to Dataset · Annotate · Info · Feedback 0 · Attributes · Events 0 · Input · [{'role': 'user', 'content': 'Which stores did the best in 2021'}] · Output · In 2021, the stores that performed the best based on total sales value were: 1. \*\*Store Number 2970\*\*: - Total Quantity Sold: 5867 - Total Sale Value: $84,454.33 2. \*\*Store Number 3300\*\*: - Total Quantity Sold: 5124 - Total Sale Value: $63,205.33 3. \*\*Store Number 1650\*\*: - Total Quantity Sold: 4673 - Total Sale Value: $62,152.43 These stores had the highest total sales value in 2021. · Status OK · Start Time 1/10/2025 08:46:16 AM · End Time 1/10/2025 08:46:22 AM · Latency 6.30s
**Visual description:** A dark-theme screenshot of the Phoenix "Trace Details" panel. Left, the
span tree: "AgentRun" (agent icon, selected) at the root; under it "router_call" (blue) with a
"ChatCompletion" (orange) child and a "tool_calls" (blue) child, which holds
"tool_call_lookup_sales_data" (yellow) with its own "ChatCompletion" (orange); then a second
"router_call" (blue) with a "ChatCompletion" (orange). Numbers next to the ChatCompletion spans
are token counts with an eye-like icon; latencies are shown in green or yellow. Right, the
AgentRun span's Info tab: an "Input" box with the user message and a green-bordered "Output" box
with the three-store answer; a side column with Status, Start Time, End Time and Latency.
**What it teaches:** What one agent run looks like as a trace: the router's LLM call chooses the
lookup tool, the tool makes its own LLM call, and a second router call writes the answer. Span
kinds are colour-coded (LLM orange, chain blue, tool yellow), with latency and token counts per
span and the run's input and output at the top level.

### Slide 5.7 — Instrumentation (deck "2b", slide 7)
**Evidence:** Narrated — "Instrumentation refers to the practice of marking which functions or code blocks within your code you want to track as spans and what attributes you want to attach to those spans. You can do this manually with clauses or decorators, as you'll see in the next notebook as well. However, tools like Phoenix do automate some of this process for you, especially if you're using popular libraries like OpenAI or LlamaIndex or LangChain."
**Text on slide:** Instrumentation · Marking from which functions or code blocks spans should be collected, and with which attributes · Arize Phoenix automates this process for you
```python
def do_work():
    with tracer.start_as_current_span("span-name") as span:
        # do some work that 'span' will track
        print("doing some work...")
        # When the 'with' block goes out of scope, 'span' is closed for you
```
**Visual description:** An italic grey definition, a light grey code block with syntax
highlighting (keywords red, function names purple, strings brown, comments grey), and a closing
grey sentence.
**What it teaches:** Instrumentation marks which code becomes a span; manually, a `with
tracer.start_as_current_span(...)` block opens a span that closes when the block ends. Phoenix
automates much of this, and the narration says especially for libraries such as OpenAI,
LlamaIndex or LangChain.

### Slide 5.8 — Why Observability is Important (deck "2b", slide 8)
**Evidence:** Narrated — "First, when you're getting off the ground and building your application, observability really simplifies the debugging process. [...] And then these traces will become the bedrock that is used to run evaluation. [...] Finally, putting these together, observability helps you really start to understand and eventually control some of the more unpredictable behavior of LLMs."
**Text on slide:** Why Observability is Important · Simplifies debugging when building your application · Provides a detailed log of each call made in your app, which is necessary to run performance evaluations · Helps you understand, and soon control, the unpredictable behavior of LLMs
**Visual description:** A three-item numbered list in grey with the key phrases in bold
("Simplifies debugging", "Provides a detailed log", "unpredictable behavior of LLMs").
**What it teaches:** Three reasons to trace: easier debugging, a log of every call that later
evaluations run on, and a handle on unpredictable LLM behaviour. The narration adds that later
notebooks export trace data from Phoenix to run evaluations at scale.

### Slide 5.9 — What you've learned (deck "2b", slide 9)
**Evidence:** Narrated — "In this lesson, you've learned what observability is, how it works, and why it's important, as well as some of the basic building blocks of observability like traces and spans, and how those traces in spans are collected."
**Text on slide:** What you've learned: · What Observability is, how it works, and why it's important · The building blocks of Observability: Traces and Spans · How traces and spans are collected
**Visual description:** Standard content slide with the title and a three-item numbered list;
the rest is empty.
**What it teaches:** Recap of the lesson.

---

## Lesson 6: Lab 2: Tracing your agent
Transcript: `## Lesson 6: Lab 2: Tracing your agent` in transcripts/evaluating-ai-agents-transcripts.md

No deck belongs to this lesson. It is a notebook lab (Lab 2) that follows the Lesson 5 slides.

---

## Lesson 7: Adding router and skill evaluations
Transcript: `## Lesson 7: Adding router and skill evaluations` in transcripts/evaluating-ai-agents-transcripts.md

All 20 slides of deck "Lesson-3" belong here, narrated in deck order.

### Slide 7.1 — Title card: Adding Router & Skill Evaluations (deck "Lesson-3", slide 1)
**Evidence:** Deck-only (title card; its subtitle is this lesson's title)
**Text on slide:** Evaluating AI Agents · Adding Router & Skill Evaluations (hidden text-layer string, not visible: [Your Logo Here])
**Visual description:** White title card. "Evaluating AI Agents" in coral red, centered; below it
"Adding Router & Skill Evaluations" in slate grey; below that the arize logo (left) and the
DeepLearning.AI logo (right). No instructor name, no wave.
**What it teaches:** Names the course and the lesson.

### Slide 7.2 — Talking Head placeholder (deck "Lesson-3", slide 2)
**Evidence:** Deck-only (placeholder for the instructor on camera; the lesson's opening lines, "In this lesson, you'll focus on evaluating each of your agent's skills, as well as the router's ability to choose the correct tool and execute it correctly given a user's request", are likely spoken here, but the slide shows nothing to match)
**Text on slide:** Talking Head
**Visual description:** A plain pale-yellow page with "Talking Head" in bold dark grey, upper
center. No logos, no wave.
**What it teaches:** Nothing; it marks a camera segment.

### Slide 7.3 — In this lesson (deck "Lesson-3", slide 3)
**Evidence:** Narrated — "You will learn about three types of evaluators: code based evaluators, LLM as a judge, and human annotations. You will then apply the appropriate evaluators to your agent example."
**Text on slide:** In this lesson: · Techniques for running evaluations (evals): · LLM-as-a-Judge · Code-based evals · Human Annotations · Router evals · Function calling, parameter extraction, function generation · Skill evals
**Visual description:** Standard content slide. Three top-level bullets in grey, the first and
second with hollow-circle sub-bullets in smaller type.
**What it teaches:** The lesson agenda: three eval techniques, then router evals (function
calling, parameter extraction, function generation), then skill evals.

### Slide 7.4 — Techniques for Running Evals (deck "Lesson-3", slide 4)
**Evidence:** Narrated — "There are three main techniques used for running evaluations. The first is code-based evals. Second is LLMs and judge evaluations. And finally, human annotations."
**Text on slide:** Techniques for Running Evals · Code-Based Evals · Running code to compare outputs to expected outputs, run calculations on outputs, etc. · LLM-as-a-Judge Evals · Using a separate LLM to judge the outputs of your application. · Human Annotations · Use human labelers or user feedback to evaluate your application outputs
**Visual description:** Three stacked full-width boxes, each with a bold heading and a one-line
definition: a white outlined box (Code-Based Evals), a red filled box (LLM-as-a-Judge Evals)
and a darker red filled box (Human Annotations), the last two in white text.
**What it teaches:** The three techniques and a one-line definition of each.

### Slide 7.5 — Code-based Evals: examples (deck "Lesson-3", slide 5)
**Evidence:** Narrated — "Code-based evaluations involve running some sort of code on the outputs of your application. Some common examples of these are checking to see if your output matches a certain regex. So maybe you want a response to only contain numbers or no alphanumeric characters. You can use a regex to check to make sure that your response matches that filter. You might also want to make sure that your response is Json passable. or a very common one that you see, especially in chatbots, is checking to see if the chatbots response contains certain keywords. Like most often, companies don't want their chatbots to mention a competitor"
**Text on slide:** Code-based Evals · Code run on the outputs of your application · Examples of code-based evaluators: · Matches regex · E.g. response only contains numbers · JSON parseable · Contains keyword(s) · E.g. response contains competitor name
**Visual description:** Standard content slide, text only: a one-line definition, then three
bullets with two hollow-circle example sub-bullets.
**What it teaches:** Code-based evals run code on the app's outputs; typical checks are a regex
match, JSON parseability, and keyword presence (e.g. a competitor's name).

### Slide 7.6 — Code-based Evals: expected outputs (deck "Lesson-3", slide 6)
**Evidence:** Narrated — "But perhaps, maybe the most common type of code-based eval is to use these evals to compare your applications outputs to expected outputs. So if you have ground truth data of what the expected output is for an input, then it's very effective to use code-based evals to either directly compare the output of your application to that expected output, or to use something like cosine similarity or cosine distance to do more of a semantic match between those two different values."
**Text on slide:** Code-based Evals · Can also be used to compare your application's outputs to expected outputs · Can be compared using: · Direct match · Cosine similarity / cosine distance
**Visual description:** Standard content slide, text only; "expected outputs" is in bold.
**What it teaches:** Code-based evals can compare outputs to ground-truth expected outputs, by
direct match or by cosine similarity/distance for a semantic match.

### Slide 7.7 — LLM-as-a-Judge (deck "Lesson-3", slide 7)
**Evidence:** Narrated — "Typically, the way that it's done is by grabbing the input and output of your application, as well as potentially a few other key pieces of information from one run of your application. Constructing a separate prompt that's going to evaluate a specific criteria based on those inputs and outputs. Sending that prompt over to a separate judge or evaluator LLM"
**Text on slide:** LLM-as-a-Judge · PROMPT · QUERY I want to go… · CONTEXT User booking history, hotel inventory… · INSTRUCTIONS You are a friendly travel assistant… · APP IN PRODUCTION · Output · {output} Hi, I'm happy to help you plan… · EVAL PROMPT TEMPLATE · <<template: hallucination>> · Is the {output} using the {context} to answer the {query} · EVALUATOR LLM · OpenAI · Gemini · MISTRAL AI_ · ANTHROPIC · cohere · EVAL · Did it hallucinate? · EVAL · No
**Visual description:** A flow diagram. Top row: a dark slate "PROMPT" box (query, context,
instructions of a travel assistant) → a hatched arrow → a pink "APP IN PRODUCTION" box with a
phone screenshot above it → a hatched arrow → a dark slate "Output" box. Dotted lines drop from
the PROMPT and Output boxes into a light-blue "EVAL PROMPT TEMPLATE" box (hallucination template,
placeholders in purple) → hatched arrow → an "EVALUATOR LLM" box showing grey logos of OpenAI,
Gemini, Mistral AI, Anthropic and Cohere → hatched arrow → a rounded white "EVAL" box with the
question "Did it hallucinate?" in purple italics and the result "No" next to a green check.
**What it teaches:** How LLM-as-a-judge works: take the app's prompt pieces and output, fill an
eval template (here a hallucination check), send it to a separate evaluator LLM, and get back a
label.

### Slide 7.8 — LLM-as-a-Judge Example (deck "Lesson-3", slide 8)
**Evidence:** Narrated — "You can examine this case of evaluating the relevance of a document that was retrieved in a RAG system. The retrieval span in this case is made up of a user query. And then the documents that were retrieved for that given query. That query and then the reference documents are then sent into the separate, eval template that you see here and then populated so as to ask another LLM, \"Are these reference retrieved documents relevant to the user's question?\" And then that separate LLM will either say those documents are relevant or irrelevant."
**Text on slide:** LLM-as-a-Judge Example · span · span · retrieval span · span · Span we want to evaluate · retrieval span · Input · User Query · Documents · Output · Eval Template · You are comparing a reference text to a question and trying to determine if the reference text contains information relevant to answering the question. Here is the data: · [BEGIN DATA] · ************ · [Question]: {query} · ************ · [Reference text]: {reference} · [END DATA] · Compare the Question above to the Reference text. Determine whether the Reference text contains information that can answer the Question. · Phoenix Library · Eval Template · Example: Retrieval · Model Params · Eval LLM · Eval · Example · "relevant" · "irrelevant"
**Visual description:** Top left, a tablet-like frame listing four spans, the "retrieval span"
outlined in red; an arrow points to a red-outlined panel titled "retrieval span" (captioned "Span
we want to evaluate") with an Input box (User Query, Documents) and an Output box. Bottom left, a
stack of pages showing the full eval template text. Arrows from the span panel and the template
lead into a grey "Phoenix Library" box holding "Eval Template / Example: Retrieval", "Model
Params" and "Eval LLM"; an arrow on the right leads to "Eval / Example "relevant" "irrelevant"".
**What it teaches:** A concrete judge: the query and retrieved documents from one retrieval span
fill a relevance template, which the Phoenix library sends to an eval LLM with model params; the
output is one of two labels, relevant or irrelevant.

### Slide 7.9 — Important considerations when using LLM Judges (deck "Lesson-3", slide 9)
**Evidence:** Narrated — "The first is that only really the best models actually align closely with human judgment. So if you're going to run LLM as a judge, you often need to use a GPT-4o or Claude3.5 Sonnet or similarly high-end model to do so. Even with these, though, a LLM as a judge is never going to be 100% accurate." and "So you should always use things like correct versus incorrect, relevant versus irrelevant, and never a measure like \"score this response on a scale from 1 to 100.\""
**Text on slide:** Important considerations when using LLM Judges · 1. Only the best models align closely with human judgement · 2. LLM-as-a-Judge will never be a 100% correct technique · 3. Tuning your LLM judge prompt can help close this gap · 4. Always use discrete classification labels, never an undefined score · a. "Incorrect" vs "correct", not 1%-100% accuracy
**Visual description:** Standard content slide, a numbered list of four points with one lettered
sub-point.
**What it teaches:** Judge caveats: use a top model, expect errors, tune the judge prompt, and
output discrete labels rather than numeric scores. The narration adds the reason: LLMs cannot
tell an 83 from a 79 out of 100.

### Slide 7.10 — Annotations (deck "Lesson-3", slide 10)
**Evidence:** Narrated — "The idea here is that you can use tools like Phoenix or other observability platforms to construct a queue of lots of runs of your application to construct an annotation queue, and then have human labelers work their way through that queue and attach feedback, or judge the responses of your application. The other method that you can use is actually gathering feedback from your end users. So you might have seen cases in the wild where LLM systems have a thumbs up, thumbs down response system"
**Text on slide:** Annotations · Add human evaluation labels to your traces: · Using annotation queues and human labelers · Using 👍 👎 responses from users · (screenshot) Trace Details · Trace Status · OK · Latency · 0.91s · Feedback · Hallucination hallucinated · Q&A Correctness incorrect · User Feedback 👍 · User Feedback · label 👍 · score 1.00 · annotator kind HUMAN · BaseQueryEngine.query 0.91s · RetrieverQueryEngine._query 0.90s · BaseRetriever.retrieve 0.24s · VectorIndexRetriever._retrieve 0.23s · BaseEmbedding.get_query_embedding 0.19s · OpenAIEmbedding._get_query_embedding 0.18s · CohereRerank._postprocess_nodes 0.17s · Attributes · Event · Input · Can I use gRPC for trace collectio[n] · Output · You can use gRPC for trace collect[ion]
**Visual description:** Two bullets with thumbs-up and thumbs-down emoji, then a dark-theme
screenshot of a "Trace Details" view: status OK, latency 0.91s, three feedback chips
(Hallucination: hallucinated, Q&A Correctness: incorrect, User Feedback: thumbs up), a tooltip
for the user feedback (label thumbs up, score 1.00, annotator kind HUMAN), a nested span tree of
a retrieval query engine on the left, and Input/Output panes on the right, cropped at the edge.
**What it teaches:** Human labels attach to traces, either from an annotation queue worked by
labelers or from end-user thumbs up/down; they sit beside LLM-judge labels on the same trace.

### Slide 7.11 — When to use each Technique (deck "Lesson-3", slide 11)
**Evidence:** Narrated — "One way to think about this is how qualitative versus quantifiable or quantitative is the metric that you're trying to measure." and "The other way to think about these is whether the evaluation needs to be 100% accurate, or if it can afford to be less than 100% accurate." and "What you might notice here is that human labels is sort of the best version of evaluation. In this case, it's flexible and it's deterministic. However, in practice it can be hard to get human labels at scale"
**Text on slide:** When to use each Technique · Non-deterministic · Deterministic · Flexible, can handle qualitative criteria · Inflexible, criteria must be quantifiable · LLM-as-a-judge · Human Labels · Code-based evals
**Visual description:** A hand-drawn 2×2 grid. Columns: "Non-deterministic", "Deterministic".
Rows: "Flexible, can handle qualitative criteria", "Inflexible, criteria must be quantifiable".
"LLM-as-a-judge" (red) sits in flexible/non-deterministic, "Human Labels" (orange) in
flexible/deterministic, "Code-based evals" (blue) in inflexible/deterministic; the
inflexible/non-deterministic cell is empty.
**What it teaches:** Choose a technique by two axes: can the criterion be quantified, and must
the result be deterministic. Human labels cover both but do not scale; the narration adds that
end-user feedback has selection bias.

### Slide 7.12 — Choosing what to evaluate (deck "Lesson-3", slide 12)
**Evidence:** Narrated — "now you'll learn about the different pieces of your agent that you can apply these techniques to to run these evaluations. This lesson we'll go through evaluating the router and the skills. And you'll have a future lesson in this course that goes into evaluating the path in detail."
**Text on slide:** Choosing what to evaluate · The Router · Function choice and parameter extraction · The Skills / Functions · Can use standard LLM evaluations · The Path · The most challenging to evaluate scalably
**Visual description:** Three black line icons in a row, each with a bold label and a two-line
caption: diverging arrows (The Router), a lightbulb with a gear (The Skills / Functions), and two
circles joined by a bent line (The Path).
**What it teaches:** The three parts of an agent to evaluate: router, skills, path; this lesson
covers the first two.

### Slide 7.13 — Evaluating a Router: two ways (deck "Lesson-3", slide 13)
**Evidence:** Narrated — "Routers are typically evaluated in two different ways. First, you'll evaluate the function calling choice, aka did the router make the right choice and choosing a function to call." and "The second kind of thing that gets evaluated in routers is typically the parameter extraction."
**Text on slide:** Evaluating a Router · Routers are usually evaluated in two ways: · 1. Function calling choice - did the router choose the right function to call? · 2. Parameter extraction - did the router extract the right function parameters from the question?
**Visual description:** Standard content slide, a lead line and a numbered list; "Function
calling choice" and "Parameter extraction" are in bold.
**What it teaches:** The two router checks: right function, right parameters.

### Slide 7.14 — Evaluating a Router: order-status example (deck "Lesson-3", slide 14)
**Evidence:** Narrated — "Looking at the example here, you might have a case where a user asks your agent, can you help me check on the status of my order? Number 1234." and "and then it takes that same one, two three, four and this time as it has a shipping tracking ID in this case that's an order number and not a shipping tracking ID. So here the agent actually failed in the parameter extraction task, even though it succeeded in the function calling task that it had."
**Text on slide:** Evaluating a Router · User: Hi, can you help check on the status of my order? #1234 · Agent: Definitely! · {tool_call: "order_status_check(order_number=1234)"} · {role: "tool", content: "status=shipped"} · Your order has been shipped! · User: When will it arrive? · Agent: Let me check. · {tool_call: "shipping_status_check(shipping_tracking_id=1234)"} · {role: "tool", content: "tracking id not found"}
**Visual description:** A chat transcript in grey body text with tool-call lines in monospace;
function names in green and the arguments (`order_number=1234`, `shipping_tracking_id=1234`) in
red.
**What it teaches:** A router can pick the right function yet pass the wrong parameter: the
order number reused as a shipping tracking ID fails ("tracking id not found").

### Slide 7.15 — Evaluating a Router using LLM-as-a-Judge (deck "Lesson-3", slide 15)
**Evidence:** Narrated — "This is an example of the prompt, the template that you would use for your LLM as a judge to evaluate a router in this case. So you'll notice at the top you have some instructions for the LLM judge to say what it's going to be evaluating. You have some places where data will be added into the prompt, in this case the user's question, and then the tool call that was chosen. And then you have some instructions saying the LLM judge should respond with a single word, either correct or incorrect."
**Text on slide:**
```
TOOL_CALLING_PROMPT_TEMPLATE = """
You are an evaluation assistant evaluating questions and tool calls to determine whether the tool called would
answer the question. The tool calls have been generated by a separate agent, and chosen from the list of tools
provided below. It is your job to decide whether that agent chose the right tool to call.
    [BEGIN DATA]
    ************
    [Question]: {question}
    ************
    [Tool Called]: {tool_call}
    [END DATA]
Your response must be single word, either "correct" or "incorrect", and should not contain any text or
characters aside from that word.
"incorrect" means that the chosen tool would not answer the question, the tool includes information that is
not presented in the question, or that the tool signature includes parameter values that don't match the
formats specified in the tool signatures below.
"correct" means the correct tool call was chosen, the correct parameters were extracted from the question, the
tool call generated is runnable and correct, and that no outside information not present in the question was
used in the generated question.
    [Tool Definitions]: {tool_definitions}
"""
```
**Visual description:** The whole template in a light-grey code box, monospace, mostly in
dark-gold text, with the placeholders `{question}`, `{tool_call}` and `{tool_definitions}` in
teal.
**What it teaches:** The router judge prompt: question and chosen tool call as data, the full
tool definitions for context, and a single-word "correct"/"incorrect" output, with each label
defined (right tool, right parameters, runnable, no outside information).

### Slide 7.16 — Evaluating Skills (deck "Lesson-3", slide 16)
**Evidence:** Narrated — "So you might use an LLM as-a-Judge to evaluate things like relevance, hallucination, question answer correctness, generated code readability, or summarization. And then you might use code based evaluators to evaluate regex matches Json parse ability in your response or comparison against ground truth."
**Text on slide:** Evaluating Skills · Skills can be evaluated using standard LLM or code-based evals: · Relevance · Hallucination · Question and answer correctness · Generated code readability · Summarization · Regex · JSON parseable · …
**Visual description:** A lead line with "standard LLM" in red and "code-based" in blue; the
bullets are color-coded to match: five red (LLM) items, two blue (code) items, then a black "…".
**What it teaches:** Skills are ordinary LLM apps or code, so ordinary evals apply; the color
code shows which are LLM-judged and which are code-based.

### Slide 7.17 — Evaluating Skills - Your Example Agent: exercise (deck "Lesson-3", slide 17)
**Evidence:** Narrated — "Looking at your example agent, you have three different skills here. You have a database lookup skill, a data analysis skill, and a data visualization code gen skill. I invite you to pause the video here and think of a few different evaluations that can be used to evaluate each of these three different skills"
**Text on slide:** Evaluating Skills - Your Example Agent · User · Router (GPT-4o-mini w/ function calling) · Look Up Sales Data Tool · Prepare database · Generate SQL · Execute SQL · Data Analysis Tool · Generate Analysis · Data Visualization Tool · Generate chart config · Generate python code based on config · Tool #1: Database Lookup · ? · Tool #2: Data Analysis · ? · Tool #3: Data Visualization Code Gen · ?
**Visual description:** A hand-drawn agent diagram: a blue "User" ellipse with arrows to and from
a red "Router" box; three arrows fan out to three tool boxes. Each tool has a chain of steps to
its right: "Prepare database" (green) → "Generate SQL" (red) → "Execute SQL" (green);
"Generate Analysis" (red); "Generate chart config" (red) → "Generate python code based on config"
(red). Dashed lines from each chain's end loop back to the router. Below, three bold tool
headings, each with a "?".
**What it teaches:** The course's example agent (router plus three tools and their internal
steps) and an invitation to choose evals for each tool.

### Slide 7.18 — Evaluating Skills - Your Example Agent: answers (deck "Lesson-3", slide 18)
**Evidence:** Narrated — "So for the database lookup tool you could use either LLM as-a-Judge or a code-based eval to do SQL generation correctness and see if the SQL that's generated is correct. For the data analysis tool, you could use an LLM as-a-Judge to check for clarity in the analysis, and make sure all of the entities that are mentioned in that analysis are correct" and "And for the data visualization code gen tool, you can use a code-based eval to make sure the code is runnable."
**Text on slide:** Evaluating Skills - Your Example Agent · (diagram as Slide 7.17) · Tool #1: Database Lookup · - SQL gen correctness · - SQL gen correctness · Tool #2: Data Analysis · - Analysis Clarity · - Entity correctness · Tool #3: Data Visualization Code Gen · - Code is runnable · Using LLM-as-a-Judge · Using code-based evals
**Visual description:** Same diagram as Slide 7.17; the "?" marks are replaced by eval names,
colored by a legend at the bottom left (red dot "Using LLM-as-a-Judge", blue dot "Using
code-based evals"). Tool #1 has "SQL gen correctness" once in blue and once in red; Tool #2 has
two red items; Tool #3 has one blue item.
**What it teaches:** One answer set: SQL correctness (code or judge), analysis clarity and entity
correctness (judge), code runnability (code).

### Slide 7.19 — Untitled: evals on the example agent, router included (deck "Lesson-3", slide 19)
**Evidence:** Narrated — "The last thing to mention is that you have SQL generation correctness being run with either LLM as-a-Judge or code-based evals. You'll see what both those look like in future notebooks." (the router label matches the earlier "One way to evaluate a router is by using an LLM as-a-Judge.")
**Text on slide:** Router: · Function calling choice and parameter extraction · (LLM-as-a-Judge) · User · Router (GPT-4o w/ function calling) · Look Up Sales Data Tool · Prepare database · Generate SQL · Execute SQL · Data Analysis Tool · Generate Analysis · Data Visualization Tool · Generate chart config · Generate python code based on config · Tool #1: Database Lookup · SQL gen correctness (code-based) · Tool #2: Data Analysis · - Analysis Clarity · - Entity Correctness (LLM-as-a-Judge) · Tool #3: Data Visualization Code Gen · Code is runnable (code-based)
**Visual description:** No title. The same agent diagram, shifted right, with a "Router:" label
top left whose caption is in red. Under each tool the chosen eval and its technique in
parentheses and italics: blue for code-based, red for LLM-as-a-Judge. Tool #1 now shows only the
code-based SQL check. The router box here reads "GPT-4o w/ function calling", not "GPT-4o-mini".
**What it teaches:** The full eval plan for the example agent: a judge on the router's function
choice and parameters, and one eval per tool, each tagged with its technique.

### Slide 7.20 — What you've learned (deck "Lesson-3", slide 20)
**Evidence:** Narrated — "In this lesson, you've learned three different techniques to run Agent evals: LLM as a judge, code-based evaluations, and human annotations. You've also learned common types of evaluations to run using each of these techniques. And finally, which pieces of your agent should apply these techniques to you to evaluate."
**Text on slide:** What you've learned: · 1. Three techniques to run Agent Evals: LLM-as-a-Judge, code-based evals, and human annotations · 2. Common types of evaluations to run using these techniques · 3. Which pieces of your agent to evaluate
**Visual description:** Standard content slide, a three-item numbered list.
**What it teaches:** Recap of the lesson.

---

## Lesson 8: Lab 3: Adding router and skill evaluations
Transcript: `## Lesson 8: Lab 3: Adding router and skill evaluations` in transcripts/evaluating-ai-agents-transcripts.md

No slide in decks "Lesson-3" or "Lesson-4" belongs to this lesson. The narration is a notebook
walkthrough (Phoenix evals imports, the judge template, running the evaluations on the agent).

---

## Lesson 9: Adding trajectory evaluations
Transcript: `## Lesson 9: Adding trajectory evaluations` in transcripts/evaluating-ai-agents-transcripts.md

All 14 slides of deck "Lesson-4" belong here, narrated in deck order.

### Slide 9.1 — Title card: Adding Trajectory Evaluations (deck "Lesson-4", slide 1)
**Evidence:** Deck-only (title card; its subtitle is this lesson's title)
**Text on slide:** Evaluating AI Agents · Adding Trajectory Evaluations (hidden text-layer string, not visible: [Your Logo Here])
**Visual description:** Same layout as Slide 7.1: course title in coral red, lesson title in
slate grey, arize and DeepLearning.AI logos below.
**What it teaches:** Names the course and the lesson.

### Slide 9.2 — Talking Head placeholder (deck "Lesson-4", slide 2)
**Evidence:** Deck-only (placeholder for the instructor on camera; the opening lines, "you need to ensure that your agent can respond to a user's query in an efficient number of steps", are likely spoken here, but the slide shows nothing to match)
**Text on slide:** Talking Head
**Visual description:** Same pale-yellow placeholder as Slide 7.2.
**What it teaches:** Nothing; it marks a camera segment.

### Slide 9.3 — In this lesson (deck "Lesson-4", slide 3)
**Evidence:** Narrated — "In this lesson, you'll learn how to assess this by computing a convergent score and apply the test to your agent example."
**Text on slide:** In this lesson: · Agent Trajectories · Calculating and Evaluating Convergence
**Visual description:** Standard content slide, two bullets.
**What it teaches:** The agenda: trajectories, then convergence.

### Slide 9.4 — What is an Agent Trajectory? Definition (deck "Lesson-4", slide 4)
**Evidence:** Narrated — "Now what is an agent trajectory? A trajectory is simply the path the agent takes through different router, tool, and other logic steps for a given input."
**Text on slide:** What is an Agent Trajectory? · Trajectory: the path through router steps, tool calls, and logic steps that the agent took for a given input.
**Visual description:** Standard content slide, one bullet.
**What it teaches:** The definition of a trajectory.

### Slide 9.5 — What is an Agent Trajectory? The example agent (deck "Lesson-4", slide 5)
**Evidence:** Narrated — "Looking at your example agent, you can examine a few different trajectories to get a sense of how these work."
**Text on slide:** What is an Agent Trajectory? · User · Router (GPT-4o-mini w/ function calling) · Look Up Sales Data Tool · Prepare database · Generate SQL · Execute SQL · Data Analysis Tool · Generate Analysis · Data Visualization Tool · Generate chart config · Generate python code based on config · Key · LLM Call · Pure code
**Visual description:** The hand-drawn example-agent diagram from Slide 7.17 (User, red Router,
three tools, step chains, dashed return loops), plus a dashed "Key" box bottom left: a red box
"LLM Call" and a green box "Pure code". The key confirms the step colors: Prepare database and
Execute SQL are pure code; the other steps are LLM calls.
**What it teaches:** The agent whose paths will be traced, and which of its steps call an LLM.

### Slide 9.6 — What is an Agent Trajectory? First query (deck "Lesson-4", slide 6)
**Evidence:** Narrated — "First, you can examine a query like: \"Which store had the most sales in 2021?\" In this case, the agent would go from the user to the router and then would go from that router to, in this case, the lookup sales data tool, as well as the data analysis tool. Back to the router and then finally back to the user."
**Text on slide:** What is an Agent Trajectory? · Which store had the most sales in 2021? · User · Router (GPT-4o-mini w/ function calling) · Look Up Sales Data Tool · Data Analysis Tool · Router (GPT-4o-mini w/ function calling) · User
**Visual description:** A hand-written query line, then one horizontal chain: blue User → red
Router → Look Up Sales Data Tool → Data Analysis Tool → red Router → blue User.
**What it teaches:** A two-tool trajectory. The narration adds that both tools run in one router
step because this agent allows several tool calls per router step, an architectural choice.

### Slide 9.7 — What is an Agent Trajectory? Second query (deck "Lesson-4", slide 7)
**Evidence:** Narrated — "To look at a more complicated trajectory. You might have a query like plot sales data volume over time. In this case, your agent would go through a user to the router to your to look up sales data and data analysis tools back to the router, which then decides to call the data visualization tool to generate that visualization code that would then return back to the router and finally go back to the user."
**Text on slide:** What is an Agent Trajectory? · Which store had the most sales in 2021? · User · Router (GPT-4o-mini w/ function calling) · Look Up Sales Data Tool · Data Analysis Tool · Router (GPT-4o-mini w/ function calling) · User · Plot daily sales volume over time · User · Router (GPT-4o-mini w/ function calling) · Look Up Sales Data Tool · Data Analysis Tool · Router (GPT-4o-mini w/ function calling) · Data Visualization Tool · Router (GPT-4o-mini w/ function calling) · User
**Visual description:** Slide 9.6's chain, plus a second query and a longer chain that wraps to
a second line: User → Router → Look Up Sales Data Tool → Data Analysis Tool → Router → (curving
arrow) Data Visualization Tool → Router → User.
**What it teaches:** A longer trajectory with a second router decision that calls the
visualization tool.

### Slide 9.8 — Trajectories get complicated quickly (deck "Lesson-4", slide 8)
**Evidence:** Narrated — "Your example agent has three tools. But agents in production can have ten, 20, 30 different tools that they use. And even some systems will start to compose multiple agents together." and "In these multi-agent systems you can have trajectories getting very complicated very, very quickly."
**Text on slide:** Trajectories get complicated quickly · User · Router (GPT-4o-mini w/ function calling) · Look Up Sales Data Tool · Data Analysis Tool · Data Visualization Tool · User · Router (GPT-4o-mini w/ function calling) · Agent 1 · Router (GPT-4o w/ function calling) · Look Up Sales Data Tool · Data Analysis Tool · Data Visualization Tool · Agent 2 · Agent 3
**Visual description:** Two hand-drawn diagrams side by side, routers filled in pale red. Left:
the single example agent (User, Router, three tools with dashed loops back). Right: a User and a
top-level Router fanning out to three boxes, "Agent 1" (which contains a whole copy of the
example agent, its router labelled "GPT-4o w/ function calling"), and empty "Agent 2" and
"Agent 3" boxes.
**What it teaches:** Path complexity grows fast with more tools and with agents nested under a
router.

### Slide 9.9 — If your Agent's output is correct, does the Trajectory matter? (deck "Lesson-4", slide 9)
**Evidence:** Narrated — "Now you might be asking if your agent's output is correct, does the trajectory really matter all that much? And the answer is yes, because efficiency matters in this case." and "If you can answer a user's question in six steps as opposed to 11 steps, that means fewer LLM calls. That means less variability. That means lower cost and lower latency for the user."
**Text on slide:** If your Agent's output is correct, does the Trajectory matter? · Yes, because efficiency matters! · 1. User input · 2. Router · 3. Database Lookup Tool · 4. Router · 5. Data Analyzer · 6. Router · 7. Database Lookup Tool · 8. Router · 9. Data Analyzer · 10. Router · 11. Output · 1. User input · 2. Router · 3. Database Lookup Tool · 4. Data Analyzer · 5. Router · 6. Output
**Visual description:** Two-line title, a lead line, then two numbered lists separated by a large
grey chevron pointing right: an 11-step path on the left (lookup and analysis repeated, a router
call between each) and a 6-step path on the right.
**What it teaches:** Two paths can reach the same answer; the shorter one means fewer LLM calls,
less variability, lower cost and latency.

### Slide 9.10 — Convergence (deck "Lesson-4", slide 10)
**Evidence:** Narrated — "So how can you track and measure trajectories? One way to do that is using a tool called Convergence. Convergence as a measurement for how closely your agent follows an optimal path for a given query."
**Text on slide:** Convergence · Convergence measures how closely your agent follows the optimal path for a given query. · Step count++ · Agent step 1 · Step count++ · Agent step 2 · Step count++ · Agent step 3 · … · Step count++ · Agent step 100
**Visual description:** A definition line, then four grey-outlined cards in a row with an
ellipsis before the last; each card is headed "Step count++" and holds a small box "Agent step
N" (1, 2, 3, 100), the box borders shading from purple to pink.
**What it teaches:** Convergence compares a run's step count with the optimal path; every agent
step increments a counter.

### Slide 9.11 — How do you test for Convergence? Steps and formula (deck "Lesson-4", slide 11)
**Evidence:** Narrated — "You can run your agent on a set of similar queries." and "Next, you run each of these queries through your agent and record the number of steps taken for each of those queries, and then find the length of the optimal path taken. In this case, that's the minimum number of steps that your agent took to get through one of these queries. Then you can use all of those different numbers to calculate your convergence score"
**Text on slide:** How do you test for Convergence? · 1. Run your agent on a set of similar queries · N: Total number of runs. · 2. Record the number of steps taken for each · S_agent,i: Steps taken by the agent in the i-th run. · 3. Find the length of the optimal path · S_optimal = min(S_agent,1, S_agent,2, …, S_agent,N) (minimum steps across all runs). · 4. Calculate the convergence score: · Overall Convergence Score = ( Σ_{i=1}^{N} min(1, S_optimal / S_agent,i) ) / N
**Visual description:** A four-step numbered list with a small-type sub-bullet under each of the
first three giving the math symbol; "convergence score" is bold. The formula is typeset in LaTeX
style at the bottom center. The symbols and formula are images, not in the text layer; they are
transcribed here from the page image with subscripts written as `_`.
**What it teaches:** The recipe and formula: run N similar queries, count steps per run, take the
minimum as the optimal length, then average min(1, optimal/actual) over runs. The narration adds
that the queries should be similar enough to share one path but varied enough to expose
deviations.

### Slide 9.12 — How do you test for Convergence? Another way to think about it (deck "Lesson-4", slide 12)
**Evidence:** Narrated — "Another way to think about the convergence score is what percent of the time is your agent taking the optimal path for that given set of inputs? So a convergence score of one means that your agent's taking the optimal path 100% of the time, and your convergence score will always be between 0 and 1."
**Text on slide:** How do you test for Convergence? · Another way to think about a convergence score: · What percentage of the time is your agent taking the optimal path, for a given set of inputs? · Convergence score of 1 means that agent is taking the optimal path 100% of the time · Overall Convergence Score = ( Σ_{i=1}^{N} min(1, S_optimal / S_agent,i) ) / N
**Visual description:** A lead line, two bullets, and the same typeset formula as Slide 9.11,
centered below.
**What it teaches:** Reads the score as how often the agent takes the optimal path; 1 means
always.

### Slide 9.13 — How do you test for Convergence? Two notes (deck "Lesson-4", slide 13)
**Evidence:** Narrated — "First is that convergence evaluations will typically not catch situations where your agent takes an unnecessary step every time for every query in your test set." and "Second, you want to make sure when running convergence evaluators that you're only running them using four completed runs of your agent. If your agent takes three steps to get into a problem and then errors out, you don't want to track those three steps because that will skew your convergence evaluation data."
**Text on slide:** How do you test for Convergence? · Another way to think about a convergence score: · What percentage of the time is your agent taking the optimal path, for a given set of inputs? · Convergence score of 1 means that agent is taking the optimal path 100% of the time · Note 1: convergence evaluations won't catch situations where an unnecessary step is taken by the agent every time. · Note 2: convergence evaluators must check that the agent fully completed a run
**Visual description:** Slide 9.12's bullets without the formula; two right-aligned notes in
small grey italics at the bottom.
**What it teaches:** Two limits: a step wasted on every run stays invisible (it is part of the
minimum), and incomplete runs must be excluded or they skew the score.

### Slide 9.14 — What you've learned (deck "Lesson-4", slide 14)
**Evidence:** Narrated — "In this lesson, you've learned what trajectory and convergence are, why they're important to track and measure. And then one way to measure and calculate convergence."
**Text on slide:** What you've learned: · 1. What trajectory and convergence are, and why they're important to track · 2. How to measure and calculate convergence
**Visual description:** Standard content slide, a two-item numbered list.
**What it teaches:** Recap of the lesson.

---

## Lesson 10: Lab 4: Adding trajectory evaluations
Transcript: `## Lesson 10: Lab 4: Adding trajectory evaluations` in transcripts/evaluating-ai-agents-transcripts.md

No slide in decks "Lesson-3" or "Lesson-4" belongs to this lesson. The narration is a notebook
walkthrough that refers back to the Lesson 9 slides ("the way that you can evaluate your
trajectory as you learned in the previous slides, is by running a set of queries through your
agent and then tracing the number of steps taken by each of those queries").

---

## Lesson 11: Adding structure to your evaluations
Transcript: `## Lesson 11: Adding structure to your evaluations` in transcripts/evaluating-ai-agents-transcripts.md

All 15 slides of deck "Lesson-5a" belong here; the deck's title-card subtitle is this lesson's
title and the narration follows the deck in order.

### Slide 11.1 — Title card: Adding Structure to your Evaluations (deck "Lesson-5a", slide 1)
**Evidence:** Deck-only (title card; its subtitle is this lesson's title)
**Text on slide:** Evaluating AI Agents · Adding Structure to your Evaluations
**Visual description:** Wide white title card. "Evaluating AI Agents" in coral red, centered; the
subtitle in slate grey below it. The arize logo (pink caret mark, black wordmark) sits bottom left
of center and the DeepLearning.AI logo (coral-red concentric mark over the name) bottom right of
center. No instructor name, no wave.
**What it teaches:** Names the course and the lesson.

### Slide 11.2 — Talking Head (deck "Lesson-5a", slide 2)
**Evidence:** Deck-only (production placeholder; the lesson's opening lines, "So far you've learned how to evaluate your agents skills, router and path convergence. You'll now learn how to combine your evaluators into a structured experiment to iterate on and improve your agent. Let's dive in.", are a likely fit for the on-camera segment, but nothing in the transcript confirms it)
**Text on slide:** Talking Head
**Visual description:** A plain pale yellow page with the words "Talking Head" in bold dark grey
in the middle. No logos, no wave.
**What it teaches:** Nothing; it marks where the instructor speaks on camera.

### Slide 11.3 — In this lesson (deck "Lesson-5a", slide 3)
**Evidence:** Narrated — "You'll now learn how to combine your evaluators into a structured experiment to iterate on and improve your agent. Let's dive in. Evaluation-driven development is a concept that involves using evaluations and measurements from your agent to help guide where you spend your time improving and iterating on and developing your agent."
**Text on slide:** In this lesson: · Evaluation-Driven Development · How to use experiments, datasets, and ground truth data to iterate on your agent
**Visual description:** Title at top center; two grey bullets below, left-aligned. Logos top
left and right, coral wave at the bottom.
**What it teaches:** The lesson's two goals: the idea of evaluation-driven development, and using
experiments, datasets and ground truth data to improve an agent.

### Slide 11.4 — Evaluation-Driven Development (deck "Lesson-5a", slide 4)
**Evidence:** Narrated — "Evaluation-driven development is made up of a few different steps. First, you curate a data set of test cases or examples that you can send through different variants of your agent. Next, you send each of those different test cases through those different variants of your agent, each time changing things like the model you're using, the prompts you're using, or the agent logic. And then once you run those different test cases through those different variations of your agent, you take the results of all of those different experiments and run them through your evaluators. Those evaluators will give you a set of scores that you can then use to compare the different iterations of your agent on an apples to apples basis. Now, this is presented linearly in the visualization here, but in practice this tends to be more of a cycle, especially as you move your agent into production. LLM apps require kind of iterative improvement as you're working on them."
**Text on slide:** Evaluation-Driven Development · Curate Dataset · Examples · Track Changes as an Experiment · (Model, Prompt, Logic) · You're a helpful assistant. When user asks about return policy respond with {vars} … · Evaluate the Experiment · New Output · Score · 0.8 · LLM APPS REQUIRE ITERATIVE PERFORMANCE IMPROVEMENTS
**Visual description:** Four stages left to right, joined by slate-grey arrows, each with a bold
slate heading. (1) "Curate Dataset": a dotted rounded box holding three stacked cards fading from
pale pink to solid red, the front one labelled "Examples". (2) "Track Changes as an Experiment"
with "(Model, Prompt, Logic)" beneath: a rounded white box holding a sample system prompt, with
"{vars}" in purple. (3) "Evaluate the Experiment": a dotted box with three stacked purple cards,
the front one labelled "New Output". (4) "Score": a small grey box showing "0.8". Below, the
closing line in bold purple capitals.
**What it teaches:** The evaluation-driven development loop: build a set of test cases, run them
through a changed version of the agent (model, prompt or logic), evaluate the outputs, and get a
score to compare versions. LLM apps need this kind of repeated improvement.

### Slide 11.5 — Curate Dataset (deck "Lesson-5a", slide 5)
**Evidence:** Narrated — "You start by curating a data set test cases. And the idea here is to be more comprehensive than exhaustive. You can have a set of examples that are representative of the inputs that you expect your agent to receive. And you just really need 1 or 2 examples from each of the different types of inputs that you might get. You don't need to have hundreds and hundreds of examples, especially if there's similar types of examples. And these examples can come from either live runs of your agent or can be constructed beforehand, manually, or even in some cases, and generated using another model. [...] And then wherever possible, it's always good to include expected outputs along with your test cases. [...] LLM as-a-Judge, evals can be used even if you don't have expected output. But certain code-based evals do require an expected output to compare against."
**Text on slide:** Curate Dataset · Construct a dataset of **test cases**: · 25+ examples of inputs to your agent · Should be **comprehensive** · Can be sourced from live runs of your agent, or constructed beforehand · Attached **expected outputs** to these test cases · *Note: LLM-as-a-Judge evals can be used without an expected output to compare against.*
**Visual description:** Title at top center; a lead-in line, then four grey bullets with the key
words in bold, and an italic sub-bullet (hollow circle) under the last one. Logos and wave as
usual.
**What it teaches:** What a test-case dataset should be: enough inputs to cover the kinds of
input the agent gets, taken from live runs or written ahead of time, with expected outputs where
possible. LLM-as-a-Judge evals work without an expected output. The slide's "25+" is not in the
narration, which asks for one or two examples per input type instead.

### Slide 11.6 — Track Agent Changes (deck "Lesson-5a", slide 6)
**Evidence:** Narrated — "So, some tests that you can often do are changing things like your prompts used by your agent, changing the tool definitions that you're passing into your router, changing the router logic itself, changing some of the skills or the skill structure, or just swapping in a new model that you want to test out. And the practice of sending each of your test cases through a variation of your agent is often referred to as an experiment."
**Text on slide:** Track Agent Changes · Test proposed changes to your agent: · Prompt iterations · Tool definitions · Router logic · Skill structure · Model changes · **Experiments** are a structure used to run each of your curated dataset test cases through your agent, and record the results
**Visual description:** Title at top center; a lead-in line and five grey bullets; lower down, a
separate sentence with "Experiments" in bold. Logos and wave as usual.
**What it teaches:** The kinds of change to test (prompts, tool definitions, router logic, skill
structure, model), and the definition of an experiment: running every test case through one
version of the agent and recording the results.

### Slide 11.7 — Evaluate your Experiment (deck "Lesson-5a", slide 7)
**Evidence:** Narrated — "Once you have all your experiment data collected, then you can use all of your evaluators from the previous lessons that you've built and apply them to the results of those experiments. So you can use your code-based evaluators, your comparison against ground truth, or checking if generated code is runnable, as well as the convergence evaluators that you run. And you can use your LLM as-a-Judge evaluators, like function calling, analysis, clarity, and entity correctness."
**Text on slide:** Evaluate your Experiment · Use your same evaluators from previous lessons: · Code-based evals · Compare against ground truth · Generated code is runnable · Convergence · LLM-as-a-Judge evals · Function calling · Analysis clarity · Entity correctness
**Visual description:** Title at top center; a lead-in line, then two grey bullets, each with
three hollow-circle sub-bullets. Logos and wave as usual.
**What it teaches:** The evaluators built in earlier lessons are reused on experiment results:
three code-based (ground-truth comparison, runnable generated code, convergence) and three
LLM-as-a-Judge (function calling, analysis clarity, entity correctness).

### Slide 11.8 — Applying Evaluation Driven Development to your Agent: the agent (deck "Lesson-5a", slide 8)
**Evidence:** Narrated — "Now, how can you apply this to your agent? As a quick reminder, your agent is set up to use this OpenAI router with function calling and then three different skills that you can evaluate."
**Text on slide:** Applying Evaluation Driven Development to your Agent · User · Router (GPT-4o-mini w/ function calling) · Look Up Sales Data Tool · Data Analysis Tool · Data Visualization Tool
**Visual description:** A hand-drawn style diagram. Left, a blue circle "User"; two arrows
between it and a pink rounded box "Router (GPT-4o-mini w/ function calling)" in red handwriting,
one in each direction. From the router, three arrows fan out to three white rounded boxes
stacked on the right: "Look Up Sales Data Tool", "Data Analysis Tool", "Data Visualization Tool".
A dashed line runs from each tool box up and over the top back to the router, ending in an arrow
on the router.
**What it teaches:** A reminder of the agent being evaluated: a GPT-4o-mini router using function
calling, three tools it can call, and results flowing back to the router before it answers the
user.

### Slide 11.9 — Applying Evaluation Driven Development to your Agent: the router (deck "Lesson-5a", slide 9)
**Evidence:** Narrated — "First, taking an example of how you would set up an experiment around with a router. You might have an example test case that looks something like this where you have an input, which is which stores have the best sales performance in 2021 and then an expected output. In this case, the database lookup tool is the tool should be chosen by the router. And then you might want to experiment with trying different tool descriptions. [...] And then once you have those experiments run, you can evaluate the results using either code based comparison against ground truth. [...] Or you can use a function calling LLM as-a-Judge."
**Text on slide:** Applying Evaluation Driven Development to your Agent · Each aspect of your agent can be built into an experiment: · Component of your agent · Example test case · Experiment · Evaluations · Router · `{ ‘input’: ‘Which stores had the best sales performance in 2021’, ‘expected_output’: ‘database_lookup’}` · Testing different tool description strings · 1. Code-based comparison against ground truth · 2. Function calling using LLM-as-a-Judge
**Visual description:** Title and a grey lead-in line above a four-column table with a bold
header row and one data row. The test case is in monospace: the keys in black, the input question
in red, "database_lookup" in green.
**What it teaches:** How one agent component maps to an experiment: the router's test case pairs
a question with the tool it should pick; the experiment varies the tool descriptions; the result
is scored by a code comparison with the expected tool and by an LLM judge of the function call.

### Slide 11.10 — Applying Evaluation Driven Development to your Agent: the database lookup tool, open question (deck "Lesson-5a", slide 10)
**Evidence:** Narrated — "Taking another component of your agent. You have your database lookup tool or skill, and you might have a test case that looks something like this, where you have the same input from the previous round. And then in this case, the expected output is some SQL code that you see there. [...] Invite you to pause the video here for a second, and see if you can think of an experiment and some evaluations that you could run on this database lookup tool."
**Text on slide:** Applying Evaluation Driven Development to your Agent · Each aspect of your agent can be built into an experiment: · Component of your agent · Example test case · Experiment · Evaluations · Router · `{ ‘input’: ‘Which stores had the best sales performance in 2021’, ‘expected_output’: ‘database_lookup’}` · Testing different tool description strings · 1. Code-based comparison against ground truth · 2. Function calling using LLM-as-a-Judge · Database lookup tool · `{ ‘input’: ‘Which stores had the best sales performance in 2021’, ‘expected_output’: ‘SELECT Store_Number, SUM(Qty_Sold) AS Total_Qty_Sold,....’}` · ? · ?
**Visual description:** The table of Slide 11.9 with a second row added. Its test case has the
same red question and a green SQL query as the expected output; the Experiment and Evaluations
cells hold only "?".
**What it teaches:** The database lookup tool's test case targets an intermediate step, the
generated SQL. The "?" cells invite the learner to propose the experiment and evaluations.

### Slide 11.11 — Applying Evaluation Driven Development to your Agent: the database analysis tool, open question (deck "Lesson-5a", slide 11)
**Evidence:** Narrated — "So one experiment you could do would be testing different SQL generation prompts. You could also test different models or other pieces of that as well. And then you can use your code based comparison against ground truth evaluator, similar to what you had looked at in previous notebooks as well, because you have that ground truth to compare against. Next, you look at the database analysis tool. In this case, you might have a test case like the one you see here where you have a message from a user, and then you actually have some retrieved data. [...] and then you don't actually have an expected output in this test case. So once again, I invite you to pause the video and see if you can think of an experiment and then an evaluation that you can run in this case."
**Text on slide:** Applying Evaluation Driven Development to your Agent · Each aspect of your agent can be built into an experiment: · Component of your agent · Example test case · Experiment · Evaluations · Router · `{ ‘input’: ‘Which stores had the best sales performance in 2021’, ‘expected_output’: ‘database_lookup’}` · Testing different tool description strings · 1. Code-based comparison against ground truth · 2. Function calling using LLM-as-a-Judge · Database lookup tool · `{ ‘input’: ‘Which stores had the best sales performance in 2021’, ‘expected_output’: ‘SELECT Store_Number, SUM(Qty_Sold) AS Total_Qty_Sold,....’}` · Testing different SQL generation prompts · 1. Code-based comparison against ground truth · Database analysis tool · `{ ‘input’: ‘{‘role’: ‘user’, ‘content’: ‘Which stores had the best sales performance in 2021’}, {‘role’: ‘tool content’: ‘Store_Number Total_Qty_Sold Total_Sale_Value 0 2970 5867.0 84454.329826….’}’}` · ? · ?
**Visual description:** The table with the database lookup row filled in and a third row added.
The third row's test case is in red monospace: a user message and a tool message holding a
fragment of a results table. It has no expected output. Its Experiment and Evaluations cells
hold only "?".
**What it teaches:** The answer for the lookup tool (vary the SQL generation prompt, compare with
the ground-truth SQL), and a new case: the analysis tool's test case is the user question plus
the retrieved data, with no expected output.

### Slide 11.12 — Applying Evaluation Driven Development to your Agent: full table (deck "Lesson-5a", slide 12)
**Evidence:** Narrated — "So here you want to experiment could be testing different LLM models. You could also test different prompts or other kind of logic changes there too. Then you can use the analysis clarity and entity correctness LLM as-a-Judge evaluations from previous slides and notebooks that you've seen to evaluate the results."
**Text on slide:** Applying Evaluation Driven Development to your Agent · Each aspect of your agent can be built into an experiment: · Component of your agent · Example test case · Experiment · Evaluations · Router · `{ ‘input’: ‘Which stores had the best sales performance in 2021’, ‘expected_output’: ‘database_lookup’}` · Testing different tool description strings · 1. Code-based comparison against ground truth · 2. Function calling using LLM-as-a-Judge · Database lookup tool · `{ ‘input’: ‘Which stores had the best sales performance in 2021’, ‘expected_output’: ‘SELECT Store_Number, SUM(Qty_Sold) AS Total_Qty_Sold,....’}` · Testing different SQL generation prompts · 1. Code-based comparison against ground truth · Database analysis tool · `{ ‘input’: ‘{‘role’: ‘user’, ‘content’: ‘Which stores had the best sales performance in 2021’}, {‘role’: ‘tool content’: ‘Store_Number Total_Qty_Sold Total_Sale_Value 0 2970 5867.0 84454.329826….’}’}` · Testing different LLM models · 1. Analysis clarity · 2. Entity correctness
**Visual description:** The same three-row table with every cell filled.
**What it teaches:** The complete mapping: router → vary tool descriptions → code comparison and
function-calling judge; lookup tool → vary SQL prompts → code comparison; analysis tool → vary
the model → analysis-clarity and entity-correctness judges. A component without an expected
output is scored by LLM judges only. The visualization tool has no row.

### Slide 11.13 — Comparing your Results (deck "Lesson-5a", slide 13)
**Evidence:** Narrated — "And as you structure all of these together and start to run multiple iterations of your agent with multiple different evaluators and create a whole process around this, you can end up with, a dashboard or a heads-up display that looks something like this. Each row has one run of your agent, and then all of your evaluators, those different columns here, and you can measure, okay, what are the effects of each change that I'm going to make to my agent across not just one part of the agent, but each part of the agent holistically."
**Text on slide:** Comparing your Results · datasets > overall_experiment_inputs-2025-01-30 00:20:41 · overall_experiment_inputs-2025-01-30 00:20:41 · pandas · Experiments 2 · Examples 7 · Code · Run Experiment · Playground · Add Example · name · description · created at · code_is_runnable · evaluate_clarity · evaluate_entity_correctness · evaluate_sql_result · function_calling_eval · run count · avg latency · error rate · #2 · Overall Experiment · Evaluating the overall experiment · 1/29/2025, 04:25 PM · 0.86 · 0.86 · 0.86 · 0.43 · 0.71 · 7 · 8.14s · 14.29% · #1 · Overall Experiment · Evaluating the overall experiment · 1/29/2025, 04:20 PM · 0.86 · 0.86 · 0.86 · 0.57 · 0.79 · 7 · 6.86s · 14.29%
**Visual description:** A dark-theme screenshot of a dataset page in a web tool, filling the
slide width. A narrow left sidebar holds a bird-shaped logo and four icons. The header shows the
breadcrumb and dataset name, "pandas" below it, and buttons for download, history, "Code",
"Run Experiment", "Playground" and "Add Example". The "Experiments" tab (2) is selected over
"Examples" (7). The table has two rows, one per experiment run. Each evaluator column shows a
score with a small purple or pink bar; latency has a clock icon and is in yellow; error rate is
in orange. The rightmost column is cut off at the slide edge (only an "n" of its header shows).
Logos at top, wave at bottom.
**What it teaches:** The goal of the structure: one table where each row is a run of the agent
and each column is an evaluator, so the effect of a change shows across every part of the agent
at once. In the example, run #2 scores lower on the SQL and function-calling evals than run #1
and is slower.

### Slide 11.14 — Building across Development and Production (deck "Lesson-5a", slide 14)
**Evidence:** Narrated — "And then again, as you start to move your agent into production, you'll find that you're going to come up with new test cases, new evaluations, and new changes that you want to make using some of that production monitoring data that you have. And then you can bring that back into your testing and development process. So this whole experimentation framework and this whole evaluation driven development framework enables you to not just create a strong application in development, but also incorporate production learnings that you have into your development process and create a large flywheel here that you can use to create a better and better agent over time."
**Text on slide:** Building across Development and Production · Development · Saving off best prompts to prompt hub · Evaluate experiments · 3. EVALUATE · 1. TRACE · Curate datasets · 2. ITERATE · Run experiment · Deploy the change · Production · App Traces · 1. TRACE · 2. EVALUATE · Online Evaluation · 3. MONITOR · Monitor App · Prod data can be brought to datasets
**Visual description:** Two light-grey panels split by a thin vertical line. Each holds a circle
made of three colored arcs with curved labels and grey arrows running clockwise. Left,
"Development": "1. TRACE" (pink, labelled "Curate datasets"), "2. ITERATE" (purple, "Run
experiment"), "3. EVALUATE" (navy, "Evaluate experiments" and "Saving off best prompts to prompt
hub"). Right, "Production": "1. TRACE" (navy, "App Traces"), "2. EVALUATE" (pink, "Online
Evaluation"), "3. MONITOR" (purple, "Monitor App"). A green dotted arrow runs from the prompt-hub
point across the divide to a green box "Deploy the change". A red dotted line runs from the
production circle through a red box "Prod data can be brought to datasets" back to "Curate
datasets". This slide has only the DeepLearning.AI logo at top right; the arize logo is missing.
**What it teaches:** Evaluation-driven development is a loop that spans development and
production: best changes are deployed, production is traced, evaluated online and monitored, and
production data feeds new test cases back into development.

### Slide 11.15 — What you've learned (deck "Lesson-5a", slide 15)
**Evidence:** Narrated — "In this lesson, you learned the purpose of evaluation-driven development, what it is and how it works, and you learned how you can structure experiments around your evals to scale them as you continually improve your agent."
**Text on slide:** What you’ve learned: · 1. The purpose of Evaluation-Driven Development and how it works · 2. How to structure experiments around your evals
**Visual description:** Title at top center; two numbered grey lines below. Logos and wave as
usual.
**What it teaches:** Recap: what evaluation-driven development is for, and how to organize
experiments around evaluators.

---

## Lesson 12: Lab 5: Adding structure to your evaluations
Transcript: `## Lesson 12: Lab 5: Adding structure to your evaluations` in transcripts/evaluating-ai-agents-transcripts.md

No deck belongs to this lesson. It is a notebook lab (Lab 5) that sits between the Lesson 11 and Lesson 13 decks.

---

## Lesson 13: Improving your LLM-as-a-judge
Transcript: `## Lesson 13: Improving your LLM-as-a-judge` in transcripts/evaluating-ai-agents-transcripts.md

All 8 slides of deck "Lesson-5b" belong here; the deck's title-card subtitle is this lesson's
title and the narration follows the deck in order.

### Slide 13.1 — Title card: Improving your LLM-as-a-Judge (deck "Lesson-5b", slide 1)
**Evidence:** Deck-only (title card; its subtitle is this lesson's title)
**Text on slide:** Evaluating AI Agents · Improving your LLM-as-a-Judge
**Visual description:** Same layout as Slide 11.1: "Evaluating AI Agents" in coral red, the
subtitle in slate grey, the arize and DeepLearning.AI logos side by side below. No wave.
**What it teaches:** Names the course and the lesson.

### Slide 13.2 — In this lesson (deck "Lesson-5b", slide 2)
**Evidence:** Narrated — "For this lesson, you'll dive into how you can improve your LLM evaluators and LLM as-a-Judge evaluations within your agent."
**Text on slide:** In this lesson: · How to tailor your LLM evaluators to your agent
**Visual description:** Title at top center; one grey bullet. Logos and wave as usual.
**What it teaches:** The lesson's single goal: adapting the LLM evaluators to the agent.

### Slide 13.3 — Improving your Evaluators: the question (deck "Lesson-5b", slide 3)
**Evidence:** Narrated — "So if you think back to the previous slides lesson, you might have noticed a case where you used both a code-based comparison against ground truth and an LLM as-a-Judge function calling evaluation to measure the performance of your router. And you might be thinking, why would you need to use two different evaluators to evaluate the same thing?"
**Text on slide:** Improving your Evaluators · Thinking back: Why would you use two evaluators to evaluate the same thing, like you did with function calling? · Component of your agent · Example test case · Experiment · Evaluations · Router · `{ ‘input’: ‘Which stores had the best sales performance in 2021’, ‘expected_output’: ‘database_lookup’}` · Testing different tool description strings · 1. Code-based comparison against ground truth · 2. Function calling using LLM-as-a-Judge*
**Visual description:** Title at top center; a large grey question below it; then the one-row
Router table from Slide 11.9, unchanged except for an asterisk after "LLM-as-a-Judge" in the
Evaluations cell. Logos and wave as usual.
**What it teaches:** Poses the question the lesson answers: why score the router with both an
exact code check and an LLM judge.

### Slide 13.4 — Improving your Evaluators: the answer (deck "Lesson-5b", slide 4)
**Evidence:** Narrated — "Well, the answer there is that you can use this technique to actually measure how effective and how closely your LLM as-a-Judge evaluator aligns to your 100% accurate code base comparison against ground truth. Because as you remember, LLM as-a-Judge is not 100% accurate method. However, it can scale a lot further beyond the comparison against ground truth."
**Text on slide:** Improving your Evaluators · Thinking back: Why would you use two evaluators to evaluate the same thing, like you did with function calling? · To see how accurate the LLM-as-a-Judge eval is compared to the 100% accurate, code-based comparison against ground truth · Remember, LLM-as-a-Judge is not a 100% accurate method!
**Visual description:** The same title and question; the table is gone. In its place, a
right-aligned answer in dark red over four lines, and a grey reminder line near the bottom.
Logos and wave as usual.
**What it teaches:** Running both evaluators on the same cases measures how often the LLM judge
agrees with the exact ground-truth check. LLM judges are not fully accurate, so their accuracy
must be measured.

### Slide 13.5 — Using Experiments to Improve your LLM-as-a-Judge: the function-calling judge (deck "Lesson-5b", slide 5)
**Evidence:** Narrated — "So you could set up an experiment on the function calling LLM judge. And you might have an example test case that looks something like we see here where you have an input. That's which stores have the best sales performance in 2021 and then an output in this case the database lookup. And the important thing is that everything in red there is the input to your LLM judge, because you're having your LLM judge judge the performance of that agent. So everything in red there is the input. And then you'd have your expected output in this case is correct. So that expected output is your ground truth data. And then you could set up the experiment to test different versions of your LLM as-a-Judge prompt. [...] And then you can evaluate the performance of your LLM as-a-Judge using the code-based comparison against ground truth. In this case, comparing to that correct or incorrect expected output label."
**Text on slide:** Using Experiments to Improve your LLM-as-a-Judge · You can use experiments to test your LLM Judges: · LLM Judge · Example test case · Experiment · Evaluations · Function calling LLM Judge · `{‘input’: ‘{‘input’: ‘Which stores had the best sales performance in 2021’, ‘expected_output’: ‘database_lookup’} }’, ‘expected_output’: ‘correct’}` · Testing different LLM-as-a-Judge prompts · 1. Code-based comparison against ground truth
**Visual description:** Title and a grey lead-in line above a four-column table, now headed "LLM
Judge" instead of "Component of your agent", with one row. In the test case, the whole inner
router test case (the nested `{‘input’: … ‘database_lookup’}`) is in red as the judge's input;
"correct" is in green as the expected output; the outer keys are black.
**What it teaches:** The same experiment structure applied to a judge: the judge's test case is
an agent test case plus the label the judge should give; the experiment varies the judge prompt;
the judge is scored by exact comparison with that label.

### Slide 13.6 — Using Experiments to Improve your LLM-as-a-Judge: the analysis-clarity judge, open question (deck "Lesson-5b", slide 6)
**Evidence:** Narrated — "And you can use the same approach for another LLM as-a-Judge that you're using, in this case the one you're using to evaluate analysis clarity. And so in that example, you might have an input that looks something like you see here: in 2021 the stores that perform the best, yada yada. And then the expected output of the analysis is clearer because of x, y and z. And this time you might judge different types of models that are being used to create that judge label. [...] Now the question here though becomes how do you evaluate that output? Because while you have expected output, it's no longer a clean just correct or incorrect label. It's this expected output of the analysis is clear because of something. And so what if your LLM as-a-Judge comes back with the analysis is easy to understand because of x, y, and z."
**Text on slide:** Using Experiments to Improve your LLM-as-a-Judge · You can use experiments to test your LLM Judges: · LLM Judge · Example test case · Experiment · Evaluations · Function calling LLM Judge · `{‘input’: ‘{‘input’: ‘Which stores had the best sales performance in 2021’, ‘expected_output’: ‘database_lookup’} }’, ‘expected_output’: ‘correct’}` · Testing different LLM-as-a-Judge prompts · 1. Code-based comparison against ground truth · Analysis Clarity LLM Judge · `{‘input’: ‘In 2021, the stores that performed the best based on total sales value were:....’, ‘expected_output’: ‘The analysis is clear because….’}` · Testing different models to judge the analysis · How do we evaluate this output? · What if the output was “The analysis is easy to understand…”
**Visual description:** The table of Slide 13.5 with a second row. Its test case has a red
analysis text as input and a green explanation as expected output. Its Evaluations cell holds a
question instead of an answer.
**What it teaches:** When the judge's expected output is free text rather than a label, an exact
comparison fails: a differently worded but correct judgment would not match.

### Slide 13.7 — Using Experiments to Improve your LLM-as-a-Judge: semantic similarity (deck "Lesson-5b", slide 7)
**Evidence:** Narrated — "That should be correct. But you can't just compare those strings exactly. That's where you can use something like semantic similarity to compare the meaning of each of those strings in a numeric way, as opposed to doing a direct comparison between output, unexpected output."
**Text on slide:** Using Experiments to Improve your LLM-as-a-Judge · You can use experiments to test your LLM Judges: · LLM Judge · Example test case · Experiment · Evaluations · Function calling LLM Judge · `{‘input’: ‘{‘input’: ‘Which stores had the best sales performance in 2021’, ‘expected_output’: ‘database_lookup’} }’, ‘expected_output’: ‘correct’}` · Testing different LLM-as-a-Judge prompts · 1. Code-based comparison against ground truth · Analysis Clarity LLM Judge · `{‘input’: ‘In 2021, the stores that performed the best based on total sales value were:....’, ‘expected_output’: ‘The analysis is clear because….’}` · Testing different models to judge the analysis · 1. Semantic similarity
**Visual description:** The same two-row table; the question in the analysis-clarity Evaluations
cell is replaced by "1. Semantic similarity".
**What it teaches:** A free-text judge output is scored against its expected output by semantic
similarity, a numeric comparison of meaning, instead of exact matching.

### Slide 13.8 — What you've learned (deck "Lesson-5b", slide 8)
**Evidence:** Narrated — "So in this lesson, you've learned how you can measure and improve your LLM as-a-Judge evals using structured experiments."
**Text on slide:** What you’ve learned: · How to measure and improve your LLM-as-a-Judge evals
**Visual description:** Title at top center; one grey line, centered, no bullet. Logos and wave
as usual.
**What it teaches:** Recap: LLM judges can be measured and improved with the same experiment
structure used for the agent.

---

## Lesson 14: Monitoring agents
Transcript: `## Lesson 14: Monitoring agents` in transcripts/evaluating-ai-agents-transcripts.md

All 13 slides of deck "Lesson-6" belong here.

### Slide 14.1 — Title card: Monitoring Agents (deck "Lesson-6", slide 1)
**Evidence:** Deck-only (title card; its subtitle is this lesson's title)
**Text on slide:** Evaluating AI Agents · Monitoring Agents · arize · DeepLearning.AI
**Visual description:** Wide white title card. "Evaluating AI Agents" in coral red, centered;
below it "Monitoring Agents" in slate grey. Bottom left the arize logo (pink caret with a dot, black
"arize"); bottom right the DeepLearning.AI logo (red concentric-circle mark over the red name). The
text layer also holds "[Your Logo Here]", which is not visible.
**What it teaches:** Names the course and the lesson.

### Slide 14.2 — Talking Head (deck "Lesson-6", slide 2)
**Evidence:** Deck-only (production placeholder for an on-camera segment)
**Text on slide:** Talking Head
**Visual description:** Plain cream background with the words "Talking Head" in bold dark grey,
centered. No logos, no wave.
**What it teaches:** Nothing in itself; it marks where the instructor speaks to camera.

### Slide 14.3 — In this lesson: (deck "Lesson-6", slide 3)
**Evidence:** Deck-only (agenda; the narration's opening states the lesson's aim but does not read the list) — closest passage: "you need to apply the same techniques of tracing evals and experimentation"
**Text on slide:** In this lesson: · Production agents · Why monitoring agents matters · Recap: Instrumentation, evals and metrics over time · Using data from production to iterate on your agent and evals (Adding experiments to a CI/CD pipeline)
**Visual description:** Standard content slide; four grey bullets under the title.
**What it teaches:** The lesson plan: production agents, why monitoring matters, a recap of
instrumentation, evals and metrics over time, and feeding production data back into the agent and
its evals through experiments in a CI/CD pipeline.

### Slide 14.4 — Recap: Going from Development to Production (deck "Lesson-6", slide 4)
**Evidence:** Narrated — "four main steps that take you from an initial agent prototype all the way" … "Choosing the right architecture, you need to decide on an agent framework" … "you can catch issues early"
**Text on slide:** Recap: Going from Development to Production · 4 Steps to go from development to production · 1. Choose the right agent architecture · 2. Choose what to evaluate and the correct metrics · 3. Build your eval structure · 4. Use your data to iterate · Development · Saving off best prompts to prompt hub · Evaluate experiments · 3. EVALUATE · 1. TRACE · Curate datasets · 2. ITERATE · Run experiment · Deploy the change · Prod data can be brought to datasets · Production · App Traces · 1. TRACE · 2. EVALUATE · Online Evaluation · 3. MONITOR · Monitor App
**Visual description:** Left, a bold grey subheading and a numbered list of four steps ("what"
and "metrics" in bold). Right, two light-grey panels. "Development" holds a circular cycle of three
arcs: pink "1. TRACE" (labelled "Curate datasets"), purple "2. ITERATE" ("Run experiment"), navy
"3. EVALUATE" ("Evaluate experiments", "Saving off best prompts to prompt hub"). "Production" holds
a second cycle: navy "1. TRACE" ("App Traces"), pink "2. EVALUATE" ("Online Evaluation"), purple
"3. MONITOR" ("Monitor App"). A green dotted arrow runs from Development to a green "Deploy the
change" box toward Production; a red dotted arrow runs back from Production through a red "Prod
data can be brought to datasets" box to "Curate datasets".
**What it teaches:** The four development steps recapped, and the two loops: develop (trace,
iterate, evaluate) then deploy; in production trace, evaluate online and monitor, and bring
production data back into development datasets.

### Slide 14.5 — Scaling Production Agent Systems (deck "Lesson-6", slide 5)
**Evidence:** Narrated — "adopting a multi-agent system where agents can call" … "or a multimodal system where your agent" … "or a continuous improving system where your agent learns"
**Text on slide:** Scaling Production Agent Systems · Multi agent systems · Multi-modal systems · Continuously improving agents · User · Router (GPT-4o w/ function calling) · Agent 1 · Router (GPT-4o w/ function calling) · Look Up Sales Data Tool · Data Analysis Tool · Data Visualization Tool · Agent 2 · Agent 3 · Agent 4 · Agent 2 · Agent 3 · Data Storage · Audio · Video · Unstructured Data · AI Agent · Which store had the most sales in 2021? · User · Router (GPT-4o w/ function calling) · Look Up Sales Data Tool · Data Analysis Tool · Router (GPT-4o w/ function calling) · User · Iterate on tool · Updated logic · Different model · Different prompt · Collect feedback · Run evals
**Visual description:** Three columns of hand-drawn diagrams under grey headings. Left: a blue
"User" circle sends to a red "Router" box that fans out to "Agent 1" (expanded: its own router and
three tool boxes) and greyed-out "Agent 2"/"Agent 3"; Agent 1 in turn points to robot-icon "Agent
2", "Agent 3", "Agent 4". Middle: a "Data Storage" box holding "Audio", "Video" and "Unstructured
Data", with dashed two-way arrows to an "AI Agent" box. Right: a vertical flow for the question
"Which store had the most sales in 2021?" — User, Router, Look Up Sales Data Tool, Data Analysis
Tool, Router, User — with an arrow from the final User (thumbs up/down, "Collect feedback", "Run
evals") to a green "Iterate on tool" box ("Updated logic", "Different model", "Different prompt")
that points back to the lookup tool.
**What it teaches:** Production agents tend to grow into multi-agent systems, multimodal systems,
or continuously improving systems that learn from user feedback.

### Slide 14.6 — What's different about production? (deck "Lesson-6", slide 6)
**Evidence:** Narrated — "or automated processes. So, what's different about production? Well, you can often discover new failure" … "that your system doesn't know about yet, like a brand new product. If your agent now calls out" … "to additional APIs or other agents, there are more chances for errors" … "You might also try A/B testing"
**Text on slide:** What’s different about production? · Discovering new failure modes · i.e. new queries or use cases · A new product releases that the system is not aware of · Higher complexity · external APIs and other agents · Making changes to agents · a/b testing and evaluating, using data
**Visual description:** Standard content slide; three top-level grey bullets, each with an
indented sub-bullet, the first with a further square-bulleted third level.
**What it teaches:** Production brings new failure modes (unseen queries, products the system does
not know), more complexity (external APIs, other agents), and changes to the agent (A/B tests)
that must be evaluated with data.

### Slide 14.7 — Tools for managing agent performance in production (deck "Lesson-6", slide 7)
**Evidence:** Narrated — "you use in development, like instrumentation and feedback" … "loops, are just as valuable in production. You'll continue to collect metrics" … "and continuous delivery flows and ongoing experiments"
**Text on slide:** Tools for managing agent performance in production · Instrumentation and feedback · Monitoring your metrics · CI/CD (continuous improvement)
**Visual description:** Standard content slide; three grey bullets.
**What it teaches:** The three production tools the rest of the lesson covers: instrumentation and
feedback, metric monitoring, and CI/CD as continuous improvement.

### Slide 14.8 — Instrumentation and feedback (deck "Lesson-6", slide 8)
**Evidence:** Narrated — "same tracing and annotation methods you had in development, only" … "for evals is crucial in production. You can take real usage data, for example," … "and attach human-labeled annotations"
**Text on slide:** Instrumentation and feedback · Collect user feedback and data for evals from your application → Tracing and Annotations · Define areas of improvement by looking at your data · Trace Details · Trace Status · OK · Latency · 0.91s · Feedback · Hallucination hallucinated · Q&A Correctness incorrect · User Feedback · BaseQueryEngine.query 0.91s · RetrieverQueryEngine._query 0.90s · BaseRetriever.retrieve 0.24s · VectorIndexRetriever._retrieve 0.23s · BaseEmbedding.get_query_embedding 0.19s · OpenAIEmbedding._get_query_embedding 0.18s · CohereRerank._postprocess_nodes 0.17s · User Feedback · label · score 1.00 · annotator kind HUMAN · Input · Can I use gRPC for trace collectio[n] · Output · You can use gRPC for trace collect[ion] · [Att]ributes · Event[s]
**Visual description:** Two bullets ("Tracing and Annotations" in bold) above a dark-theme
screenshot of a trace-detail view: status OK, latency 0.91s, and three feedback chips
(purple "Hallucination hallucinated", orange "Q&A Correctness incorrect", green "User Feedback"
with a thumbs-up). Below, a span tree of nested retrieval and embedding calls with timings. A pink
box highlights a popup for the user-feedback annotation: label thumbs-up, score 1.00, annotator
kind HUMAN. Right side, cropped Input/Output panels about gRPC trace collection. Bracketed letters
in the text field mark words cut off by the crop.
**What it teaches:** In production, traces carry both automatic eval labels and human feedback
annotations; looking at that data shows where to improve.

### Slide 14.9 — Monitoring metrics (deck "Lesson-6", slide 9)
**Evidence:** Narrated — "if you're using convergence evals, you can see how many steps it takes" … "LLM APIs, you should track those calls, too. They can have a significant impact on latency and costs," … "which can impact your end user experience. Your choice of model, perhaps a large reasoning model versus"
**Text on slide:** Monitoring metrics · Efficiency of your system (i.e. Convergence evals) · Ensure your system performance does not degrade over time · Dependencies on external services (latency, cost) · Ensure that you are monitoring external LLM calls as they can have a large impact on end user experience · i.e. reasoning model vs smaller model for a certain application · projects > demo_llama_index · Total Traces 100 · Total Tokens 126,148 · Latency P50 1.44s · Latency P99 2.85s · Q&A Correctness 0.80 · Hallucination 0.17 · Traces · Spans · Sessions
**Visual description:** Two bullets with sub-bullets above a dark-theme screenshot strip of a
project header ("projects > demo_llama_index") showing summary metrics: trace count, token count,
P50 and P99 latency (green clock icons), and Q&A Correctness and Hallucination as ring gauges, with
Traces / Spans / Sessions tabs.
**What it teaches:** Track efficiency over time (for example convergence evals, so performance
does not degrade) and external-service dependencies (latency, cost, model choice) at the project
level alongside eval scores.

### Slide 14.10 — CI/CD (continuous improvement): collect user feedback (deck "Lesson-6", slide 10)
**Evidence:** Narrated — "When you gather human feedback" … "and run your evals on real traffic, you'll gain a clearer picture"
**Text on slide:** CI/CD (continuous improvement) · Collect user feedback (human labels) to understand end-to-end Agent performance · Which store had the most sales in 2021? · User · Router (GPT-4o-mini w/ function calling) · Look Up Sales Data Tool · Data Analysis Tool · Router (GPT-4o-mini w/ function calling) · User · Collect feedback · Run evals · Iterate on tool · Updated logic · Different model · Different prompt
**Visual description:** One bullet above a horizontal hand-drawn flow for "Which store had the
most sales in 2021?": blue User circle → red Router box → Look Up Sales Data Tool → Data Analysis
Tool → red Router box → blue User circle. From the final User, an arrow with thumbs up/down
("Collect feedback", "Run evals") points to a green "Iterate on tool" box ("Updated logic",
"Different model", "Different prompt"), which has two-way arrows with the Data Analysis Tool. Note
the routers here read "GPT-4o-mini", where Slide 14.5 reads "GPT-4o".
**What it teaches:** Human labels on real interactions measure the agent end to end and drive
changes to a tool's logic, model or prompt.

### Slide 14.11 — CI/CD (continuous improvement): curate datasets (deck "Lesson-6", slide 11)
**Evidence:** Narrated — "One effective approach is curating golden" … "data sets that capture your most critical use cases" … "Experiments can act like gates" … "for shipping changes, so you can decide whether to roll forward"
**Text on slide:** CI/CD (continuous improvement) · Curate datasets for continuous experimentation as you iterate · Datasets can be representative of specific failure modes + general performance (golden datasets) · Experiments act as “gates” for shipping changes · datasets > overall_experiment_questions_all · overall_experiment_questions_all · pandas · Experiments 1 · Examples 6 · Code · Run Experiment · Playground · Add Example · name · description · created at · code_is_runnable · evaluate_clarity · evaluate_entity_correctness · evaluate_sql_result · function_calling_eval · run count · avg latency · error rate · m[…] · #1 Overall Experiment · Evaluating the overall experiment · 1/24/2025, 09:43 AM · 1.00 · 1.00 · 1.00 · 0.50 · 0.92 · 6 · 7.83s · 0.00% · –
**Visual description:** One bullet with two sub-bullets above a dark-theme screenshot of a dataset
page ("overall_experiment_questions_all", tag "pandas", 1 experiment, 6 examples) with buttons for
Code, Run Experiment, Playground and Add Example. A table row for experiment #1 "Overall
Experiment" shows a score bar per evaluator column (1.00, 1.00, 1.00, 0.50, 0.92), run count 6,
average latency 7.83s (yellow clock) and error rate 0.00%. The last column header is cut off.
**What it teaches:** Keep curated datasets (failure-mode sets plus golden datasets), rerun
experiments on them with every change, and use the results as gates before shipping.

### Slide 14.12 — Example: Self Improving Agent (deck "Lesson-6", slide 12)
**Evidence:** Narrated — "Let's imagine you have a self-improving" … "agent that collects feedback automatically whenever a user interacts" … "CI/CD experiments on this data set, checking" … "from the newly collected data. This lets your system learn from mistakes" … "is essentially applying evaluation driven development in production. You're watching for new failure modes, monitoring how well your agent"
**Text on slide:** Example: Self Improving Agent · Which store had the most sales in 2021? · User · Router (GPT-4o-mini w/ function calling) · Look Up Sales Data Tool · Data Analysis Tool · Router (GPT-4o-mini w/ function calling) · User · Collect feedback · Self Improvement · Updated logic · Different model · Different prompt · Iterate on tool · run CI/CD experiment · add to dataset · (optional) use few shot examples to improve prompt · i.e. cases passing 4/5 --> 3/5 · Evaluation-driven development in production
**Visual description:** The same horizontal flow as Slide 14.10. The feedback arrow ("Collect
feedback", thumbs up/down) now enters a dashed "Self Improvement" box holding three green boxes
read right to left: "add to dataset" → "run CI/CD experiment" (note "i.e. cases passing 4/5 -->
3/5", with "3/5" in red) → "Iterate on tool" (notes "Updated logic / Different model / Different
prompt" above, "(optional) use few shot examples to improve prompt" below). Two-way arrows link the
box to the Data Analysis Tool. Left, the caption "Evaluation-driven development in production".
**What it teaches:** A self-improving loop: add feedback-tagged production examples to a dataset,
run a CI/CD experiment on it (a drop such as 4/5 to 3/5 passing flags a regression), then iterate
on the tool, optionally adding few-shot examples from the new data.

### Slide 14.13 — What you've learned: (deck "Lesson-6", slide 13)
**Evidence:** Narrated — "In this lesson, you've learned what to watch out for new queries," … "you used in development carry seamlessly over to production," … "by using CI/CD pipelines"
**Text on slide:** What you’ve learned: · 1. What to watch out for when your agent is in production · 2. How to use tooling and data from development through to production · 3. Future architectural considerations for CI/CD
**Visual description:** Standard content slide; a numbered list of three grey items.
**What it teaches:** Recaps the lesson: production risks, carrying development tooling and data
into production, and CI/CD architecture going forward.

---

## Lesson 15: Conclusion
Transcript: `## Lesson 15: Conclusion` in transcripts/evaluating-ai-agents-transcripts.md

No deck belongs to this lesson.
