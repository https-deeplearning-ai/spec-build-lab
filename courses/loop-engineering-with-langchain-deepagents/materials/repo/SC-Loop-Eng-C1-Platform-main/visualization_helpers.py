"""
Visualization helper functions for Loop Engineering course notebooks.

These functions handle the detailed plotting code to keep notebooks clean and focused.
"""

import html as _html

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
from matplotlib.lines import Line2D
from IPython.display import HTML, Markdown

from deepagent_helpers import first_ambiguity


def render_review_trace(trace):
    """Render a Requirements Review Agent's step-by-step trace (a list of
    objects with .step/.actor/.action/.detail) as a clean, calmly-styled
    table, including what each tool call actually recorded.

    Model turns and tool turns alternate; this is what makes the loop
    itself visible - each row is one turn, not one metric. The Step number
    is dropped (row order already shows it); Actor and its row get a
    distinct color per turn type so the alternation reads at a glance
    instead of needing the text to be read. Colors are set explicitly
    (never "transparent") so the table looks the same in light and dark
    notebook themes.
    """
    import pandas as pd

    # ⚙ and 🗨 rather than a wrench or a brain: both are in the small set of
    # symbols Unicode marks "text presentation by default," so most fonts
    # render them as plain monochrome glyphs instead of full-color emoji.
    # There is no monochrome "brain" - that codepoint has no text variant.
    icon = {"Model reasoning": "🗨", "Tool": "⚙"}

    df = pd.DataFrame(
        [
            {
                "Actor": f"{icon.get(s.actor, '')} {s.actor}".strip(),
                "Action": s.action,
                "Result": getattr(s, "detail", "") or "—",
            }
            for s in trace
        ]
    )

    model_bg, model_text = "#eaf1fb", "#1d4ed8"   # light blue / blue
    tool_bg, tool_text = "#eafaf1", "#15803d"     # light green / green
    header_bg, header_text = "#1f2937", "#ffffff"  # dark slate / white

    def _row_style(row):
        bg = model_bg if "Model reasoning" in row["Actor"] else tool_bg
        return [f"background-color: {bg}; color: #1a1a1a;"] * len(row)

    def _actor_color(value):
        color = model_text if "Model reasoning" in value else tool_text
        return f"color: {color}; font-weight: 600;"

    return (
        df.style.hide(axis="index")
        .apply(_row_style, axis=1)
        .map(_actor_color, subset=["Actor"])
        .set_properties(**{"text-align": "left", "padding": "6px 10px"})
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": (
                        f"background-color: {header_bg}; color: {header_text}; "
                        "font-weight: 700; text-align: left; padding: 6px 10px;"
                    ),
                },
                {"selector": "td", "props": "max-width: 480px; white-space: normal;"},
            ]
        )
    )


_REPORT_CARD_STYLE = """
<style>
.lc-report-card { background:#fdfaf3; border:1px solid #e3dcc5; border-radius:10px;
                   padding:4px 24px 20px; margin:14px 0; box-shadow:0 1px 3px rgba(0,0,0,0.08); }
.lc-report-card.lc-report-card-muted { background:#f3f1ec; border:1px solid #dcdad2; }
.lc-report-card .lc-report-label { font-size:0.95em; letter-spacing:0.02em; color:#8a7d4f;
                   font-weight:700; padding-top:14px; }
.lc-report-card h1, .lc-report-card h2 { font-size:1.15em; margin:16px 0 6px 0; color:#1a1a1a; }
.lc-report-card h3 { font-size:1.05em; margin:14px 0 4px 0; color:#1a1a1a; }
.lc-report-card p, .lc-report-card li { color:#1a1a1a; line-height:1.5; }
.lc-report-card ul, .lc-report-card ol { margin:4px 0 10px 0; padding-left:22px; }
</style>
"""


def render_report(markdown_text: str, title: str = "Report", icon: str = "📄", muted: bool = False) -> HTML:
    """An agent-produced markdown report (analysis.md, proposal.md, a poem,
    anything written to a file), rendered in a visibly distinct card instead
    of a plain Jupyter markdown cell.

    On a recording, a bare `display(Markdown(...))` sits on the same white
    background as everything else in the notebook, so there is nothing that
    marks it as the agent's actual output rather than more notebook prose.
    Converts to HTML with `mistune` rather than relying on raw HTML nested
    inside a `Markdown()` call, which different notebook frontends handle
    inconsistently; `mistune` is already a transitive dependency via
    `jupyter`, so this adds nothing new to install.

    `muted` swaps the default warm card background for a grayer one, same
    lightness, less yellow, for content that isn't itself the agent's output
    (reference material like the grader's rubric or system prompt) but still
    deserves a visibly distinct card rather than plain notebook prose.
    """
    import mistune

    body_html = mistune.html(markdown_text)
    card_class = "lc-report-card lc-report-card-muted" if muted else "lc-report-card"
    label = f"{icon} {title}" if icon else title
    return HTML(
        _REPORT_CARD_STYLE +
        f'<div class="{card_class}">'
        f'<div class="lc-report-label">{label}</div>'
        f'{body_html}'
        f'</div>'
    )


_COMPARISON_STYLE = """
<style>
.lc-compare-card { border-radius:10px; padding:4px 24px 20px; margin:14px 0;
                    box-shadow:0 1px 3px rgba(0,0,0,0.08); }
.lc-compare-card .lc-compare-label { font-size:0.95em; letter-spacing:0.02em;
                    font-weight:700; padding-top:14px; }
.lc-compare-card h1, .lc-compare-card h2 { font-size:1.15em; margin:16px 0 6px 0; color:#1a1a1a; }
.lc-compare-card h3 { font-size:1.05em; margin:14px 0 4px 0; color:#1a1a1a; }
.lc-compare-card p, .lc-compare-card li { color:#1a1a1a; line-height:1.5; }
.lc-compare-card ul, .lc-compare-card ol { margin:4px 0 10px 0; padding-left:22px; }
.lc-compare-card pre { white-space:pre-wrap; font-family:monospace; font-size:0.9em; margin:0;
                   background:transparent !important; border:none !important; padding:0 !important;
                   color:inherit !important; }
.lc-compare-initial { background:#fffaf1; border:1px solid #ffe3b3; }
.lc-compare-initial .lc-compare-label { color:#a9781a; }
.lc-compare-draft { background:#fdf3f2; border:1px solid #f3c6c4; }
.lc-compare-draft .lc-compare-label { color:#c23b3b; }
.lc-compare-final { background:#f1f8f2; border:1px solid #c3e2c5; }
.lc-compare-final .lc-compare-label { color:#3f8f49; }
</style>
"""


def render_requirement_comparison(
    requirement_text: str, report_markdown: str, report_title: str = "analysis.md"
) -> HTML:
    """The raw requirement the agent started from, stacked above the report
    it produced, so a learner can judge the review against the input without
    scrolling back to find it.

    The requirement is shown as preformatted text rather than rendered
    markdown: AGENTS.md forbids the agent from ever modifying it, so it is
    always exactly what was typed, not something to render as prose.
    """
    import mistune

    requirement_html = f"<pre>{_html.escape(requirement_text.strip())}</pre>"
    report_html = mistune.html(report_markdown)

    return HTML(
        _COMPARISON_STYLE +
        f'<div class="lc-compare-card lc-compare-initial">'
        f'<div class="lc-compare-label">📝 Initial Requirement</div>'
        f'{requirement_html}'
        f'</div>'
        f'<div class="lc-compare-card lc-compare-final">'
        f'<div class="lc-compare-label">✅ {report_title} (agent output)</div>'
        f'{report_html}'
        f'</div>'
    )


def render_report_progression(requirement_doc: str, pass0_md: str, final_md: str) -> HTML:
    """Three full report cards stacked: the original requirement, the agent's
    first complete draft (pass 0, what the grader rejected), and the final
    draft (what satisfied the rubric) -- the whole documents, not excerpts.

    `render_revision_progression` ("What the Revision Changed") shows these
    same two analysis.md snapshots but truncated to the first couple of
    Ambiguities bullets, to make the *kind* of change the grader asked for
    concrete without a wall of text. This shows each document in full, so the
    *scope* of the change -- every section, not just one -- is visible too.
    """
    import mistune

    requirement_html = f"<pre>{_html.escape(requirement_doc.strip())}</pre>"
    pass0_html = mistune.html(pass0_md)
    final_html = mistune.html(final_md)

    return HTML(
        _COMPARISON_STYLE +
        f'<div class="lc-compare-card lc-compare-initial">'
        f'<div class="lc-compare-label">📝 Initial Requirement</div>'
        f'{requirement_html}'
        f'</div>'
        f'<div class="lc-compare-card lc-compare-draft">'
        f'<div class="lc-compare-label">✏️ analysis.md: Pass 0 (First Draft, Rejected)</div>'
        f'{pass0_html}'
        f'</div>'
        f'<div class="lc-compare-card lc-compare-final">'
        f'<div class="lc-compare-label">✅ analysis.md: Final (Satisfied)</div>'
        f'{final_html}'
        f'</div>'
    )


# ---------------------------------------------------------------------------
# Lesson 4: the verification loop
# ---------------------------------------------------------------------------

def render_agent_middleware(agent) -> Markdown:
    """What `build_review_agent` actually wired into this agent: the
    middleware stack and whether a checkpointer is attached, read directly
    off the compiled graph rather than asserted in prose.

    Lesson 3's agent and this one come from the exact same function. Reading
    this off the agent itself, right after it is built and before it has run
    a single turn, is what makes "what did `rubric_iterations` actually add"
    a fact rather than a claim -- and the only thing this does add, on top of
    everything Lesson 3's agent already had.
    """
    names = sorted({name.split(".")[0] for name in agent.nodes if "." in name})
    lines = ["**Middleware wired into this agent:**"]
    for name in names:
        tag = "  ← the grader; Lesson 3's agent has none of this" if name == "RubricMiddleware" else ""
        lines.append(f"- `{name}`{tag}")
    cp = agent.checkpointer
    cp_line = (
        "none — Lesson 3's agent has none either"
        if cp is None
        else f"`{type(cp).__name__}` — needed to carry rubric state across revision passes"
    )
    lines.append(f"\n**Checkpointer:** {cp_line}")

    rubric_iterations = getattr(agent, "rubric_iterations", None)
    if rubric_iterations:
        lines.append(
            f"\n**Grader config:** model `{agent.grader_model}`, "
            f"revision budget {rubric_iterations} passes, tools `['read_file']`"
        )
        lines.append(
            "\n**Not fixed yet:** the rubric's actual pass/fail criteria. "
            "Everything above is *how* the grader grades; *what* it grades "
            "against is supplied fresh on each call to "
            "`run_verification_loop_live(agent, requirement_doc, rubric=...)`, "
            "not baked in here."
        )
    return Markdown("\n".join(lines))


def render_verification_summary(run) -> Markdown:
    """One clean line per fact: the verdict sequence, the turn/step counts, and
    why the loop actually stopped.

    'satisfied' and 'max_iterations_reached' are different outcomes and have to
    read differently, not just differ in one word inside a sentence.
    """
    verdicts = " → ".join(g.result for g in run.grading)
    stopped = ("the rubric was satisfied" if run.satisfied
               else f"the loop ended as '{run.status}'")
    return Markdown(
        f"**Grader verdicts:** {verdicts}  \n"
        f"**Turns:** {run.turns} model turns, {len(run.trace)} steps, "
        f"{len(run.grading)} grading passes  \n"
        f"**Stopped because:** {stopped}"
    )


def render_grading_grid(run):
    """Pass/fail grid: one row per criterion, one column per grading pass, plus
    the verdict and the file's size at each pass.

    Every criterion has to pass in the same pass for the loop to stop, so
    red/green on the grid is what makes "two of three passing" visibly not
    enough. A single criterion reading "Pass" does not mean that pass
    succeeded; the "Verdict" row, set apart below with a divider, is the only
    row that says so.

    "Criterion" is a plain column here, not a named pandas index. A named
    index renders on its own header row above "Pass 0" / "Pass 1" instead of
    sharing their row, which reads as a broken table rather than one with a
    row-label column.
    """
    import pandas as pd

    summary_rows = ("Verdict", "File size (chars)")
    pass_cols = [f"Pass {g.iteration}" for g in run.grading]

    names = [c["name"].split(":")[0].strip().capitalize() for c in run.grading[0].criteria]
    grid = pd.DataFrame({"Criterion": names})
    for g in run.grading:
        grid[f"Pass {g.iteration}"] = ["Pass" if c.get("passed") else "Fail" for c in g.criteria]

    grid.loc[len(grid)] = ["Verdict"] + [g.result for g in run.grading]
    grid.loc[len(grid)] = ["File size (chars)"] + [len(g.analysis_markdown) for g in run.grading]

    def _cell_color(value):
        if value == "Fail":
            return "color:#b91c1c; font-weight:700;"
        if value == "Pass":
            return "color:#15803d; font-weight:700;"
        return ""

    def _summary_row_style(row):
        if row["Criterion"] in summary_rows:
            return ["font-weight:700; border-top:2px solid #555;"] * len(row)
        return [""] * len(row)

    return (
        grid.style.hide(axis="index")
        .map(_cell_color, subset=pass_cols)
        .apply(_summary_row_style, axis=1)
        .set_properties(subset=["Criterion"], **{"text-align": "left"})
        .set_table_styles([{"selector": "th.col0", "props": "text-align: left;"}])
    )


def render_revision_progression(
    requirement_doc: str, before_md: str, after_md: str, n: int = 2
) -> HTML:
    """Three stacked, colored blocks: the requirement the agent started from,
    the first n Ambiguities bullets from pass 0 (the draft the grader
    rejected), and the same bullets from pass 1 (the revision that satisfied
    the rubric).

    The requirement never changes across passes -- AGENTS.md forbids editing
    it -- so it is shown once, plain text, ahead of the two analysis
    snapshots that do. Those two are real markdown (bold clauses, bulleted
    "Resolved by:"/"Edge case:" lines), so they go through `mistune` rather
    than a `<pre>` block, or the bold syntax would show up as literal
    asterisks instead of rendering.

    `hard_wrap=True` turns each single newline into a `<br>` instead of a
    soft break. Without it, "Reason:"/"Resolved by:"/"Edge case:" would only
    separate with `white-space: pre-line` on the container -- but that
    preserves every literal newline in mistune's output, including the
    incidental ones between `<li>`/`<p>` tags, which renders as a wall of
    blank lines. Explicit `<br>` tags give exact control with plain CSS.
    """
    import mistune

    render_markdown = mistune.create_markdown(hard_wrap=True)

    requirement_html = (
        '<pre style="white-space:pre-wrap; margin:8px 0 0 0; font-family:monospace; '
        'font-size:0.9em; background:transparent; border:none; padding:0; '
        f'color:inherit;">{_html.escape(requirement_doc.strip())}</pre>'
    )
    # The "..." lines above and below are not markdown and not part of the
    # excerpt; they mark it as a cut taken out of a larger document, so no
    # one mistakes 2 bullets for the whole Ambiguities section.
    ellipsis = (
        '<div style="color:#666; text-align:center; font-size:1.4em; '
        'font-weight:700; letter-spacing:8px; margin:4px 0;">...</div>'
    )

    before_html = (
        f'{ellipsis}<div style="font-size:0.9em;">'
        f'{render_markdown(first_ambiguity(before_md, n))}</div>{ellipsis}'
    )
    after_html = (
        f'{ellipsis}<div style="font-size:0.9em;">'
        f'{render_markdown(first_ambiguity(after_md, n))}</div>{ellipsis}'
    )

    def _block(title, body_html, meta, bg, border):
        return (
            f'<div style="background:{bg}; border-left:5px solid {border}; '
            f'padding:12px 16px; border-radius:6px; margin:6px 0;">'
            f'<strong>{title}</strong> '
            f'<span style="color:#555; font-size:0.85em;">({meta})</span>'
            f'{body_html}'
            f'</div>'
        )

    resolved = (before_md.count("Resolved by:"), after_md.count("Resolved by:"))
    edge_case = (before_md.count("Edge case:"), after_md.count("Edge case:"))

    item_word = "item" if n == 1 else "items"
    pass0_title = f"Ambiguities – {n} {item_word} – Pass 0 – First Draft"
    pass1_title = f"Ambiguities – {n} {item_word} – Pass 1 – Revised (Final)"

    html = (
        _block("Initial Requirement", requirement_html,
               f"{len(requirement_doc.strip())} chars", "#fffaf1", "#ffe3b3")
        + _block(pass0_title, before_html, f"{len(before_md)} chars",
                  "#fdf3f2", "#f3c6c4")
        + _block(pass1_title, after_html, f"{len(after_md)} chars",
                  "#f1f8f2", "#c3e2c5")
        + f'<p style="color:#555; font-size:0.85em; margin-top:6px;">'
          f'"Resolved by:" lines: {resolved[0]} → {resolved[1]} &nbsp;•&nbsp; '
          f'"Edge case:" lines: {edge_case[0]} → {edge_case[1]}</p>'
    )
    return HTML(html)


def render_grader_feedback(run) -> HTML:
    """What the grader told the agent, one card per pass: verdict, explanation,
    and per-criterion pass/fail with the exact gap sent back on a failure.

    Same card style as the grader's system prompt and rubric, so this reads as
    the grader's actual output rather than blending into notebook prose the
    way a bare `Markdown(...)` cell would. One card per pass, not one block
    of text separated by "---" rules, keeps each verdict visually distinct.

    The gap text is what drives the next revision, so it is shown verbatim
    rather than summarized.
    """
    import mistune

    cards = []
    for g in run.grading:
        lines = [g.explanation, ""]
        for c in g.criteria:
            name = c["name"].split(":")[0]
            if c.get("passed"):
                lines.append(f"- ✅ {name}")
            else:
                lines.append(f"- ❌ {name}")
                lines.append(f"  - gap: {c.get('gap')}")
        body_html = mistune.html("\n".join(lines))
        title = f"Pass {g.iteration} Feedback: {g.result.replace('_', ' ').title()}"
        cards.append(
            f'<div class="lc-report-card">'
            f'<div class="lc-report-label" style="color:#4a3b00;">{title}</div>'
            f'{body_html}'
            f'</div>'
        )

    return HTML(_REPORT_CARD_STYLE + "".join(cards))


def plot_agent_tools(used_tools, idle_tools, figsize=(9, 6)):
    """Small reference diagram: the Model wired to every tool it was offered.

    Not a technical diagram of the loop (that's Loop1_AgentLoop.png) - just a
    quick, presentable picture of the tool list for a slide or a live
    explanation. Used tools (this run) are filled in solid; idle tools
    (offered but never called) are outlined only.
    """
    fig, ax = plt.subplots(figsize=figsize)

    cx, cy = 0.16, 0.5
    ax.add_patch(Circle((cx, cy), 0.11, facecolor="#1f2937", edgecolor="black",
                         linewidth=2, zorder=3))
    ax.text(cx, cy, "Model", ha="center", va="center", fontsize=12,
            fontweight="bold", color="white", zorder=4)

    entries = [(name, True) for name in used_tools] + [(name, False) for name in idle_tools]
    box_x = 0.64
    n = len(entries)
    ys = [0.90 - i * (0.80 / max(n - 1, 1)) for i in range(n)] if n > 1 else [0.5]

    for (name, used), y in zip(entries, ys):
        face = "#3b82f6" if used else "white"
        edge = "#1d4ed8" if used else "#9ca3af"
        text_color = "white" if used else "#4b5563"
        box = FancyBboxPatch((box_x - 0.17, y - 0.045), 0.34, 0.09,
                              boxstyle="round,pad=0.02", facecolor=face,
                              edgecolor=edge, linewidth=2, zorder=3)
        ax.add_patch(box)
        ax.text(box_x, y, name, ha="center", va="center", fontsize=10,
                fontweight="bold" if used else "normal", color=text_color, zorder=4)
        ax.annotate(
            "", xy=(box_x - 0.18, y), xytext=(cx + 0.11, cy),
            arrowprops=dict(
                arrowstyle="->", lw=2 if used else 1, color=edge,
                linestyle="-" if used else "--", alpha=1.0 if used else 0.6,
            ),
        )

    ax.text(box_x, 0.98, "Tools offered to the agent", ha="center", fontsize=12,
            fontweight="bold", color="#1a1a1a")

    legend_used = FancyBboxPatch((0.03, 0.05), 0.035, 0.035, boxstyle="round,pad=0.01",
                                  facecolor="#3b82f6", edgecolor="#1d4ed8", linewidth=1.5)
    legend_idle = FancyBboxPatch((0.03, -0.01), 0.035, 0.035, boxstyle="round,pad=0.01",
                                  facecolor="white", edgecolor="#9ca3af", linewidth=1.5)
    ax.add_patch(legend_used)
    ax.add_patch(legend_idle)
    ax.text(0.08, 0.0675, "Used this run", fontsize=9, va="center", color="#1a1a1a")
    ax.text(0.08, 0.0075, "Offered, not used", fontsize=9, va="center", color="#1a1a1a")

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.05, 1)
    ax.axis("off")
    plt.tight_layout()
    return fig


def plot_nested_circles(figsize=(10, 10)):
    """Circular nested loops visualization"""
    fig, ax = plt.subplots(figsize=figsize)

    # Outer loop - Verification Loop
    outer_circle = Circle((0.5, 0.5), 0.42, fill=False, edgecolor='#e74c3c',
                         linewidth=6, linestyle='--')
    ax.add_patch(outer_circle)
    ax.text(0.5, 0.95, 'VERIFICATION LOOP', ha='center', va='center',
            fontsize=16, fontweight='bold', color='#e74c3c',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                     edgecolor='#e74c3c', linewidth=3))

    # Inner loop - Agent Loop
    inner_circle = Circle((0.5, 0.52), 0.25, fill=False, edgecolor='#3498db', linewidth=5)
    ax.add_patch(inner_circle)

    # Agent & Tools boxes
    agent_box = FancyBboxPatch((0.37, 0.68), 0.26, 0.10, boxstyle="round,pad=0.02",
        facecolor='#3498db', edgecolor='black', linewidth=2)
    ax.add_patch(agent_box)
    ax.text(0.5, 0.73, 'AGENT\nReasoning', ha='center', va='center',
            fontsize=12, fontweight='bold', color='white')

    tools_box = FancyBboxPatch((0.37, 0.37), 0.26, 0.10, boxstyle="round,pad=0.02",
        facecolor='#2ecc71', edgecolor='black', linewidth=2)
    ax.add_patch(tools_box)
    ax.text(0.5, 0.42, 'TOOLS\nExecution', ha='center', va='center',
            fontsize=12, fontweight='bold', color='white')

    # Agent Loop label
    ax.text(0.5, 0.55, 'AGENT\nLOOP', ha='center', va='center',
            fontsize=13, fontweight='bold', color='#3498db',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                     edgecolor='#3498db', linewidth=2))

    # Evaluation box
    eval_box = FancyBboxPatch((0.35, 0.12), 0.30, 0.12, boxstyle="round,pad=0.02",
        facecolor='#f39c12', edgecolor='black', linewidth=2)
    ax.add_patch(eval_box)
    ax.text(0.5, 0.18, 'EVALUATION\nQuality Check', ha='center', va='center',
            fontsize=12, fontweight='bold', color='white')

    # Arrows
    ax.annotate('', xy=(0.25, 0.55), xytext=(0.35, 0.24),
               arrowprops=dict(arrowstyle='->', lw=3, color='#e74c3c'))
    ax.text(0.22, 0.38, 'Continue\n(Quality < Threshold)', ha='center', va='center',
            fontsize=9, fontweight='bold', color='#e74c3c')

    ax.annotate('', xy=(0.75, 0.05), xytext=(0.65, 0.18),
               arrowprops=dict(arrowstyle='->', lw=3, color='#27ae60'))
    ax.text(0.82, 0.11, 'Stop\n(Quality ≥ Threshold)', ha='center', va='center',
            fontsize=9, fontweight='bold', color='#27ae60',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#d5f4e6',
                     edgecolor='#27ae60', linewidth=2))

    ax.annotate('', xy=(0.5, 0.47), xytext=(0.5, 0.68),
               arrowprops=dict(arrowstyle='->', lw=2, color='#34495e'))
    ax.annotate('', xy=(0.72, 0.70), xytext=(0.72, 0.45),
               arrowprops=dict(arrowstyle='->', lw=2, color='#34495e',
                              connectionstyle="arc3,rad=.3"))
    ax.annotate('', xy=(0.5, 0.24), xytext=(0.5, 0.37),
               arrowprops=dict(arrowstyle='->', lw=2, color='#34495e'))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Nested Loop Structure: Verification Loop Contains Agent Loop',
                fontsize=18, fontweight='bold', pad=20)

    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Lesson 6: the hill climbing loop
# ---------------------------------------------------------------------------

_TABLE_HEADER_STYLE = ("background-color:#1f2937; color:white; font-weight:700; "
                       "text-align:left; padding:10px 14px;")


def render_batch_overview(runs, summary):
    """One row per document in a run-history batch: how many attempts it took.

    Document and Attempts are plain columns, with pandas' own numeric index
    hidden, rather than a named index: a named index renders as its own
    header row, which reads as an empty row with nothing visible in it.
    """
    import pandas as pd

    rows = [{"Document": r["doc_name"], "Attempts": len(r["grading"])} for r in runs]
    df = pd.DataFrame(rows)
    caption = (f"{len(runs)} runs, model {summary['model']}, "
               f"{df['Attempts'].sum()} attempts total")
    return (
        df.style.hide(axis="index")
        .set_properties(**{"text-align": "left", "padding": "10px 14px"})
        .set_table_styles([
            {"selector": "th", "props": _TABLE_HEADER_STYLE},
            {"selector": "caption", "props": "font-size:0.95em; font-weight:600; "
                                              "text-align:left; padding-bottom:6px;"},
        ])
        .set_caption(caption)
    )


def render_first_attempt_grid(runs, summary):
    """Pass/fail grid for the first attempt on each document: one row per
    document, one column per criterion, with the Pass Rate row highlighted.

    Document is a plain column with pandas' index hidden, for the same
    reason as `render_batch_overview`. Color carries the signal here on
    purpose: a red column is what makes "this criterion, not these
    documents" visible before anyone reads a word.
    """
    import pandas as pd

    labels = list(summary["first_attempt"].keys())
    columns = ["Document"] + [l.title() for l in labels]

    rows = [[r["doc_name"]] +
            ["Pass" if c.get("passed") else "Fail" for c in r["grading"][0]["criteria"]]
            for r in runs]
    rows.append(["Pass Rate"] +
                [f"{summary['first_attempt'][l]['passed']}/{summary['runs']}" for l in labels])
    grid = pd.DataFrame(rows, columns=columns)

    def _cell_style(value):
        if value == "Fail":
            return "background-color:#fdecea; color:#b91c1c; font-weight:700;"
        if value == "Pass":
            return "background-color:#eaf7ec; color:#15803d; font-weight:700;"
        return ""

    def _row_style(row):
        if row["Document"] == "Pass Rate":
            return ["background-color:#eef2ff; color:#1e3a8a; font-weight:700;"] * len(row)
        return [""] * len(row)

    caption = f"Documents needing a revision: {summary['revisions_needed']}/{summary['runs']}"
    return (
        grid.style.hide(axis="index")
        .apply(_row_style, axis=1)
        .map(_cell_style, subset=columns[1:])
        .set_properties(**{"text-align": "left", "padding": "10px 14px"})
        .set_table_styles([
            {"selector": "th", "props": _TABLE_HEADER_STYLE},
            {"selector": "caption", "props": "font-size:0.9em; color:#555; "
                                              "text-align:left; padding-top:6px;"},
        ])
        .set_caption(caption)
    )


def render_recurring_gaps(runs) -> HTML:
    """Every first-attempt gap, as one small Document/Gap table per
    criterion, rather than a flat bullet list.

    Grouping by document would show five separate complaints. Grouping by
    criterion is what makes the repetition itself visible: the same heading
    recurring with a different document under it each time reads as "this
    agent always does this," not "this document was hard."

    Grouped by *position*, not by the grader's own wording of the criterion:
    the grader paraphrases each criterion differently run to run, sometimes
    dropping the leading label, so matching on text would silently split one
    recurring criterion into several. Position is stable because the
    criteria always come back in rubric order; `criterion_labels()` is what
    the codebase already uses for the same reason in `run_history.py`.
    """
    import pandas as pd
    from run_history import criterion_labels

    labels = criterion_labels()
    n = len(runs)
    by_criterion = {label: [] for label in labels}
    for r in runs:
        for i, c in enumerate(r["grading"][0]["criteria"]):
            if not c.get("passed"):
                by_criterion[labels[i]].append((r["doc_name"], str(c.get("gap"))[:160]))

    blocks = []
    for label in labels:
        items = by_criterion[label]
        if not items:
            continue
        df = pd.DataFrame(items, columns=["Document", "Gap"])
        table_html = (
            df.style.hide(axis="index")
            .set_properties(**{"text-align": "left", "padding": "10px 14px"})
            .set_table_styles([{"selector": "th", "props": _TABLE_HEADER_STYLE}])
            .to_html()
        )
        heading = (f'<p style="margin:18px 0 6px 0; font-weight:700;">'
                   f'{label.title()}: failed in {len(items)}/{n} runs</p>')
        blocks.append(heading + table_html)
    return HTML("".join(blocks))


def render_harness_change(change) -> Markdown:
    """The analyst's structured proposal, as one readable block instead of a
    column of separate print statements.
    """
    lines = [
        f"**Target:** {change.target}",
        f"**Issue:** {change.issue}",
        f"**Recurrence:** {change.recurrence}",
        f"**Section:** `{change.section}`",
    ]
    if change.rejected:
        lines += ["", "**Considered and rejected:**"]
        lines += [f"- {r}" for r in change.rejected]
    return Markdown("\n".join(lines))


def render_comparison(result, before="v1", after="v2"):
    """Before/after first-attempt pass rate per criterion, plus run-level
    usage and cost, as one styled table.

    Metric is a plain column with pandas' index hidden, for the same reason
    as `render_batch_overview`: a named index renders its own header row,
    which looks like an empty row with nothing in it.

    Only the per-criterion counts get red/green. Revisions, tokens, and cost
    are informational rather than pass/fail, and for revisions a lower number
    is the good outcome, so painting it on the same pass/fail scale would say
    the opposite of what it means.
    """
    import pandas as pd

    n = result["runs"]
    rows, is_criterion = [], []
    for name, (b, a) in result["criteria"].items():
        rows.append([name.title(), f"{b}/{n}", f"{a}/{n}"])
        is_criterion.append(True)

    rb, ra = result["revisions_needed"]
    rows.append(["Revisions Needed", f"{rb}/{n}", f"{ra}/{n}"]); is_criterion.append(False)
    for key, label in (("attempts", "Attempts Total"),
                        ("input_tokens", "Input Tokens"),
                        ("output_tokens", "Output Tokens")):
        b, a = result[key]
        rows.append([label, f"{b:,}", f"{a:,}"]); is_criterion.append(False)
    b, a = result["cost_usd"]
    rows.append(["Cost (USD)", f"{b:.4f}", f"{a:.4f}"]); is_criterion.append(False)

    df = pd.DataFrame(rows, columns=["Metric", before, after])

    def _style(col):
        styles = []
        for value, crit in zip(col, is_criterion):
            if not crit:
                styles.append("")
                continue
            num, denom = value.split("/")
            if num == denom:
                styles.append("background-color:#eaf7ec; color:#15803d; font-weight:700;")
            elif num == "0":
                styles.append("background-color:#fdecea; color:#b91c1c; font-weight:700;")
            else:
                styles.append("font-weight:600;")
        return styles

    return (
        df.style.hide(axis="index")
        .apply(_style, subset=[before, after])
        .set_properties(**{"text-align": "left", "padding": "10px 14px"})
        .set_table_styles([
            {"selector": "th", "props": _TABLE_HEADER_STYLE},
            {"selector": "caption", "props": "font-size:1em; font-weight:700; "
                                              "text-align:left; padding-top:8px;"},
        ])
        .set_caption(f"Verdict: {result['verdict'].title()}")
    )


def plot_before_after_pass_rates(result, figsize=(9, 4.5)):
    """Before/after first-attempt pass rate per criterion, as dumbbells
    rather than grouped bars.

    A bar chart hides a count of zero: there is nothing to see at the bottom
    of the axis. A dot is visible at any value, including zero, so a
    criterion that jumped from 0 to 5 reads the same as one that only moved
    from 3 to 5.
    """
    labels = list(result["criteria"].keys())
    n = result["runs"]
    before = [result["criteria"][l][0] for l in labels]
    after = [result["criteria"][l][1] for l in labels]

    fig, ax = plt.subplots(figsize=figsize)
    ys = list(range(len(labels)))

    for y, b, a in zip(ys, before, after):
        ax.plot([b, a], [y, y], color="#9ca3af", linewidth=2, zorder=1)
        ax.scatter([b], [y], color="#e74c3c", s=160, zorder=2,
                   edgecolor="black", linewidth=1)
        ax.scatter([a], [y], color="#2ecc71", s=160, zorder=3,
                   edgecolor="black", linewidth=1)
        ax.annotate(f"{b}/{n}", (b, y), xytext=(0, 12), textcoords="offset points",
                    ha="center", fontsize=10, fontweight="bold", color="#b91c1c")
        ax.annotate(f"{a}/{n}", (a, y), xytext=(0, -16), textcoords="offset points",
                    ha="center", fontsize=10, fontweight="bold", color="#15803d")

    ax.set_yticks(ys)
    ax.set_yticklabels([l.title() for l in labels])
    ax.set_xlim(-0.5, n + 0.5)
    ax.set_xlabel("passed on first attempt (of 5 runs)", fontweight="bold")
    ax.set_title("First-attempt pass rate, before and after the change",
                 fontsize=14, fontweight="bold", pad=14)
    ax.invert_yaxis()
    ax.grid(True, axis="x", alpha=0.3)

    handles = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#e74c3c",
               markersize=10, label="before"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#2ecc71",
               markersize=10, label="after"),
    ]
    ax.legend(handles=handles, loc="upper left")
    plt.tight_layout()
    return fig


def plot_hill_climbing_loop(figsize=(10, 10)):
    """Learning Loop diagram: an outer loop that reaches back inside and updates the agent loop"""
    fig, ax = plt.subplots(figsize=figsize)

    # Outermost loop - Learning Loop
    outer_circle = Circle((0.5, 0.5), 0.46, fill=False, edgecolor='#9b59b6',
                         linewidth=6, linestyle='--')
    ax.add_patch(outer_circle)
    ax.text(0.5, 0.98, 'LEARNING LOOP (Hill Climbing)', ha='center', va='center',
            fontsize=14, fontweight='bold', color='#9b59b6',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                     edgecolor='#9b59b6', linewidth=3))

    # Middle loop - Verification Loop
    mid_circle = Circle((0.5, 0.48), 0.32, fill=False, edgecolor='#e74c3c',
                         linewidth=5, linestyle='--')
    ax.add_patch(mid_circle)
    ax.text(0.5, 0.83, 'VERIFICATION LOOP', ha='center', va='center',
            fontsize=11, fontweight='bold', color='#e74c3c',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='white',
                     edgecolor='#e74c3c', linewidth=2))

    # Inner loop - Agent Loop
    inner_circle = Circle((0.5, 0.5), 0.18, fill=False, edgecolor='#3498db', linewidth=4)
    ax.add_patch(inner_circle)
    ax.text(0.5, 0.5, 'AGENT\nLOOP', ha='center', va='center',
            fontsize=11, fontweight='bold', color='#3498db')

    # Trace collection box, outside the rings
    trace_box = FancyBboxPatch((0.06, 0.06), 0.24, 0.12, boxstyle="round,pad=0.02",
        facecolor='#34495e', edgecolor='black', linewidth=2)
    ax.add_patch(trace_box)
    ax.text(0.18, 0.12, 'TRACES\nMany Runs', ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')

    # Issue / fix box
    issue_box = FancyBboxPatch((0.70, 0.06), 0.24, 0.12, boxstyle="round,pad=0.02",
        facecolor='#9b59b6', edgecolor='black', linewidth=2)
    ax.add_patch(issue_box)
    ax.text(0.82, 0.12, 'NEW AGENT\nVERSION (Prompt)', ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')

    # Traces -> Issue/Fix
    ax.annotate('', xy=(0.70, 0.12), xytext=(0.30, 0.12),
               arrowprops=dict(arrowstyle='->', lw=2.5, color='#34495e'))
    ax.text(0.5, 0.16, 'repeated failure pattern', ha='center', va='center',
            fontsize=9, style='italic', color='#34495e')

    # Structural-replacement arrow reaching back INSIDE the agent loop (the key idea:
    # this is not feedback into the current run, it swaps the agent used next time)
    ax.annotate('', xy=(0.62, 0.5), xytext=(0.82, 0.18),
               arrowprops=dict(arrowstyle='->', lw=3.5, color='#9b59b6',
                              connectionstyle="arc3,rad=-0.35"))
    ax.text(0.86, 0.42, 'replaces the\nagent version\n(not feedback)', ha='center', va='center',
            fontsize=9, fontweight='bold', color='#9b59b6')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('The Learning Loop: Improvement Reaches Back Into the Agent Loop',
                fontsize=16, fontweight='bold', pad=20)

    plt.tight_layout()
    return fig


def render_requirement_doc(doc_name: str) -> HTML:
    """One requirement document from requirement_docs/, read directly off
    disk and shown in the same card `render_report` uses.

    Reads the file itself rather than going through a loaded run, so it can
    be called before `generate_run_history` has produced anything: showing
    an input does not depend on a result existing yet.
    """
    from run_history import DOCS_DIR

    text = (DOCS_DIR / f"{doc_name}.md").read_text()
    return render_report(text, title=doc_name)


def render_injected_feedback(run, run_index: int, total_runs: int, max_chars: int = 1200) -> HTML:
    """The grader's feedback exactly as the agent received it: the message
    injected into the conversation after the first attempt, in a card
    colored like Lesson 4's rejected first draft -- "this got sent back",
    same meaning, now at the scale of a whole batch instead of one run.

    `run_index`/`total_runs` are 1-based numbers for the label ("run 2 of
    5"), not something this function looks up itself; the caller already
    knows which run it is passing in.
    """
    import mistune

    injected = [m for m in run["messages"]
                if m["type"] == "human" and "grader" in m["content"].lower()]

    if not injected:
        body_html = "<p><em>No feedback was injected: this run passed on the first attempt.</em></p>"
    else:
        text = injected[0]["content"]
        truncated = len(text) > max_chars
        body_html = mistune.html(text[:max_chars] + ("..." if truncated else ""))

    label = f"{run['doc_name']}: run {run_index} of {total_runs}, {len(run['grading'])} attempts"

    return HTML(
        _COMPARISON_STYLE +
        f'<div class="lc-compare-card lc-compare-draft">'
        f'<div class="lc-compare-label">{label}</div>'
        f'{body_html}'
        f'</div>'
    )


def render_diff(before: str, after: str, from_label: str = "before", to_label: str = "after") -> HTML:
    """A unified diff as a colored card: added lines on a light green
    background, removed lines on a light pink one, context plain.

    A plain ```diff code fence relies on the notebook frontend's own syntax
    highlighting, which is inconsistent between Jupyter environments and
    exports. Coloring each line explicitly, with the same palette already
    used elsewhere in the course, renders the same everywhere.
    """
    import difflib

    diff_lines = list(difflib.unified_diff(
        before.splitlines(), after.splitlines(),
        fromfile=from_label, tofile=to_label, lineterm="",
    ))

    def _line_html(line: str) -> str:
        esc = _html.escape(line) or "&nbsp;"
        if line.startswith(("+++", "---")):
            return f'<div style="color:#555; font-weight:700;">{esc}</div>'
        if line.startswith("@@"):
            return f'<div style="color:#6b4fa0; font-weight:700; margin:6px 0 2px 0;">{esc}</div>'
        if line.startswith("+"):
            return f'<div style="background:#f1f8f2; color:#3f8f49;">{esc}</div>'
        if line.startswith("-"):
            return f'<div style="background:#fdf3f2; color:#c23b3b;">{esc}</div>'
        return f'<div style="color:#555;">{esc}</div>'

    body = "".join(_line_html(line) for line in diff_lines)
    style = (
        '<style>.lc-diff-card { background:#fafafa; border:1px solid #ddd; '
        'border-radius:10px; padding:14px 18px; margin:14px 0; '
        'font-family:monospace; font-size:0.85em; white-space:pre-wrap; '
        'overflow-x:auto; line-height:1.5; }</style>'
    )
    return HTML(style + f'<div class="lc-diff-card">{body}</div>')


