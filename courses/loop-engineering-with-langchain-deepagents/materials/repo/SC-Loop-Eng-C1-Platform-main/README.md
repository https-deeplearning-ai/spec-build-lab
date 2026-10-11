# Loop Engineering Course - Educational Notebooks

This repository contains educational Jupyter notebooks for teaching **Loop Engineering** as an architectural pattern for building reliable AI agents using LangChain.

## Course Overview

The course teaches Loop Engineering through a running project: a **Requirements Analysis Agent** that analyzes software requirement documents and produces structured analysis reports.

### Educational Philosophy

These notebooks follow a **concept-first approach**:
- 80% focus on visualizations, outputs, and architectural concepts
- 20% focus on code implementation
- Learning happens primarily through observing outputs
- Code exists to produce educational insights

## Lessons

### Lesson 3: Building the Execution Loop
**File:** `lesson_3_execution_loop.ipynb`

Learn how an agent performs iterative work through:
- Visualizing execution traces (agent reasoning → tool execution cycles)
- Observing state evolution over time
- Examining structured analysis outputs
- Understanding progressive knowledge building

**Key Concepts:**
- Iterative execution
- Agent state management
- Tool usage
- Structured outputs

### Lesson 4: Controlling the Execution Loop
**File:** `lesson_4_evaluation_loop.ipynb`

Learn how to control agent execution through:
- Rubric-based quality evaluation
- Stop conditions and retry policies
- Evaluation feedback loops
- Iteration comparison

**Key Concepts:**
- Quality assessment
- Stopping decisions
- Controlled iteration
- Feedback-driven improvement

### Lesson 6: Building the Hill Climbing Loop
**File:** `lesson_6_hill_climbing_loop.ipynb`

Learn how a system improves itself over time through:
- Collecting traces across many historical runs
- Detecting repeated failure patterns (not just single-run scores)
- Targeted prompt refinement based on a systemic weakness
- Before/after comparison to verify the fix worked

**Key Concepts:**
- Cross-run trace analysis
- Repeated failure detection
- Prompt/rubric refinement
- Verified improvement

## Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd SC-Loop-Eng-C1
```

### 2. Create Virtual Environment

**Python 3.12 or newer is required.** Check yours first:

```bash
python3 --version
```

On 3.11 or older the install fails while building numpy and pandas, which is a
compiler error rather than a clear message about the version.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set OpenAI API Key (optional)

By default, Lessons 2 and 3 run entirely offline: they replay a real, pre-captured `gpt-5.4-mini` trace (`lesson_3_prebaked_trace.json` / `lesson_4_prebaked_trace.json`), so **no API key is required** to run them top to bottom.

If you want to call the API yourself and see fresh, non-deterministic output, add your key to a `.env` file (not committed to git, loaded automatically via `python-dotenv`):
```
OPENAI_API_KEY=your-api-key-here
```
Then flip `USE_LIVE_LLM = True` in the configuration cell near the top of the notebook.

### 5. Set Up LangSmith Tracing (optional)

[LangSmith](https://smith.langchain.com) gives you a hosted, shareable view of every Model call, tool call, and retry a live run makes — useful for inspecting a run in detail, or for sharing what happened with someone who doesn't have the notebook running.

**Create an account:**
1. Go to [smith.langchain.com](https://smith.langchain.com) and sign up (a free tier is available; you can sign up with Google/GitHub or an email).
2. Once logged in, open **Settings → API Keys** and create a new API key.

**Enable tracing** by adding to your `.env` file:
```
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your-langsmith-api-key-here
LANGSMITH_PROJECT=loop-engineering-lesson-2
```

No code changes are needed — LangChain picks these up automatically for every `USE_LIVE_LLM = True` run. After running the notebook live, go to your project in the LangSmith UI to see the trace.

**To let a learner see your traces without their own account:** open the run in LangSmith and use the **Share** button — it creates a public, read-only link to that specific trace that anyone can open without logging in. This is the simplest way to show a class what a real trace looks like without asking everyone to create an account. If you instead want each learner to see *their own* live runs, they'll need their own free LangSmith account and their own `LANGSMITH_API_KEY`.

## Running the Notebooks

### Option 1: Jupyter Notebook (Recommended)

```bash
source venv/bin/activate
jupyter notebook
```

Then open:
- `lesson_2/lesson_2_deepagent_primer.ipynb`
- `lesson_3/lesson_3_execution_loop.ipynb` (or the recorded `lesson_3/L3_student.ipynb`)
- `lesson_4/lesson_4_evaluation_loop.ipynb` (or the recorded `lesson_4/L4_student.ipynb`)
- `lesson_6/lesson_6_hill_climbing_loop.ipynb` (or the recorded `lesson_6/L6_student.ipynb`)

Each lesson folder is self-contained: its own copy of `workspace/` (and `requirement_docs/`, `run_history/` for Lesson 6), its own `images/`. The shared helper modules (`deepagent_helpers.py`, `visualization_helpers.py`, `run_history.py`, `hill_climbing.py`) live once at the repo root and are symlinked into each lesson folder that needs them — edit the root copy, not the symlink.

Lesson 5 (the Automation Loop) has no notebook; it's a small Flask app simulating Jira + Confluence, in `lesson_5_event_driven/` — see that folder's own README.

### Option 2: Jupyter Lab

```bash
source venv/bin/activate
jupyter lab
```

### Option 3: VS Code

1. Open the repository in VS Code
2. Install the "Jupyter" extension
3. Open a `.ipynb` file
4. Select the Python interpreter from `./venv/bin/python`

## Cost & Safety (Lessons 2 and 3, live mode)

Live mode is bounded per lesson. Lesson 3 caps model turns with `MAX_TURNS` (default 12). Lesson 4 caps how many times the grader may send the work back with `MAX_RUBRIC_ITERATIONS` (default 3), and makes one grader call per attempt. Lesson 6 replays two committed batches of five runs each, and regenerating them live costs about $0.08 per batch.

The review agent and its grader run on `gpt-5.4-mini`. Lesson 6's analysis agent runs on `gpt-5.5`, because reading five full run traces and finding what recurs is the one job the cheaper model does unreliably.

If `OPENAI_API_KEY` isn't set, `USE_LIVE_LLM` automatically falls back to the pre-baked trace with a printed warning instead of crashing.

## Project Structure

One folder per lesson, each self-contained (own data copy, own `images/`) except
for the handful of shared helper modules, which live once at the root and are
symlinked into every lesson folder that needs them. Lesson 1 has no folder
(slides only); Lesson 5 has no notebook (see its own README).

```
SC-Loop-Eng-C1/
├── deepagent_helpers.py                # The review agent. Symlinked into lessons 2, 3, 4, 6
├── run_history.py                      # Runs the agent over every document. Symlinked into lesson 6
├── hill_climbing.py                    # Reads a batch of runs, proposes a harness change. Symlinked into lesson 6
├── visualization_helpers.py            # Loop diagrams. Symlinked into lessons 2, 3, 4, 6
├── agent_for_slides.py                 # Generates the Lesson 1 slide assets
├── jira_tickets.json                   # Fake-Jira seed data deepagent_helpers.py reads by ticket ID
├── workspace/memories/AGENTS.md        # The review agent's instructions (root copy, used by agent_for_slides.py and lesson_5_event_driven)
├── requirement_docs/                   # The five documents the agent reviews (root copy, used by agent_for_slides.py)
├── images/                             # Loop diagrams (root copy)
│
├── lesson_2/
│   ├── lesson_2_deepagent_primer.ipynb
│   ├── primer_workspace/               # memories/AGENTS.md + one SKILL.md per poem form
│   └── deepagent_helpers.py, visualization_helpers.py, images/   # symlinks / own copy
│
├── lesson_3/
│   ├── lesson_3_execution_loop.ipynb   # instructor notebook
│   ├── L3_student.ipynb                # recorded notebook
│   ├── lesson_3_prebaked_trace.json
│   └── workspace/, images/, deepagent_helpers.py, visualization_helpers.py
│
├── lesson_4/
│   ├── lesson_4_evaluation_loop.ipynb  # instructor notebook
│   ├── L4_student.ipynb                # recorded notebook
│   ├── lesson_4_prebaked_trace.json
│   └── workspace/, images/, deepagent_helpers.py, visualization_helpers.py
│
├── lesson_5_event_driven/              # Flask app simulating Jira + Confluence; no notebook
│
├── lesson_6/
│   ├── lesson_6_hill_climbing_loop.ipynb  # instructor notebook
│   ├── L6_student.ipynb                   # recorded notebook
│   ├── requirement_docs/, run_history/    # own copies (v1/, v2/ = before/after batches)
│   └── workspace/, images/, deepagent_helpers.py, run_history.py, hill_climbing.py, visualization_helpers.py
│
├── pyproject.toml                      # Dependencies, source of truth (one file for the whole repo)
├── requirements.txt                    # Generated from pyproject.toml for the pip path
└── .env.example                        # Copy to .env and add your keys
```

## Key Dependencies

Floors are set in `pyproject.toml`; `requirements.txt` is generated from it.

- **deepagents** (0.7.11+) - The agent harness: filesystem, memory, skills, grader
- **LangChain** (1.3.14+) - Models, tools, middleware
- **LangGraph** (1.2.9+) - Orchestration and checkpointing underneath deepagents
- **OpenAI** (2.47.0+) - LLM API client. The notebooks use `gpt-5.4-mini` and `gpt-5.5`
- **LangSmith** (0.10.9+) - Optional hosted tracing for live runs (see Setup)
- **python-dotenv** (1.2.2+) - Loads `OPENAI_API_KEY` from `.env`
- **Pydantic** (2.13.4+) - Structured LLM output schemas
- **Matplotlib** (3.11.1+) - Visualization
- **Seaborn** (0.13.2+) - Enhanced visualizations
- **Pandas** (3.0.3+) - Data manipulation

## Notebook Features

### Rich Visualizations
- Execution flow diagrams
- State evolution charts
- Quality metric tracking
- Decision point highlighting
- Timeline visualizations
- Comparison views

### Interactive Elements
- Configurable quality thresholds
- Adjustable iteration limits
- Experiment sections
- Try-your-own requirements

### Educational Outputs
- Color-coded analysis results
- Formatted reports
- Progress tracking
- Detailed feedback

## Usage Tips

1. **Run cells in order** - Each cell builds on previous ones
2. **Observe outputs carefully** - The visualizations tell the story
3. **Experiment with parameters** - Try different thresholds and limits
4. **Try your own requirements** - Test with different requirement documents
5. **Compare iterations** - Notice how quality improves over time

## Troubleshooting

### "No module named 'langchain'"
```bash
source venv/bin/activate  # Ensure venv is activated
pip install -r requirements.txt
```

### "⚠ OPENAI_API_KEY not found in .env"
This only appears if you set `USE_LIVE_LLM = True` without a key configured. Either add `OPENAI_API_KEY` to your `.env` file, or leave `USE_LIVE_LLM = False` to use the pre-baked trace.

### Visualizations not displaying
```bash
# Install matplotlib backend support
pip install ipympl
# Then in notebook: %matplotlib inline
```

### Kernel not found
```bash
python -m ipykernel install --user --name=venv
```

## Learning Path

1. Start with **Lesson 3** to understand the Execution Loop
2. Progress to **Lesson 4** to learn about control and evaluation
3. Experiment with different configurations
4. Try analyzing your own requirement documents
5. Observe how evaluation improves quality

## Educational Outcomes

After completing these notebooks, you should understand:

- How agents execute iteratively to build complex outputs
- How state evolves during agent execution
- How evaluation controls iteration
- How feedback loops improve quality
- The architectural pattern of Loop Engineering
- How to apply these patterns to different agent types

## Contributing

This is an educational project. Feedback and improvements are welcome!

## License

[Specify your license here]

## Support

For questions or issues:
1. Check the troubleshooting section above
2. Read the agent's own instructions in `workspace/memories/AGENTS.md`, which is
   everything the review agent is told
3. Read `deepagent_helpers.py`, which builds the agent the lessons share

---

**Remember:** The goal is to learn Loop Engineering concepts through observation, not to master LangChain syntax!
