# Slide descriptions: AI Agents in LangGraph
Source decks: ../repo/slides/Copy of Langchain_short course wide slides template.pdf (20 slides, wide 16:9, "Wide deck"), ../repo/slides/Copy of Langchain_short course 8in wide 9in high.pdf (53 slides, tall 8×9, "Tall deck")
Instructors: Harrison Chase (co-founder and CEO of LangChain) and Rotem Weiss (co-founder and CEO of Tavily), with Andrew Ng in the introduction

Rich text descriptions of the course slides, organized by lesson in the same order and with the
same lesson titles as the transcripts in `../transcripts/`. Each entry gives the deck and original
slide number, the evidence that ties the slide to a lesson (a verbatim transcript passage, or a
note that none exists), every word visible on the slide, a description of the visual, and what it
teaches.

## How to read this file

- **Lesson assignment rests on transcript content, not video frames.** No lesson videos were
  available, so no slide was matched to a video by frame sampling and there are no timestamps.
  Each slide was placed in the lesson whose narration describes what it shows. The decks were
  rendered to one PNG per slide and read alongside their extracted text layer. Both decks carry
  one title card per transcript lesson, so the lesson boundaries inside each deck are explicit.
- **Evidence field.** "Narrated" means a transcript passage clearly describes what the slide shows;
  the passage is quoted verbatim, including the transcript's own spelling errors, with the
  transcript's line breaks joined by single spaces. "Deck-only" means no transcript passage
  matches. "Title card" means the slide is a lesson title card whose subtitle is the transcript
  heading. "Narrated" is the best available proxy for "shown in the video", but it is a proxy: a
  narrated slide may have been on screen for a different span than the quote, or replaced by a
  notebook or the instructor. This course is mostly taught in notebooks; the slides are concept
  interludes and title cards, and Lesson 5 has no content slide at all.
- **Lesson numbering comes from the transcripts:** 1 Introduction, 2 Build an Agent from Scratch,
  3 LangGraph Components, 4 Agentic Search Tools, 5 Persistence and Streaming, 6 Human in the loop,
  7 Essay Writer, 8 LangChain Resources, 9 Conclusion. The decks carry no lesson numbers; the
  course notebooks are numbered `L1`–`L6` in `works/` and count one lower than the transcripts
  (see `../notebooks/from-repo/ai-agents-in-langgraph-context.md`). The mapping:

  | Transcript lesson | Notebook | Slides here |
  |---|---|---|
  | 1 Introduction | — | Wide 2, 4–7; Tall 2 |
  | 2 Build an Agent from Scratch | L1 | Wide 8; Tall 3–4 |
  | 3 LangGraph Components | L2 | Wide 9; Tall 5–13 |
  | 4 Agentic Search Tools | L3 | Wide 10; Tall 14–16 |
  | 5 Persistence and Streaming | L4 | Wide 11; Tall 17 (title cards only) |
  | 6 Human in the loop | L5 | Wide 12; Tall 18–33 |
  | 7 Essay Writer | L6 | Wide 13; Tall 34–36 |
  | 8 LangChain Resources | — | Wide 14; Tall 37–38, 40–41 |
  | 9 Conclusion | — | Wide 15–20; Tall 42–43, 45, 47–48 |
  | Backup (no lesson) | — | Tall 49–53 |

  Transcripts win wherever the decks disagree. The Wide deck's Topics slide (1.2) lists
  "LangChain Components" where the transcript lesson is "LangGraph Components", and lists six
  topics against the transcript's nine lessons (it omits the introduction, resources and
  conclusion).
- **Production-note and blank pages have no entry of their own.** Six pages are not content:
  Wide 1 "Meta-slide: The next section is the marketing teaser info", Wide 3 "Meta-slide: The
  next section is about the intro slide", Tall 1 the template's cover ("Short Course Template ·
  8 wide by 9 high"), and Tall 39, 44 and 46, which are blank frames (logos and wave only, no
  text layer). Tall 44 and 46 sit where the Wide deck has Supervisor (9.3) and Plan and Execute
  (9.5), so they read as placeholders for those two diagrams; that is a reading of the page
  order, not a fact.
- **The two decks overlap.** Every lesson title card exists in both decks (the Wide one first in
  each lesson section, then the Tall one). The Conclusion diagrams exist in both: the Wide deck
  holds clean drawings with source URLs, the Tall deck holds earlier versions, two of them
  screenshots of a YouTube video with the player controls and presenter visible (9.8) or the
  player bar (Tall 44's missing twin). The Wide deck is the finished version of those slides.
- **Backup slides (Tall 49–53) belong to no lesson.** They sit after a "Backup" divider and
  nothing in the transcripts describes them. They are listed at the end so every page is
  accounted for, with a note on what each appears to be.
- **Slide numbering** is `Lesson.Order` in deck order within the lesson, Wide-deck slides first.
  The deck and original slide number follow in parentheses so each entry can be traced back to
  the PDF.
- **Text on slide** is transcribed verbatim from the extracted text layer; text inside
  screenshots and diagrams (the ReAct paper header, the LangChain ecosystem diagram, the
  documentation screenshot, the hand-drawn flow diagrams) was read from the page images, because
  the text layer skips it. Items are separated by " · ". Code is reproduced as code. Typos on
  the slides are kept as printed (for example `call)tool`, `weights 50 lbs`, `Langchain`).
- **Animations cannot be known** from a PDF, so no entry claims a build order. The State Memory
  run (6.3–6.17) is fifteen consecutive slides that differ by one added element each; they read
  as stages of one build, and the entries say so as a reading of the drawings, not a fact. The
  same applies to the Break Down / Prompts / Tools / New in LangGraph run (3.3–3.6), which keeps
  one flow diagram and changes what is highlighted beside it.
- **Text-layer artefacts.** The small labels inside the flow diagram on 3.3–3.6 and 3.9–3.10
  ("what is the .. poodle", "System: you are a…", "action: call)tool", "Obs: 37") are
  transcribed once, on 3.3, and summarised after that.
- All 73 pages are accounted for: 62 lesson entries (6 in Lesson 1, 3 in Lesson 2, 10 in Lesson
  3, 4 in Lesson 4, 2 in Lesson 5, 17 in Lesson 6, 4 in Lesson 7, 5 in Lesson 8, 11 in Lesson 9),
  5 backup entries, 2 production notes, the template cover and 3 blank pages.
- Course-wide visual conventions: every content slide has the LangChain logo (a parrot-and-chain
  mark in dark green with the wordmark) top left and the DeepLearning.AI logo top right, and a
  coral-to-crimson wave along the bottom edge; the two Tavily slides (4.3, 4.4) carry the Tavily
  wordmark top left instead. Title cards have no header logos and no wave: the course title
  "AI Agents in LangGraph" in coral red, the lesson title in grey below it, a square watercolour
  illustration of a mechanical parrot that changes per lesson, and the LangChain and
  DeepLearning.AI logos near the bottom (Tavily's as well on the course and Agentic Search
  cards). Graph diagrams use one fixed vocabulary from 3.8 onward: a light-blue circle for the
  agent (LLM) node, an orange circle for the function (action) node, a pink diamond for a
  conditional edge labelled "action", a dark grey circle for the End node, and an orange
  down-arrow for the entry point.

---

## Lesson 1: Introduction
Transcript: `## Lesson 1: Introduction` in transcripts/ai-agents-in-langgraph-transcripts.md

Five Wide-deck slides and one Tall-deck slide: the course title card, a Topics list, the
instructors card, the three cyclic-graph papers Andrew and Harrison discuss, and the
acknowledgments. The narration is a three-way conversation in front of these.

### Slide 1.1 — Title card: AI Agents in LangGraph (Wide deck, slide 2)
**Evidence:** Narrated — "Welcome to AI Agents and LangGraph. Built in partnership with LangChain and Tivoli."
**Text on slide:** AI Agents in LangGraph
**Visual description:** Course title card: the course title in coral red, centred, with the
LangChain, Tavily and DeepLearning.AI logos in a row beneath. No header logos, no wave. Wide 1
before it is the production note "The next section is the marketing teaser info".
**What it teaches:** The course title and the three partners.

### Slide 1.2 — Topics (Wide deck, slide 4)
**Evidence:** Narrated — "In this course, you will start by building an agent from scratch with just an LLM and Python. Then, you'll learn about the components of LangGraph by rebuilding that same agent using the LangGraph components directly. Since search tools are such an important part of many agent applications, you will learn the capabilities of agentic search and how to use it. There are two additional capabilities that are helpful when building agents. First, is being able to receive human input. This allows you to guide an agent at critical points. The second is persistence. This is the ability to store the current state of information so that you can return to it later. This is great for both debugging agents and for productionalizing them. We will build a project using LangGraph, but you'll have to reach the last lesson to figure out what it is."
**Text on slide:** Topics · Build an Agent from Scratch · LangChain Components · Agentic Search Tools · Persistence · Human In the Loop · Project
**Visual description:** A plain bulleted list of six topics under the heading "Topics". Wide 3
before it is the production note "The next section is about the intro slide".
**What it teaches:** The course plan. Note the slide says "LangChain Components" where the lesson
is titled "LangGraph Components", and "Project" where the lesson is "Essay Writer"; the narration
keeps the project a surprise.

### Slide 1.3 — Instructors (Wide deck, slide 5)
**Evidence:** Narrated — "Taught by Harrison Chase, co-founder and CEO of LangChain, as well as Rotem Weiss who is the co-founder and CEO of Tavily."
**Text on slide:** AI Agents in LangGraph · Harrison Chase · Rotem Weiss
**Visual description:** The course title in coral red; below it the LangChain logo with
"Harrison Chase" under it and the Tavily wordmark with "Rotem Weiss" under it, side by side. No
header logos, no wave.
**What it teaches:** Who teaches the course and which company each instructor represents.

### Slide 1.4 — LangGraph supports Cyclic Graphs (Wide deck, slide 6)
**Evidence:** Narrated — "So, ReAct agents was an early paradigm for building agents, and ReAct stands for reasoning and action. Another example that we recently added support for is the example presented in the Self Refine paper, where it does the iterative refinement that you were talking about. And most recently, you can see the alpha coding example. Which creates a coding agent using flow engineering. And from all these diagrams you can see that these agents and their behavior is defined by a cyclical graph. And to support directly building agents like this, LangChain has extended to support LangGraph."
**Text on slide:** LangGraph supports Cyclic Graphs · https://arxiv.org/pdf/2210.03629.pdf · https://arxiv.org/pdf/2303.17651.pdf · https://arxiv.org/pdf/2401.08500.pdf · (in the figures) ReAct (Reason + Act) · Reasoning Traces · LM · Env · Actions · Observations · ReAct: Synergizing Reasoning and Acting in Language Models · Feedback · Model M · Refine · Input · Self-Refine: Iterative Refinement with Self-Feedback · (a) The proposed AlphaCodium flow. · Code Generation with AlphaCodium: From Prompt Engineering to Flow Engineering
**Visual description:** Three paper figures side by side, each with its title and arXiv URL
beneath. Left: the ReAct loop, an LM box and an Env box joined by two curved arrows labelled
Actions and Observations, with a Reasoning Traces loop on the LM. Middle: the Self-Refine
diagram, Model M in the centre with Feedback and Refine arrows looping back into it. Right: the
AlphaCodium flow, a grey Pre-processing block of six boxes feeding an orange Code iterations
block with dotted loop arrows.
**What it teaches:** Three published agent designs are all cycles, which is the motivation for a
graph framework that allows cycles. The same three figures reappear on 3.7.

### Slide 1.5 — Acknowledgments (Wide deck, slide 7)
**Evidence:** Narrated — "Many people have worked to create this course from LangChain. I'd like to thank Lance Martin and Nuno Campos. From Tavily, Assaf Elovic And from DeepLearning.AI. Geoff Ladwig."
**Text on slide:** Acknowledgments · Lance Martin · LangChain · Nuno Campos · LangChain · Assaf Elovic · Tavily · Geoff Ladwig · DeepLearning.AI
**Visual description:** Four circular portrait photos in a 2×2 grid, each with a name and
organisation beneath. The header carries LangChain, Tavily and DeepLearning.AI logos.
**What it teaches:** Who contributed to the course.

### Slide 1.6 — Title card: AI Agents in LangGraph, instructors (Tall deck, slide 2)
**Evidence:** Title card — twin of 1.3 in the Tall deck.
**Text on slide:** AI Agents in LangGraph · Harrison Chase · Rotem Weiss
**Visual description:** The course title in coral red with both instructor names in grey beneath,
and the LangChain, Tavily and DeepLearning.AI logos in a row near the bottom. No header logos,
no wave. Tall 1 before it is the template cover.
**What it teaches:** The course title and instructors; same content as 1.3 in the tall format.

---

## Lesson 2: Build an Agent from Scratch
Transcript: `## Lesson 2: Build an Agent from Scratch` in transcripts/ai-agents-in-langgraph-transcripts.md

Two title cards and one concept slide. The rest of the lesson is the notebook (`works/L1`).

### Slide 2.1 — Title card: Build an agent from scratch (Wide deck, slide 8)
**Evidence:** Title card — "In this lesson, we'll build an agent from scratch."
**Text on slide:** AI Agents in LangGraph · Build an agent from scratch
**Visual description:** Title card: a watercolour of a blue mechanical parrot with visible gears
in its chest, perched on a branch, at left; course title and lesson title to its right.
**What it teaches:** Lesson title. Note the lower-case "agent" here against "Agent" on the Tall
twin (2.2).

### Slide 2.2 — Title card: Build an Agent from Scratch (Tall deck, slide 3)
**Evidence:** Title card — twin of 2.1.
**Text on slide:** AI Agents in LangGraph · Build an Agent from Scratch
**Visual description:** Same parrot illustration centred under the titles, LangChain and
DeepLearning.AI logos at the bottom.
**What it teaches:** Lesson title.

### Slide 2.3 — Let's build an agent from scratch (Tall deck, slide 4)
**Evidence:** Narrated — "The agent we're going to build from scratch is based on the ReAct pattern. ReAct stands for reasoning plus acting. So in this pattern, an LLM first thinks about what to do and then decides an action to take. That action is then executed in an environment and an observation is returned. With that observation, The LLM then repeats."
**Text on slide:** Let's build an agent from scratch · thought · (in the figure) Reasoning Traces · LM · Env · Actions · Observations · ReAct (Reason + Act) · Published as a conference paper at ICLR 2023 · ReAct: Synergizing Reasoning and Acting in Language Models · Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao · Department of Computer Science, Princeton University · Google Research, Brain team · https://arxiv.org/pdf/2210.03629.pdf
**Visual description:** The ReAct loop figure from 1.4, with the word "thought" added in green
above the Reasoning Traces loop, over a screenshot of the paper's title block (title, authors,
affiliations, email addresses) and the arXiv URL.
**What it teaches:** The ReAct pattern the hand-built agent follows: the LM reasons ("thought"),
acts on the environment, observes, and loops. The green "thought" ties the paper's "Reasoning
Traces" to the prompt keyword used in the notebook.

---

## Lesson 3: LangGraph Components
Transcript: `## Lesson 3: LangGraph Components` in transcripts/ai-agents-in-langgraph-transcripts.md

Two title cards and eight concept slides, the longest slide run of any lesson. They retrace the
Lesson 2 agent as a flow diagram, name the LangChain pieces (prompts, tools), introduce LangGraph
(cycles, persistence, human in the loop), define nodes, edges, conditional edges and the agent
state, and end with the concrete node names the notebook uses.

### Slide 3.1 — Title card: LangGraph Components (Wide deck, slide 9)
**Evidence:** Title card — "Now let's implement the agent using the LangGraph. And along the way, introduce some of its components and features."
**Text on slide:** AI Agents in LangGraph · LangGraph Components
**Visual description:** Title card: a watercolour of a mechanical parrot drawing a node-and-edge
graph on a whiteboard in a library, at left.
**What it teaches:** Lesson title.

### Slide 3.2 — Title card: LangGraph Components (Tall deck, slide 5)
**Evidence:** Title card — twin of 3.1.
**Text on slide:** AI Agents in LangGraph · LangGraph Components
**Visual description:** Same illustration centred, logos at the bottom.
**What it teaches:** Lesson title.

### Slide 3.3 — Break Down (Tall deck, slide 6)
**Evidence:** Narrated — "All right, so let's break down what exactly we did in the last lesson. We had this user message that came in. We then had the system prompt. And this was this very long one. We then called an LLM along with that. This output something like what's right there, a thought and an action. Based on that, we then made a decision. We would either return or we would call a tool, and we put this all in a big loop. This query function. And we had these two tools that we would call "calculate an average dog weight." And if we called the tool we would get back an observation. And then we'd loop back in, to the prompt and would put that observation as a new message."
**Text on slide:** Break Down · User · Prompt · LLM · action · return · tool · (diagram labels) what is the .. poodle · System: you are a… · what is the .. poodle · Obs: 37 · action: call)tool · Obs: 37 · (system prompt excerpt) “”” System: You run in a loop of Thought, Action, PAUSE, Observation. … Your available actions are: calculate: e.g. calculate: 4 * 7 / 3 … Example session: … User: … weight of collie… · (LLM output) 'Thought: To find the combined weight of a Border Collie and a Scottish Terrier, I need to first find the average weight of each breed and then add those weights together. Action: average_dog_weight: Border Collie\n PAUSE' · Observation: a Border Collies average weight is 37 lbs
Code on slide:
```python
def query(question, max_turns=5):
    i = 0
    bot = Agent(prompt)
    next_prompt = question
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print(result)
        actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            observation = known_actions[action](action_input)
            print("Observation:", observation)
            next_prompt = "Observation: {}".format(observation)
        else:
            return
```
```python
def calculate(what):
    return eval(what)

def average_dog_weight(name):
    if name in "Scottish Terrier":
        return("Scottish Terriers average 20 lbs")
    elif name in "Border Collie":
        return("a Border Collies average weight is 37 lbs")
    elif name in "Toy Poodle":
        return("a toy poodles average weight is 7 lbs")
    else:
        return("An average dog weights 50 lbs")
```
**Visual description:** A dense slide. Down the left, a vertical flow diagram labelled User →
Prompt → LLM → action: a blue user-message box, a stacked prompt (green system message, blue user
message, blue "Obs: 37"), a blue LLM circle, an orange "action: call tool" box, a pink diamond
labelled "action" that branches to "return" or to an orange tool circle, whose "Obs: 37" output
loops back up into the prompt stack. Right column: the system-prompt excerpt with "System:" and
"User:" in green and blue, the LLM's Thought/Action/PAUSE output with the keywords in orange, and
the Observation line in blue. Bottom: the `query` loop in a code block on the left and the two
tool functions in a boxed code block on the right.
**What it teaches:** Everything the hand-built agent did, drawn as one loop: prompt assembly, LLM
call, parse for an action, call the tool, feed the observation back. This is the structure
LangGraph will represent. The query loop and tools are the Lesson 2 notebook code, reproduced.

### Slide 3.4 — LangChain: Prompts (Tall deck, slide 7)
**Evidence:** Narrated — "So let's break this down into LangChain components. First, let's talk about prompts. So prompt templates allow reusable prompts. And what this basically means is that we can create something like this, right here, a little string with some formatted variables that we can replace. … If you want to see a bunch of examples of these prompt templates, you can actually see them in the LangChain hub. So here is one that's very similar to the agent prompt that we just used."
**Text on slide:** LangChain: Prompts · Prompt templates allow reusable prompts · There are also prompts for agents available in the hub: · https://smith.langchain.com/hub/hwchase17/react · (diagram labels as on 3.3)
Code on slide:
```python
from langchain.prompts import PromptTemplate
prompt_template = PromptTemplate.from_template(
    "Tell me a {adjective} joke about {content}."
```
```python
prompt = hub.pull("hwchase17/react")
```
**Visual description:** The same flow diagram from 3.3 at left, smaller. At right, the heading
"Prompt templates allow reusable prompts" over a three-line PromptTemplate example with
`{adjective}` and `{content}` highlighted in blue, then "There are also prompts for agents
available in the hub:" over `hub.pull("hwchase17/react")` and the hub URL in green.
**What it teaches:** The Prompt box of the loop maps to a LangChain PromptTemplate, and the
ReAct system prompt from Lesson 2 has a published equivalent in the LangChain hub.

### Slide 3.5 — LangChain: Tools (Tall deck, slide 8)
**Evidence:** Narrated — "The next component in LangChain that we have is tools. So here's a Tavily tool. And this is the search that we will be using from here on out. You can see that we import it from the LangChain community package which contains hundreds of other tools."
**Text on slide:** LangChain: Tools · # get a tool from the library · (diagram labels as on 3.3)
Code on slide:
```python
# get a tool from the library
from langchain_community.tools.tavily_search import \
TavilySearchResults
tool = TavilySearchResults(max_results=2)

self.tools = {t.name: t for t in tools}
self.model = model.bind_tools([tool])
```
**Visual description:** The same flow diagram at left. At right, a boxed code block: the Tavily
import, `TavilySearchResults(max_results=2)`, and two lines that register the tools on the agent
(`self.tools` dictionary, `model.bind_tools`).
**What it teaches:** The tool box of the loop maps to a LangChain tool; from here on the tool is
Tavily search, not the mocked dog-weight functions. The two `self.` lines preview how the
notebook's Agent class keeps tools and binds them to the model.

### Slide 3.6 — New in LangGraph (Tall deck, slide 9)
**Evidence:** Narrated — "Maybe the biggest part of this application, the most code that we wrote, was this function that would loop. And that's represented by all these arrows, here. And that's one way to think about LangGraph. LangGraph helps you describe and orchestrate that control flow. Specifically, it allows you to create cyclic graphs, which is exactly what we have here. It also comes with built-in persistence. And this is really nice for having multiple conversations at the same time, or remembering previous iterations and actions. This persistence also enables really cool human in the loop features."
**Text on slide:** New in LangGraph · Cyclic Graphs · Persistence · Human-in-the-loop · (diagram labels as on 3.3)
**Visual description:** The same flow diagram at left, but every arrow is now drawn in red,
including the loop from the tool's observation back up to the prompt. At right, three bullets.
**What it teaches:** The arrows, which were the loop code in Lesson 2, are what LangGraph
describes. Its three headline features are cycles, persistence and human in the loop; the last
two are Lessons 5 and 6.

### Slide 3.7 — Graphs: papers and bullets (Tall deck, slide 10)
**Evidence:** Narrated — "If you look at these diagrams here, and these are all diagrams of agents from academic papers, these are all represented as graphs. And that realization was what led us to create LangGraph, an extension of LangChain specifically aimed at agent and multi-agent flows. Crucially, it allows for really controlled flows. So in these diagrams there's really specific arrows leading from one box or state to the next. We've seen that this controllability is crucial for creating agents that can perform well."
**Text on slide:** Graphs · LangGraph is an extension of LangChain that supports graphs. · Single and Multi-agent flows are described and represented as graphs. · Allows for extremely controlled “flows” · Built-in persistence allows for human-in-the-loop workflows · (figure labels) ReAct (Reason + Act) · Agent · Self-reflection (LM) · Evaluator (LM) · Experience (long-term memory) · Trajectory (short-term memory) · Actor (LM) · Environment · Obs / Reward · Action · Pre-processing · Code iterations · (a) The proposed AlphaCodium flow.
**Visual description:** Three paper figures in a row across the top (the ReAct loop, a Reflexion
agent block diagram with Actor, Evaluator and Self-reflection LMs around short- and long-term
memory, and the AlphaCodium flow), then four bullets. The middle figure differs from 1.4's:
here it is the Reflexion architecture, there it was Self-Refine.
**What it teaches:** Published agents are graphs; LangGraph exists to express them with explicit,
controlled flow, and its persistence is what makes human-in-the-loop possible.

### Slide 3.8 — Graphs: nodes, edges, conditional edges (Tall deck, slide 11)
**Evidence:** Narrated — "Three of the core concepts of LangGraph are nodes, edges, and conditional edges. Nodes are agents or functions. Edges connect these nodes, and then conditional edges are used when you need to make decisions about which node you should go to next. So let's take a look at an example of a LangGraph you can create that is equivalent to the function that we wrote in the lesson before. We can have an agent node. This is the LLM. We can then have a conditional edge which takes the result of that LLM call and decides what to do next. One of those edges can be an action edge which calls a function node, and that automatically loops back to the agent node. There's an entry point, which is where you start, and then there's the end node, which is the other action available to take after the agent."
**Text on slide:** Graphs · Nodes: Agents or functions · Edges: connect nodes · Conditional edges: decisions · entrypoint : starting node · agent node · conditional edge · End node · action · edge · function node
**Visual description:** A legend at the top: a blue and an orange circle for Nodes, a plain arrow
for Edges, an arrow into a pink diamond that forks for Conditional edges. Below, the canonical
small graph used for the rest of the course: an orange entry arrow into a blue agent node, down
to a pink diamond labelled "action", which forks left to a dark End node and right to an orange
function node, whose edge loops back up to the agent node. Each element is labelled in grey.
**What it teaches:** The three LangGraph primitives and the exact shape of the Lesson 2 agent as
a graph: agent node, conditional edge, action node looping back, entry point, end.

### Slide 3.9 — Data/State (Tall deck, slide 12)
**Evidence:** Narrated — "One of the most important things to understand when working with LangGraph is the state that is tracked over time. This is often called the agent state. This is accessible at all parts of the graph at each node in each edge. It is local to the graph and it can be stored in persistence layer, meaning that you can resume with that state at any point in time, later on. Looking at two examples, we first have a simple state where we just have this list of messages. … Let's take a look at a more complex state. Here we have input, chat history, agent outcome, and intermediate steps."
**Text on slide:** Data/State · Agent State · Agent State is accessible to all parts of the graph · It is local to the graph · Can be stored in a persistence layer · Simple · Complex · (diagram labels) System: you are a… · what is the .. poodle · Obs: 37 · action
Code on slide:
```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
```
```python
class AgentState(TypedDict):
    input: str
    chat_history: list[BaseMessage]
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
```
**Visual description:** A large grey rounded box encloses the small graph from 3.8 together with
a stacked message box labelled "Agent State", showing the state lives inside the graph. Three
bullets beneath. Then "Simple" over the one-field AgentState and "Complex" over the four-field
AgentState, both as syntax-highlighted code.
**What it teaches:** The agent state is a typed dictionary visible everywhere in the graph and
checkpointable. `Annotated[..., operator.add]` makes a field accumulate instead of overwrite; the
transcript spells out that three of the complex fields overwrite and `intermediate_steps` adds.

### Slide 3.10 — CODE (Tall deck, slide 13)
**Evidence:** Narrated — "Getting really specific about the previous agent that we created and how that would map to a LangGraph object. We can see that we will have one node. We'll call this call OpenAI. And this will call the LLM. We'll then have a conditional edge which will check for the existence of an action to take. And so we'll call this 'exists action'. And then we'll have another node which actually executes that action. We'll call that 'take action'. And the state that will track is pretty simple. It's just this list of messages to which we add over time."
**Text on slide:** CODE · Agent State · END · llm: call_openai · c_edge: exists_action · action:take_action · State · (diagram labels) what is the .. poodle · Obs: 37
Code on slide:
```python
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
```
**Visual description:** The small graph from 3.8 with the End node now labelled "END" in red, and
to its right three mappings in red-and-black: `llm: call_openai`, `c_edge: exists_action`,
`action:take_action`. The Agent State box at left holds only the user message and "Obs: 37".
Below, "State" over the one-field AgentState using `list[AnyMessage]`.
**What it teaches:** The names the notebook uses: node `llm` is the method `call_openai`, the
conditional edge is `exists_action`, node `action` is `take_action`, and the state is a list of
`AnyMessage` with `operator.add`. This is the bridge from diagram to the Lesson 3 notebook code.

---

## Lesson 4: Agentic Search Tools
Transcript: `## Lesson 4: Agentic Search Tools` in transcripts/ai-agents-in-langgraph-transcripts.md

Two title cards and two hand-drawn Tavily diagrams, taught by Rotem Weiss. These two content
slides carry the Tavily wordmark instead of LangChain's.

### Slide 4.1 — Title card: Agentic Search Tools (Wide deck, slide 10)
**Evidence:** Title card — "A frequently used tool in agents is search. This lesson is going to dive into how agentic search is different from standard search and how to use it."
**Text on slide:** AI Agents in LangGraph · Agentic Search Tools
**Visual description:** Title card: a watercolour of a mechanical parrot with a magnifying glass
among gears, at left; LangChain, Tavily and DeepLearning.AI logos.
**What it teaches:** Lesson title.

### Slide 4.2 — Title card: Agentic Search Tools (Tall deck, slide 14)
**Evidence:** Title card — twin of 4.1.
**Text on slide:** AI Agents in LangGraph · Agentic Search Tools
**Visual description:** Same illustration centred, three logos at the bottom.
**What it teaches:** Lesson title.

### Slide 4.3 — Why Search Tool (Tall deck, slide 15)
**Evidence:** Narrated — "Looking at the slide, we can see the prompt is received by the agent, which then decides to call the search tool. Then the information found is returned to the agent."
**Text on slide:** Why Search Tool · (diagram, hand-lettered) Prompt · Agent · Search Query · Search Tool · RAG Context · Agent
**Visual description:** A hand-drawn flow: a Prompt box feeds an Agent box; the Agent sends a
"Search Query" down to a green Search Tool box; "RAG Context" comes back up diagonally into a
second Agent box, which the first Agent also points to directly. Tavily wordmark top left.
**What it teaches:** Where a search tool sits in an agent loop: the agent decides to search, and
what comes back is context for the agent's next step, not links for a human. The transcript
precedes this with the motivation: static weights can't answer about last night's game, and
sources reduce hallucination.

### Slide 4.4 — Inside a Search Tool (Tall deck, slide 16)
**Evidence:** Narrated — "This is an example of a very basic search tool implementation. Let's go over it step by step. If the agent decides it will send the query to the search tool, the first step would work on understanding the question and divide it to sub-questions if needed. This is an important step because it can handle complex queries. Then, for each subquery, the search tool will have to find the best source. Choosing from multiple integrations. … The search tool would then have to extract only the relevant information to the subquery. A basic implementation of this can be achieved through a process of chunking the source, and run a quick vector search to retrieve the top-K chunks. After retrieving the data from its source, the search tool would then score the results and filter out the less relevant information."
**Text on slide:** Inside a Search Tool · (diagram, hand-lettered) Query · Sub-Query · Retrieve · Source · Source · Source · Source · Source · Scoring & Filtering · Return Top-K Docs · Chunked Source · Sub-Query · Top-K Chunks
**Visual description:** A hand-drawn pipeline: Query → a stack of Sub-Query boxes → Retrieve,
which fans out to five Source ovals → Scoring & Filtering → Return Top-K Docs. Below, a zoomed
inset of one Source: a Sub-Query against a Chunked Source (green and white stripes) yields Top-K
Chunks (green). Tavily wordmark top left.
**What it teaches:** The four stages of an agentic search tool: split the query into
sub-queries, pick a source per sub-query, extract only relevant chunks by vector search, then
score and filter before returning top-K documents.

---

## Lesson 5: Persistence and Streaming
Transcript: `## Lesson 5: Persistence and Streaming` in transcripts/ai-agents-in-langgraph-transcripts.md

Title cards only. The whole lesson (checkpointer, SqliteSaver, thread config, `stream`,
`astream_events`) is taught in the notebook (`works/L4`); no slide describes any of it. The
State Memory drawings that explain what the checkpointer stores are in Lesson 6 (6.3–6.17).

### Slide 5.1 — Title card: Persistence and Streaming (Wide deck, slide 11)
**Evidence:** Title card — "When building agents, they're often working on longer running tasks. For these types of tasks, there are two really important concepts. Persistence and streaming."
**Text on slide:** AI Agents in LangGraph · Persistence and Streaming
**Visual description:** Title card: a watercolour of a stone-grey mechanical parrot statue on a
mossy plinth, at left.
**What it teaches:** Lesson title.

### Slide 5.2 — Title card: Persistence and Streaming (Tall deck, slide 17)
**Evidence:** Title card — twin of 5.1.
**Text on slide:** AI Agents in LangGraph · Persistence and Streaming
**Visual description:** Same statue illustration centred.
**What it teaches:** Lesson title.

---

## Lesson 6: Human in the loop
Transcript: `## Lesson 6: Human in the loop` in transcripts/ai-agents-in-langgraph-transcripts.md

Two title cards and a fifteen-slide "State Memory" run. The run is narrated in one block in the
middle of the lesson ("Before we get to the next section, let's talk a little bit more about
state memory"), after the interrupt-before demo and before the modify-state, time-travel and
add-message demos. The transcript calls the snapshot identifier "thread TS"; the slides print
`thread_ts`.

### Slide 6.1 — Title card: Human in the loop (Wide deck, slide 12)
**Evidence:** Title card — "There are many occasions when you would like to put a human in the loop to keep tabs on what an agent is doing. This is pretty easy to do with LangGraph."
**Text on slide:** AI Agents in LangGraph · Human in the loop
**Visual description:** Title card: a watercolour of a pirate looking through a ship's porthole at
a small mechanical parrot, at left.
**What it teaches:** Lesson title.

### Slide 6.2 — Title card: Human in the loop (Tall deck, slide 18)
**Evidence:** Title card — twin of 6.1.
**Text on slide:** AI Agents in LangGraph · Human in the loop
**Visual description:** Same pirate illustration centred.
**What it teaches:** Lesson title.

### Slide 6.3 — State Memory: state 0 (Tall deck, slide 19)
**Evidence:** Narrated — "As a graph is executing, a snapshot of each state is stored in memory."
**Text on slide:** State Memory · Memory · state 0 · 0 · action
**Visual description:** The small graph from 3.8 at left with a blue "0" beside the agent node and
the entry arrow. At right, a column headed "Memory" holding one blue box, "state 0". The graph
and the Memory column stay fixed through 6.17; only the step counter, the boxes and the
annotations below change.
**What it teaches:** Before the first node runs there is already a snapshot, state 0.

### Slide 6.4 — State Memory: state 1 (Tall deck, slide 20)
**Evidence:** Narrated — same passage as 6.3.
**Text on slide:** State Memory · Memory · state 1 · state 0 · 1 · action
**Visual description:** The counter "1" has moved down beside the conditional-edge diamond.
Memory now holds "state 1" above "state 0".
**What it teaches:** Each step pushes a new snapshot on top; earlier ones are kept.

### Slide 6.5 — State Memory: state 2 (Tall deck, slide 21)
**Evidence:** Narrated — same passage as 6.3.
**Text on slide:** State Memory · Memory · state 2 · state 1 · 2 · state 0 · action
**Visual description:** Counter "2"; three boxes in Memory.
**What it teaches:** Same as 6.4, one step further.

### Slide 6.6 — State Memory: state 3 (Tall deck, slide 22)
**Evidence:** Narrated — same passage as 6.3.
**Text on slide:** State Memory · Memory · state 3 · state 2 · 3 · state 1 · state 0 · action
**Visual description:** Counter "3" back beside the agent node (the loop has come round); four
boxes in Memory, state 3 on top. This four-box column is the base for every following slide.
**What it teaches:** After one full loop there are four snapshots in memory.

### Slide 6.7 — State Memory: StateSnapshot contents (Tall deck, slide 23)
**Evidence:** Narrated — "What's in that snapshot? Well there's the agent state which you've already defined. And then there's some other useful things."
**Text on slide:** State Memory · Memory · state 3 · state 2 · 3 · state 1 · state 0 · { AgentState, useful_things} · StateSnapshot: · action
**Visual description:** As 6.6, plus an arrow from "state 0" down to a line "StateSnapshot:
{ AgentState, useful_things}" in teal and grey.
**What it teaches:** A snapshot holds the AgentState and extra bookkeeping.

### Slide 6.8 — State Memory: thread and thread_ts (Tall deck, slide 24)
**Evidence:** Narrated — "For example, there's a thread and a unique identifier for each of the snapshots. That's the thread TS right there. You can use that to access the snapshots."
**Text on slide:** State Memory · Memory · state 3 · state 2 · 3 · state 1 · state 0 · { AgentState, useful_things} · { .., thread, thread_ts..} · StateSnapshot: · config={'configurable': {'thread_id': '1', 'thread_ts': '1ef17b36-ed06-6185-8001-15cf75dea535'}} · action
**Visual description:** As 6.7, with "useful_things" expanded by an arrow into "{ .., thread,
thread_ts..}", and that expanded by two arrows into a literal config dictionary with a
`thread_id` of `'1'` and a long `thread_ts` UUID.
**What it teaches:** The "useful things" include the thread id and a per-snapshot unique id,
`thread_ts`, and both live in a `config['configurable']` dictionary.

### Slide 6.9 — State Memory: get_state(thread) (Tall deck, slide 25)
**Evidence:** Narrated — "There's some commands to access memory. There's get state which you've already seen. If you provide the thread without the unique identifier and just return that thread ID, it will return the current state."
**Text on slide:** State Memory · Memory · state 3 · state 2 · 3 · state 1 · state 0 · g.get_state(thread) · state 3 · Returns ‘current state’ · config={'configurable': {'thread_id': '1'}} · action
**Visual description:** As 6.6, with a bracket from the top box "state 3" out to a lone "state 3"
box at lower right, beside `g.get_state(thread)`; a config with only `thread_id` is drawn above
the call with an arrow into it; "Returns 'current state'" beneath.
**What it teaches:** `get_state` with a thread id alone returns the latest snapshot.

### Slide 6.10 — State Memory: get_state_history(thread) (Tall deck, slide 26)
**Evidence:** Narrated — "There's also get state history, which returns an iterator over all of the state snapshots. You can use the iterator to get access to all of the unique identifiers for each of the states."
**Text on slide:** State Memory · Memory · state 3 · state 2 · 3 · state 1 · state 0 · g.get_state_history(thread) · state 3 · Returns iterator over all StateSnapshots · action
**Visual description:** As 6.9, but brackets from all four Memory boxes converge on a stacked
pile of "state 3" boxes beside `g.get_state_history(thread)`.
**What it teaches:** `get_state_history` yields every snapshot, which is how you find the
`thread_ts` of an earlier state.

### Slide 6.11 — State Memory: invoke with thread_ts, Time Travel (Tall deck, slide 27)
**Evidence:** Narrated — "Given the thread identifier, or rather that thread TS the unique identifier, you could, for example, access that first state, state one, and use that in an invoke command. That will use state one as the current state or the starting point for the rest of the graph. This is effectively time travel."
**Text on slide:** State Memory · Memory · state 3 · state 2 · 1 · state 1 · state 0 · g.invoke(None,{ .., thread, thread_ts..}) · state 1 · runs with state 1 as starting point · Time Travel · g.stream(None,{ .., thread, thread_ts..}) · action
**Visual description:** As 6.6, but the counter beside the agent node is "1" and the bracket runs
from "state 1" to a "state 1" box beside two calls, `g.invoke(None, {.., thread, thread_ts..})`
and `g.stream(...)`; "runs with state 1 as starting point" and, in italics, "Time Travel" below.
**What it teaches:** Passing `None` as input with a config that names a `thread_ts` resumes the
graph from that past snapshot.

### Slide 6.12 — State Memory: invoke without thread_ts (Tall deck, slide 28)
**Evidence:** Narrated — "Conversely, without that thread TS, if you just pass in the thread ID, it will use the current state of the thread as the starting point."
**Text on slide:** State Memory · Memory · state 3 · state 2 · 1 · state 1 · state 0 · g.invoke(None,{ .., thread}) · state 3 · Uses current state as starting point · g.stream(None,{ .., thread}) · without thread_ts · action
**Visual description:** As 6.11 but the bracket runs from "state 3", the label "without thread_ts"
points at the config, and the caption reads "Uses current state as starting point". The step
counter still shows "1", which looks like a leftover from 6.11.
**What it teaches:** The same `None`-input call without a `thread_ts` continues from the latest
snapshot; this is what the interrupt-and-continue demo does.

### Slide 6.13 — State Memory: get_state with thread_ts (Tall deck, slide 29)
**Evidence:** Narrated — "You can also use that unique identifier to access a particular state."
**Text on slide:** State Memory · Memory · state 3 · state 2 · 3 · state 1 · state 0 · g.get_state({thread, thread_ts}) · state 1 · Returns ‘thread_ts state-snapshot’ · action
**Visual description:** As 6.6, bracket from "state 1" to a "state 1" box beside
`g.get_state({thread, thread_ts})`, with `thread_ts` in blue; caption "Returns 'thread_ts
state-snapshot'".
**What it teaches:** `get_state` with a `thread_ts` returns that specific past snapshot.

### Slide 6.14 — State Memory: modify it (Tall deck, slide 30)
**Evidence:** Narrated — "You can then modify that state,"
**Text on slide:** State Memory · Memory · state 3 · state 2 · 3 · state 1 · state 0 · g.get_state({thread, thread_ts}) · state 1 · state 1m · modify it · action
**Visual description:** As 6.13, plus an arrow from the fetched "state 1" box down to a purple
"state 1m" box labelled "modify it".
**What it teaches:** A fetched snapshot can be edited locally (the "m" suffix marks the modified
copy); nothing in memory has changed yet.

### Slide 6.15 — State Memory: update_state (Tall deck, slide 31)
**Evidence:** Narrated — "and then you can use update state, to update the state and store it back into memory in the location of the current state."
**Text on slide:** State Memory · Memory · state 4 · state 3 · 3 · state 2 · state 1 · state 1 · state 1m · modify it · g.update_state(thread, state1m.values) · state 0 · g.get_state({thread, thread_ts}) · action
**Visual description:** As 6.14, plus `g.update_state(thread, state1m.values)` under the modified
box, and a line from "state 1m" round to the top of the Memory column, where a new purple
"state 4" box now sits above state 3.
**What it teaches:** `update_state` does not overwrite state 1; it pushes the modified values as
a new snapshot on top of the thread.

### Slide 6.16 — State Memory: run it (Tall deck, slide 32)
**Evidence:** Narrated — "From there, if you run Stream or Invoke, it'll use the new state, the modified state as a starting point."
**Text on slide:** State Memory · Memory · state 4 · state 3 · 3 · state 2 · state 1 · state 1 · state 1m · modify it · state 0 · g.get_state({thread, thread_ts}) · g.stream(None, thread) · run it · g.update_state(thread, state1m.values) · action
**Visual description:** As 6.15, plus a final line "run it  g.stream(None, thread)" in teal and
blue beneath `update_state`.
**What it teaches:** After `update_state`, a plain `stream(None, thread)` continues from the
modified state because it is now the current one.

### Slide 6.17 — State Memory: stream the modified state directly (Tall deck, slide 33)
**Evidence:** Deck-only. The narration describes `update_state` followed by stream (6.15–6.16);
nothing describes passing the modified state as the stream input. The notebook also uses the
`update_state` route.
**Text on slide:** State Memory · Memory · state 4 · state 3 · 3 · state 2 · state 1 · g.get_state(thread, thread_ts) · state 1 · state 1m · modify it · g.stream(state 1m, thread) · state 0 · action
**Visual description:** As 6.15 without the `update_state` line: the modified "state 1m" box
feeds `g.stream(state 1m, thread)` and the line from it still lands on the purple "state 4" at
the top of Memory. `get_state` is written here with positional arguments, `(thread, thread_ts)`,
unlike the dictionary form on 6.13–6.16.
**What it teaches:** An alternative drawing of the same outcome: streaming with the modified
state as input also produces a new state 4. Not narrated; treat as a variant of 6.16.

---

## Lesson 7: Essay Writer
Transcript: `## Lesson 7: Essay Writer` in transcripts/ai-agents-in-langgraph-transcripts.md

Two title cards, the essay-writer graph with its prompts, and the plan the agent produced. The
GUI walkthrough at the end of the lesson has no slides; it was shown on screen.

### Slide 7.1 — Title card: Essay Writer (Wide deck, slide 13)
**Evidence:** Title card — "In this lesson, you'll build a project with a bit more scope. We'll build a compact version of an AI researcher, in this case, an essay writer."
**Text on slide:** AI Agents in LangGraph · Essay Writer
**Visual description:** Title card: a watercolour of four mechanical parrots in hats and scarves
around a typewriter in a study, at left.
**What it teaches:** Lesson title. The "Project" of 1.2 is revealed.

### Slide 7.2 — Title card: Essay Writer (Tall deck, slide 34)
**Evidence:** Title card — twin of 7.1.
**Text on slide:** AI Agents in LangGraph · Essay Writer
**Visual description:** Same four-parrot illustration centred.
**What it teaches:** Lesson title.

### Slide 7.3 — Essay Writer graph and prompts (Tall deck, slide 35)
**Evidence:** Narrated — "So first we're going to generate a plan for the essay. This is going to happen once upfront. Then based on that plan we're going to do some research. This involves calling Tavily and getting back some documents. From there we're going to go into generate, and then generate. We're going to follow the plan using the documents that we researched. And we're going to write the essay. From there, we're either going to finish or we're going to continue. If we continue, we're going to go into a reflect node where we're going to generate a critique of the current essay. Then based on that critique, we're going to do another research step with Tavily, and get another set of documents. We're going to append those to the existing set of documents and go all the way back to the generate step, where we're going to once again try to write this essay. And we're going to continue this until some criteria is met and we exit."
**Text on slide:** Essay Writer · plan · research_plan · generate · continue · reflect · research_critique · You are an expert writer tasked with writing a high level outline of an essay. Write such an outline for the user provided topic. Give an outline of the essay along with any relevant notes or instructions for the sections. · You are a researcher charged with providing information that can be used when writing the following essay. Generate a list of search queries that will gather any relevant information. Only generate 3 queries max. · You are an essay assistant tasked with writing excellent 5-paragraph essays.Generate … If the user provides critique, respond with a revised version of your previous attempts. Utilize information:
**Visual description:** At left, a vertical graph in the course vocabulary: entry arrow → blue
`plan` → orange `research_plan` → blue `generate` → pink diamond, which goes left to the dark
End node or right along an edge labelled "continue" to blue `reflect` → blue
`research_critique`, whose edge loops back up into `generate`. At right, three prompt excerpts
placed beside the nodes they belong to, with the key phrases in bold: "high level outline",
"search queries that will gather any relevant information", "writing excellent 5-paragraph
essays", "user provides critique, respond with a revised version".
**What it teaches:** The whole project in one picture: five nodes, one conditional edge, one
cycle, and which prompt drives each LLM node. The prompt text matches the notebook's
`PLAN_PROMPT`, `RESEARCH_PLAN_PROMPT` and `WRITER_PROMPT` (the GUI in `helper.py` uses
3-paragraph variants instead).

### Slide 7.4 — Plan (Tall deck, slide 36)
**Evidence:** Narrated — "Let's ask it what is the difference between LangChain and LangSmith. … So we can see that it generates a plan. First."
**Text on slide:** Plan: · I. Introduction · A. Brief overview of Langchain and Langsmith · B. Thesis statement: Exploring the key differences between Langchain and Langsmith · II. Langchain · A. Definition and purpose · B. Technology and applications · C. Key features and benefits · III. Langsmith · A. Definition and purpose · B. Technology and applications · C. Key features and benefits · IV. Comparison between Langchain and Langsmith · A. Technology stack · B. Use cases and industries · C. Scalability and performance · D. Security and privacy considerations · V. Conclusion · A. Recap of main differences between Langchain and Langsmith · B. Future implications and potential developments in the field · Notes: · - Ensure to provide clear definitions and examples for both Langchain and Langsmith. · - Compare and contrast the technologies in terms of their features, applications, and benefits. · - Include real-world examples or case studies to illustrate the differences between Langchain and Langsmith. · - Conclude by summarizing the key points and discussing the potential impact of these technologies on the industry.
**Visual description:** A plain-text outline, five Roman-numeral sections with lettered
sub-points and four trailing notes, filling the slide under the heading "Plan:".
**What it teaches:** What the `plan` node actually produced for the lesson's example topic; the
model's own spelling "Langchain"/"Langsmith" is kept.

---

## Lesson 8: LangChain Resources
Transcript: `## Lesson 8: LangChain Resources` in transcripts/ai-agents-in-langgraph-transcripts.md

Two title cards and three resource slides; Tall 39 between the Guide and Organization slides is
blank. The narration also walks through sites that have no slide (LangServe templates, the
LangSmith playground, earlier DeepLearning.AI courses).

### Slide 8.1 — Title card: LangChain Resources (Wide deck, slide 14)
**Evidence:** Title card — "Look, we have only covered some of the basics here today. I want to point out where you can find some more information to continue your agent journey."
**Text on slide:** AI Agents in LangGraph · LangChain Resources
**Visual description:** Title card: a watercolour of a mechanical parrot on a stack of open
treasure chests at a beach, at left.
**What it teaches:** Lesson title.

### Slide 8.2 — Title card: LangChain Resources (Tall deck, slide 37)
**Evidence:** Title card — twin of 8.1.
**Text on slide:** AI Agents in LangGraph · LangChain Resources
**Visual description:** Same treasure-chest illustration centred.
**What it teaches:** Lesson title.

### Slide 8.3 — Guide: the LangChain ecosystem (Tall deck, slide 38)
**Evidence:** Narrated — "The LangChain documentation is a great place to start. Specifically, it provides a great high level overview of all the packages and services in the LangChain ecosystem. So we break down the different LangChain core packages as well as all the LangChain community packages. So we used Tavily as part of LangChain community. And then we also use LangChain OpenAI which is a separate partner package. … LangChain itself is more high level and covers agents and other chains and different retrieval strategies … We also have a bunch of templates that can be deployed easily with LangServe … Helping out with all of this is LangSmith"
**Text on slide:** Guide · (in the diagram) Observability · LangSmith · Deployments · LangServe · Chains as Rest APIs · Python · Templates · Reference Applications · Python · Cognitive Architectures · LangChain · Python · JavaScript · Chains · Agents · Retrieval Strategies · LangChain-Community · Model I/O · Model · Prompt · Example Selector · Output Parser · Retrieval · Retriever · Document Loader · Vector Store · Text Splitter · Embedding Model · Agent Tooling · Tool · Toolkit · Integrations Components · LangChain-Core · LCEL - LangChain Expression Language · Parallelization · Fallbacks · Tracing · Batching · Streaming · Async · Composition · Protocol · Debugging · Playground · Evaluation · Annotation · Monitoring
**Visual description:** The LangChain documentation's ecosystem diagram, a screenshot: stacked
layers from LangChain-Core (LCEL) at the bottom, through LangChain-Community (Model I/O,
Retrieval, Agent Tooling) and LangChain (Chains, Agents, Retrieval Strategies), to Templates and
LangServe above, with LangSmith (Debugging, Playground, Evaluation, Annotation, Monitoring) as a
purple band across the top and down the right side. Row labels at left: Observability,
Deployments, Cognitive Architectures, Integrations Components, Protocol.
**What it teaches:** How the packages used in the course fit together: Tavily came from
langchain-community, ChatOpenAI from the langchain-openai partner package, LangGraph extends
LangChain, LangServe deploys, LangSmith observes.

### Slide 8.4 — Organization (Tall deck, slide 40)
**Evidence:** Narrated — same passage as 8.3 ("So we used Tavily as part of LangChain community. And then we also use LangChain OpenAI which is a separate partner package.").
**Text on slide:** Organization · (in the screenshot) Concretely, the framework consists of the following open-source libraries: · langchain-core: Base abstractions and LangChain Expression Language. · langchain-community: Third party integrations. · Partner packages (e.g. langchain-openai, langchain-anthropic, etc.): Some integrations have been further split into their own lightweight packages that only depend on langchain-core. · langchain: Chains, agents, and retrieval strategies that make up an application's cognitive architecture. · langgraph: Build robust and stateful multi-actor applications with LLMs by modeling steps as edges and nodes in a graph. · langserve: Deploy LangChain chains as REST APIs. · The broader ecosystem includes: · LangSmith: A developer platform that lets you debug, test, evaluate, and monitor LLM applications and seamlessly integrates with LangChain. · Describe when to use LangGraph vs LangChains agents
**Visual description:** A screenshot of the documentation's package list, then a large grey line
"Describe when to use LangGraph vs LangChains agents" beneath it.
**What it teaches:** The package names behind 8.3. The last line reads as a speaker note or
to-do left on the slide; the transcript does not answer it directly, though Lesson 3 makes the
case for LangGraph (controlled cyclic flows, persistence).

### Slide 8.5 — Resources (Tall deck, slide 41)
**Evidence:** Narrated — "The LangChain GitHub repo has a lot of good resources, a lot of good cookbooks, and a lot of templates for getting started. The LangGraph repo, of course, has in-depth documentation on LangGraph, everything that we just covered. So great reference docs, great tutorials, and great how-to guides. … We already saw the prompt hub once, but just to reiterate, this is a great place to go to get inspiration"
**Text on slide:** Resources · github Examples: · https://github.com/langchain-ai/langchain · Hub · Docs · GitHub LangGraph · Descriptions and pointers to examples · https://github.com/langchain-ai/langgraph/tree/main
**Visual description:** A four-item bulleted list with two URLs as sub-bullets.
**What it teaches:** Where to go next: the LangChain repo, the prompt hub, the docs, and the
LangGraph repo.

---

## Lesson 9: Conclusion
Transcript: `## Lesson 9: Conclusion` in transcripts/ai-agents-in-langgraph-transcripts.md

Two title cards and five architecture diagrams, each present in both decks. The Wide deck has
the finished drawings with source links (9.2–9.6); the Tall deck has earlier versions (9.8–9.11)
with two blank placeholders (Tall 44, 46) where Supervisor and Plan and Execute would sit.

### Slide 9.1 — Title card: Conclusion (Wide deck, slide 15)
**Evidence:** Title card — "Congratulations. You now have a good hand on how to build your own agents. With what you have learned today, you can build simple or quite complex agents. But before we go, I wanted to cover some of the agent flows that we couldn't build today, but I think you should know about."
**Text on slide:** AI Agents in LangGraph · Conclusion
**Visual description:** Title card: a watercolour of two mechanical parrots side by side on a
fence at sunset, at left.
**What it teaches:** Lesson title.

### Slide 9.2 — Multi-Agent (Wide deck, slide 16)
**Evidence:** Narrated — "The first architecture I want to talk about is a multi-agent architecture. And we covered this a little bit with the writing agent. But just to make it a little bit more concrete. A multi-agent architecture is when multiple different agents work on the same shared state. And so these agents could be just a prompt and a language model as they were in the writer. They could also have different tools that they could call this. … The crucial thing here, and the differentiator between the next thing that we'll see is that they all work on the same shared state."
**Text on slide:** Multi-Agent · https://github.com/langchain-ai/langgraph/tree/main/examples/multi_agent · (diagram, hand-lettered) User · Input: Generate a chart of average temperature in Alaska over the last decade · 1) first go to researcher · Researcher · (Call a 'search' function or FINISH) · Message · Router · (If statements basd on agent output) · Message · Chart Generator · (Code Execution) · If "continue and state["sender"] == "Chart Generators" · if "continue" and state ["sender"] == researcher · if function is called · if state["sender"] == "Researcher" · if state["sender"] == "Chart Generator" · Call_tool
**Visual description:** A hand-drawn graph: a green User box at top feeds a blue Researcher
oval; Researcher and a blue Chart Generator oval both send Messages into a pink Router diamond
in the middle; dotted "if" edges from the Router go back to either agent or down to a green
Call_tool box, which returns to whichever agent sent it. Source URL beneath.
**What it teaches:** Multi-agent in LangGraph: several agents, one shared state, a router node
that reads `state["sender"]` to decide who acts next. The "basd" typo is on the slide.

### Slide 9.3 — Supervisor (Wide deck, slide 17)
**Evidence:** Narrated — "Let's contrast that with a supervisor agent. So here we have a supervisor which is calling into some sub-agents. And here the supervisor will actually determine what the input to that agent is. And those agents themselves could have different states inside them. There are graphs. And so there's not necessarily the same concept of a shared state. … This is often good when you can use a really powerful language model as the supervisor."
**Text on slide:** Supervisor · https://github.com/langchain-ai/langgraph/tree/main/examples/multi_agent · (diagram, hand-lettered) User · Supervisor · route · route · route · Agent 1 · Agent 2 · Agent 3
**Visual description:** A hand-drawn tree: green User box at top exchanging arrows with a green
Supervisor bar, which has dotted "route" edges down to three blue Agent ovals and solid return
arrows back up. Same source URL as 9.2.
**What it teaches:** The supervisor pattern: one coordinating agent routes to sub-agents and
chooses their inputs; sub-agents may be their own graphs with their own state.

### Slide 9.4 — Flow Engineering (Wide deck, slide 18)
**Evidence:** Narrated — "One term that's popped up a bunch recently is flow engineering. This comes from an AlphaCodium paper, where they achieve state of the art coding performance. And they do it with a very graphical like solution like this. And so looking at it you can see that it's basically a pipeline. But there are a few key nodes where there's actually a loop. So there's loops on the initial code solution. There's loops when you iterate on public tests and there's loops when you iterate on AI tasks."
**Text on slide:** Flow Engineering · (figure) Pre-processing · Input - Problem Description + Public Tests · Problem Reflection · Public Tests Reasoning · Generate Possible Solutions · Rank Solutions · Generate Additional AI Tests · Code iterations · Initial Code Solution · Iterate on Public Tests · Iterate on AI Tests · Final Solution · (a) The proposed AlphaCodium flow.
**Visual description:** The AlphaCodium flow figure, large: a grey Pre-processing block of six
boxes in a snake order, feeding an orange Code iterations block of four boxes with dotted
self-loops on Initial Code Solution, Iterate on Public Tests and Iterate on AI Tests. No URL on
this version; the Tall twin (9.9) has one.
**What it teaches:** Flow engineering: a mostly directed pipeline with loops at a few chosen
nodes, as a bespoke architecture for a coding task.

### Slide 9.5 — Plan and Execute (Wide deck, slide 19)
**Evidence:** Narrated — "A common paradigm is to have a plan and execute style flow where first, you do an explicit planning, step upfront and then you start to execute on that plan. So you may come up with a few steps that a sub-agent should go do. It can then go do one come back. Maybe you update the plan, maybe you don't. … Then you maybe check to see if the plan is successfully accomplished or whether you need to replan. And then if all is good, you return to the user."
**Text on slide:** Plan and Execute · https://github.com/langchain-ai/langgraph/blob/main/examples/plan-and-execute/plan-and-execute.ipynb?ref=blog.langchain.dev · (diagram, hand-lettered) Plan-and-Execute · 1. User Request · Plan · 2. Generate Tasks · Task List · 1. 2. 3. … · 3 Exec Tasks · Single-Task Agent · Loop to solve task · 4. Update state with task results · Replan · 5b. Re-plan more tasks · 5a. Respond to user
**Visual description:** A hand-drawn flow with a cartoon user avatar at left: User Request → a
Plan box (brain icon) → a Task List → a Single-Task Agent with a "Loop to solve task" circle and
tools icon → Update state → a Replan box, which either re-plans more tasks (back to the list) or
responds to the user. Source URL beneath.
**What it teaches:** Plan-and-execute: explicit upfront planning, one task at a time by a
sub-agent, state updated with results, then replan or finish.

### Slide 9.6 — Language Agent Tree Search (Wide deck, slide 20)
**Evidence:** Narrated — "The final one I want to touch on is a really interesting paper called Language Agent Tree Search. So this basically does a tree search over the state of possible actions. And so it first generates an action. It then reflects and then goes down based on that action and generates some other sub-actions reflects on that. And throughout all these reflections it can basically reflect on where in the tree of action states it wants to jump back to. So it can backpropagate and update parent nodes to have more information, which may inform future directions from that previous state. For this in particular, you can really see why persistence is really important, because you need to be able to go back in time to previous states."
**Text on slide:** Language Agent Tree Search · https://github.com/langchain-ai/langgraph/blob/main/examples/lats/lats.ipynb · (diagram, hand-lettered) Generate · Reflect · Generate · Reflect · Generate · Reflect · Act · 0.3 · 0.3 · 0.6 · 0.8 · 0.4 · 0.6 · 0.8 · 0.4 · 0.7 · 0.9 · 0.4 · 0.2 · 1 · Language Agent Tree Search · Repeat until solved: · 1. Select node · 2. Generate new candidates · 2. Act, reflect, and score · 3. Backpropagate (update parents)
**Visual description:** A hand-drawn sequence of six alternating Generate/Reflect brain boxes
across the top, each above a growing tree of dashed "Act" nodes with scores; green nodes mark
the chosen branch, red ones rejected, and the final tree ends at a node scored "1". A "Repeat
until solved" loop with four numbered steps (two of them numbered 2) at lower right, a user
avatar at lower left, source URL beneath.
**What it teaches:** LATS: tree search over actions with reflection scores and backpropagation
to parent nodes, and why that needs the persistence and time travel from Lessons 5 and 6.

### Slide 9.7 — Title card: Conclusion (Tall deck, slide 42)
**Evidence:** Title card — twin of 9.1.
**Text on slide:** AI Agents in LangGraph · Conclusion
**Visual description:** Same two-parrot illustration centred.
**What it teaches:** Lesson title.

### Slide 9.8 — Multi-Agent, video screenshot (Tall deck, slide 43)
**Evidence:** Narrated — same passage as 9.2; earlier version of the same diagram.
**Text on slide:** Multi-Agent · (screenshot) the same hand-lettered diagram as 9.2, plus the video player bar "2:28 / 24:01"
**Visual description:** A screenshot of a YouTube video showing the multi-agent diagram, with the
player's progress bar, timestamp and controls along the bottom and the presenter's webcam
circle at lower right. No source URL.
**What it teaches:** Same as 9.2; this is the draft the Wide-deck drawing replaced.

### Slide 9.9 — Flow Engineering, AlphaCodium figure with URL (Tall deck, slide 45)
**Evidence:** Narrated — same passage as 9.4.
**Text on slide:** (figure labels as on 9.4) · (a) The proposed AlphaCodium flow. · https://arxiv.org/abs/2401.08500
**Visual description:** The AlphaCodium figure, smaller than on 9.4, with the paper's arXiv
abstract URL beneath and no slide heading. Tall 44 before it is a blank frame.
**What it teaches:** Same as 9.4, and gives the paper link the Wide version lacks.

### Slide 9.10 — Language Agent Tree Search, drawing (Tall deck, slide 47)
**Evidence:** Narrated — same passage as 9.6.
**Text on slide:** https://github.com/langchain-ai/langgraph/blob/main/examples/lats/lats.ipynb · (diagram as on 9.6)
**Visual description:** The same LATS drawing as 9.6 at smaller size, with the notebook URL
beneath and no heading. Tall 46 before it is a blank frame.
**What it teaches:** Same as 9.6.

### Slide 9.11 — Language Agent Tree Search, paper figure (Tall deck, slide 48)
**Evidence:** Deck-only. The narration describes LATS but not this comparison with
Tree-of-Thoughts and RAP.
**Text on slide:** https://arxiv.org/pdf/2310.04406.pdf · (figure) Observation · Action · Reward · Thought · Input · Output · a) Tree-of-Thoughts · b) Reasoning via Planning · c) Language Agent Tree Search · Reflection · Environment · Figure 2: An overview of the differences between LATS and recently proposed LM search algorithms ToT (Yao et al., 2023a) and RAP (Hao et al., 2023). LATS leverages environmental feedback and self-reflection to further adapt search and improve performance.
**Visual description:** Figure 2 from the LATS paper: three search trees side by side, each from
an Input oval through layers of state boxes to Output ovals, with a legend of arrow types
(observation, action, reward, thought); the LATS tree adds a Reflection cloud and an Environment
globe. Paper URL beneath.
**What it teaches:** LATS differs from earlier LM tree searches by using environment feedback and
reflection. Background for 9.6, not narrated.

---

## Backup slides (no lesson)

Tall 49 is a divider titled "Backup" (coral red, with the LangChain and DeepLearning.AI logos,
no wave). The four pages after it are not described anywhere in the transcripts. What each
appears to be is a reading of the page, not a fact.

### Slide B.1 — Backup divider (Tall deck, slide 49)
**Evidence:** Deck-only.
**Text on slide:** Backup
**Visual description:** The word "Backup" in coral red, centred, logos at the bottom; the same
layout as a title card without an illustration.
**What it teaches:** Nothing; a section divider.

### Slide B.2 — Platform diagram (Tall deck, slide 50)
**Evidence:** Deck-only.
**Text on slide:** AWS hardware running xx hypervisor · Ubuntu xx · jupyter notebook · docker: RHEL w mongo · jupyter notebook · docker: RHEL w mongo · jupyter notebook · docker: RHEL w mongo · you are here
**Visual description:** Nested boxes: a blue AWS box containing an Ubuntu box containing three
yellow "docker: RHEL w mongo" boxes each tagged "jupyter notebook" in orange; an arrow labelled
"you are here" points at the top one.
**What it teaches:** Appears to describe where the course notebooks run (a Jupyter container on a
cloud VM). Not part of any lesson.

### Slide B.3 — Mysteries: Return types (Tall deck, slide 51)
**Evidence:** Deck-only.
**Text on slide:** Mysteries: Return types · dictionary · dictionary · string · Actually, pretty clear as these nicely match the state, but · who/what is taking this output and doing something with it? · and where is it going? (Global data structure?)
Code on slide:
```python
# Define the agent
def run_agent(data):
    agent_outcome = agent_runnable.invoke(data)
    return {"agent_outcome": agent_outcome}

# Define the function to execute tools
def execute_tools(data):
    # Get the most recent agent_outcome - this is the key added in the `agent` above
    agent_action = data["agent_outcome"]
    output = tool_executor.invoke(agent_action)
    return {"intermediate_steps": [(agent_action, str(output))]}

# Define logic that will be used to determine which conditional edge to go down
def should_continue(data):
    # If the agent outcome is an AgentFinish, then we return `exit` string
    # This will be used when setting up the graph to define the flow
    if isinstance(data["agent_outcome"], AgentFinish):
        return "end"
    # Otherwise, an AgentAction is returned
    # Here we return `continue` string
    # This will be used when setting up the graph to define the flow
    else:
        return "continue"
```
**Visual description:** Three node functions from a LangGraph agent-executor example as
syntax-highlighted code, each annotated at right with its return type (dictionary, dictionary,
string), then a comment and two questions.
**What it teaches:** Appears to be a working note from course development: node functions return
partial state updates (dictionaries whose keys match the "Complex" AgentState of 3.9) and a
conditional-edge function returns a routing string. The questions are the ones Lesson 3 answers
(LangGraph merges the returned dictionary into the state).

### Slide B.4 — Code-generation graph, cropped (Tall deck, slide 52)
**Evidence:** Deck-only.
**Text on slide:** (no text layer) · (diagram, hand-lettered) Question · Generation (Node) · LCEL docs · Stack trace · Answer · Pydantic Object · Preamble · Imports · Code · Import Check (Node) · Fail? · No · Yes · Code Execution Check (Node) · Fail? · No · Yes · Answer
**Visual description:** A hand-drawn flow pasted so large it covers the header logos: Question →
Generation node (fed by LCEL docs and a stack trace) → a Pydantic Answer object with Preamble,
Imports, Code → Import Check node → pink Fail? diamond → Code Execution Check node → Fail?
diamond → Answer, with Yes branches looping back to Generation. A stray blue circle and pink
square sit below the diagram.
**What it teaches:** Appears to be a LangGraph code-assistant example (generate, check imports,
execute, retry on failure). Unlabelled and not narrated.

### Slide B.5 — ReAct Example (Tall deck, slide 53)
**Evidence:** Deck-only.
**Text on slide:** ReAct Example · https://arxiv.org/pdf/2210.03629.pdf · (figure) (1) Hotspot QA · Question: Aside from the Apple Remote, what other device can control the program Apple Remote was originally designed to interact with? · (1d) ReAct (Reason + Act) · Thought 1: I need to search Apple Remote and find the program it was originally designed to interact with. · Act 1: Search[Apple Remote] · Obs 1: The Apple Remote is a remote control introduced in October 2005 by Apple … originally designed to control the Front Row media center program … · Thought 2: Apple Remote was originally designed to control the Front Row media center program. I need to search Front Row next and find what other device can control it. · Act 2: Search[Front Row] · Obs 2: Could not find [Front Row]. Similar: ['Front Row Seat to Earth', 'Front Row Motorsports',' Front Row (software)', …] · Thought 3: Front Row is not found. I need to search Front Row (software). · Act 3: Search[Front Row (software)] · Obs 3: Front Row is a discontinued media center software … · Thought 4: Front Row (software) is controlled by an Apple Remote or the keyboard function keys. So the answer is keyboard function keys. · Act 4: Finish[keyboard function keys]
**Visual description:** The HotpotQA worked example from the ReAct paper: a question box and a
four-step Thought/Act/Obs trace with the key phrases highlighted in green and a green check mark
at the end. The arXiv URL is partly hidden behind the question box.
**What it teaches:** A concrete ReAct trace from the paper, the pattern Lesson 2 implements.
Would fit Lesson 2 but is filed under Backup and not narrated.
