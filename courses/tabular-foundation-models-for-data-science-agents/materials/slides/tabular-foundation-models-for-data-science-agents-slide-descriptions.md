# Slide descriptions: Tabular Foundation Models for Data Science Agents
Source decks: ../repo/slides/L1_What_are_TFMs_v1_In_Template_FH.pptx.pdf (15 slides, wide), ../repo/slides/L2_ Prediction with TabPFN_ Classification and Regression .pdf (8 slides, tall), ../repo/slides/L3 and L4.pdf (12 slides, tall), ../repo/slides/L5-Building Predictive Agents with TabPFN.pdf (10 slides, wide)
Instructors: Frank Hutter, Tuana Çelik and Eliott Kalfon (Prior Labs)

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
- **Lesson numbering comes from the transcripts:** 1 Introduction, 2 What Are Tabular Foundation
  Models?, 3 Classification, Regression & Forecasting with TabPFN, 4 Interpreting TabPFN
  predictions, 5 Real-time inference with the KV cache, 6 Building a Data Science Agent,
  7 Conclusion. **The deck file names use a different, off-by-one numbering** and must not be read
  as transcript lesson numbers. The decks map onto the transcript lessons by their title cards:
  - deck "L1" (title card subtitle "What Are Tabular Foundation Models?") = Lesson 2;
  - deck "L2" (title card "Classification, Regression & Forecasting with TabPFN") = Lesson 3;
  - deck "L3 and L4", slides 1–6 (title card "Interpreting TabPFN predictions") = Lesson 4;
  - deck "L3 and L4", slides 7–12 (title card "Real-time inference with the KV cache") = Lesson 5;
  - deck "L5" (title card "Building a Data Science Agent") = Lesson 6.

  Transcripts win wherever the decks disagree.
- **Swapped lesson openings in the transcripts.** The first two or three sentences of the Lesson 4
  and Lesson 5 transcripts appear swapped: Lesson 4 ("Interpreting TabPFN predictions") opens with
  "In this lesson, you'll use KV caching to reuse that context and make repeated predictions
  faster", and Lesson 5 ("Real-time inference with the KV cache") opens with "In this lesson,
  you'll use SHAP values and partial dependence plots". In both, the heading and the rest of the
  narration match each other and the slides, and the closing line of Lesson 4 ("In the next lesson,
  you will learn how to accelerate TabPFN inference with KV cache") confirms the order. Slides are
  placed by heading and body, not by the opening sentences.
- **Other cross-references in the narration use their own numbering.** Lesson 6 says "Lesson 1
  with Frank" for what the transcripts number Lesson 2.
- **Slide numbering** is `Lesson.Order` in deck order within the lesson. The deck and original
  slide number follow in parentheses so each entry can be traced back to the PDF.
- **Text on slide** is transcribed verbatim from the extracted text layer, with labels inside
  charts and diagrams read from the page images where the text layer skipped them. Items are
  separated by " · ". Code is reproduced as code. Typos on the slides are kept as printed.
- **Animations cannot be known** from a PDF, so no entry claims a build order. Where two slides
  look like stages of one build (Slides 3.4–3.6, 6.5–6.6), that is stated as a reading of the
  drawings, not a fact.
- **Lessons 1 and 7 have no slides** in any deck. They are listed with a note so the file still
  has one section per lesson. All 45 slides are accounted for: 15 in Lesson 2, 8 in Lesson 3, 6 in
  Lesson 4, 6 in Lesson 5 (one of them blank), 10 in Lesson 6.
- **No slide covers training a tiny TabPFN.** Lessons 1 and 7 both say the course trains a tiny
  TabPFN from scratch; no deck, and no transcript lesson, covers it.
- **No slide covers the Lesson 6 demo.** The Claude Code walkthrough (the `.mcp.json` file, the
  TabPFN handoff skill, the helper scripts, the telco churn data split, the report) is narrated in
  Lesson 6 but shown on screen, not on slides. The deck's last slide is the MCP tool chain.
- Course-wide visual conventions: every content slide has the PRIOR (Prior Labs) wordmark top left
  and the DeepLearning.AI logo top right, a centered black title in a sans face, and a coral-red
  wave along the bottom edge. Title cards are white with the course title "Tabular Foundation
  Models for Data Science Agents" in coral red on two lines, the lesson title in black or grey
  below, often the instructor's name and "Prior Labs", and both logos near the bottom, with no
  wave. The two wide decks (Lessons 2 and 6) share a navy-and-lavender palette for tables and
  panels; the two tall decks (Lessons 3 to 5) use light grey cards, blue highlights and coral-red
  "TabPFN" boxes.

---

## Lesson 1: Introduction
Transcript: `## Lesson 1: Introduction` in transcripts/tabular-foundation-models-for-data-science-agents-transcripts.md

No slide in any deck belongs to this lesson. The narration previews every later topic (in-context
learning, classification and regression, forecasting, the KV cache, interpretation, the agent with
MCP and skills, and training a tiny TabPFN), but every slide covering those topics is narrated in
detail in Lessons 2 to 6 and is placed there.

---

## Lesson 2: What Are Tabular Foundation Models?
Transcript: `## Lesson 2: What Are Tabular Foundation Models?` in transcripts/tabular-foundation-models-for-data-science-agents-transcripts.md

All 15 slides of deck "L1" belong here; the deck's title-card subtitle is this lesson's title and
the narration walks through them in deck order: what tabular data and a tabular prediction task
are, three example tables, why LLMs fail on tables, LLMs versus TFMs, why the traditional workflow
does not scale, TabPFN as the replacement, the benchmark picture, pretraining versus inference,
the Nature paper, row-limit growth, ways to access TabPFN, and application areas.

### Slide 2.1 — Title card: What Are Tabular Foundation Models? (deck L1, slide 1)
**Evidence:** Deck-only (title card; its subtitle is this lesson's title)
**Text on slide:** Tabular Foundation Models for Data Science Agents · What Are Tabular Foundation Models?
**Visual description:** Wide white title card. The course title in coral red on two lines,
centered; below it the subtitle in grey. The PRIOR wordmark (navy, with its wave-lines square
mark) sits bottom left of center and the DeepLearning.AI logo (red concentric mark over the name)
bottom right of center. No instructor name.
**What it teaches:** Names the course and the lesson.

### Slide 2.2 — What is tabular data? A concrete example (deck L1, slide 2)
**Evidence:** Narrated — "Here is a concrete example from medicine. You have 5,000 previous patients, one per row, and for each of them, you took a blood sample and measured four different omics blood markers, one per column. And you also know which of these patients had a particular disease, like in this case, early-stage Alzheimer's. We then measure these omics blood markers for new patients, and would like to predict the probability that they have the disease to allow us to start the right treatment early. You have training data, where you have some measured features, Xtrain, and you know the value of the target variable, ytrain. And then you get the features of some new data, Xtest, and would like to make a probabilistic prediction for the target, ytest."
**Text on slide:** What is tabular data? A concrete example · Which patients have early-stage Alzheimer (based on omics blood markers)? · ID · L-Carnitin · Creatinin · Homocystein · Beta-hydroxybutyrat · Early-stage Alzheimer · X_train · y_train · X_test · y_test · Tabular prediction task · Further examples (among 1000s) · Will this treatment work for this patient? · How strong will this material be? · What type of galaxy is this data from? · Which product will this customer buy? · Will this credit be paid back? · … · The decade-old problem formulation many of you saw in Machine Learning 101
**Visual description:** Left, a table in a serif (paper-style) face with an ID column and four
blood-marker columns plus a red-headed "Early-stage Alzheimer" column. Rows 1–10 and 5000 are
filled (marker values such as 45.2, 85, 12.1, 0.4; labels Yes/No); rows 5001–5003 have marker
values but no label. Translucent overlays split the table into four blocks: a large light-blue
"X_train" over the training features, a green "y_train" over the training labels, a darker blue
"X_test" over the three new rows, and a darker green "y_test" with a red arrow pointing at it
labelled "Tabular prediction task". Right, a grey rounded box listing the further examples as
navy bullets. The bottom line is navy.
**What it teaches:** The supervised tabular prediction setup: rows are examples, columns are
features, one column is the target; the task is to predict y_test for new rows from X_train,
y_train and X_test. The setup applies to thousands of problems.

### Slide 2.3 — Tabular foundation models solve a broad range of tasks: treatment success prediction (deck L1, slide 3)
**Evidence:** Narrated — "So Tabular Foundation Models can be used to predict how likely a new drug is to work based on the characteristics of a patient, like in this case."
**Text on slide:** Tabular foundation models solve a broad range of tasks · Example: treatment success prediction · Age · Existing Conditions (ICD) · Biomarker · Stage of Cancer · … · Responder ? · 38 · E11.9, I10 · BRCA1+ · IIIA · … · Yes · 83 · — · HER2+ · IIB · … · Yes · 71 · N18.3, E78.5 · EGFR− · IV · … · No · … · 52 · I10, E11.2 · None · IIIA · … · ?
**Visual description:** A navy-headed table with light-blue feature cells and a green target
column ("Responder ?") framed by a thick navy border. Three filled rows (Yes in green, Yes in
green, No in red), an ellipsis row, then a darker-blue last row whose target cell holds a "?".
**What it teaches:** A clinical example of a classification table with mixed feature types (age,
diagnosis codes, biomarker status, cancer stage); the last row is the one to predict.

### Slide 2.4 — Tabular foundation models solve a broad range of tasks: credit risk assessment (deck L1, slide 4)
**Evidence:** Narrated — "They can also be used to predict how likely a bank customer is to pay back a credit."
**Text on slide:** Tabular foundation models solve a broad range of tasks · Example: credit risk assessment · Loan ID · FICO · Existing Products · … · Default ? · PR_PLM_PD_2401 · 750 · 3C · … · No · PR_PLM_PD_2501 · 530 · 2C1M · … · Yes · PD_PLA_PD_0459 · 820 · 1A · … · No · … · PD_PWL_PD_1021 · 650 · 2A2C · … · ?
**Visual description:** Same table layout as Slide 2.3. Targets: No (green), Yes (red), No
(green), ellipsis, and a "?" on the darker-blue last row.
**What it teaches:** A finance classification example (loan default) in the same shape.

### Slide 2.5 — Tabular foundation models solve a broad range of tasks: customer spend forecasting (deck L1, slide 5)
**Evidence:** Narrated — "And they can also be used to predict how much a customer is likely to spend in the next quarter, along with a full probability distribution."
**Text on slide:** Tabular foundation models solve a broad range of tasks · Example: customer spend forecasting · Lifetime value so far · Multiple accounts · Last Login Days · … · Spend Next Quarter · $1290.20 · Yes · 8 · … · $310.40 · $901.01 · Yes · 18 · … · $45.80 · $652.10 · No · 3 · … · $188.30 · … · $1147.49 · No · 8 · … · ?
**Visual description:** Same table layout as Slide 2.3, with dollar amounts in bold in the green
target column and a "?" on the last row.
**What it teaches:** A regression example: the target is a number (next-quarter spend), and the
narration adds that the prediction comes with a full probability distribution.

### Slide 2.6 — LLMs aren't built for this (deck L1, slide 6)
**Evidence:** Narrated — "You might ask yourself if we can simply use LLMs for these tabular predictions. The answer is no, they're terrible for this task. And that is the case because they weren't built for this and structurally fail for tabular predictions. The reasons for this are plentiful. First, they don't understand entire numbers, but tokenize individual digits or pairs of digits, and make stupid math mistakes like this. They're inherently sequential, and therefore flatten tables into a very long sequence. [...] LLMs also don't understand table invariances. If you exchange two rows or you exchange two columns, it's still the same dataset, but the LLM doesn't realize that. LLMs are also much larger than they need to be. They're on the range of 10,000 times more parameters than the best tabular foundation models, and are still way worse. [...] Finally, LLMs are non-deterministic, and they hallucinate, both of which you really can't have in data science. So in summary, while we all love LLMs for unstructured data, they are far too slow, expensive, and inaccurate for tabular predictions."
**Text on slide:** LLMs aren't built for this · Why language models structurally fail on tabular data · 8.8 − 8.11 = −0.31 · LLMs tokenize digits, don't understand entire numbers · LLMs flatten tables into a (very long) sequence · LLMs don't understand table invariances · 10.000x more parameters · Most LLM parameters are wasted on tables · LLMs are non-deterministic · "The James Webb Space Telescope took the very first pictures of exoplanets." · LLMs hallucinate · LLMs are far too slow, expensive and inaccurate for tabular predictions
**Visual description:** Six tiles in a row, each with a caption below. (1) The wrong subtraction
"8.8 − 8.11 = −0.31" with each token shaded a different pastel color. (2) A snippet of a table
flattened into pipe-separated text ("| Customer ID | Monthly Spend| Data Usage (GB) | Churn? |
--- | ... CUST001 | $65 | ..."), also token-shaded. (3) A grey-violet tile with a small grid and
a horizontal and a vertical double arrow (swapping columns and rows). (4) A solid purple tile
reading "10.000x more parameters". (5) A grey tree of dots with arrows branching (non-determinism).
(6) A pale tile with the false claim about the James Webb Space Telescope in italics
(hallucination). The summary line sits below in large navy text.
**What it teaches:** Six structural reasons LLMs are a poor fit for tabular prediction:
digit-level tokenization, flattening into very long sequences, blindness to row/column order
invariance, oversized parameter counts, non-determinism, and hallucination.

### Slide 2.7 — LLMs vs Tabular Foundation Models (TFMs) (deck L1, slide 7)
**Evidence:** Narrated — "You can think of Tabular Foundation Models as the equivalent of LLMs, but actually made for tabular structured data. Now don't get me wrong, LLMs are amazing. They work on all kinds of unstructured data no matter the domain. They excel at language and world knowledge. They're great at generating summaries and explanations, and especially coding. and thereby really boost our productivity. But the fact remains that they're terrible for predictions on structured data, like databases, CSVs, spreadsheets, and time series. And to make predictions and forecasts on those, you really need to excel at numbers and statistics and recognizing patterns. And if you can do that, you can directly plug into the machine learning value chain that has been set up for the last 50 years with traditional machine learning methods for tabular data."
**Text on slide:** LLMs · Tasks over unstructured data, no matter the domain · - Excel at language & knowledge · - Generate summaries, explanations, code · - Boost business productivity · Tabular Foundation Models (TFMs) · Tasks over structured data, no matter the domain · databases · CSVs · spreadsheets · time series · - Excel at numbers, statistics & patterns · - Generate predictions, forecasts, scores · - Directly plug into existing ML value chain
**Visual description:** Two side-by-side panels with no slide title. Left, a coral-red panel
headed "LLMs" in white, containing a white card with "Tasks over **unstructured** data, no matter
the domain" and the OpenAI, Anthropic, Mistral AI, xAI and Cohere logos, then a pale card with
the three bullets. Right, a lavender panel headed "Tabular Foundation Models (TFMs)" in black,
containing a dark navy-violet card with "Tasks over **structured** data, no matter the domain",
the four data kinds, and a faded PRIOR wordmark, then a navy card with the three bullets in white.
(The extracted text layer repeats the left panel's heading line; it appears once on the page.)
**What it teaches:** LLMs and TFMs are parallel kinds of foundation model: LLMs for unstructured
data and language work, TFMs for structured data and predictions, forecasts and scores that slot
into the existing ML value chain. The same comparison returns as Slide 6.2.

### Slide 2.8 — Traditional ML doesn't scale – nothing compounds (deck L1, slide 8)
**Evidence:** Narrated — "Given a dataset, the typical data science workflow usually includes cleaning the data and selecting the right machine learning model, engineering better features and tuning model hyperparameters, and finally model deployment, maintenance, and governance. And given a new dataset, all of these steps repeat. Such data science projects often take 3 to 6 months until production, and a dedicated ML team for each problem. There's zero knowledge transfer between the models for each of these different tasks, and 60% of machine learning engineering time is actually spent on model maintenance."
**Text on slide:** Traditional ML doesn't scale – nothing compounds · Each prediction task requires its own pipeline, infra and team · EHR dataset · Data cleaning & model selection · Feature engineering & model tuning · Model deployment, maintenance & governance · predictions · … · CRM dataset · Data cleaning & model selection · Feature engineering & model tuning · Model deployment, maintenance & governance · predictions · 3–6 months and a dedicated ML team – per problem · Zero transfer: models learn nothing from each other · 60% of ML engineering spent on maintenance
**Visual description:** Two identical horizontal pipelines, one above the other, separated by a
large "· · ·". Top in navy: a 5×5 grid of squares labelled "EHR dataset", arrows through the three
stages, ending in a navy "predictions" box. Bottom in magenta-purple: the same with "CRM dataset".
Three navy statements sit along the bottom.
**What it teaches:** In the traditional workflow every dataset needs its own full pipeline, which
is slow, transfers nothing between tasks, and is dominated by maintenance cost.

### Slide 2.9 — Foundation models to the rescue (deck L1, slide 9)
**Evidence:** Narrated — "Instead of all these custom pipelines, you can simply get instant predictions in a single neural network forward pass. You simply input the data into a tabular foundation model, like TabPFN, and it makes predictions with no need for training or hyperparameter tuning. Some of our customers have replaced over 100 custom models by a single tabular foundation model like TabPFN, and this can help data scientists become dramatically more efficient, so becoming a 10x data scientist."
**Text on slide:** Foundation models to the rescue · One model can replace all these custom pipelines: instant predictions in a forward pass · any dataset · TabPFN · predictions · Helping data scientists become "10x data scientists"
```python
clf = TabPFNClassifier().fit(X_train, y_train)
predictions = clf.predict(X_test)
```
**Visual description:** One short pipeline: a navy 5×5 grid labelled "any dataset", an arrow to
the bold word "TabPFN", an arrow to a navy "predictions" box. Below, a grey code card with the
two-line scikit-learn-style snippet (class name in blue, method names in magenta). A light-blue
tilted sticker with red text, "Helping data scientists become "10x data scientists"", overlaps the
code card's lower edge.
**What it teaches:** A single pretrained model replaces the per-dataset pipelines of Slide 2.8,
used through a familiar fit/predict interface.

### Slide 2.10 — Deep Learning finally excels for tabular data (deck L1, slide 10)
**Evidence:** Narrated — "Tabular foundation models have taken the lead in all kinds of tabular benchmarks by storm, in an area for which deep learning didn't used to work well. Gradient-boosted decision trees like XGBoost, LightGBM, and CatBoost ruled tabular data for over a decade. But then, over the course of two years, dozens of new tabular foundation models appeared, and they now completely dominate gradient-boosted decision trees, with a similar difference in Elo scores like there is between gradient-boosted decision trees and the simplest machine learning models out there like k-nearest neighbors."
**Text on slide:** Deep Learning finally excels for tabular data · TabArena: Elo vs. method introduction date · Pareto front (best over time) · Foundation Model · Neural Network · Tree-based · Other · Elo · Date introduced · The new wave of DL methods · TabArena classification (benchmark with datasets up to 100k data points); https://tabarena.ai · (labelled points) XGBoost · LightGBM · CatBoost · FastaiMLP · EBM · TorchMLP · PerpetualBooster · ModernNCA · TabPFNv2 · TabM · TabDPT · RealMLP · TabICL · BetaTabPFN · LimiX · xRFM · SAP-RPT-OSS · Mitra · TabSwift · ILTM · TabSTAR · TabFlex · OrionMSP · Nori-30M · Nori · TabDPT-Turbo · ChimeraBoost · TabICLv2 · RealTabPFN-2.5 · TabPFN-2.6 · TabPFN-3 · EXAONE-Tabular · TabPFN-3-Thinking · TabFM · TabPFN-3.5-prerelease · TabPFN-3.5-Thinking-prerelease
**Visual description:** A scatter chart with Elo (about 1000 to 1900) on the y-axis and date
introduced (2014 to 2026) on the x-axis. Dots are colored by method type (purple foundation model,
blue neural network, green tree-based, grey other). An orange step line, the Pareto front, runs
flat from XGBoost (2014, about 1350) to LightGBM (2016, about 1400) until 2024, then climbs in
steps through RealMLP, RealTabPFN-2.5, TabPFN-2.6, TabPFN-3, TabPFN-3-Thinking and TabFM to
TabPFN-3.5-Thinking-prerelease (about 1900). A red ellipse encloses the 2024–2026 cluster,
labelled in red "The new wave of DL methods". The source caption sits below the chart.
**What it teaches:** On the TabArena benchmark, tabular foundation models arrived in about two
years and now lead tree-based methods that had been the state of the art for a decade.

### Slide 2.11 — TabPFN overview of pretraining & inference (deck L1, slide 11)
**Evidence:** Narrated — "So we can simply download a pretrained TabPFN and apply it out of the box to arbitrary real-world datasets that the model never saw before. and without any training phase on this new dataset, you take the entire dataset, present it to TabPFN in context, do a forward pass, and read out the probabilistic predictions for the test rows. [...] On the left side is how we pre-train TabPFN. [...] So, during pre-training, The types of inputs to TabPFN look like the same as you would see in practice, entire datasets with a question mark for the y_test portion. For the pre-training datasets, however, we know this y_test, and we compute a loss function that judges how likely this y_test is under the predictions that TabPFN makes. And this loss function is what we optimize. We use the standard stochastic gradient descent training [...] And then we iterate. We throw away the data set, generate another synthetic data set from scratch, make a prediction on it, compute the loss, and change the weights of TabPFN again. And we do that hundreds of millions of times, with a new dataset each time."
**Text on slide:** TabPFN overview of pretraining & inference · TabPFN is pretrained on synthetic data to take entire datasets as inputs and predict in a forward pass. · X_train · y_train · X_test · ? · TabPFN · NN parameterized by θ · y_test · −log q_θ(y_test|…) · to be optimized by SGD on θ across millions of datasets · Slow, done by the model provider once per release · The pretrained TabPFN can be applied out-of-the-box to arbitrary unseen real-world datasets. · X_train · y_train · X_test · ? · TabPFN · An arbitrary real-world dataset. · Fast; one forward pass on the real data
**Visual description:** Two paper-style diagrams side by side. Left, under a purple header band on
a lavender panel: a dataset block (X_train, y_train, X_test, "?") with an arrow into a "TabPFN /
NN parameterized by θ" box, then an arrow to a grey histogram (a predictive distribution); a
separate y_test box feeds a loss box "−log q_θ(y_test|…) to be optimized by SGD on θ across
millions of datasets", and an arrow loops from the histogram down into the loss. Caption below:
"Slow, done by the model provider once per release". Right, under a teal header band on a pale
green panel: the same dataset block into "TabPFN" and a histogram, with a curved arrow pointing at
X_test labelled "An arbitrary real-world dataset." Caption below: "Fast; one forward pass on the
real data".
**What it teaches:** TabPFN is pretrained once, by the provider, on many synthetic datasets with
a likelihood loss; at use time it takes a whole new dataset as input and returns a predictive
distribution for the test rows in a single forward pass, with no training on that dataset.

### Slide 2.12 — TabPFN v2: deep learning finally made it for tabular data (deck L1, slide 12)
**Evidence:** Narrated — "So in January 2025, we published the second version of this work, TabPFN v2, in Nature magazine. And that became a breakthrough moment for tabular data. In 2025, it was actually the most cited paper published in Nature. In '24, that was AlphaFold, and in late 2025, DeepSeek-R1 was also published in Nature and is also highly cited by now. So we're in really good company. TabPFN v2 was the first model that clearly outperformed gradient-boosted trees for tabular data and became a standard tool for data scientists."
**Text on slide:** TabPFN v2: deep learning finally made it for tabular data · Nature's #1 most cited paper published in 2025, along with DeepSeek-R1 · nature · TABULAR FOUNDATION · Foundation Models advance prediction on small data tables · Article · Open access · Published: 08 January 2025 · Accurate predictions on small data with a tabular foundation model · Noah Hollmann, Samuel Müller, Lennart Purucker, Arjun Krishnakumar, Max Körfer, Shi Bin Hoo, Robin Tibor Schirrmeister & Frank Hutter · Nature 637, 319–326 (2025) · Cite this article · 432k Accesses · 438 Citations · 515 Altmetric · Metrics · Alejandro Saucedo | KubeCon 2025 AI Day Keynote · @AxSaucedo · We've entered the ImageNet moment for Tabular Data! A new Tabular Foundational Model is released with TabPFN 2.5 tackling zero-shot predictions; and the sky is the limit in a world that runs on tabular data (spreadsheets anyone?): · GitHub · 6K+ STARS · 3M+ DOWNLOADS · Normalized ROC AUC · LightGBM · XGBoost · Catboost · TabPFN-2.5 · Tuned (1h) · Default
**Visual description:** A banner at top (pink-violet box inside a navy frame) with the Nature
claim. Below, three images: left, the Nature magazine cover headlined "TABULAR FOUNDATION" with a
microscope and lab objects on a grid; center, a screenshot of the paper's article header with a
quoted social post beneath it (the phrase "ImageNet moment for Tabular Data!" highlighted yellow);
right, a navy card with the GitHub logo, "6K+ STARS", a download icon with "3M+ DOWNLOADS", and a
small bar chart of normalized ROC AUC where TabPFN-2.5's bar (about 0.85–0.88) stands well above
LightGBM, XGBoost and CatBoost (about 0.3–0.55), with light "Tuned (1h)" and dark "Default"
segments.
**What it teaches:** The TabPFN v2 paper in Nature (January 2025) as the breakthrough, with
evidence of adoption (stars, downloads) and of TabPFN-2.5 beating tuned gradient-boosted trees.

### Slide 2.13 — TabPFN size limit over the years (deck L1, slide 13)
**Evidence:** Narrated — "Initially, TabPFN was limited to small datasets with up to 10,000 rows only for TabPFN v2. but this limit quickly moved to 100,000 with TabPFN-2.5, a million with TabPFN-3, and then 10 million with TabPFN-4. So an increase of a factor of 1,000, going from 10,000 to 10 million in less than 2 years."
**Text on slide:** TabPFN size limit over the years · Row Limit (Log Scale) · 1,000 · 10,000 · 100,000 · 1,000,000 · 10,000,000 · Jan 2025 · Nov 2025 · May 2026 · Late 2026 · TabPFN v2 · TabPFN-2.5 · TabPFN-3 · TabPFN-4 · 1000x increase in row limit in less than 2 years
**Visual description:** A line chart on a log y-axis (1,000 to 10,000,000 rows). Four navy dots
joined by a line: TabPFN v2 at 10,000 (Jan 2025), TabPFN-2.5 at 100,000 (Nov 2025), TabPFN-3 at
1,000,000 (May 2026), TabPFN-4 at 10,000,000 (Late 2026), each with a lavender label box. The
summary line is in italic navy below. (The extracted text layer lists the labels out of order;
the order above is the one on the chart.)
**What it teaches:** Each TabPFN release raised the row limit by ten times, a thousand-fold
increase in under two years.

### Slide 2.14 — TabPFN is easy to use (deck L1, slide 14)
**Evidence:** Narrated — "Like an open-weight language model, you can access it in a variety of different ways: locally downloading the weights from Hugging Face or by a simple pip install and running it on your machine, through our API where it runs on our GPUs, through our VPC where it runs in your own trusted cloud, or via agents talking to our MCP server. So I really encourage you to try it out."
**Text on slide:** TabPFN is easy to use · It can be accessed in a variety of ways · OSS (Non-Commercial) · API & VPC · MCP
**Visual description:** A navy rounded band holding three purple tiles: "OSS (Non-Commercial)"
with a GitHub logo, "API & VPC" with the PRIOR wordmark, and "MCP" with the PRIOR wordmark.
**What it teaches:** TabPFN can be used as an open-source package (non-commercial license), via
Prior Labs' hosted API or a VPC deployment, or through an MCP server for agents.

### Slide 2.15 — TabPFN is used in thousands of applications (deck L1, slide 15)
**Evidence:** Narrated — "TabPFN has been used in thousands of prediction tasks in many different verticals like healthcare, finance, industrials, energy, tech, and many more."
**Text on slide:** TabPFN is used in thousands of applications · Prediction tasks in healthcare, finance, industrials, energy, tech and many more · HEALTHCARE · Drug response · ENERGY · Load forecasting · INDUSTRIALS · Predictive maintenance · BUSINESS ANALYTICS · Lead scoring · FINANCE · Market Forecasting · SUPPLY CHAIN · Resource planning · MANUFACTURING · Quality control · TabPFN · TRADING · Signal generation · PHARMACEUTICAL · Clinical trial forecasting · INSURANCE · Fraud detection · INDUSTRIALS · Site Operations · BUSINESS ANALYTICS · Sales forecasting · BANKING · Credit risk scoring · TECH · Customer lifetime value · 15
**Visual description:** A 5×3 grid of rounded tiles in alternating navy, violet and pink; each
tile has a small uppercase industry label at top and a use case below. The center tile is a
blurred lavender gradient with "TabPFN" in large white type. A small page number "15" sits bottom
right on the wave.
**What it teaches:** The breadth of real tabular prediction use cases across industries.

---

## Lesson 3: Classification, Regression & Forecasting with TabPFN
Transcript: `## Lesson 3: Classification, Regression & Forecasting with TabPFN` in transcripts/tabular-foundation-models-for-data-science-agents-transcripts.md

All 8 slides of deck "L2" belong here; the title card names this lesson, and the narration covers
them in deck order before switching to the notebook: fit/predict mechanics, classification,
the confusion matrix with precision and recall, regression as a point and as a distribution, and
time-series forecasting.

### Slide 3.1 — Title card: Classification, Regression & Forecasting with TabPFN (deck L2, slide 1)
**Evidence:** Deck-only (title card; it names this lesson)
**Text on slide:** Tabular Foundation Models for Data Science Agents · Classification, Regression & Forecasting with TabPFN · Tuana Çelik · Prior Labs
**Visual description:** Tall white title card. Course title in coral red on two lines, the lesson
title in black on two lines, "Tuana Çelik · Prior Labs" in grey, and the PRIOR and DeepLearning.AI
logos near the bottom. No wave.
**What it teaches:** Names the lesson and its instructor.

### Slide 3.2 — Same API, different mechanics (deck L2, slide 2)
**Evidence:** Narrated — "And TabPFN is also scikit-learn compatible, It uses the same fit, predict terminology. However, what happens during fit and what happens during predict is slightly different. For classical machine learning models, when you fit a model, this usually means that you're training a model from scratch with your own dataset. And then predict is pretty fast because it just applies a prediction over the pre-trained model. However, with TabPFN, when we say .fit(), we're really just providing our training data or historical data as context to the model, but most of the work really happens during predict. We do the one forward pass over our context and the new rows that we want to predict, and we learn about our data, as well as predict during this predict call."
**Text on slide:** Same API, different mechanics · scikit-learn compatible · same fit / predict — swap in as a drop-in estimator, no pipeline rewrite · Classical ML · .fit() → Trains a new model — slow, per dataset · .predict() → Applies it — cheap · TabPFN · .fit() → Uploads the training table as context — no training · .predict() → One transformer forward pass over context + new rows · in-context learning — all the compute lives here
**Visual description:** A grey "scikit-learn compatible" label beside its one-line explanation.
Below, two cards. "Classical ML" (grey border): ".fit()" with a long grey bar under its
description and ".predict()" with a short grey bar. "TabPFN" (red border, blue heading): ".fit()"
with a very short red bar and ".predict()" with a long red bar; "context + new rows" and the
in-context-learning line are in blue. The bar lengths show where the compute goes.
**What it teaches:** TabPFN keeps the scikit-learn fit/predict interface but inverts the cost: fit
only hands over the training table as context, and the work happens in predict, as one forward
pass over context plus the new rows.

### Slide 3.3 — Classification: is this patient at risk? (deck L2, slide 3)
**Evidence:** Narrated — "Let's think about a use case where we have data about patients. This data comes in a tabular format and it holds information about patients, such as their age, but also, for example, information that may come from scans like chest pain, cholesterol levels, and so on. And we have a target value about whether a disease exists or not. [...] We do this with no training. The model learns the historical table in context, and we have two options. Either we can use predict, which will give us the label that our model predicts directly, or we could use predict_proba, which would give us the probability distribution for all possible labels. In this case we have the option of label 0 and 1, so for example we might get the response that the probability of label 1 is 0.81."
**Text on slide:** Classification: is this patient at risk? · Data about patients · target: disease · age · sex · chest pain · chol · thal · disease · 63 · Male · typical · 233 · fixed · 0 · 54 · Female · — · 286 · — · 1 · 41 · Male · atypical · — · normal · 0 · ⋮ · 58 · Female · non-ang. · — · normal · ? · missing value · No training — the model learns the (historical) table in context · predict() → label 1 · predict_proba() → 0.81 probability for label 1
**Visual description:** A light table with a blue-outlined "disease" target column. Three
historical rows, a dotted ellipsis row, and a highlighted last row (58, Female, non-ang., —,
normal) whose target cell is a solid blue "?". Several cells are grey with "—", and a grey legend
swatch reads "missing value". A blue-ruled callout states "No training — the model learns the
(historical) table in context". A bottom card shows the two calls and their outputs, "0.81" in
blue.
**What it teaches:** Binary classification on a patient table, including missing values; predict
returns a label and predict_proba returns per-class probabilities.

### Slide 3.4 — How well did the model do? (deck L2, slide 4)
**Evidence:** Narrated — "Once we've made predictions with our model, we can also have a look at how well the model did. For example, we can see what the predicted values of the labels were versus the actual values. So in our case, where we're looking at patients, we can have a look at how many we predicted to be sick versus how many actually were, and the same for healthy people. We can also use all of this information to evaluate our model and look at precision and recall. Precision in this case gives us: Of those flagged sick, what ratio is really sick? And recall tells us: Of the truly sick, what ratio did we catch?"
**Text on slide:** How well did the model do? · predicted sick · predicted healthy · actually sick · actually healthy · Caught · true positive · Missed disease · false negative · the costly one · False alarm · false positive · one extra test · Correct · true negative · Precision · of those flagged sick, what's ratio is really sick? · TP / TP+FP · Recall · of the truly sick, what ratio did we catch? · TP / TP+FN
**Visual description:** A 2×2 confusion matrix: columns "predicted sick" and "predicted healthy",
rows "actually sick" and "actually healthy". The diagonal cells are solid green ("Caught / true
positive", "Correct / true negative"); "Missed disease / false negative / the costly one" has a
red outline and red text; "False alarm / false positive / one extra test" has an orange outline
and orange text. Two grey cards below give Precision and Recall in blue with their fractions.
**What it teaches:** How to read a confusion matrix in a medical framing, why false negatives cost
more than false positives here, and the definitions of precision and recall.

### Slide 3.5 — "Every regression is a distribution" with a single-price output (deck L2, slide 5)
**Evidence:** Narrated — "Other than predicting labels of specific classes, we can also use TabPFN to predict a number. We call this a regression task. Imagine a scenario where we have information about houses, like how big they are, how many bedrooms they have, what year they were built, etc., and we can use TabPFN to predict a specific price of what the sale price might be."
**Text on slide:** Every regression is a distribution · sqft · beds · year · price · 1,840 · 3 · 1998 · ? · TabPFN · a specific price · 345.000
**Visual description:** Title at top; the rest is one row near the top left: a small table (sqft
1,840, beds 3, year 1998, price "?" in blue), a blue arrow to a coral-red "TabPFN" box, a blue
arrow to "a specific price" with "345.000" in grey beneath. The lower two thirds are empty. The
drawing is the same as Slide 3.6 but shifted left, under the title of Slide 3.7.
**What it teaches:** Same content as Slide 3.6 (a point prediction of price). It reads as a build
stage between Slides 3.6 and 3.7, filed out of order in the deck; that is a reading of the
drawings, not a fact.

### Slide 3.6 — Predict a number: regression (deck L2, slide 6)
**Evidence:** Narrated — the same passage as Slide 3.5: "we can use TabPFN to predict a specific price of what the sale price might be."
**Text on slide:** Predict a number: regression · sqft · beds · year · price · 1,840 · 3 · 1998 · ? · TabPFN · a specific price · 345.000
**Visual description:** The same one-row diagram as Slide 3.5, centered horizontally, under the
title "Predict a number: regression". The lower two thirds are empty.
**What it teaches:** Regression predicts a number; for a house with given size, bedrooms and year,
TabPFN returns a single price.

### Slide 3.7 — Every regression is a distribution (deck L2, slide 7)
**Evidence:** Narrated — "However, we can also go beyond that. Every regression is also a distribution. We can use TabPFN to predict quantiles, for example, the 10th and 90th quantile, which basically gives us the edge of the estimation of what TabPFN thinks the value might be. You can think of these quantiles, 10 and 90 and everything in between, as the model saying that "I'm 80% sure that the value lies within this distribution." When these two numbers are close to each other, there's a higher confidence of what the actual value might be, but TabPFN may also provide a wider distribution, which should indicate to you that the model is not very certain about what the value would be."
**Text on slide:** Every regression is a distribution · sqft · beds · year · price · 1,840 · 3 · 1998 · ? · TabPFN · a distribution over sale price · p10 · p90 · 80% of the model's belief · thousands of fine bins · $200k · median · mean · $800k · "My best single guess is the mean — but I'd bet 80% odds the real price lands between the 10th and 90th percentile." · When these two numbers are close to each other, then higher confidence · A tight band is confidence; a wide band is the model telling you it's guessing.
**Visual description:** The same input row and TabPFN box, now ending in "a distribution over sale
price". Below, a blue bell-shaped density curve over a price axis from $200k to $800k, slightly
right-skewed. A light-blue shaded band spans from "p10" to "p90" with "80% of the model's belief"
beside it; a black dotted line marks the median at the peak and a grey dashed line, labelled
"mean" in orange, sits just right of it. Small grey text "thousands of fine bins" lies along the
left tail. A blue-ruled italic quotation and its follow-up line sit below, then a grey line with
"tight band" in blue and "wide band" in orange.
**What it teaches:** A TabPFN regression output is a full predictive distribution: the mean is the
default point estimate, the 10th–90th percentile band is an 80% interval, and the band's width
signals the model's confidence.

### Slide 3.8 — Time-series forecasting (deck L2, slide 8)
**Evidence:** Narrated — "TabPFN can also do time-series forecasting. It turns out that if we represent time-series data as a tabular problem, we can use the TabPFN regressor as a way to predict future values as well. For example, let's think of a scenario where we have hourly electricity prices, and we want to predict what the next 48 hours of electricity might be. We can represent this information in tabular format and ask TabPFN to predict future price estimates. We can also add additional features to help TabPFN be a bit more certain about future predictions too."
**Text on slide:** Time-series forecasting · atmospheric CO₂, monthly · observed · forecast · next 2 years · 80% band · 1 · Represent time-series as a tabular problem · 2 · A forecast is just a table with empty target rows · 3 · The model only knows what's in its context — adding additional features may help with time-series forecasting
**Visual description:** A line chart labelled "atmospheric CO₂, monthly": a black wavy, rising
"observed" series, then, after a dashed vertical divider, a grey-shaded "forecast · next 2 years"
region with a blue dotted forecast line inside a light-blue "80% band". Below, three numbered
cards; the third has a blue border and its second clause is in blue.
**What it teaches:** Forecasting is regression on a table whose future rows have empty targets;
the result has an uncertainty band, and adding features to the context can help. The chart's
example (monthly CO₂ over two years) differs from the narration's example (hourly German
electricity prices over the next 48 hours, which the notebook uses); the narration is
authoritative for what the lesson builds.

---

## Lesson 4: Interpreting TabPFN predictions
Transcript: `## Lesson 4: Interpreting TabPFN predictions` in transcripts/tabular-foundation-models-for-data-science-agents-transcripts.md

Slides 1–6 of deck "L3 and L4" belong here; slide 1 is a title card naming this lesson, and the
narration covers the concept slides (interpretability, SHAP waterfall, SHAP beeswarm, partial
dependence) before the notebook, then closes with the summary that Slide 4.6 repeats. See "How to
read this file" on the swapped opening sentence of this transcript.

### Slide 4.1 — Title card: Interpreting TabPFN predictions (deck L3 and L4, slide 1)
**Evidence:** Deck-only (title card; it names this lesson)
**Text on slide:** Tabular Foundation Models for Data Science Agents · Interpreting TabPFN predictions · Eliott Kalfon · Prior Labs
**Visual description:** Tall white title card in the same style as Slide 3.1, with "Eliott
Kalfon · Prior Labs" in grey. No wave.
**What it teaches:** Names the lesson and its instructor.

### Slide 4.2 — Interpreting TabPFN predictions (deck L3 and L4, slide 2)
**Evidence:** Narrated — "Interpretability helps us inspect how the model arrived at the output and what patterns its predictions reflect. We will use SHAP values to explain a single prediction and understand global feature importance. We will also build partial dependence plots to analyze the relationships between model features and predicted probabilities."
**Text on slide:** Interpreting TabPFN predictions · 63 1 233 0 · 37 1 250 0 · 41 0 204 1 · 56 1 236 0 · + · 52 1 199 ? · outputs predictions · ŷ = 1 · interpretability · how the model arrived at the output · & · what patterns predictions reflect
**Visual description:** An illustration (no text layer for its labels). Top: a 4-row numeric
training table plus a blue-outlined query row "52 1 199 ?", and "outputs predictions / ŷ = 1".
A red arrow bends down from the prediction into a coral-red "interpretability" box with a
magnifying-glass icon. On the left, a copy of the table with one column shaded blue, one shaded
red and one row shaded red feeds the box; under the box, two small magnified snippets (red and
blue lenses) of the table. To the right, the box points to a blue card "how the model arrived at
the output", an "&", a grey card "what patterns predictions reflect", and two small chart icons
(a bar-and-line chart and a line chart).
**What it teaches:** Interpretability asks which feature values and rows drove a prediction and
what patterns the model's predictions follow.

### Slide 4.3 — What feature values explain a single prediction? (deck L3 and L4, slide 3)
**Evidence:** Narrated — "SHAP values are estimated contributions of a feature value to a model prediction. We start by explaining the predicted probability of disease of a single patient with a SHAP waterfall plot. The waterfall starts at a reference prediction of about 0.4, and ends well above 0.9. Red contributions, positive SHAP values, move the model output upward, blue contributions, negative SHAP values, move it downward. For this patient, three blocked vessels contribute about 30 percentage points upward. Chest pain and Max heart rate also push the predicted probability of disease higher, while the normal Thallium scan contributes downward. All the contributions together bridge the gap from the reference to the final prediction."
**Text on slide:** What feature values explain a single prediction? · SHAP Value: estimated contribution of a feature value to a model prediction · Highest-risk patient: predicted risk 98% · f(x) = 0.981 · 3 = Blocked vessels +0.3 · asymptomatic = Chest pain type +0.09 · 109 = Max heart rate +0.06 · flat = ST slope +0.05 · male = Sex +0.04 · normal = Thallium scan −0.03 · 2.4 = ST depression +0.03 · no = Exercise angina −0.02 · 322 = Cholesterol +0.01 · 4 other features +0.01 · E[f(X)] = 0.445 · 0.4 · 0.5 · 0.6 · 0.7 · 0.8 · 0.9 · 1.0
**Visual description:** A SHAP waterfall chart titled "Highest-risk patient: predicted risk 98%".
Each row is a "value = feature" label with a horizontal arrow-bar: magenta-red bars pointing right
for positive contributions, blue bars pointing left for negative ones (Thallium scan −0.03,
Exercise angina −0.02). The bars chain from the base value E[f(X)] = 0.445 at the bottom to
f(x) = 0.981 at the top; the largest bar is Blocked vessels (+0.3). The x-axis runs 0.4 to 1.0.
**What it teaches:** How a SHAP waterfall decomposes one patient's predicted probability into
per-feature contributions that add up from the average prediction to this prediction.

### Slide 4.4 — Which features does the model use? (deck L3 and L4, slide 4)
**Evidence:** Narrated — "To understand which features the model uses in general, we can visualize all SHAP values for all features together. This is a SHAP beeswarm plot. Each dot represents one patient's attribution for one feature. A dot to the right indicates a contribution towards a higher predicted disease probability, a dot on the left indicates a contribution in the other direction. Features are ordered by their average absolute contribution across the records shown. Blocked vessels is at the top. Its higher values, shown in red, push the predicted probabilities up, while lower values in blue mostly appear on the negative side. color is the feature value, not the prediction."
**Text on slide:** Which features does the model use? · We can also plot all SHAP values for all features and records. · This gives us a high-level summary of feature importance. · Global drivers of coronary-disease risk · each dot is a patient; right = pushed toward disease, red = high feature value · Blocked vessels · Chest pain type · Thallium scan · ST slope · Sex · Exercise angina · Max heart rate · ST depression · Resting ECG · Resting BP · Cholesterol · High fasting sugar · Age · SHAP value (impact on model output) · −0.1 · 0.0 · 0.1 · 0.2 · 0.3 · Feature value · High · Low
**Visual description:** A SHAP beeswarm chart with 13 features on the y-axis in the order listed
and SHAP value on the x-axis (about −0.15 to 0.3), a vertical grey line at 0. Each dot is colored
on a blue (low) to magenta (high) feature-value scale shown on a color bar at right. Blocked
vessels spreads widest, with red dots up to about +0.3 and blue dots on the left; the bottom
features (Cholesterol, High fasting sugar, Age) cluster tightly near 0.
**What it teaches:** A beeswarm summarizes SHAP values across many patients to rank features by
global importance and show which direction high and low values push the prediction.

### Slide 4.5 — What is the impact of these features on model predictions? (deck L3 and L4, slide 5)
**Evidence:** Narrated — "To better understand how the model responds to changes in input features, We can use Partial Dependence Plots. To build a Partial Dependence Plot, we keep all feature values constant and vary the value of a single selected feature. On the top-left chart, we can see that the predicted probability of disease increases as the number of blocked vessels increases, too. On the other hand, the predicted probability of disease decreases as the Max heart rate increases, as a sign of good cardiovascular health."
**Text on slide:** What is the impact of these features on model predictions? · Partial Dependence Plots: show the relationship between the predicted probability and continuous features. · How average predicted risk moves with each measurement · shared y-axis, so panel steepness is directly comparable · Predicted P(disease) · Blocked vessels · Max heart rate · ST depression · Resting BP
**Visual description:** A 2×2 grid of line plots sharing a y-axis "Predicted P(disease)" (about
0.35 to 0.65). The top two panels sit on a pink highlight. Top left, Blocked vessels (0 to 3):
rises steeply from about 0.35 to about 0.67. Top right, Max heart rate (about 110 to 180): falls
from about 0.52 to about 0.39. Bottom left, ST depression (0 to 3): rises gently from about 0.42
to about 0.51. Bottom right, Resting BP (about 110 to 160): nearly flat, about 0.43 to 0.46. Each
x-axis has rug ticks.
**What it teaches:** Partial dependence plots show how the average predicted probability changes
as one feature varies; steeper panels mean stronger influence. (The narrated notebook later plots
Cholesterol where this slide shows Resting BP.)

### Slide 4.6 — Interpreting TabPFN predictions: summary (deck L3 and L4, slide 6)
**Evidence:** Narrated — "In this notebook, we explored three methods to interpret TabPFN predictions. We first explain individual predictions with SHAP values and a waterfall plot. We then plotted all of these SHAP values on a beeswarm plot to get a better idea of feature importance. We also explored partial dependence plots that show us how the model responds to changes in individual feature values."
**Text on slide:** Interpreting TabPFN predictions · Three methods to interpret TabPFN predictions: · Explain individual prediction with shad values and waterfall plot · Plot all the shad values on visual plot to get better idea of feature importance. · Partial dependence plots that shows how the model responds to changes in individual feature values.
**Visual description:** A text-only slide: an intro line and three bullets, each starting with a
bold phrase ("Explain individual prediction", "Plot all the shad values", "Partial dependence
plots"). "shad values" is printed as written (a misspelling of SHAP), and "visual plot" stands
where the narration says "beeswarm plot".
**What it teaches:** Recap of the three interpretation methods: SHAP waterfall for one
prediction, SHAP beeswarm for global importance, partial dependence for response to one feature.

---

## Lesson 5: Real-time inference with the KV cache
Transcript: `## Lesson 5: Real-time inference with the KV cache` in transcripts/tabular-foundation-models-for-data-science-agents-transcripts.md

Slides 7–12 of deck "L3 and L4" belong here; slide 7 is a title card naming this lesson, and the
narration covers slides 8–11 in order before the notebook. Slide 12 is blank. See "How to read
this file" on the swapped opening sentence of this transcript.

### Slide 5.1 — Title card: Real-time inference with the KV cache (deck L3 and L4, slide 7)
**Evidence:** Deck-only (title card; it names this lesson)
**Text on slide:** Tabular Foundation Models for Data Science Agents · Real-time inference with the KV cache · Eliott Kalfon · Prior Labs
**Visual description:** Tall white title card in the same style as Slide 4.1. No wave.
**What it teaches:** Names the lesson and its instructor.

### Slide 5.2 — Real-time inference with the KV cache (deck L3 and L4, slide 8)
**Evidence:** Narrated — "In this lesson, we'll use TabPFN's Key Value Cache to reuse a fixed training context and measure its impact on request latency, the time it takes for TabPFN to output a prediction."
**Text on slide:** Real-time inference with the KV cache · TabPFN Key Value (KV) Cache to reuse a fixed training context and measure its impact on request latency, the time it takes for TabPFN for output a prediction. · DEFAULT MODE · full forward pass · ŷ = 0 · recomputes entire context every query · WITH KV CACHE · CACHED KV · 52 1 199 ? · cached forward pass · ŷ = 0 · REUSE
**Visual description:** The lesson statement as a justified paragraph, then an illustration (its
labels are not in the text layer). Left, "DEFAULT MODE": a 4-row numeric table plus a "?" query
feeds a red "full forward pass" box giving "ŷ = 0", with a red dashed curved arrow back to the
table labelled in handwriting "recomputes entire context every query". Right, "WITH KV CACHE": a
reduced table next to a blue "CACHED KV" block with a padlock icon holding the query row
"52 1 199 ?", feeding a red "cached forward pass" box giving "ŷ = 0"; a green circular-arrows
icon below reads "REUSE".
**What it teaches:** Without a cache, every query reprocesses the whole training context; with the
KV cache, the context's representation is kept and reused across queries, lowering latency.

### Slide 5.3 — Inference without KV cache (deck L3 and L4, slide 9)
**Evidence:** Narrated — "Without the KV cache, TabPFN processes both the training context and the query row at every request. On the left are four labeled examples. The new row has feature values, but its target is unknown. the model processes the context and the new row to produce a prediction. For the second request, the blue row changes, but the training set is the same. Without the cache, that context is processed again, The third request repeats the pattern. Without the KV cache, we repeatedly process the context rows. This slows down inference."
**Text on slide:** Inference without KV cache · age · sex · chol · target · 1 · 63 1 233 0 · 37 1 250 0 · 41 0 204 1 · 56 1 236 0 · + · 57 0 354 ? · forward pass · ŷ = 1 · 2 · (same four rows) · + · 44 1 263 ? · forward pass · ŷ = 0 · 3 · (same four rows) · + · 52 1 199 ? · forward pass · ŷ = 0 · 3× · full forward passes · 32 / 48 · cells re-read for nothing
**Visual description:** Three numbered requests stacked vertically. Each shows the same 4-row
training table (columns age, sex, chol, target), a "+", a blue-outlined query row with "?", a
coral "forward pass" box, and a light-blue prediction box. Queries and predictions: 57 0 354 →
ŷ = 1; 44 1 263 → ŷ = 0; 52 1 199 → ŷ = 0 (the third query row is shaded darker). Two grey stat
cards at the bottom: "3×" in blue over "full forward passes", and "32 / 48" over "cells re-read
for nothing". (The text layer repeats the training rows more often than the page shows.)
**What it teaches:** Without a cache, three queries cost three full passes over the same context;
of the three reads of the 16-cell table, two (32 of 48 cells) are wasted work.

### Slide 5.4 — Inference with KV cache (deck L3 and L4, slide 10)
**Evidence:** Narrated — "With the KV cache, we process the fixed training context once, and retain its key and value representations. Each new query can then use those representations rather than rebuild them from the training table. Notice that each query still requires model computation to generate predictions. Still, the KV cache saves a significant amount of computation."
**Text on slide:** Inference with KV cache · age · sex · chol · target · 63 1 233 0 · 37 1 250 0 · 41 0 204 1 · 56 1 236 0 · read once · encode · KV cache · keys + values for all 4 rows, in memory · 57 0 354 ? · read cache · ŷ = 1 · 44 1 263 ? · read cache · ŷ = 0 · 52 1 199 ? · read cache · ŷ = 0 · 1× · encode, then cheap reads · 16 / 16 · cells read, none wasted
**Visual description:** The training table once, labelled "read once", with an "encode" arrow to a
blue rounded "KV cache" box ("keys + values for all 4 rows, in memory"). A line drops from the box
to three query rows, each feeding a blue-outlined "read cache" oval and a prediction (the same
three queries and predictions as Slide 5.3). Two grey stat cards at the bottom: "1×" in blue over
"encode, then cheap reads", and "16 / 16" over "cells read, none wasted".
**What it teaches:** With the KV cache the context is encoded once into stored keys and values;
each query only reads the cache, giving the same predictions with no repeated context work.

### Slide 5.5 — When to use the KV-cache? (deck L3 and L4, slide 11)
**Evidence:** Narrated — "Use the cache for repeated requests, when latency matters, and when the training context stays fixed or changes slowly. On the other hand, in batch workflows, the training data is processed only once for all test rows, so there is no need to build the KV-cache for that. There is no repeated processing. When the training data changes frequently, the cost of rebuilding new caches could outweigh the benefits. Summarizing, the decision is about reuse. How often will we predict from the same context before replacing it?"
**Text on slide:** When to use the KV-cache? · ✓ Use it · Real-time inference · Low latency is critical · Fixed or slowly changing training set · ✕ Skip it · Batch workflows in which predictions are done in one go · Training set changes often or is used once · Rule of thumb: many predictions on the same training set? Cache it.
**Visual description:** Two stacked cards: a pale-green "Use it" card with a green check circle
and three bullets, and a pale-red "Skip it" card with a red cross circle and two bullets. A rule
of thumb sits below, its label in bold black and the rest in grey.
**What it teaches:** The cache pays off for repeated, latency-sensitive predictions on a stable
training set, and not for one-shot batch jobs or frequently changing data.

### Slide 5.6 — Blank slide (deck L3 and L4, slide 12)
**Evidence:** Deck-only (blank; no content to narrate)
**Text on slide:** (none)
**Visual description:** The content-slide frame only: PRIOR wordmark top left, DeepLearning.AI
logo top right, coral-red wave at the bottom; the body is empty.
**What it teaches:** Nothing; an empty trailing slide in the deck.

---

## Lesson 6: Building a Data Science Agent
Transcript: `## Lesson 6: Building a Data Science Agent` in transcripts/tabular-foundation-models-for-data-science-agents-transcripts.md

All 10 slides of deck "L5" belong here; the title card names this lesson, and the narration walks
through them in deck order before the Claude Code demo: LLMs versus TFMs (repeated from Lesson 2),
an LLM answering from data it has and guessing on data it lacks, the prediction framing, next-token
versus outcome distributions, TabPFN as a tool, the tool-call flow, and the TabPFN MCP server.
The demo itself has no slides (see "How to read this file").

### Slide 6.1 — Title card: Building a Data Science Agent (deck L5, slide 1)
**Evidence:** Deck-only (title card; it names this lesson)
**Text on slide:** Tabular Foundation Models for Data Science Agents · Building a Data Science Agent · Tuana Çelik · Prior Labs
**Visual description:** Wide white title card: course title in large coral red on two lines,
"Building a Data Science Agent" in black, "Tuana Çelik · Prior Labs" in grey, then the PRIOR and
DeepLearning.AI logos. No wave.
**What it teaches:** Names the lesson and its instructor.

### Slide 6.2 — LLMs vs TFMs (deck L5, slide 2)
**Evidence:** Narrated — "Lesson 1 with Frank, you had a brief look into the difference between Large Language Models and tabular foundation models, and how while Large Language Models are great with dealing with unstructured data, how tabular foundation models really focus on dealing with structured data like tables. In this lesson, we're going to also see how they work better together to create agents that are able to make predictions over your tabular data."
**Text on slide:** LLMs vs TFMs · LLMs · Tasks over unstructured data, no matter the domain · - Excel at language & knowledge · - Generate summaries, explanations, code · - Boost business productivity · Tabular Foundation Models (TFMs) · Tasks over structured data, no matter the domain · databases · CSVs · spreadsheets · time series · - Excel at numbers, statistics & patterns · - Generate predictions, forecasts, scores · - Directly plug into existing ML value chain
**Visual description:** The same content as Slide 2.7, restyled and with a title "LLMs vs TFMs":
a white left panel with a grey border ("LLMs" in black, the five LLM vendor logos, a pale bullets
card) and a navy right panel ("Tabular Foundation Models (TFMs)" in white, the four data kinds,
the PRIOR wordmark in white, a white bullets card).
**What it teaches:** Recalls Lesson 2's split: LLMs for language and reasoning, TFMs for
predictions on tables. This lesson combines them. ("Lesson 1 with Frank" in the narration is the
transcripts' Lesson 2.)

### Slide 6.3 — LLMs for reasoning - not prediction (deck L5, slide 3)
**Evidence:** Narrated — "Large language models are great for reasoning, not necessarily prediction. But let's think of a scenario where we have all this information about customers, how long they've been your customer, how much they pay you, and all the information about past customers who've churned or not churned. If we were to ask a large language model, did customer C-1042 churn? In this particular scenario, we'll get an answer, but if you pay attention, you will also see that the answer is in fact in the data."
**Text on slide:** LLMs for reasoning - not prediction · LLMs excel at language tasks: parsing, lookup, extraction. · CUSTOMERS.CSV · customer · tenure · plan · $/mo · tickets · churned · C-1041 · 34 · annual · 49 · 0 · no · C-1042 · 3 · monthly · 89 · 4 · yes · C-1043 · 18 · monthly · 59 · 1 · no · C-1044 · 7 · monthly · 99 · 5 · yes · C-1045 · 52 · annual · 39 · 0 · no · USER · Did customer C-1042 churn? · LLM · Yes — C-1042 churned after 3 months on the monthly plan, with 4 support tickets. · The answer was in the data.
**Visual description:** Left, a table captioned "CUSTOMERS.CSV" with five customers; the C-1042
row is shaded pink with "yes" in red. Right, a chat: a grey "USER" bubble with the question, a
blue-bordered "LLM" bubble with the answer ("Yes" in bold), and a blue check mark beside "The
answer was **in the data**."
**What it teaches:** An LLM answers correctly when the answer is a lookup in data it can see.

### Slide 6.4 — What about unseen data? (deck L5, slide 4)
**Evidence:** Narrated — "Now asking some questions about unseen data is a slightly different task. Instead, let's assume we have a new customer, and we don't yet know that they've churned or not. And let's ask the same question. will customer C-1046 churn? It will give you an answer, but it will be a plausible answer, and we won't know where this answer really is coming from statistically."
**Text on slide:** What about unseen data? · The answer isn't in the table. The model produces one anyway. · CUSTOMERS.CSV · customer · tenure · plan · $/mo · tickets · churned · C-1041 · 34 · annual · 49 · 0 · no · C-1042 · 3 · monthly · 89 · 4 · yes · C-1043 · 18 · monthly · 59 · 1 · no · C-1044 · 7 · monthly · 99 · 5 · yes · C-1045 · 52 · annual · 39 · 0 · no · C-1046 · 5 · monthly · 94 · 3 · ? · USER · Will customer C-1046 churn? · LLM · Similar to other short-tenure monthly customers — I'd say about 70% likely. · Plausible — but nothing was statistically learned from the rows. "70%" is a phrase, not a probability.
**Visual description:** The same table with a sixth row, C-1046, shaded peach under an orange
rule, its "churned" cell an orange "?". Right, the USER question, the LLM's answer ("about 70%
likely" in bold), and a red exclamation-mark circle beside the warning ("nothing was
statistically learned" in bold).
**What it teaches:** For a row whose outcome is unknown, an LLM still answers, but its number is
a plausible-sounding phrase, not a probability learned from the data.

### Slide 6.5 — This is a prediction problem (deck L5, slide 5)
**Evidence:** Narrated — "We're going to look at how we can use TabPFN the same way we've used it before, but instead of a large language model answering the question on its own, it will use our historical data as training sets or, in this case, context sets, and our new row as the query. This is really a supervised learning problem."
**Text on slide:** This is a prediction problem · Five customers with a known outcome, one without: supervised learning. · features · target · tenure · plan · $/mo · tickets · churned · 34 · annual · 49 · 0 · no · 3 · monthly · 89 · 4 · yes · 18 · monthly · 59 · 1 · no · 7 · monthly · 99 · 5 · yes · 52 · annual · 39 · 0 · no · 5 · monthly · 94 · 3 · ? · training (context) set · query · Every pattern the answer should be based on lives in the labelled rows. We need a model that actually learns from them.
**Visual description:** The same six rows without the customer-ID column. A red rule above the
four feature columns is labelled "features" and an orange rule above "churned" is labelled
"target". A red vertical bracket beside the five pink rows reads "training (context) set"; an
orange bracket beside the peach last row reads "query". A grey card at right holds the
explanation, with "labelled rows" in red bold and "learns from them" in bold.
**What it teaches:** Reframes the churn question as supervised learning: labelled rows are the
training (context) set, the new customer is the query, and the answer should be learned from the
labelled rows.

### Slide 6.6 — Prediction is a different job: the LLM side (deck L5, slide 6)
**Evidence:** Narrated — "Large language models are trained to predict the next best token, so really it's only looking at text and generating what the next value of that text might be. For example, "this customer will", and then what's the next best token."
**Text on slide:** Prediction is a different job · WHAT AN LLM IS TRAINED TO DO · This customer will ___ · likely .31 · churn .24 · probably .18 · stay .09 · Trained to generate the next best token · A distribution over words → great to reason and plan
**Visual description:** A single bordered card on the left half; the right half is empty. The
prompt "This customer will" with a red dashed blank, then four red horizontal bars with their
probabilities. Grey caption, then the summary line with "words" in bold and "reason" and "plan"
in blue.
**What it teaches:** An LLM produces a probability distribution over next words, which suits
reasoning and planning. The slide reads as the first build stage of Slide 6.7; that is a reading
of the drawings, not a fact.

### Slide 6.7 — Prediction is a different job: LLM vs prediction task (deck L5, slide 7)
**Evidence:** Narrated — "Whereas a Tabular Foundation Model is working fundamentally differently. It's going to be giving us a distribution over the outcomes of what our question is. We're going to be predicting a value not based on what the large language model knows about the world, but specifically on what the Tabular Foundation Model has learned about our data."
**Text on slide:** Prediction is a different job · WHAT AN LLM IS TRAINED TO DO · This customer will ___ · likely .31 · churn .24 · probably .18 · stay .09 · Trained to generate the next best token · A distribution over words → great to reason and plan · WHAT A PREDICTION TASK ASKS FOR · tenure=5 · monthly · $94 · 3 tickets → P(churn | features) = ? · churn 0.83 · stay 0.17 · A distribution over outcomes, calibrated on the rows → needed to predict and decide based on your data
**Visual description:** The card from Slide 6.6 on the left and a new orange-bordered card on the
right: the query's features and "P(churn | features) = ?" in orange, an orange bar for "churn
0.83" and a pale peach bar for "stay 0.17", and the summary line with "outcomes" in bold and
"predict" and "decide based on your data" in orange.
**What it teaches:** A prediction task needs a calibrated distribution over outcomes conditioned on
the features and learned from the rows, which is a different job from next-word generation.

### Slide 6.8 — TabPFN as a tool call: one model for every dataset (deck L5, slide 8)
**Evidence:** Narrated — "What this would look like is the following. The pre-trained transformer TabPFN will receive the context, i.e., the history, as well as the query. We'll then forward that to TabPFN, and then TabPFN will return a prediction. This is different to how classical machine learning models work, and why we can use TabPFN relatively easily as a tool within an agent. Because only one TabPFN model can act as a tool for all datasets and all domains, And this means we can avoid having to retrain the model every time we have a new domain."
**Text on slide:** TabPFN as a tool call · A pre-trained transformer that predicts in-context. Your table is the context. · context · labelled customers + query · TabPFN · one forward pass · prediction · class or value, with calibrated uncertainty · Classical ML · churn data → churn model · prices → price model · risk → risk model · trains one model per dataset · TabPFN · churn · prices · risk · ↓ read in-context by · one pre-trained model · trained once, no training loop
**Visual description:** Top row: a blue-bordered "context" card with four light-blue lines and one
orange line ("labelled customers + query"), an arrow to a solid blue "TabPFN / one forward pass"
box, an arrow to an orange-bordered "prediction" card. Bottom row: a grey "Classical ML" card
listing three dataset-to-model pairs ending "trains **one model per dataset**", and a
blue-bordered "TabPFN" card listing the same three tasks "read in-context by **one pre-trained
model**", ending "trained **once**, no training loop".
**What it teaches:** Because one pretrained TabPFN serves any table through in-context learning,
it can be a single general-purpose prediction tool for an agent, instead of one trained model per
dataset.

### Slide 6.9 — TabPFN as a tool call: the agent flow (deck L5, slide 9)
**Evidence:** Narrated — "Let's look at the same scenario as we saw before. We had customer C-1046, who is a new customer and we don't yet know whether they've churned or not. our agent that's using a large language model should reason that this is a prediction task because it's data that we haven't seen before. So it will decide to call our TabPFN tool with all of the relevant inputs for the TabPFN tool to run a prediction. TabPFN will then return a prediction, and then our large language model can do what it's best at, and produce a sentence giving us the answer."
**Text on slide:** TabPFN as a tool call · USER · Will customer C-1046 churn? · LLM agent · "This is a prediction task — call the tool, don't guess." · reasons · ① tool call · tabpfn.predict (train = customers.csv, target = "churned", task = "classification", query = {tenure: 5, plan: "monthly", usd: 94, tickets: 3}) · ② result · { "churn": 0.83, "stay": 0.17 } · TabPFN tool · Learns about past customers in-context — one forward pass. · predicts · ③ agent reasons over the result · C-1046 has an 83% churn probability, learned from your past customers. Worth a retention offer.
**Visual description:** A grey USER bubble at top left. Below, a blue-bordered "LLM agent" card at
left (its quoted thought, and "reasons" in blue) and an orange-bordered "TabPFN tool" card at
right ("predicts" in orange). Between them, a blue arrow to the right labelled "① tool call" over
a grey box with the call (function name in red), and an orange arrow to the left labelled
"② result" over a grey box with the JSON result and an orange bar about 83% full. At the bottom,
"③ agent reasons over the result" in blue beside a blue-bordered answer box ("83% churn
probability" in bold).
**What it teaches:** The agent pattern: the LLM recognizes a prediction task, calls TabPFN with
the training file, target, task type and query row, receives class probabilities, and turns them
into a natural-language answer. The single `tabpfn.predict(...)` call is a schematic; the MCP
server's actual five-tool chain is on Slide 6.10, and the narration adds that for classification
the server runs predict_proba by default.

### Slide 6.10 — TabPFN MCP (deck L5, slide 10)
**Evidence:** Narrated — "We're going to do all of this using the TabPFN MCP server and Claude Code. The MCP server will come with five tools that allow you to fit and predict and even get statuses on how your fit is going. Additionally, the TabPFN MCP server is using TabPFN via the API. It also has the capability to cache your fitted models, so once you've fitted the model once, you'll just use the cached version so you don't have to spend time fitting again."
**Text on slide:** TabPFN MCP · The tabpfn MCP server exposes 5 tools — a chain of ids from files to predictions. · local files → train_set_upload_id → fitted_train_set_id → test_set_upload_id → prediction · prepare_train_set_upload() · fit(upload_id, task) · get_fit_status(fitted id) · prepare_test_set_upload(fitted id) · predict(…, task) · One fit, unlimited predicts — fits get cached
**Visual description:** A horizontal chain of five boxes joined by red arrows: a grey "local
files" box, three orange-bordered id boxes, and an orange-bordered "prediction" box in orange
bold. Below left, a grey code card listing the five tool signatures with the function names in red
monospace bold. Below right, a white card with a blue bullet: "One fit, unlimited predicts —
**fits get cached**".
**What it teaches:** The TabPFN MCP server's five tools and the order they chain in (upload the
training set, fit, poll fit status, upload the test set against the fitted id, predict), and that
a fit is cached so later predictions reuse it.

---

## Lesson 7: Conclusion
Transcript: `## Lesson 7: Conclusion` in transcripts/tabular-foundation-models-for-data-science-agents-transcripts.md

No slide in any deck belongs to this lesson. The narration is a short recap of the course (making,
accelerating and interpreting predictions, TabPFN as an agent tool, and training a tiny TabPFN)
with no visual content of its own.
