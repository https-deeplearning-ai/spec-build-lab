# Slide descriptions: Multi AI Agent Systems with crewAI
Source decks: ../repo/slides/Copy of crewai_short course wide slides template (1).pdf (143 slides, wide 16:9, "Wide deck"), ../repo/slides/Copy of crewai_short course 8in wide 9in high.pdf (37 slides, tall 8×9, "Tall deck")
Instructor: João Moura (founder and CEO of crewAI), with Andrew Ng in the introduction

Rich text descriptions of the course slides, organized by lesson in the same order and with the
same lesson titles as the transcripts in `../transcripts/`. Each entry gives the deck and original
slide number, the evidence that ties the slide to a lesson (a verbatim transcript passage, or a
note that none exists), every word visible on the slide, a description of the visual, and what it
teaches.

## How to read this file

- **Lesson assignment rests on transcript content and on the decks' own production notes, not
  video frames.** No lesson videos were available, so no slide was matched to a video by frame
  sampling and there are no timestamps. Each slide was placed in the lesson whose narration
  describes what it shows. The decks were rendered to one PNG per slide and read alongside their
  extracted text layer. Both decks also carry production-note pages (below) that mark where each
  lesson's slides start and which deck holds them; every placement agrees with those notes.
- **Evidence field.** "Narrated" means a transcript passage clearly describes what the slide shows;
  the passage is quoted verbatim, including the transcript's own spelling errors. "Deck-only"
  means no transcript passage matches. "Title card" means the slide is a lesson title card whose
  subtitle is the transcript heading. "Narrated" is the best available proxy for "shown in the
  video", but it is a proxy: a narrated slide may have been on screen for a different span than
  the quote, or replaced by a notebook or the instructor.
- **Lesson numbering comes from the transcripts:** 1 Introduction, 2 Overview, 3 AI Agents,
  4 Create agents to research and write an article, 5 Key elements of AI agents, 6 Multi agent
  customer support automation, 7 Mental framework for agent creation, 8 Key elements of agent
  tools, 9 Tools for a customer outreach campaign, 10 Recap of tools, 11 Key elements of well
  defined tasks, 12 Automate event planning, 13 Recap on tasks, 14 Multi agent collaboration,
  15 Mutli agent collaboration for financial analysis (sic), 16 Build a crew to tailor job
  applications, 17 Next steps with AI agent systems, 18 Conclusion.
  **The decks' production notes use a different numbering** and must not be read as transcript
  lesson numbers. They number the hands-on lessons L2 to L7 and split each into A (concept
  slides, Wide deck), B (code walkthrough, Tall deck) and C (recap, Wide deck). The same L2 to L7
  numbers name the course notebooks (`works/L2/` … `works/L7/` in
  `../notebooks/from-repo/multi-ai-agent-systems-with-crewai-context.md`). The mapping:

  | Transcript lesson | Deck label | Notebook | Slides here |
  |---|---|---|---|
  | 1 Introduction | — | — | Wide 1–2 |
  | 2 Overview | — | — | Wide 3–41 |
  | 3 AI Agents | — | — | Wide 42–68 |
  | 4 Create agents to research and write an article | L2 | L2 | Tall 3–11 |
  | 5 Key elements of AI agents | L3A | — | Wide 70–93 |
  | 6 Multi agent customer support automation | L3B | L3 | Tall 13–17 |
  | 7 Mental framework for agent creation | L3C | — | Wide 94–103 |
  | 8 Key elements of agent tools | L4A | — | Wide 105–120 |
  | 9 Tools for a customer outreach campaign | L4B | L4 | Tall 21–23 |
  | 10 Recap of tools | L4C | — | Wide 121–122 |
  | 11 Key elements of well defined tasks | L5A | — | Wide 124–126 |
  | 12 Automate event planning | L5B | L5 | Tall 25, 27–28 |
  | 13 Recap on tasks | L5C | — | Wide 128–129 |
  | 14 Multi agent collaboration | L6A | — | Wide 131–141 |
  | 15 Mutli agent collaboration for financial analysis | L6B | L6 | Tall 31–33 |
  | 16 Build a crew to tailor job applications | L7 | L7 | Tall 35–37 |
  | 17 Next steps with AI agent systems | — | — | Wide 142 |
  | 18 Conclusion | — | — | Wide 143 |

  Transcripts win wherever the decks disagree. One narration cross-reference also uses its own
  numbering: Lesson 16 says "We're basically going back into lesson one" for the job-application
  example, which the transcripts place in Lesson 2.
- **Production-note pages have no entry of their own.** Fifteen pages are notes from the course
  team, not content: Tall 2 "L2 starts here", Tall 12 "Lesson 3 starts here? · See wide slides
  for L3A · Lesson 3B is narrow slides for code, found here.", Tall 18 "Lesson 3C · see wide
  slides", Tall 19 "Lesson 4A · (move to wide slides)", Tall 20 "Lesson 4B · (code, so narrow
  slides)", Tall 24 "L4C (use wide slides)", Tall 26 "Lesson 5B · (slides to be used within code
  walkthrough)", Tall 29 "Lesson 5C · (see wide slides)", Tall 30 "Lesson 6A (see wide slides) ·
  Lesson 6B (narrow slides here)", Tall 34 "Lesson 7 · All in narrow slides", Wide 69 "L3A starts
  here", Wide 104 "Lesson 4A", Wide 123 "Lesson 5A", Wide 127 "Lesson 5C", Wide 130 "Lesson 6A".
  Each lesson section names the notes that mark it. Tall 1 is the template's cover ("Short Course
  Template · 8 wide by 9 high") and belongs to no lesson.
- **Slide numbering** is `Lesson.Order` in deck order within the lesson. The deck and original
  slide number follow in parentheses so each entry can be traced back to the PDF. Where a lesson
  draws on both decks, the Wide-deck slides come first unless noted.
- **Text on slide** is transcribed verbatim from the extracted text layer; text inside
  screenshots and diagrams (the job posting, résumé, ChatGPT replies, documentation pages) was
  read from the page images, because the text layer skips it. Items are separated by " · ". Code
  is reproduced as code. Typos on the slides are kept as printed.
- **Animations cannot be known** from a PDF, so no entry claims a build order. Many runs of
  consecutive slides differ by one added element (Slides 2.23–2.26, 2.28–2.38, 3.13–3.15,
  3.17–3.24, 7.2–7.5, 14.3–14.5, 14.6–14.8, the six-element overview in Lesson 5 and the
  tool-qualities overview in Lesson 8).
  They read as stages of one build, and the entries say so as a reading of the drawings, not a
  fact.
- **Slide 2.27 renders with an empty table.** Its text layer holds full cell contents, in black,
  but they are covered on the rendered page, probably by masks for an animated reveal. The cell
  text is transcribed from the text layer and the entry says so.
- **One slide's lesson is a judgement call.** Tall 25 is a "[Jupyter Notebook]" placeholder that
  sits between the "L4C" and "Lesson 5B" notes. It is placed in Lesson 12, because Lesson 12
  (deck L5B) is the only code lesson without its own placeholder and Lesson 11 ends "let's jump
  into code real quick". It could instead be a stray copy of Lesson 9's placeholder.
- **Lessons 17 and 18 have only a title card.** The Lesson 17 narration walks through crewai.com,
  the documentation, a "crewAI Assistant" custom GPT, crewAI+ (deploying crews as APIs), YouTube,
  the ChatDev paper, the Discord community and the GitHub repository. None of that is on a
  slide; it was shown on screen. Lesson 1 shows only the course title card and the six-element
  overview.
- All 180 pages are accounted for: 164 entries (2 in Lesson 1, 39 in Lesson 2, 27 in Lesson 3,
  9 in Lesson 4, 24 in Lesson 5, 5 in Lesson 6, 10 in Lesson 7, 16 in Lesson 8, 3 in Lesson 9,
  2 in Lesson 10, 3 in Lesson 11, 3 in Lesson 12, 2 in Lesson 13, 11 in Lesson 14, 3 in Lesson
  15, 3 in Lesson 16, 1 each in Lessons 17 and 18), 15 production notes and the template cover.
- Course-wide visual conventions: every content slide has the crewAI script wordmark (dark brown
  with a red "ai") top left and the DeepLearning.AI logo top right, and a coral-to-crimson wave
  along the bottom edge. Title cards have no wave: the course title "Multi AI Agent Systems with
  crewAI" in coral red, the lesson title in grey below it, and the crewAI and DeepLearning.AI
  logos side by side near the bottom. Section-question slides ("What can I do with
  Multi-Agents?", "Let's recap!") are a single large bold coral headline. Agents are drawn as a
  black computer monitor labelled "AGENT" (or "LLMs") with two curved arrows circling it, tasks
  and answers as light-grey rounded boxes with bold black labels, and people as outline circle
  avatars. Coral fill marks the item the slide is about, for example the highlighted button on an
  overview of qualities.

---

## Lesson 1: Introduction
Transcript: `## Lesson 1: Introduction` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Two Wide-deck slides open the course: the course title card naming the instructor, and the
six-element overview the narration lists as the course's building blocks.

### Slide 1.1 — Title card: Multi AI Agent Systems with crewAI (Wide deck, slide 1)
**Evidence:** Narrated — "Welcome to Multi AI agent systems with CrewAI, built in partnership with CrewAI and taught by its founder and CEO, João Moura."
**Text on slide:** Multi AI Agent Systems · with crewAI · Joao Moura
**Visual description:** Course title card: the course title in coral red, "Joao Moura" in grey
beneath, the crewAI wordmark and the DeepLearning.AI logo side by side near the bottom. No wave.
**What it teaches:** The course title and the instructor.

### Slide 1.2 — Six elements around an agent (Wide deck, slide 2)
**Evidence:** Narrated — "Building blocks you learn include: role-playing, tool use, memory, guardrails, and collaboration."
**Text on slide:** Role Playing · Focus · Tools · Cooperation · Guardrails · Memory
**Visual description:** A large outline person avatar centered above a 3×2 grid of white
rounded buttons with dark outlines: Role Playing, Focus, Tools on the top row; Cooperation,
Guardrails, Memory on the bottom row. Nothing is highlighted. The same layout returns throughout
Lesson 5 with buttons filled in coral one by one.
**What it teaches:** The six qualities of an agent the course is organized around.

---

## Lesson 2: Overview
Transcript: `## Lesson 2: Overview` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Wide slides 3 to 41. The narration covers the course map, the job-application crew that the
course builds last (a job posting, the candidate's original résumé, four agents and their tools,
and the rewritten résumé), agentic automation versus traditional automation, fuzzy versus
strongly typed software, and a lead-scoring example redone with a crew of agents. Slides 2.18 to
2.21 (the interview questions, the two "What can I do with Multi-Agents?" slides and the
repeated course map) are not narrated.

### Slide 2.1 — Title card: Overview (Wide deck, slide 3)
**Evidence:** Title card — "And in this first lesson we are going to understand what makes them tick, how they work, and even look at some of the examples that we're going to do together throughout the entire course."
**Text on slide:** Multi AI Agent Systems · with crewAI · Overview
**Visual description:** Title card in the course style (see conventions), subtitle "Overview".
**What it teaches:** Opens the overview lesson.

### Slide 2.2 — Multi-Agent Collaboration (Wide deck, slide 4)
**Evidence:** Narrated — "We're going to talk about how the different ways that agents can collaborate, not only working sequentially and hierarchically, but also asynchronously."
**Text on slide:** Multi-Agent Collaboration
**Visual description:** Coral headline above three small network drawings, each made of coral
dots joined by coral lines with a tiny outline person avatar beside every dot: a vertical chain
of three; an inverted V (one dot on top joined to two below); and a diamond (one dot on top, two
pairs of dots side by side in the middle, one dot at the bottom). The same three shapes return as
the "Processes" slides in Lesson 14 (Slides 14.6–14.8).
**What it teaches:** Previews the three ways agents can be arranged: in sequence, under a
manager, and in parallel branches.

### Slide 2.3 — What we will cover in this course (Wide deck, slide 5)
**Evidence:** Narrated — "We're going to start with an overview. We're going to build a simple research and write crew. But we are going to go all the way to build more complex ones. Building a customer support crew, our customer outreach crew and event planning agent system in a financial analysis agent system."
**Text on slide:** What we will cover · in this course · Overview · Research & write a technical article · Multi Agents core concepts · Customer support AI Agents · Using Tools at Scale · Customer outreach campaign · Tasks and Processes · Event planning · Agentic Collaboration · Financial analysis · Build a complete Crew · Tailor-made resumes · Next Steps
**Visual description:** Coral two-line title. Two columns of grey bullets, each topic followed by
an indented hollow-bullet example: left column Overview / Research & write a technical article,
Multi Agents core concepts / Customer support AI Agents, Using Tools at Scale / Customer outreach
campaign; right column Tasks and Processes / Event planning, Agentic Collaboration / Financial
analysis, Build a complete Crew / Tailor-made resumes, and Next Steps.
**What it teaches:** The course map: six topics, each paired with the crew built for it.

### Slide 2.4 — What will we build in this course? (Wide deck, slide 6)
**Evidence:** Narrated — "So what we will build in this course. Let's look at this full stack engineering job posting."
**Text on slide:** What will we build in · this course?
**Visual description:** Section-question slide: a large bold coral headline on white.
**What it teaches:** Introduces the worked example of the final crew.

### Slide 2.5 — Job posting: Full Stack Engineer (Wide deck, slide 7)
**Evidence:** Narrated — "If you look close at the job description, you're going to notice that they're basically looking for a full stack developer."
**Text on slide:** Full Stack Engineer · APPLY FOR THIS JOB · Colombia · AI Fund – AI Fund / Full Time / · Job Description: · We are looking for Full Stack Engineers to produce scalable software solutions for our portfolio companies. You'll be part of a cross-functional and will be responsible for the full software development life cycle, from conception to deployment. · As a Full Stack Developer, you should be comfortable around both front-end and back-end coding languages, development frameworks and third-party libraries. You should also be a team player with a knack for visual design and utility. · What You Will be Doing: · - Work with development teams and product managers to ideate software solutions · - Build the front-end of applications through appealing visual design · - Develop and manage well-functioning databases and applications · - Write effective APIs · - Test software to ensure responsiveness and efficiency · - Troubleshoot, debug and upgrade software · - Create security and data protection settings · - Build features and applications
**Visual description:** A screenshot of a job-board page: large grey "Full Stack Engineer" title,
a blue "APPLY FOR THIS JOB" button to its right, location and employer lines below, and the
description in a light-grey panel. No annotations.
**What it teaches:** The input to the job-application crew: a real-looking job posting.

### Slide 2.6 — Job posting with requirements circled (Wide deck, slide 8)
**Evidence:** Narrated — "They want someone that nails both front and back end."
**Text on slide:** Same text as Slide 2.5.
**Visual description:** Slide 2.5 with two coral rounded rectangles drawn over the screenshot:
one around the "As a Full Stack Developer…" paragraph and one around the whole "What You Will be
Doing" list.
**What it teaches:** Which parts of the posting carry the real requirements.

### Slide 2.7 — Job posting: What You Must Bring (Wide deck, slide 9)
**Evidence:** Narrated — "And there is a bunch of like actual criteria in there."
**Text on slide:** What You Must Bring: · Must Haves: · - Proven experience as a Full Stack Developer or similar role · - Experience developing desktop and mobile applications · - Familiarity with common stacks · - Knowledge of multiple front-end languages and libraries (e.g. HTML/ CSS, JavaScript, XML, jQuery) · - Knowledge of multiple object-oriented languages (e.g. Java, Python) and multiple frameworks (e.g. Angular, React, Node.js) · - Familiarity with databases (e.g. MySQL, MongoDB), web servers (e.g. Apache) and UI/UX design · - Excellent communication skills and the ability to have in-depth technical discussions with both the engineering team and business people · - Excellent English language skills · - Self-starter and comfort working in an early-stage environment · - Strong project management and organizational skills
**Visual description:** The second half of the posting in the same light-grey panel; "Node.js"
is underlined as a link.
**What it teaches:** The posting's must-have skills.

### Slide 2.8 — Must Haves with technical skills circled (Wide deck, slide 10)
**Evidence:** Narrated — "They want you to be able to write APIs and to have experience with databases and all of that."
**Text on slide:** Same text as Slide 2.7.
**Visual description:** Slide 2.7 with one coral rounded rectangle around the three technical
lines: front-end languages, object-oriented languages and frameworks, and databases / web
servers / UI/UX design.
**What it teaches:** The concrete technical requirements a tailored résumé must answer.

### Slide 2.9 — Original résumé: Profile (Wide deck, slide 11)
**Evidence:** Narrated — "So this is what Noah's profile looks like. I'm not going to read over it, but I just highlight some of this stuff."
**Text on slide:** Profile · Noah Williams is a distinguished Software Engineering Leader with an 18-year tenure in the technology industry, where he has excelled in leading both remote and in-office engineering teams. His expertise spans across software development, process innovation, and enhancing team collaboration. He is highly proficient in programming languages such as Ruby, Python, JavaScript, TypeScript, and Elixir, alongside deep expertise in various frameworks. Noah's significant experience in data science and machine learning has enabled him to spearhead successful deployments of scalable AI solutions and innovative data model development.
**Visual description:** A bold "Profile" heading over one paragraph of black body text, as a
screenshot of a résumé. No annotations.
**What it teaches:** The candidate's original profile, written for a leadership role.

### Slide 2.10 — Original profile: leadership and AI underlined (Wide deck, slide 12)
**Evidence:** Narrated — "You can see that Noah is trying to highlight how he's a good leader. So he mentioned how he has excelled in leading teams both remote and in an office. He mentioned some data science and machine learning, and he also mentions about deploying scalable AI solutions."
**Text on slide:** Same text as Slide 2.9.
**Visual description:** Slide 2.9 with three phrases underlined in coral: "has excelled in
leading", "data science and machine learning" and "deployments of scalable AI solutions".
**What it teaches:** What the original résumé emphasizes, none of which the posting asks for.

### Slide 2.11 — Original profile: hidden technical skills underlined (Wide deck, slide 13)
**Evidence:** Narrated — "You can see that mentions there that he knows Ruby, Python, JavaScript and that it has been a software engineer for 18 years."
**Text on slide:** Same text as Slide 2.9.
**Visual description:** The profile moved up the slide, now with more coral underlines:
"Software Engineering Leader", "18-year tenure in the technology", "has excelled in leading",
"Ruby, Python, JavaScript, TypeScript, and Elixir", "data science and machine learning" and
"deployments of scalable AI solutions".
**What it teaches:** The matching skills are present but buried.

### Slide 2.12 — Original résumé: work history (Wide deck, slide 14)
**Evidence:** Narrated — "So there are definitely enough things in there that the kind of could explore and that make Noah qualify for this position."
**Text on slide:** BetCraft: CTO — 2013 - 2015 · Led the technology strategy post-Series A funding, directly reporting to the board and guiding the company through a phase of significant technological advancement and network expansion. · His strategic initiatives and partnerships significantly improved platform performance and expanded the company's market reach. · Helped build his initial product using both React and Angular and got pretty good at it. · InnovPet: Founder & CEO (remote) — 2019 - 2022 · Noah founded InnovPet, a startup focused on innovative IoT solutions for pet care, including a revolutionary GPS tracking collar that significantly enhanced pet safety and owner peace of mind. · He was responsible for overseeing product development from concept through execution, working closely with engineering teams and marketing partners to ensure a successful market entry. · Successfully set up an advisory board, established production facilities overseas, and navigated the company through a successful initial funding phase, showcasing his leadership and entrepreneurial acumen. · Built the initial version of the product leveraging MongoDB
**Visual description:** Two bold job headings, each with bullets. The last bullet of each job
("Helped build his initial product using both React and Angular…", "Built the initial version
of the product leveraging MongoDB") is underlined in coral.
**What it teaches:** Relevant hands-on experience sits at the bottom of leadership-focused
entries.

### Slide 2.13 — Agents (Wide deck, slide 15)
**Evidence:** Narrated — "we do that by leveraging four different agents. It's going to have a tech job, a researcher, a personal profile for engineer, a resume strategist for engineers and engineering interviewer preparer."
**Text on slide:** Agents · Tech Job Researcher · Personal Profiler for Engineers · Resume Strategist for Engineers · Engineering Interview Preparer
**Visual description:** Coral "Agents" title above four large outline person avatars in a row,
each with its role name in bold black beneath.
**What it teaches:** The four roles of the job-application crew.

### Slide 2.14 — Agents and their tools (Wide deck, slide 16)
**Evidence:** Narrated — "Together,those four agents, we'll have a few tools that they're going to be able to use from searching the internet all the way to do rag over your resume"
**Text on slide:** Agents · Tech Job Researcher · Personal Profiler for Engineers · Resume Strategist for Engineers · Engineering Interview Preparer · Search the internet · Read websites · Read resume · Perform RAG (Retrieval Augmented Generation) on resume
**Visual description:** Slide 2.13 with a four-item bullet list added below the avatars.
**What it teaches:** The crew's tool set: web search, website reading, résumé reading and
semantic search (RAG) over the résumé.

### Slide 2.15 — Rewritten résumé: Profile (Wide deck, slide 17)
**Evidence:** Narrated — "So this is what the new profile looks like."
**Text on slide:** Profile · Noah Williams is an accomplished Full Stack Developer with 18 years of experience in software engineering. He is proficient in multiple programming languages including JavaScript, Python, and Ruby, and has extensive experience with front-end frameworks such as React and Angular, as well as back-end development using Node.js. His expertise also extends to UI/UX design, mastering HTML, CSS, and JavaScript to create responsive and visually appealing interfaces. Additionally, Noah has a strong background in managing databases like MySQL and MongoDB, ensuring data integrity and security across all applications.
**Visual description:** Same layout as Slide 2.9 with the rewritten paragraph. No annotations.
**What it teaches:** The crew's output: the same person, reframed for the posting.

### Slide 2.16 — Original versus rewritten profile (Wide deck, slide 18)
**Evidence:** Narrated — "Let's compare both for a second." … "But now in the second one, it's kind of like doubling down on the other skills that he has that better match the job that he's applying to."
**Text on slide:** (original) · Profile · [original profile text, as Slide 2.9] · re-written by an AI agent · Profile · [rewritten profile text, as Slide 2.15]
**Visual description:** The two profiles stacked, split by a coral horizontal rule, labelled
"(original)" above and "re-written by an AI agent" below. The original keeps its three coral
underlines from Slide 2.10. The rewrite has coral underlines on "Full Stack Developer with 18
years of experience in software engineering", "JavaScript, Python, and Ruby, and has extensive
experience with front-end frameworks such as React and Angular," and "His expertise also extends
to UI/UX design, mastering HTML, CSS, and JavaScript".
**What it teaches:** Before and after: the rewrite promotes the skills the posting asks for.

### Slide 2.17 — Rewritten work history (Wide deck, slide 19)
**Evidence:** Narrated — "So we can also see these throughout his experience."
**Text on slide:** BetCraft: CTO — 2013 - 2015 · Managed full-stack development during a critical growth phase, enhancing platform capabilities using Angular and React for the front-end, and improving backend services. · InnovPet: Founder & CEO (remote) — 2019 - 2022 · Developed an innovative IoT solution for pet care, from database management with MongoDB to front-end user interface design, ensuring a seamless user experience. · EliteDevs: Engineering Manager (remote) — 2018 - 2019 · Implemented new product features using Ruby on Rails and React, focusing on both server-side and client-side code.
**Visual description:** Three bold job headings, each now with a single hands-on bullet.
**What it teaches:** The rewrite also trims each job down to the matching technical work.

### Slide 2.18 — Key Interview Questions and Talking Points (Wide deck, slide 20)
**Evidence:** Deck-only. The Lesson 2 narration does not reach the interview material; Lesson 16 narrates the crew's interview output ("Now let's check the interview materials, the things that you're going to use to prepare in case you do get the interview.").
**Text on slide:** Key Interview Questions and Talking Points for Noah Williams · Technical Skills and Experience: · 1. Front-end Development: · Question: "Could you walk us through your experience using front-end frameworks like React and Angular in your projects at BetCraft and EliteDevs?" · Talking Point: Discuss the challenges and outcomes of integrating these frameworks into existing systems. · 2. Back-end and API Development: · Question: "At DriveAI, you developed a central API. What were some of the key considerations and challenges you faced in optimizing backend logic and database efficiency?" · Talking Point: Highlight the impact of these optimizations on system performance and user satisfaction. · 3. Database Management: · Question: "You have significant experience with MySQL and MongoDB. Can you share how you ensured data integrity and security in your role at InnovPet and DataKernel?" · Talking Point: Focus on the strategies employed to manage large datasets and ensure high availability and security. · Project Management and Leadership: · 4. Strategic Initiatives: · Question: "As Director of Software Engineering at DataKernel, you've led strategic initiatives integrating AI technologies. How did you align these technologies with business goals?" · Talking Point: Emphasize the role of AI in enhancing product capabilities and the challenges of implementing such advanced technologies. · 5. Team Leadership and Culture Building: · Question: "Managing remote teams across multiple time zones presents unique challenges. How did you foster a culture of transparency and high performance at DataKernel?" · Talking Point: Discuss methods for motivating teams and maintaining productivity in a remote setting.
**Visual description:** A dense screenshot of a generated document: bold title and section
headings, numbered topics, each with bold "Question:" and "Talking Point:" bullets.
**What it teaches:** The crew's second output: interview questions and talking points tied to
the candidate's history.

### Slide 2.19 — What can I do with Multi-Agents? (Wide deck, slide 21)
**Evidence:** Deck-only.
**Text on slide:** What can I do with · Multi-Agents?
**Visual description:** Section-question slide, large bold coral headline. The logos here are
drawn smaller than on other slides.
**What it teaches:** Introduces a list of use cases.

### Slide 2.20 — What can I do with Multi-Agents? (list) (Wide deck, slide 22)
**Evidence:** Deck-only.
**Text on slide:** What can I do with Multi-Agents? · Tailor job applications for each job description · Generate reports on many fronts (ex. financials, HR, development, etc..) · Help research and qualify leads · Documentation generation · Marketing analysis, research and creation · Monitoring manufacturing data
**Visual description:** Coral title above six grey bullets; the parenthetical in the second
bullet is set smaller.
**What it teaches:** Example use cases for multi-agent systems.

### Slide 2.21 — What we will cover in this course (repeat) (Wide deck, slide 23)
**Evidence:** Deck-only.
**Text on slide:** Same as Slide 2.3, except "Tailor made resumes" has no hyphen.
**Visual description:** Same as Slide 2.3.
**What it teaches:** Repeats the course map.

### Slide 2.22 — What is Agentic Automation? (Wide deck, slide 24)
**Evidence:** Narrated — "So, what is agentic automation?"
**Text on slide:** What is · Agentic Automation?
**Visual description:** Section-question slide, large bold coral headline.
**What it teaches:** Introduces agentic automation.

### Slide 2.23 — Point A to point B (Wide deck, slide 25)
**Evidence:** Narrated — "In the past you would say, hey, "I want to go from point A to point B." And you can write code to automate that."
**Text on slide:** A · B
**Visual description:** Two outline circles labelled A (top left) and B (bottom right) joined by
a thick dark-grey diagonal line. First of four slides that read as one build (2.23–2.26).
**What it teaches:** Traditional automation as one fixed path.

### Slide 2.24 — An edge case branches in (Wide deck, slide 26)
**Evidence:** Narrated — "And then what happens is that as edge cases appear, you start to kind of make that a little more complex."
**Text on slide:** A · B · C
**Visual description:** Slide 2.23 with circle C added below A, joined by a short branch to the
A–B line.
**What it teaches:** Each edge case adds a branch to the code.

### Slide 2.25 — More branches (Wide deck, slide 27)
**Evidence:** Narrated — "Where like, well, if X do C, if z do D, and you can see how these things can become quite complex, especially as you start adding more and more edge cases."
**Text on slide:** D · A · B · C
**Visual description:** Slide 2.24 with circle D added on the right, joined by a second branch
near B.
**What it teaches:** Conditions accumulate into a complex code base.

### Slide 2.26 — The whole space instead of the paths (Wide deck, slide 28)
**Evidence:** Narrated — "The beauty of agentic automation is that you don't need to drown the map. You can show the options."
**Text on slide:** D · A · B · C
**Visual description:** The four circles with all connecting lines removed, enclosed together
in one dashed freeform outline.
**What it teaches:** Agentic automation is given the options rather than every hard-coded path.

### Slide 2.27 — Fuzzy inputs, transformations, outputs (Wide deck, slide 29)
**Evidence:** Narrated — "So in regular applications you have strong inputs." … "You have a fuzzy input, meaning that you don't know what the user is input into your application."
**Text on slide:** Fuzzy inputs, transformations, outputs · Traditional Software Development · AI Software Development · Inputs · - text (string) with defined set ("happy", "calm") · - numeric (int, float) · Fuzzy inputs: Open-ended text · - Tabular data · - markdown · - Text · - math operation · Transformations · - Math calculation (+ - ➗✖ ) · - f"Hello {first_name}, how are you?" · - if, elif, else · - for/while loops · Fuzzy transformations · - Extract list of key words · - Rewrite as a paragraph · - Answer a question · - Brainstorm new ideas · - Perform logic/math reasoning · Outputs · - text (string) with defined set ("Positive", "Neutral") · - numeric (int, float), · Fuzzy outputs: text · - Paragraph · - Number(s) · - JSON · - Markdown · Notes · - Can be replicated · - Probabilistic: can be different every time
**Visual description:** A black title over a bordered table: columns "Traditional Software
Development" and "AI Software Development", rows Inputs, Transformations, Outputs and Notes.
On the rendered page every body cell is blank except a stray `")` fragment; the cell text above
comes from the PDF's text layer, where it is present in black but covered on the page.
**What it teaches:** Traditional software has typed inputs, deterministic transformations and
reproducible outputs; AI software takes open-ended text, transforms it with an LLM, and returns
outputs whose form can vary from run to run.

### Slide 2.28 — Data Collection and Analysis: the funnel (Wide deck, slide 30)
**Evidence:** Narrated — "Your company probably has a website that captures leads data through a form. And those leads eventually go into your sales team that are going to try to make them into customers."
**Text on slide:** Data Collection and Analysis · Web Site Visitor · LEAD · SALE · High Priority · Medium Priority · Low Priority
**Visual description:** Coral title. Three filled coral boxes in a row joined by thin coral
arrows: Web Site Visitor → LEAD → SALE, with "High Priority / Medium Priority / Low Priority" in
small grey text under SALE. First of eleven slides that read as one build (2.28–2.38).
**What it teaches:** The classic lead funnel.

### Slide 2.29 — The lead form (Wide deck, slide 31)
**Evidence:** Narrated — "So you have your form and you capture information about this company through that form,"
**Text on slide:** Data Collection and Analysis · Web Site Visitor · LEAD · SALES · High Priority · Medium Priority · Low Priority
**Visual description:** Slide 2.28 shifted left, the last box now reading "SALES", with a stack
of grey horizontal lines (a form) under Web Site Visitor.
**What it teaches:** Lead data is captured through a form.

### Slide 2.30 — Rule-based classification (Wide deck, slide 32)
**Evidence:** Narrated — "and then goes through an automated process of classifying these leads"
**Text on slide:** Same as Slide 2.29.
**Visual description:** Slide 2.29 with a small coral decision tree (one node branching to two)
added under LEAD.
**What it teaches:** Leads pass through a fixed classification step.

### Slide 2.31 — Classification rules (Wide deck, slide 33)
**Evidence:** Narrated — "like, hey, is this company a big company has more than ten employees. Is this company located in the U.S. or is this company located somewhere else?"
**Text on slide:** Data Collection and Analysis · Web Site Visitor · LEAD · SALES · High Priority · Medium Priority · Low Priority · > 10 employees · Located in US
**Visual description:** Slide 2.30 with the tree's two branches labelled "> 10 employees" and
"Located in US".
**What it teaches:** Traditional lead scoring is a few hard-coded data points.

### Slide 2.32 — Classification rules (repeat) (Wide deck, slide 34)
**Evidence:** Narrated — "So this is regular data analysis and data collection."
**Text on slide:** Same as Slide 2.31.
**Visual description:** Identical to Slide 2.31.
**What it teaches:** Closes the description of the traditional process.

### Slide 2.33 — A crew of AI agents replaces the rules (Wide deck, slide 35)
**Evidence:** Narrated — "Let's add a crew of AI agents on the lead generation process."
**Text on slide:** Data Collection and Analysis · Web Site Visitor · LEAD · Crew of AI Agents
**Visual description:** Web Site Visitor → LEAD → a white box with a thick coral outline reading
"Crew of AI Agents". The decision tree and SALES box are gone.
**What it teaches:** The crew takes the place of the classification rules.

### Slide 2.34 — Crew step: research (Wide deck, slide 36)
**Evidence:** Narrated — "you could have this AI agents do research. Go out there and do data collection."
**Text on slide:** Data Collection and Analysis · Web Site Visitor · LEAD · Crew of AI Agents · research · (data collection)
**Visual description:** Slide 2.33 with a coral-outlined box "research (data collection)" under
the crew box.
**What it teaches:** First crew step: gather information about the lead.

### Slide 2.35 — Crew step: comparison (Wide deck, slide 37)
**Evidence:** Narrated — "Then you can also have this agents drawn comparisons between these companies and companies that you already have in your data set"
**Text on slide:** … · research · (data collection) · comparison
**Visual description:** Slide 2.34 with a "comparison" box added below.
**What it teaches:** Second step: compare with known customers.

### Slide 2.36 — Crew step: scoring (Wide deck, slide 38)
**Evidence:** Narrated — "And then you can also have this AI agents do some scoring so they can actually score this company"
**Text on slide:** … · research · (data collection) · comparison · scoring
**Visual description:** Slide 2.35 with a "scoring" box added below.
**What it teaches:** Third step: score the lead.

### Slide 2.37 — Crew step: talking points (Wide deck, slide 39)
**Evidence:** Narrated — "And then the final point is coming up with talking points."
**Text on slide:** … · research · (data collection) · comparison · scoring · talking points
**Visual description:** Slide 2.36 with a "talking points" box added below.
**What it teaches:** Fourth step: prepare what sales should say.

### Slide 2.38 — Crew output to sales (Wide deck, slide 40)
**Evidence:** Narrated — "And now you can take that and send that to your sales team."
**Text on slide:** Data Collection and Analysis · Web Site Visitor · LEAD · Crew of AI Agents · research · (data collection) · comparison · scoring · talking points · SALES · High Priority · Medium Priority · Low Priority
**Visual description:** Slide 2.37 with an arrow from the crew box to a filled coral SALES box,
the three priority levels beneath it.
**What it teaches:** The crew's richer output feeds the same sales prioritization.

### Slide 2.39 — What are AI Agents? (Wide deck, slide 41)
**Evidence:** Narrated — "But in the end of the day what are agents. So let's talk about that for a second and step back."
**Text on slide:** What are · AI Agents?
**Visual description:** Section-question slide, large bold coral headline.
**What it teaches:** Hands over to the next lesson's question.

---

## Lesson 3: AI Agents
Transcript: `## Lesson 3: AI Agents` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Wide slides 42 to 68. The narration goes from LLMs predicting the next token, through the
regular prompting experience and its feedback loop, to the agent (an LLM that asks and answers
its own questions, takes a task, uses tools), multi-agent systems, and crewAI's offer and
building blocks.

### Slide 3.1 — Title card: AI Agents (Wide deck, slide 42)
**Evidence:** Title card.
**Text on slide:** Multi AI Agent Systems · with crewAI · AI Agents
**Visual description:** Title card in the course style, subtitle "AI Agents".
**What it teaches:** Opens the lesson.

### Slide 3.2 — LLMs and their vendors (Wide deck, slide 43)
**Evidence:** Narrated — "They come with all these different shapes and sizes and forms. And there's a bunch of different vendors. You have Open AI, you have Hugging Face, you having a Ollama."
**Text on slide:** OpenAI · HuggingFace · Ollama · and more · LLMs
**Visual description:** A black rounded "LLMs" label overlapping a document icon (lined pages),
with the vendor names right-aligned under a thin rule to its left. First of the diagrams that
grow into Slide 3.12.
**What it teaches:** LLMs are available from many providers.

### Slide 3.3 — LLMs predict the next token (Wide deck, slide 44)
**Evidence:** Narrated — "And what those LLMs do is predict the most likely next token."
**Text on slide:** OpenAI · HuggingFace · Ollama · and more · LLMs · predict the next · most likely token · (create content)
**Visual description:** Slide 3.2 with a curved black arrow from the LLMs icon down to "predict
the next most likely token" and "(create content)" in bold coral, next to a speech-bubble icon.
**What it teaches:** An LLM's core operation is next-token prediction.

### Slide 3.4 — Fill in the blank (Wide deck, slide 45)
**Evidence:** Narrated (concept only) — "And what those LLMs do is predict the most likely next token." The example sentence is not spoken.
**Text on slide:** I'm an engineer and I really love · __________
**Visual description:** A large grey sentence with a dashed blank line beneath it.
**What it teaches:** Sets up a next-token example.

### Slide 3.5 — The predicted word (Wide deck, slide 46)
**Evidence:** Narrated (concept only), as Slide 3.4.
**Text on slide:** I'm an engineer and I really love · programming
**Visual description:** The blank replaced by "programming" in bold coral.
**What it teaches:** The model fills the blank with the most likely word.

### Slide 3.6 — The prediction depends on context (Wide deck, slide 47)
**Evidence:** Narrated (concept only), as Slide 3.4.
**Text on slide:** I'm an engineer and I really love · programming
**Visual description:** Slide 3.5 with two hand-drawn coral arrows: one arcing from "engineer"
over to "love", and one curling from the end of the sentence back to "programming".
**What it teaches:** The earlier words ("engineer") steer which word comes next.

### Slide 3.7 — LLMs predict the next token (repeat) (Wide deck, slide 48)
**Evidence:** Narrated — as Slide 3.3.
**Text on slide:** Same as Slide 3.3.
**Visual description:** Identical to Slide 3.3, shown again after the example.
**What it teaches:** Returns to the diagram.

### Slide 3.8 — Regular Prompting Experience (Wide deck, slide 49)
**Evidence:** Narrated — "you're going to end up having like a regular prompting experience similar to one you get with ChatGPT, where you kind of got to give feedback to it"
**Text on slide:** Regular Prompting · Experience · LLMs
**Visual description:** A monitor icon labelled "LLMs" on the left and a person icon on the
right, joined top and bottom by two bracket-shaped lines forming a loop.
**What it teaches:** Chatting with an LLM is a loop between the model and a person.

### Slide 3.9 — Let's use chatGPT! (Wide deck, slide 50)
**Evidence:** Narrated — "so let's use ChatGPT for a second to see how exactly does that interaction works and why."
**Text on slide:** Let's use chatGPT!
**Visual description:** A single bold coral line, centered.
**What it teaches:** Introduces a live ChatGPT demo (the demo itself is not on a slide).

### Slide 3.10 — Regular Prompting Experience (repeat) (Wide deck, slide 51)
**Evidence:** Narrated — "So what you quickly realize here is that through the interactions you can get a better results, but you quickly become a blocker."
**Text on slide:** Same as Slide 3.8.
**Visual description:** Identical to Slide 3.8.
**What it teaches:** The person in the loop is the bottleneck.

### Slide 3.11 — LLMs imply a kind of cognition (Wide deck, slide 52)
**Evidence:** Narrated — "they create a state where they kind of have cognition. And by that, I mean that they can reasonably react."
**Text on slide:** OpenAI · HuggingFace · Ollama · and more · LLMs · predict the next · most likely token · (create content) · implies on a kind · of cognition · (reasonably react)
**Visual description:** Slide 3.3 with a second curved arrow leading left to "implies on a kind
of cognition" and "(reasonably react)" in bold coral, next to an icon of two small monitors in a
loop.
**What it teaches:** Next-token prediction yields enough reasoning to choose between options.

### Slide 3.12 — An agent is born (Wide deck, slide 53)
**Evidence:** Narrated — "if you can have the LLM to kind of insert some questions, an agent is born."
**Text on slide:** OpenAI · HuggingFace · Ollama · and more · LLMs · predict the next · most likely token · (create content) · implies on a kind · of cognition · (reasonably react) · An agent is born 🐣
**Visual description:** The full chain from Slide 3.11 moved to the upper left, with "An agent
is born" and a hatching-chick emoji in grey below.
**What it teaches:** An agent is an LLM that questions and answers itself.

### Slide 3.13 — AGENT (Wide deck, slide 54)
**Evidence:** Narrated — "So the agent is born when you get these LLM to basically into in their thinking process throughout it ask questions and answer the questions itself"
**Text on slide:** AGENT
**Visual description:** The course's agent icon alone: a black monitor labelled "AGENT" with two
curved arrows circling it. First of three slides that read as one build (3.13–3.15).
**What it teaches:** The agent as a self-looping model.

### Slide 3.14 — Task → AGENT → Answer (Wide deck, slide 55)
**Evidence:** Narrated — "it allows you to pass a task into this agent. And throughout this thinking process, this agent can then come up with a better answer."
**Text on slide:** Task · AGENT · Answer
**Visual description:** A grey "Task" box with an arrow down into the agent icon, and an arrow
from the agent down to a grey "Answer" box.
**What it teaches:** An agent turns a task into an answer by iterating on its own.

### Slide 3.15 — Tools feed the agent (Wide deck, slide 56)
**Evidence:** Narrated — "and that's the ability to use tools."
**Text on slide:** Task · Tools · AGENT · Answer
**Visual description:** Slide 3.14 with a smaller grey "Tools" box on the left, an arrow pointing
into the agent.
**What it teaches:** Tools let the agent act on the outside world; with them it is "a fully
fledged agent".

### Slide 3.16 — Multi Agent Systems (Wide deck, slide 57)
**Evidence:** Narrated — "So let's talk real quick about what our multi-agent systems."
**Text on slide:** Multi Agent Systems
**Visual description:** A single bold coral headline, left of center.
**What it teaches:** Introduces multi-agent systems.

### Slide 3.17 — One agent (Wide deck, slide 58)
**Evidence:** Narrated — "So multi-agent systems grow on top of the agent behavior that we just described."
**Text on slide:** AGENT
**Visual description:** Identical to Slide 3.13. First of eight slides that read as one build
(3.17–3.24).
**What it teaches:** Starts from the single agent.

### Slide 3.18 — Two agents (Wide deck, slide 59)
**Evidence:** Narrated — "Where instead of having just one agent, you can now can have multiple of them."
**Text on slide:** AGENT · AGENT
**Visual description:** Two smaller agent icons side by side.
**What it teaches:** Several agents in one system.

### Slide 3.19 — A task to the first agent (Wide deck, slide 60)
**Evidence:** Narrated — "So whenever you task an agent with something"
**Text on slide:** Task · AGENT · AGENT
**Visual description:** Slide 3.18 with a "Task" box and arrow above the left agent.
**What it teaches:** The first agent receives a task.

### Slide 3.20 — The first agent tasks the second (Wide deck, slide 61)
**Evidence:** Narrated — "this agent can also task another agent with another task."
**Text on slide:** Task · Task · AGENT · AGENT
**Visual description:** A second "Task" box above the right agent, with a diagonal arrow from the
left agent up to it.
**What it teaches:** Agents can hand work to each other.

### Slide 3.21 — One final answer (Wide deck, slide 62)
**Evidence:** Narrated — "And in the end you get one single final answer."
**Text on slide:** Task · Task · AGENT · AGENT · Answer
**Visual description:** Slide 3.20 with a long arrow from between the agents down to one
"Answer" box.
**What it teaches:** The system still returns a single answer.

### Slide 3.22 — Researcher and Writer (Wide deck, slide 63)
**Evidence:** Narrated — "You can have one agent, for example, being a researcher and another agent being a writer."
**Text on slide:** Researcher · Writer · Task · Task · AGENT · AGENT
**Visual description:** Slide 3.20 (no Answer box) with a coral bar and coral "Researcher" under
the left agent and a dark-grey bar and dark "Writer" under the right one.
**What it teaches:** Each agent specializes in one job.

### Slide 3.23 — Different models per agent (Wide deck, slide 64)
**Evidence:** Narrated — "So you can have your researcher running on Llama-3, while your writers running on GPT-4."
**Text on slide:** Researcher · Llama 3 70B · Writer · GPT-4 · Task · Task · AGENT · AGENT
**Visual description:** Slide 3.22 with the model names in small type under each role: "Llama 3
70B" in coral, "GPT-4" in grey.
**What it teaches:** Agents in one system can run on different LLMs.

### Slide 3.24 — Two pairs of agents (Wide deck, slide 65)
**Evidence:** Narrated — "where you can actually say, "well, now I want to multiple multiple agents," but this is getting to meta."
**Text on slide:** Task · Task · Task · Task · AGENT · AGENT · AGENT · AGENT
**Visual description:** Two copies of the two-agent task handoff (Slide 3.20), one upper left and
one lower right.
**What it teaches:** Multi-agent groups can themselves be combined.

### Slide 3.25 — Framework & Platform (Wide deck, slide 66)
**Evidence:** Narrated — "The first thing is, it breaks all these concepts into very simple structures." … "it also offers a platform for bringing these agents into production."
**Text on slide:** Framework & Platform · Breaks all these concepts into simple structures · Provides a pattern to put these systems together · Provides tools / skills ready to be used by agents · Gives you a model to build custom tools for agents · Offers a platform for bringing these agents into production
**Visual description:** Coral title over five grey bullets.
**What it teaches:** What crewAI offers. (The narration says "a module to build custom tools or
agents" where the slide says "a model to build custom tools for agents".)

### Slide 3.26 — What is crewAI? (Wide deck, slide 67)
**Evidence:** Narrated — "Before we jump into examples, let's talk about what is crewAI?"
**Text on slide:** What is crewAI? · crewai.com
**Visual description:** Section-question slide with "crewai.com" in smaller bold coral beneath.
It comes after Slide 3.25 in the deck, though the narration asks the question first.
**What it teaches:** Names the framework and its website.

### Slide 3.27 — Initial Building Blocks (Wide deck, slide 68)
**Evidence:** Narrated — "So let's start looking at some of our initial building blocks. In this case, agents, tasks and crews."
**Text on slide:** Initial Building Blocks · Agents · Tasks · Crews
**Visual description:** Coral title over three large grey words stacked and centered.
**What it teaches:** crewAI's three core abstractions.

---

## Lesson 4: Create agents to research and write an article
Transcript: `## Lesson 4: Create agents to research and write an article` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Tall slides 3 to 11, after the production note Tall 2 ("L2 starts here"). The lesson is the
first notebook walkthrough (deck L2, notebook `works/L2/`): a title card, a notebook
placeholder, one slide on sequential tasks, a documentation screenshot, and a recap.

### Slide 4.1 — Title card: Create agents to research and write an article (Tall deck, slide 3)
**Evidence:** Title card.
**Text on slide:** Multi AI Agent Systems · with crewAI · Create agents to research and · write an article
**Visual description:** Title card in the course style on the tall page.
**What it teaches:** Opens the first hands-on lesson.

### Slide 4.2 — [Jupyter Notebook] (Tall deck, slide 4)
**Evidence:** Narrated — "Now let's get our hands on and actually build our first multi-agent systems ourselves."
**Text on slide:** [Jupyter Notebook]
**Visual description:** A placeholder: grey bracketed text near the top of an otherwise empty
content page.
**What it teaches:** Marks where the video switches to the notebook.

### Slide 4.3 — Tasks are Sequential by Default (Tall deck, slide 5)
**Evidence:** Narrated — "One thing that I want to call out is that by default, a crew operates sequentially, meaning that one task is going to be executed after the next." Also: "this verbose setting being set to two".
**Text on slide:** Tasks are Sequential · by Default · `crew = Crew(` · `agents=[planner, writer, editor],` · `tasks=[plan, write, edit],` · `verbose=2` · `)` · 1. plan · 2. write · 3. edit
**Visual description:** Black title over a code block in a grey monospace face:
```
crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=2
)
```
The `tasks=[…]` line is boxed in coral, and a thin line leads from it to a black-bordered box
listing "1. plan 2. write 3. edit".
**What it teaches:** A crew runs its tasks in list order by default, so the order of `tasks`
matters; each task's output feeds the next.

### Slide 4.4 — crewAI documentation screenshots (Tall deck, slide 6)
**Evidence:** Narrated — "So let me go ahead and tell you how the documentation that you find in crewAI is actually written by a crew."
**Text on slide:** crewAI · v0.22.4 · 9.8k · 1.2k · crewAI · Home · Core Concepts · How to Guides · Tools Docs · Examples · Telemetry · crewAI Documentation · Cutting-edge … empowers … · Agents · What is an Agent? · Agent Attributes · Creating an Agent · Conclusion · Tasks · Tools · Processes · Crews · Collaboration · What is an Agent? · An agent is an autonomous unit programmed to: · Perform tasks · Make decisions · Communicate with other agents · Think of an agent as a member of a team, with specific skills and a particular job to do. Agents can have different roles like 'Researcher', 'Writer', or 'Customer Support', each contributing to the overall goal of the crew. · Collaboration · Collaboration Fundamentals · Core of Agent Interaction · Collaboration in CrewAI is fundamental, enabling agents to combine their skills, share information, and assist each other in task execution, embodying a truly cooperative ecosystem. · Information Sharing: Ensures all agents are well-informed and can contribute effectively by sharing data and findings. · Task Assistance: Allows agents to seek help from peers with the required expertise for specific tasks. · Resource Allocation: Optimizes task execution through the efficient distribution and sharing of resources among agents. · Enhanced Attributes for Improved Collaboration · The Crew class has been enriched with several attributes to support advanced functionalities: · Language Model Management (`manager_llm`, `function_calling_llm`): … · Process Flow (`process`): Defines the execution logic (e.g., sequential, hierarchical) to streamline task distribution and execution. · Verbose Logging (`verbose`): Offers detailed logging capabilities for monitoring and debugging purposes. It supports both integer and boolean types to indicate the verbosity level.
**Visual description:** Three overlapping screenshots of the crewAI documentation site, each
with a coral header bar showing the GitHub badge "crewAI v0.22.4", 9.8k stars and 1.2k forks:
the documentation home, the "Agents" page with a blue-bordered "What is an Agent?" callout, and
the "Collaboration" page. The bottom screenshot's text is very small; the lines elided with "…"
are too small to read.
**What it teaches:** The crewAI docs, which the narration says a crew writes, and the version of
the docs shown (v0.22.4).

### Slide 4.5 — Let's recap! (Tall deck, slide 7)
**Evidence:** Narrated — "Let's do a quick recap about everything that we learned so far."
**Text on slide:** Let's recap!
**Visual description:** Section-question slide: large bold coral line, centered.
**What it teaches:** Opens the recap.

### Slide 4.6 — Recap: an agent (Tall deck, slide 8)
**Evidence:** Narrated — "They're LLMs that can talk to itself. They have in your thought process. And they can receive tasks and use tools in order to give way more complex answers"
**Text on slide:** Task · LLMs · Tools · Answer
**Visual description:** Task box → a looping monitor labelled "LLMs" → Answer box, with a "Tools"
box pointing in from the left. Same shape as Slide 3.15, with "LLMs" in place of "AGENT".
**What it teaches:** Recaps the agent: an LLM in a loop that takes tasks and uses tools.

### Slide 4.7 — Recap: agents pass tasks along (Tall deck, slide 9)
**Evidence:** Narrated — "We also learned that you can have multiple agents hooked up together, showed that one agent can pass tasks to another agent."
**Text on slide:** Task · Task · LLMs · LLMs · Researcher · Writer
**Visual description:** Two Task → LLMs pairs with a diagonal handoff arrow between them, a coral
"Researcher" bar under the left and a dark "Writer" bar under the right (as Slide 3.22).
**What it teaches:** Recaps specialized agents handing work to one another.

### Slide 4.8 — Recap: Agent, Task, Crew (Tall deck, slide 10)
**Evidence:** Narrated — "We learned about agents, tasks, and crews, and we now know how to put them together."
**Text on slide:** Agent · Task · Crew
**Visual description:** Three grey rounded boxes with coral outlines, stacked inside a larger
coral rounded frame.
**What it teaches:** The three building blocks, grouped.

### Slide 4.9 — Recap: lessons learned (Tall deck, slide 11)
**Evidence:** Narrated — "First, we learned that agents perform better when role-playing. Two you should focus on goals and expectations whenever creating or tasks in your agents."
**Text on slide:** Agent · Task · Crew · Agents perform better when role-playing · You should focus on goals and expectations · One Agent can do multiple tasks · Tasks and Agents should be granular · Tasks can be executed in different ways · It's pretty easy to create multi-agents with crewAI
**Visual description:** The Agent/Task/Crew frame from Slide 4.8 on the left, six grey bullets
on the right.
**What it teaches:** Six takeaways: role-play, clear goals and expectations, one agent may do
several tasks, keep tasks and agents granular, tasks can run in different ways (sequential,
parallel, hierarchical), and crewAI makes this easy.

---

## Lesson 5: Key elements of AI agents
Transcript: `## Lesson 5: Key elements of AI agents` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Wide slides 70 to 93, after the production note Wide 69 ("L3A starts here"). The narration walks
the six elements in order, returning to the six-button overview between them with one more
button filled in coral each time (Slides 5.9, 5.12, 5.15, 5.17, 5.19). Memory has no overview
return; it ends the lesson with three slides on memory types.

### Slide 5.1 — Title card: Key elements of AI agents (Wide deck, slide 70)
**Evidence:** Title card.
**Text on slide:** Multi AI Agent Systems · with crewAI · Key elements of AI agents
**Visual description:** Title card in the course style.
**What it teaches:** Opens the lesson.

### Slide 5.2 — What makes a great Agent? (Wide deck, slide 71)
**Evidence:** Narrated — "So, what does make an agent great?"
**Text on slide:** What makes a great Agent?
**Visual description:** Black title above a large outline person avatar.
**What it teaches:** Poses the lesson's question.

### Slide 5.3 — The six elements (Wide deck, slide 72)
**Evidence:** Narrated — "The first one is role playing. The second one is focus. The third one is tools, the fourth one is cooperation. The fifth one is guardrails, and the sixth one is memory."
**Text on slide:** Role Playing · Focus · Tools · Cooperation · Guardrails · Memory
**Visual description:** Identical to Slide 1.2: avatar over a 3×2 grid of white buttons, none
highlighted.
**What it teaches:** The six elements of a great agent.

### Slide 5.4 — Role Playing (Wide deck, slide 73)
**Evidence:** Narrated — "So let's start with role play."
**Text on slide:** Role Playing
**Visual description:** Grey "Role Playing" heading over a person avatar filled in solid red.
**What it teaches:** Opens the first element.

### Slide 5.5 — Role Playing: plain prompt (Wide deck, slide 74)
**Evidence:** Narrated — "But in here, I just asked ChatGPT to give me an analysis on the Tesla stock."
**Text on slide:** Role Playing · You · give me an analysis on tesla stock
**Visual description:** "Role Playing" beside the logo at top left; below, one chat message in
ChatGPT style: a blue circular user icon, bold "You", and the prompt.
**What it teaches:** The baseline prompt with no role.

### Slide 5.6 — Role Playing: prompt with a role (Wide deck, slide 75)
**Evidence:** Narrated — "Saying that "you are a FINRA approved financial analyst.""
**Text on slide:** Role Playing · You · give me an analysis on tesla stock · You · you are a FINRA approved financial analyst. · give me an analysis on tesla stock
**Visual description:** Slide 5.5 with a second "You" message below adding the role line.
**What it teaches:** The same request with a specific role set.

### Slide 5.7 — Roles, Goals, Backstory (Wide deck, slide 76)
**Evidence:** Narrated — "make sure that you're setting the appropriate roles, the appropriate goals and their profit backstories"
**Text on slide:** Role Playing · You · give me an analysis on tesla stock · You · you are a FINRA approved financial analyst. · give me an analysis on tesla stock · Roles · Goals · Backstory
**Visual description:** Slide 5.6 with a three-item grey bullet list on the right.
**What it teaches:** Role playing is set through an agent's role, goal and backstory.

### Slide 5.8 — Role Playing: the two answers (Wide deck, slide 77)
**Evidence:** Narrated — "The first answer you can see that it basically mentions about many factors." … "But the second one you can see that is already digging straight into it, talking about Nasdaq, talking about like the actual Tesla stock and talking about EV manufacturing market."
**Text on slide:** Role Playing · ChatGPT · Tesla's stock analysis involves looking at various factors, including financial performance, industry trends, technological advancements, competition, and market sentiment. Here's a brief overview: · 1. Financial Performance: Tesla's financial performance has been a mix of impressive revenue growth and periodic profitability challenges. Investors often scrutinize metrics like revenue, earnings per share (EPS), and gross margins. Quarterly earnings reports, as well as annual filings, provide insights into the company's financial health. · ChatGPT · As a financial analyst, I'd be happy to provide an analysis of Tesla's stock. Please note that this information is for educational purposes only and should not be considered as financial advice. · Company Overview: · Tesla, Inc. (NASDAQ: TSLA) is a leading electric vehicle (EV) manufacturer, energy storage company, and solar panel manufacturer. Founded in 2003, Tesla has become synonymous with innovation in the automotive industry, particularly in the realm of sustainable transportation. · Recent Performance:
**Visual description:** Two ChatGPT reply excerpts stacked, each with the ChatGPT logo and bold
"ChatGPT"; the second has bold "Company Overview:" and "Recent Performance:" headings and is cut
off after the second heading.
**What it teaches:** The role-framed answer is more specific (ticker, sector) than the generic
one.

### Slide 5.9 — Overview: Role Playing done (Wide deck, slide 78)
**Evidence:** Narrated — "All right. So we talked about role play. Let's talk about focus."
**Text on slide:** Role Playing · Focus · Tools · Cooperation · Guardrails · Memory
**Visual description:** The six-button overview with "Role Playing" filled coral.
**What it teaches:** Progress marker.

### Slide 5.10 — Focus: one agent, many hats (Wide deck, slide 79)
**Evidence:** Narrated — "So another thing that makes agents great is their ability to be focused."
**Text on slide:** Focus
**Visual description:** Black "Focus" heading. One large person avatar at center surrounded by
four outline icons: a chef's hat, a graduation cap, a top hat with a wand, and a hard hat over a
wrench.
**What it teaches:** One agent wearing many hats.

### Slide 5.11 — Focus: one hat each (Wide deck, slide 80)
**Evidence:** Narrated — "You shouldn't rely on one agent to do it all, but instead many agents that work better together."
**Text on slide:** Focus
**Visual description:** The same four hat icons, each now above its own person avatar.
**What it teaches:** Split the work across focused agents, one role each.

### Slide 5.12 — Overview: Focus done (Wide deck, slide 81)
**Evidence:** Narrated — "So all right, we know that agents work better when they're role-playing and when they are focused. So what about tools?"
**Text on slide:** Role Playing · Focus · Tools · Cooperation · Guardrails · Memory
**Visual description:** The overview with Role Playing and Focus filled coral.
**What it teaches:** Progress marker.

### Slide 5.13 — Tools: a chosen set (Wide deck, slide 82)
**Evidence:** Narrated — "You want to make sure that you're providing them with the key tools to do the job that they need."
**Text on slide:** Tools
**Visual description:** A person avatar inside a thin red square, with four crossed-tool icons
inside the square and about a dozen more scattered outside it.
**What it teaches:** Give the agent a selected subset of the available tools.

### Slide 5.14 — Tools: overloaded (Wide deck, slide 83)
**Evidence:** Narrated — "You can overload your agents with too many tools, so they're going to have a hard time to choose a tool."
**Text on slide:** Tools
**Visual description:** A person avatar surrounded by about sixteen scattered crossed-tool icons,
with no frame.
**What it teaches:** Too many tools confuse the agent, especially on smaller models.

### Slide 5.15 — Overview: Tools done (Wide deck, slide 84)
**Evidence:** Narrated — "So we already know that agents now are great at role-playing focus and using tools. Let's talk about cooperation,"
**Text on slide:** Role Playing · Focus · Tools · Cooperation · Guardrails · Memory
**Visual description:** The overview with the whole top row filled coral.
**What it teaches:** Progress marker.

### Slide 5.16 — Collaboration (Wide deck, slide 85)
**Evidence:** Narrated — "They can basically take feedback from each other. They can delegate tasks to each other."
**Text on slide:** Collaboration · Take feedback · Delegate tasks
**Visual description:** Three person avatars joined by curved two-headed arrows, two bullets on
the right. The heading says "Collaboration" where the overview button says "Cooperation".
**What it teaches:** Agents improve outcomes by exchanging feedback and delegating.

### Slide 5.17 — Overview: Cooperation done (Wide deck, slide 86)
**Evidence:** Narrated — "The next one is guardrails."
**Text on slide:** Role Playing · Focus · Tools · Cooperation · Guardrails · Memory
**Visual description:** The overview with the top row and Cooperation filled coral.
**What it teaches:** Progress marker.

### Slide 5.18 — Guardrails (Wide deck, slide 87)
**Evidence:** Narrated — "we implemented a series of guardrails that prevents your agent from derailing and nudge our agents to stay on track."
**Text on slide:** Guardrails
**Visual description:** A person avatar on a road drawn in perspective: two converging edge lines
and a dashed center line running through the avatar.
**What it teaches:** Guardrails keep agents on track: no endless loops, repeated tool calls or
runaway answers.

### Slide 5.19 — Overview: Guardrails done (Wide deck, slide 88)
**Evidence:** Narrated — "Now there's just one last thing to talk about, memory."
**Text on slide:** Role Playing · Focus · Tools · Cooperation · Guardrails · Memory
**Visual description:** The overview with all but Memory filled coral.
**What it teaches:** Progress marker.

### Slide 5.20 — Memory (Wide deck, slide 89)
**Evidence:** Narrated — "Memory is the ability of your agent to remember what it has done."
**Text on slide:** Memory
**Visual description:** A horizontal coral line with seven coral dots (a timeline) above a person
avatar.
**What it teaches:** Memory spans an agent's past actions.

### Slide 5.21 — Three types of memory (Wide deck, slide 90)
**Evidence:** Narrated — "our agents will gather three types of memory for free, out of the box: long term memory, short term memory, and entity memory."
**Text on slide:** Memory · 1. Long-term memory · 2. Short-term memory · 3. Entity memory
**Visual description:** Slide 5.20 with a coral arc jumping from an early dot to a later one, and
a numbered list beside the avatar.
**What it teaches:** crewAI gives agents long-term, short-term and entity memory.

### Slide 5.22 — Short term Memory (Wide deck, slide 91)
**Evidence:** Narrated — "And these memories are shared across all the agents."
**Text on slide:** Short term · Memory · Memory during execution of a task. · Share knowledge, activities, and learnings · with other agents. · Share intermediate information even · before providing "task completion" output.
**Visual description:** Three avatars inside a grey ellipse labelled "Short term Memory" in bold,
three grey bullets to the lower right.
**What it teaches:** Short-term memory lives for one crew run and is shared across its agents.

### Slide 5.23 — Long term Memory (Wide deck, slide 92)
**Evidence:** Narrated — "every time that your agent completes a task, it self critiques itself to learn what it should have done better"
**Text on slide:** Remember · and Learn · Long term · Memory · Memory stored after execution of current · tasks. · Long term memory can be used in any · future tasks. · Leads to "self-improving" agents.
**Visual description:** Three avatars in a grey ellipse labelled "Long term Memory", with a thick
coral arrow looping out of the ellipse and back into it, labelled "Remember and Learn"; three
bullets to the lower right.
**What it teaches:** Long-term memory persists after a run (stored locally) so agents improve
across runs.

### Slide 5.24 — Entity Memory (Wide deck, slide 93)
**Evidence:** Narrated — "So if your agents trying to learn something about a specific company, it might store that company as an entity"
**Text on slide:** Entity Memory · Pretend news article (by ChatGPT) · Renewable energy corporations such as Tesla, led by CEO Elon Musk, and Orsted, based in Denmark, are at the forefront of the transition to sustainable energy. Meanwhile, tech giants like Google, under the leadership of Sundar Pichai, and Microsoft, with CEO Satya Nadella at the helm, are investing heavily in renewable energy projects and carbon offset programs to achieve carbon neutrality. Notably, countries like Germany, with its ambitious Energiewende policy, and China, the world's largest emitter of greenhouse gases, are implementing aggressive strategies to reduce emissions and accelerate the adoption of renewable energy. Additionally, startups like Beyond Meat, founded by Ethan Brown, and Impossible Foods, led by CEO Pat Brown, are disrupting the food industry with plant-based alternatives, significantly reducing the environmental impact of food production. · Entities · persons, · organizations, · locations
**Visual description:** A grey paragraph with named entities highlighted by type: people in cyan
(Elon Musk, Sundar Pichai, Satya Nadella, Ethan Brown, Pat Brown), organizations in green
(Tesla, Orsted, Google, Microsoft, Beyond Meat, Impossible Foods), locations in pink (Denmark,
Germany, China). A legend on the right uses the same three highlight colors.
**What it teaches:** Entity memory records the people, organizations and places a run talks
about.

---

## Lesson 6: Multi agent customer support automation
Transcript: `## Lesson 6: Multi agent customer support automation` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Tall slides 13 to 17, after the production note Tall 12 ("Lesson 3 starts here? · See wide
slides for L3A · Lesson 3B is narrow slides for code, found here."). Deck L3B, notebook
`works/L3/`.

### Slide 6.1 — Title card: Multi agent customer support automation (code) (Tall deck, slide 13)
**Evidence:** Title card.
**Text on slide:** Multi AI Agent Systems · with crewAI · Multi agent customer · support automation · (code)
**Visual description:** Title card in the course style on the tall page; "(code)" on its own
line.
**What it teaches:** Opens the code lesson.

### Slide 6.2 — [Jupyter Notebook] (Tall deck, slide 14)
**Evidence:** Narrated — "Let's try to do some code and see how that works."
**Text on slide:** [Jupyter Notebook]
**Visual description:** Placeholder, as Slide 4.2.
**What it teaches:** Marks the switch to the notebook.

### Slide 6.3 — Allow Delegation (Tall deck, slide 15)
**Evidence:** Narrated — "You can also see how one agent is not allowed to do any delegation, because we are setting allow delegation to false, but we are not doing that for the support quality assurance agent."
**Text on slide:** Allow Delegation · Do Task · Review · Task · AGENT · QA · AGENT · Not allowed to · delegate to · other agents · (does its own · work) · Can do its own · work and · delegate back · to other agent
**Visual description:** Two columns. Left: "Do Task" box → AGENT icon, with a blue curved arrow
looping back onto the agent itself, captioned "Not allowed to delegate to other agents (does its
own work)". Right: "Review Task" box → "QA AGENT" icon, with a blue arrow pointing from the QA
agent back to the left agent, captioned "Can do its own work and delegate back to other agent".
**What it teaches:** Delegation is set per agent: the support agent works alone, the QA agent may
send work back.

### Slide 6.4 — Design Pattern: Quality Assurance (Tall deck, slide 16)
**Evidence:** Narrated — "So I do recommend you considering adding a QA agent of sorts into whatever multi-agent systems that you do"
**Text on slide:** Design Pattern: · Quality Assurance · Do Task · Review · Task · AGENT · QA · AGENT
**Visual description:** The two columns of Slide 6.3 without the arrows and captions.
**What it teaches:** A reusable pattern: a doing agent followed by a reviewing QA agent.

### Slide 6.5 — Assigning Tools (Tall deck, slide 17)
**Evidence:** Narrated — "You can give them at the agent level or you can give them at the task level." … "So an easier way to put this, is that task tools override the agent tools."
**Text on slide:** Assigning Tools · Agent · Task
**Visual description:** Two overlapping ellipses: a large red one labelled "Agent" containing a
person avatar and two tool icons, and a smaller blue one labelled "Task" overlapping its right
side, with one tool icon in the overlap.
**What it teaches:** Tools can be given to an agent or to a task; when a task lists tools, the
agent uses only those for that task.

---

## Lesson 7: Mental framework for agent creation
Transcript: `## Lesson 7: Mental framework for agent creation` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Wide slides 94 to 103. The Tall deck's production note Tall 18 ("Lesson 3C · see wide slides")
points here: this is deck L3C. It ends with a recap of Lesson 5's six elements.

### Slide 7.1 — Title card: Mental framework for agent creation (Wide deck, slide 94)
**Evidence:** Title card.
**Text on slide:** Multi AI Agent Systems · with crewAI · Mental framework for · agent creation
**Visual description:** Title card in the course style.
**What it teaches:** Opens the lesson.

### Slide 7.2 — Manager (Wide deck, slide 95)
**Evidence:** Narrated — "So the framework is to think as a manager"
**Text on slide:** Manager
**Visual description:** A small outline person icon labelled "Manager" in bold grey, at the top.
First of four slides that read as one build (7.2–7.5).
**What it teaches:** Design a crew the way a manager staffs a team.

### Slide 7.3 — Goal and Process (Wide deck, slide 96)
**Evidence:** Narrated — "managers are conditioned to think about what is the goal and what is the process."
**Text on slide:** Manager · What is the Goal · What is the Process
**Visual description:** Slide 7.2 with two wide coral buttons beneath, white text.
**What it teaches:** Start from the goal and the process.

### Slide 7.4 — Who would you hire? (Wide deck, slide 97)
**Evidence:** Narrated — "If I had to hire people to do this, what would it be the people that I would hire?"
**Text on slide:** What kind of people would I need to hire to get this done? · Manager · What is the Goal · What is the Process
**Visual description:** Slide 7.3 (moved up) with a bold coral question beneath the buttons.
**What it teaches:** The hiring question defines the agents.

### Slide 7.5 — The hires (Wide deck, slide 98)
**Evidence:** Narrated — "So once that you get that answer, you need to know what agency need to be."
**Text on slide:** Same as Slide 7.4.
**Visual description:** Slide 7.4 with four small person avatars in a row below the question.
**What it teaches:** The answers become the agents, with their roles, goals and backstories.

### Slide 7.6 — "Okay" Agent roles (Wide deck, slide 99)
**Evidence:** Narrated — "These are some examples that are not necessarily the best."
**Text on slide:** "Okay" Agent roles · Researcher · Writer · Financial Analyst
**Visual description:** One bold bullet with three hollow sub-bullets, upper left.
**What it teaches:** Generic role names.

### Slide 7.7 — Okay versus Better roles (Wide deck, slide 100)
**Evidence:** Narrated — "So, better examples would be an HR research specialist, instead of just a researcher or a senior copywriter, instead of just a writer, or a FINRA approved analyst instead of a financial analyst."
**Text on slide:** Okay · Researcher · Writer · Financial Analyst · Better · HR Research Specialist · Senior copywriter · FINRA Approved Analyst
**Visual description:** Two bulleted columns, "Okay" and "Better", with three blue arrows from
each generic role to its specific counterpart.
**What it teaches:** Specific, keyword-rich roles get better results than generic ones.

### Slide 7.8 — Let's recap! (Wide deck, slide 101)
**Evidence:** Narrated — "All right, let's do a quick recap to see everything that we learned this lesson."
**Text on slide:** Let's recap!
**Visual description:** Section-question slide, large bold coral line.
**What it teaches:** Opens the recap.

### Slide 7.9 — Recap: all six elements (Wide deck, slide 102)
**Evidence:** Narrated — "they are doing role-playing. They have focus. They have the appropriate tools. They're allowed to cooperate. They have some guardrails. They also can leverage memory."
**Text on slide:** Role Playing · Focus · Tools · Cooperation · Guardrails · Memory
**Visual description:** The six-button overview with all six filled coral.
**What it teaches:** Recaps the six elements.

### Slide 7.10 — Recap: takeaways (Wide deck, slide 103)
**Evidence:** Narrated — "We've learned that agents are able to self improve by using memory. We also learned that crewAI prevents our agents to get into rabbit roles by making sure to steer them in the right way."
**Text on slide:** Agents · Tasks · Crew · Tools · Agents "self improve" using memory · Guardrails prevents agents from going into "rabbit holes" · (unproductive, repetitive loops) · Agents always attempt to get to an answer (avoid · iterating indefinitely) · Focus · narrowly defined task · specific agent roles and objectives · limited set of tools assigned to one agent
**Visual description:** Left: four grey boxes (Agents, Tasks, Crew, Tools) inside a coral rounded
frame, the building-blocks frame of Slide 4.8 with Tools added. Right: four bullets, the last
with three sub-bullets.
**What it teaches:** Memory makes agents self-improving, guardrails stop unproductive loops,
agents always attempt an answer, and focus means narrow tasks, specific roles and few tools.

---

## Lesson 8: Key elements of agent tools
Transcript: `## Lesson 8: Key elements of agent tools` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Wide slides 105 to 120, after the production note Wide 104 ("Lesson 4A"); the Tall deck's note
Tall 19 ("Lesson 4A (move to wide slides)") points here. The narration covers three qualities of
a great tool (versatile, fault-tolerant, caching), returning to a three-button overview with one
button filled each time, then examples of tools, crewAI's built-in tools, its documentation and
LangChain compatibility.

### Slide 8.1 — Title card: Key elements of agent tools (Wide deck, slide 105)
**Evidence:** Title card.
**Text on slide:** Multi AI Agent Systems · with crewAI · Key elements of agent tools
**Visual description:** Title card in the course style.
**What it teaches:** Opens the lesson.

### Slide 8.2 — What makes a great Tool? (Wide deck, slide 106)
**Evidence:** Narrated — "So what makes a great tool?"
**Text on slide:** What makes a great Tool?
**Visual description:** Black title above a large crossed screwdriver-and-wrench icon.
**What it teaches:** Poses the lesson's question.

### Slide 8.3 — Three qualities (Wide deck, slide 107)
**Evidence:** Narrated — "The tools that are versatile, the tools, that are fault-tolerant, and the tools that implement caching."
**Text on slide:** What makes a great Tool? · Versatile · Fault-tolerant · Caching
**Visual description:** Slide 8.2 with three white outlined buttons beneath the icon.
**What it teaches:** A great tool is versatile, fault-tolerant and cached.

### Slide 8.4 — Versatile highlighted (Wide deck, slide 108)
**Evidence:** Narrated — "So what it means for a tool to be versatile."
**Text on slide:** Same as Slide 8.3.
**Visual description:** Slide 8.3 with "Versatile" filled coral.
**What it teaches:** Opens the first quality.

### Slide 8.5 — Versatile: from fuzzy inputs to typed output (Wide deck, slide 109)
**Evidence:** Narrated — "The tool is the connection between the AI apps that have fuzzy inputs with the external world that have strong typed inputs."
**Text on slide:** Versatile · Agent · AGENT · fuzzy · inputs · text · instructions · Mix of words, · numbers · tool · strongly typed · output · JSON (key-value pairs) · list of strings, categories · numbers · External world · (traditional software systems)
**Visual description:** A coral "Versatile" button at top. Below, left to right: the agent icon
labelled "Agent"; a light-grey block arrow labelled "fuzzy inputs" with bullets (text,
instructions, mix of words and numbers); the tool icon labelled "tool"; a second block arrow
labelled "strongly typed output" with bullets (JSON, list of strings or categories, numbers); and
a desktop computer with keyboard labelled "External world (traditional software systems)".
**What it teaches:** A tool translates whatever the LLM sends into the typed input the outside
system needs.

### Slide 8.6 — Fault-tolerant highlighted (Wide deck, slide 110)
**Evidence:** Narrated — "The second thing: is being fault-tolerant."
**Text on slide:** Same as Slide 8.3.
**Visual description:** The overview with "Fault-tolerant" filled coral.
**What it teaches:** Opens the second quality.

### Slide 8.7 — What happens when an exception occurs? (Wide deck, slide 111)
**Evidence:** Narrated — "So even if an exception happens when running a tool, instead of stopping the execution, it sends that message back to the agent so the agent can take action on that."
**Text on slide:** What happens when an exception/error · occurs? · Option 1: stop execution · Option 2: Fail gracefully (and try again) · send error message back to agent · Ask agent to retry given the error message
**Visual description:** Left: a person avatar with two tool icons nearby and a large red X over a
third; a curved coral arrow runs from the avatar back up to the X. Right: grey text listing the
two options.
**What it teaches:** On an error, a tool can either stop the run or return the error to the agent
so it can retry.

### Slide 8.8 — Caching highlighted (Wide deck, slide 112)
**Evidence:** Narrated — "What about caching?"
**Text on slide:** Same as Slide 8.3.
**Visual description:** The overview with "Caching" filled coral (a slightly redder shade than
the other highlights).
**What it teaches:** Opens the third quality.

### Slide 8.9 — Tools call the internet (Wide deck, slide 113)
**Evidence:** Narrated — "Whenever you have a tool, most of the times, that you is using to communicate it with the web."
**Text on slide:** internet · agent
**Visual description:** A large globe at top labelled "internet". An avatar labelled "agent" at
bottom left holds a tool, with a black arrow curving up into the globe; two more tool icons sit to
the right, with a second arrow rising toward the globe.
**What it teaches:** Each tool use is typically an external request.

### Slide 8.10 — Cross-agent caching (Wide deck, slide 114)
**Evidence:** Narrated — "So in crewAI we offer cross-agent caching." … "That prevents unnecessary requests, that prevents hitting rate limits"
**Text on slide:** Caching Layer · Cross-agent caching · prevent unnecessary · requests · Stay within rate limits · (number of requests per · second allowed for an API · call) · Save time (retrieving · cached results is much · faster than an API call)
**Visual description:** The globe at top with a wide coral bar labelled "Caching Layer" beneath
it. Two avatars, each holding a tool, have arrows rising to the bar; only one arrow continues
from the bar to the globe. "Cross-agent caching" sits between the avatars; three bullets on the
right.
**What it teaches:** A cache shared across agents avoids repeat calls, respects rate limits and
saves time.

### Slide 8.11 — Examples of tools (Wide deck, slide 115)
**Evidence:** Narrated — "There are the simple ones like search the internet or scrape a website" … "You also can connect to a database. You can call an API, you can send notification and many, many more."
**Text on slide:** Examples of tools · Search the internet · Scrape a website · Connect to a database · Call an API · Send notifications · and many more
**Visual description:** Coral title, five grey bullets and an unbulleted "and many more".
**What it teaches:** Typical tool actions.

### Slide 8.12 — Agents, Tasks, Crew, Tools (Wide deck, slide 116)
**Evidence:** Narrated — "So you can see here how tools are such a cornerstone."
**Text on slide:** Agents · Tasks · Crew · Tools
**Visual description:** Four grey boxes stacked in a coral rounded frame, centered.
**What it teaches:** Tools join agents, tasks and crews as a core building block.

### Slide 8.13 — crewAI tool list (Wide deck, slide 117)
**Evidence:** Narrated — "Showing, crewAI tools are such an important piece that crew offers a bunch of them out of the gate that you can use."
**Text on slide:** Google Serper Search · Scrape Website · Directory Read · File Read · Selenium Scraper · Directory RAG Search · PDF RAG Search · TXT RAG Search · CSV RAG Search · XML RAG Search · JSON RAG Search · Docx Rag Search · MDX RAG Search · PG RAG Search · Website RAG Search · Github RAG Search · Code Docs RAG Search · Youtube Video RAG Youtube · Channel RAG Search
**Visual description:** Nineteen tool names in three columns of large grey text (listed here in
column order). The last two lines of the third column read "Youtube Video RAG Youtube" and
"Channel RAG Search", a line break of "Youtube Video RAG Search" and "Youtube Channel RAG Search"
(both names appear in the documentation sidebar on Slide 8.14).
**What it teaches:** crewAI's built-in tools: search, scraping, file and directory reading, and
RAG search over many formats.

### Slide 8.14 — crewAI Documentation (Wide deck, slide 118)
**Evidence:** Narrated — "make sure to check crewAI's documentation where you're going to find all the documentation for all the existing tools in there."
**Text on slide:** crewAI · Home · Core Concepts · How to Guides · Tools Docs · Google Serper Search · Scrape Website · Directory Read · File Read · Selenium Scraper · Directory RAG Search · PDF RAG Search · TXT RAG Search · CSV RAG Search · XML RAG Search · JSON RAG Search · Docx Rag Search · MDX RAG Search · PG RAG Search · Website RAG Search · Github RAG Search · Code Docs RAG Search · Youtube Video RAG Search · Youtube Channel RAG Search · Examples · Telemetry · crewAI Documentation · Cutting-edge framework for orchestrating role-playing, autonomous AI agents. · empowers agents to work together seamlessly, tackling complex tasks. · Core Concepts · Agents · Tasks · Tools · Processes · Crews · Memory · How-To Guides · Getting Started · Create Custom Tools · Using Sequential Process · Using Hierarchical Process · Connecting to LLMs · Customizing Agents · Human Input on Execution · Agent Observability using AgentOps
**Visual description:** A screenshot of the documentation home page: a left sidebar with "Tools
Docs" expanded, the crewAI logo, and two link columns (Core Concepts, How-To Guides) in coral.
Part of the tagline between its two lines is not visible.
**What it teaches:** Where the tool and concept documentation lives.

### Slide 8.15 — crewAI Documentation, main panel boxed (Wide deck, slide 119)
**Evidence:** Narrated — as Slide 8.14.
**Text on slide:** Same as Slide 8.14.
**Visual description:** Slide 8.14 with a coral rectangle around the main panel (title, tagline
and the two link columns).
**What it teaches:** Points at the concept and how-to guides.

### Slide 8.16 — crewAI + LangChain (Wide deck, slide 120)
**Evidence:** Narrated — "crewAI supports all LangChain tools"
**Text on slide:** + · 🦜🔗 LangChain
**Visual description:** The crewAI wordmark, a plus sign, and the LangChain parrot-and-chain logo
with "LangChain", stacked at center.
**What it teaches:** LangChain's tools can be used in crewAI.

---

## Lesson 9: Tools for a customer outreach campaign
Transcript: `## Lesson 9: Tools for a customer outreach campaign` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Tall slides 21 to 23, after the production note Tall 20 ("Lesson 4B · (code, so narrow
slides)"). Deck L4B, notebook `works/L4/`.

### Slide 9.1 — Title card: Tools for a customer outreach campaign (code) (Tall deck, slide 21)
**Evidence:** Title card.
**Text on slide:** Multi AI Agent Systems · with crewAI · Tools for a customer · outreach campaign · (code)
**Visual description:** Title card in the course style on the tall page.
**What it teaches:** Opens the code lesson.

### Slide 9.2 — [Jupyter Notebook] (Tall deck, slide 22)
**Evidence:** Narrated — "And let's start build our crew."
**Text on slide:** [Jupyter Notebook]
**Visual description:** Placeholder, as Slide 4.2.
**What it teaches:** Marks the switch to the notebook.

### Slide 9.3 — Exception Handling (Tall deck, slide 23)
**Evidence:** Narrated — "So for crew, it was a conscious decision early on that we would prevent exceptions from stopping execution. But you might find other frameworks that choose it otherwise and choose to allow exceptions, actually stop executions."
**Text on slide:** Exception Handling · Option 1: Framework stops execution · (you can choose how to handle the · exceptions, such as restart execution.) · Option 2: Framework continues execution · (CrewAI is designed this way)
**Visual description:** Black title over two grey bullets.
**What it teaches:** Frameworks either halt on a tool exception or keep going; crewAI keeps going
and tells the agent about the error.

---

## Lesson 10: Recap of tools
Transcript: `## Lesson 10: Recap of tools` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Wide slides 121 to 122; the Tall deck's note Tall 24 ("L4C (use wide slides)") points here.

### Slide 10.1 — Title card: Recap of tools (Wide deck, slide 121)
**Evidence:** Title card.
**Text on slide:** Multi AI Agent Systems · with crewAI · Recap of tools
**Visual description:** Title card in the course style.
**What it teaches:** Opens the recap.

### Slide 10.2 — Versatile, Fault-tolerant, Caching (Wide deck, slide 122)
**Evidence:** Narrated — "you need to make sure they're versatile. You need to make sure they're fault tolerant and need to make sure that they have a caching strategy."
**Text on slide:** Versatile · Fault-tolerant · Caching
**Visual description:** The tool icon above the three unfilled buttons, without the "What makes
a great Tool?" title.
**What it teaches:** The three tool qualities, restated.

---

## Lesson 11: Key elements of well defined tasks
Transcript: `## Lesson 11: Key elements of well defined tasks` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Wide slides 124 to 126, after the production note Wide 123 ("Lesson 5A").

### Slide 11.1 — Title card: Key elements of well defined tasks (Wide deck, slide 124)
**Evidence:** Title card.
**Text on slide:** Multi AI Agent Systems · with crewAI · Key elements of well defined tasks
**Visual description:** Title card in the course style.
**What it teaches:** Opens the lesson.

### Slide 11.2 — The manager framework extended to tasks (Wide deck, slide 125)
**Evidence:** Narrated — "think about what processes and tasks I expect individuals on my team to do, and you can use that to create the tasks."
**Text on slide:** Manager · What is the Goal · What is the Process · What kind of individuals would I need to hire to get this done? · Which processes and tasks do I expect the individuals on my team to do? · Task · Task · Task · Task · Task
**Visual description:** Slide 7.5 ("people" now reads "individuals") with a second coral question
below the four avatars and five coral "Task" buttons in rows of three and two.
**What it teaches:** After choosing the agents, list the tasks you expect them to do.

### Slide 11.3 — What a task needs (Wide deck, slide 126)
**Evidence:** Narrated — "One: a clear description of what is the task. And two: set a clear and concise expectation." … "like setting a context, or setting a callback, or overriding the agent tools with a specific task, force human input"
**Text on slide:** Which processes and tasks do I expect the individuals on my team to do? · Task · Clear description of the task · Set a clear and concise expectation · Set context · Set a callback · Override Agent tools with specific task tools · Force human input before end of task · Execute asynchronously · Output as Pydantic · Output as JSON · Output as file · Run in parallel
**Visual description:** Four small avatars at top, the coral question, one wide coral "Task" bar,
and eleven bullets beneath. The first two bullets are pale coral; the other nine are dark red.
**What it teaches:** Every task needs a clear description and a clear expected output (crewAI
makes both mandatory); tasks can also take context, callbacks, task-level tools, human input,
asynchronous or parallel execution, and Pydantic, JSON or file output.

---

## Lesson 12: Automate event planning
Transcript: `## Lesson 12: Automate event planning` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Tall slides 25, 27 and 28, around the production note Tall 26 ("Lesson 5B · (slides to be used
within code walkthrough)"). Deck L5B, notebook `works/L5/`. Tall 25's placement here is a
judgement call; see "How to read this file".

### Slide 12.1 — [Jupyter Notebook] (Tall deck, slide 25)
**Evidence:** Narrated (by position) — Lesson 11 ends "So with that in mind, let's jump into code real quick," and Lesson 12 is the notebook walkthrough. The slide itself carries no lesson marker.
**Text on slide:** [Jupyter Notebook]
**Visual description:** Placeholder, as Slide 4.2, but with the text at left of center rather
than centered.
**What it teaches:** Marks a switch to a notebook.

### Slide 12.2 — Title card: Automate event planning (code) (Tall deck, slide 27)
**Evidence:** Title card.
**Text on slide:** Multi AI Agent Systems · with crewAI · Automate · event planning · (code)
**Visual description:** Title card in the course style on the tall page.
**What it teaches:** Opens the code lesson.

### Slide 12.3 — Asynchronous Execution (Tall deck, slide 28)
**Evidence:** Narrated — "So what that means is that the first task, the task that selects the venue, it's going to be executed by itself, alone." … "Then after that, the logistics tasks and the marketing tasks are going to be executed in parallel."
**Text on slide:** Asynchronous Execution · Find Venue · Venue · AGENT · Logistics · Logistics · AGENT · Marketing · Marketing · AGENT · 1 · 2
**Visual description:** Left column, numbered "1": "Find Venue" task → "Venue AGENT". A blue
block arrow points right to column "2", which stacks "Logistics" → "Logistics AGENT" and
"Marketing" → "Marketing AGENT".
**What it teaches:** The venue task runs first; the logistics and marketing tasks then run in
parallel because neither depends on the other.

---

## Lesson 13: Recap on tasks
Transcript: `## Lesson 13: Recap on tasks` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Wide slides 128 to 129, after the production note Wide 127 ("Lesson 5C"); the Tall deck's note
Tall 29 ("Lesson 5C · (see wide slides)") points here.

### Slide 13.1 — Title card: Recap of tasks (Wide deck, slide 128)
**Evidence:** Title card. The subtitle reads "Recap of tasks"; the transcript heading is "Recap on tasks".
**Text on slide:** Multi AI Agent Systems · with crewAI · Recap of tasks
**Visual description:** Title card in the course style.
**What it teaches:** Opens the recap.

### Slide 13.2 — Manager framework with tasks (Wide deck, slide 129)
**Evidence:** Narrated — "So we learned that this mental framework for creating agents is super helpful. Because it helps us to understand what are the agents that are going to create. Also, what are the tasks that we expect them to do?"
**Text on slide:** Same as Slide 11.2.
**Visual description:** Identical to Slide 11.2.
**What it teaches:** Restates goal → process → hires → tasks.

---

## Lesson 14: Multi agent collaboration
Transcript: `## Lesson 14: Multi agent collaboration` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Wide slides 131 to 141, after the production note Wide 130 ("Lesson 6A"). Three short builds:
a chain of tasks whose initial context fades (14.3–14.5), three processes (14.6–14.8), and
collaboration across processes (14.9–14.11).

### Slide 14.1 — Title card: Multi agent collaboration (Wide deck, slide 131)
**Evidence:** Title card.
**Text on slide:** Multi AI Agent Systems · with crewAI · Multi agent collaboration
**Visual description:** Title card in the course style.
**What it teaches:** Opens the lesson.

### Slide 14.2 — How do Multi Agents Collaborate? (Wide deck, slide 132)
**Evidence:** Narrated — "So let's dive into that. How multi-agents collaborate."
**Text on slide:** How do Multi Agents Collaborate?
**Visual description:** Section-question slide, large bold coral headline.
**What it teaches:** Poses the lesson's question.

### Slide 14.3 — Two tasks in sequence (Wide deck, slide 133)
**Evidence:** Narrated — "where you didn't have one agent finish a task and then pass its output into the next."
**Text on slide:** Task · Task · LLMs · LLMs
**Visual description:** Two Task → LLMs pairs with a diagonal handoff arrow between them.
**What it teaches:** The sequential handoff seen so far.

### Slide 14.4 — A longer chain (Wide deck, slide 134)
**Evidence:** Narrated — "We already saw this happenning The true like crews by seeing like one agent passed the test to another."
**Text on slide:** Task · Task · Task · Task · LLMs · LLMs · LLMs · LLMs
**Visual description:** Four Task → LLMs pairs in a row joined by handoff arrows; the row runs off
the left edge of the slide.
**What it teaches:** Chains can be long.

### Slide 14.5 — Context fades along the chain (Wide deck, slide 135)
**Evidence:** Narrated — "The most common is the fact that the initial context moves slowly fade away as the tasks get passed from one agent to another."
**Text on slide:** Task · Task · Task · Task · LLMs · LLMs · LLMs · LLMs
**Visual description:** The chain shifted further left, with a horizontal coral band below it
that starts as a solid coral circle at the left and fades to white toward the right.
**What it teaches:** In a long sequence the original context weakens with each handoff.

### Slide 14.6 — Processes: sequential (Wide deck, slide 136)
**Evidence:** Narrated — "So let's talk about processes. All of our agents so far have been working mainly in a sequential process."
**Text on slide:** Processes
**Visual description:** Coral "Processes" title, upper left. One drawing: a vertical chain of
three coral dots joined by a coral line, each with a small avatar beside it.
**What it teaches:** The sequential process.

### Slide 14.7 — Processes: hierarchical (Wide deck, slide 137)
**Evidence:** Narrated — "Another big one, is hierarchical."
**Text on slide:** Processes
**Visual description:** The chain plus an inverted-V drawing: one dot on top joined to two dots
below, each with an avatar.
**What it teaches:** The hierarchical process: a manager that keeps the goal, delegates and
reviews.

### Slide 14.8 — Processes: parallel branches (Wide deck, slide 138)
**Evidence:** Narrated — "You can also do some of what we did with asynchronous execution."
**Text on slide:** Processes
**Visual description:** The chain, the inverted V and a diamond: one dot on top, two pairs of dots
side by side, one dot at the bottom, each with an avatar. These are the three drawings of
Slide 2.2.
**What it teaches:** Tasks can also run in parallel branches and rejoin, whatever the process.

### Slide 14.9 — Collaboration: two agents (Wide deck, slide 139)
**Evidence:** Narrated — "In terms of the collaboration itself, you can have agents ask questions, vaguely talk to each other."
**Text on slide:** Collaboration
**Visual description:** Coral title over two avatars joined by a two-headed arrow.
**What it teaches:** Agents can talk to each other directly.

### Slide 14.10 — Collaboration inside a hierarchy (Wide deck, slide 140)
**Evidence:** Narrated — "Meaning that even if you choose to use hierarchical processes where you have one manager, delegating work, that still means that the agents benefit can delegated work between themselves."
**Text on slide:** Collaboration
**Visual description:** The pair from Slide 14.9 above a group: one avatar on top with paired
arrows to and from two of four avatars below, and a long curved two-headed arrow joining the
outer two of those four.
**What it teaches:** Under a manager, workers can still delegate to each other.

### Slide 14.11 — Collaboration across processes (Wide deck, slide 141)
**Evidence:** Narrated — "We already talked a bit about this, but this happens independently of the process that you choose."
**Text on slide:** (no text)
**Visual description:** The sequential chain and the hierarchical inverted V, each with curved
coral two-headed arrows added: one looping beside the chain, one between the manager and a
worker, and one between the two workers.
**What it teaches:** Collaboration works whichever process is chosen.

---

## Lesson 15: Mutli agent collaboration for financial analysis
Transcript: `## Lesson 15: Mutli agent collaboration for financial analysis` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Tall slides 31 to 33, after the production note Tall 30 ("Lesson 6A (see wide slides) · Lesson
6B (narrow slides here)"). Deck L6B, notebook `works/L6/`.

### Slide 15.1 — Title card: Multi agent collaboration for financial analysis (code) (Tall deck, slide 31)
**Evidence:** Title card. The slide spells "Multi"; the transcript heading reads "Mutli".
**Text on slide:** Multi AI Agent Systems · with crewAI · Multi agent collaboration · for financial analysis · (code)
**Visual description:** Title card in the course style on the tall page.
**What it teaches:** Opens the code lesson.

### Slide 15.2 — [Jupyter Notebook] (Tall deck, slide 32)
**Evidence:** Narrated — Lesson 14 ends "Let's jump into our Jupyter notebook real quick."
**Text on slide:** [Jupyter Notebook]
**Visual description:** Placeholder, as Slide 4.2.
**What it teaches:** Marks the switch to the notebook.

### Slide 15.3 — Crew: agents, process, tasks, outcome (Tall deck, slide 33)
**Evidence:** Narrated — "This is more of a simplistic representation of crewAI specifically, but this is very similar to what you find on other frameworks out there. You have crews, you have agents, you have do's, you have processes, you have tasks."
**Text on slide:** Crew · AI Agents · AI Agents · AI Agents · Tools · Process · Task · Task · Outcome · Delegation · to other · agents · Processes · define how · agents · collaborate · Task tool set · overrides · agent's tool set.
**Visual description:** A coral rounded frame labelled "Crew". Inside: three black "AI Agents"
pills (one with a small "Tools" tag), a wide "Process" bar with a grey shadow below them, and two
white "Task" boxes beneath; black arrows run from the agents to the Process bar and from the bar
to the tasks. An arrow from the frame's bottom points to coral "Outcome". Captions around the
frame: "Delegation to other agents" (left), "Processes define how agents collaborate" (right,
upper) and "Task tool set overrides agent's tool set." (right, lower).
**What it teaches:** The whole model in one picture: a crew of agents with tools works through a
process on tasks to produce an outcome; agents can delegate, the process sets how they
collaborate, and task tools override agent tools.

---

## Lesson 16: Build a crew to tailor job applications
Transcript: `## Lesson 16: Build a crew to tailor job applications` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Tall slides 35 to 37, after the production note Tall 34 ("Lesson 7 · All in narrow slides").
Deck L7, notebook `works/L7/`. The crew's agents, posting and résumé were shown in Lesson 2
(Slides 2.4–2.18).

### Slide 16.1 — Title card: Build a crew to tailor job applications (Tall deck, slide 35)
**Evidence:** Title card.
**Text on slide:** Multi AI Agent Systems · with crewAI · Build a crew to tailor job · applications
**Visual description:** Title card in the course style on the tall page; no "(code)" suffix.
**What it teaches:** Opens the final lesson.

### Slide 16.2 — Job Application Crew (Tall deck, slide 36)
**Evidence:** Deck-only. The narration calls this crew "our most complex crew yet" (Lesson 2) and "going full circle"; the slide's "your first multi-agent system" contradicts its place as the last crew.
**Text on slide:** Job Application Crew · your first multi-agent system
**Visual description:** Large bold coral title with a smaller bold coral subtitle, centered.
**What it teaches:** Names the crew.

### Slide 16.3 — Goal and Process for the crew (Tall deck, slide 37)
**Evidence:** Narrated — "So what is the goal? The goal is to maximize your chances of getting an interview for a given job posting" … "And then as a bonus, we can also have this crew sell some talking points for an initial interview"
**Text on slide:** What is the Goal? · Maximize your chances of getting an · interview for a given job posting · What is the Process? · Learn about the job requirements · Cross that with your skill set and experiences · Reshape resume to highlight relevant areas · Rewrite resume with appropriate language · Set talking points for your initial interview
**Visual description:** Two wide coral buttons with bold white questions, each followed by grey
text: the goal sentence, then five bullets.
**What it teaches:** Applies the manager framework (goal, then process) to this crew.

---

## Lesson 17: Next steps with AI agent systems
Transcript: `## Lesson 17: Next steps with AI agent systems` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Only the title card. The resources the narration walks through were shown on screen, not on
slides (see "How to read this file").

### Slide 17.1 — Title card: Next steps with AI agent systems (Wide deck, slide 142)
**Evidence:** Title card.
**Text on slide:** Multi AI Agent Systems · with crewAI · Next steps with AI agent systems
**Visual description:** Title card in the course style.
**What it teaches:** Opens the lesson.

---

## Lesson 18: Conclusion
Transcript: `## Lesson 18: Conclusion` in transcripts/multi-ai-agent-systems-with-crewai-transcripts.md

Only the title card.

### Slide 18.1 — Title card: Conclusion (Wide deck, slide 143)
**Evidence:** Title card.
**Text on slide:** Multi AI Agent Systems · with crewAI · Conclusion
**Visual description:** Title card in the course style.
**What it teaches:** Closes the course.
