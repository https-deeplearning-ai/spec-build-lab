# Tabular Foundation Models For Data Science Agents

## How to read this file

- **Lesson numbering and titles come from the transcripts**, and the transcripts win whenever the
  numberings in these materials disagree. The transcripts have seven lessons: 1 Introduction,
  2 What Are Tabular Foundation Models?, 3 Classification, Regression & Forecasting with TabPFN,
  4 Interpreting TabPFN predictions, 5 Real-time inference with the KV cache, 6 Building a Data
  Science Agent, 7 Conclusion.
- **The repo uses a second numbering, one lower:** `L2/L2.ipynb` is transcript Lesson 3,
  `L3/L3.ipynb` is Lesson 4, `L4/L4.ipynb` is Lesson 5. The notebooks' own title cells ("# L2: …",
  "# L3: …", "# L4: …") and the Lesson 3 recap's line "Lesson 3 caches that context for real-time
  serving" use the repo numbering; they are left verbatim. In the transcript numbering the KV
  cache is Lesson 5.
- **Lessons 1, 2, 6 and 7 have no notebook in the repo.** Lesson 6 (Building a Data Science
  Agent) is a Claude Code demo with the TabPFN MCP server, a TabPFN handoff skill, helper scripts
  and telco churn data; none of that code is in this repo snapshot, so the transcript and the
  slide descriptions are the only sources for it.
- **Three repo notebooks are platform files, not course lessons:** `Appendix – Tips, Help, and
  Download/Appendix.ipynb` (learning-platform help), `MonitorSetup.ipynb` and `ProxyTest.ipynb`
  (platform setup and an OpenAI proxy check). They follow the lessons under "Platform notebook"
  headings and teach no course content.
- Cell contents and the helper module section are unchanged from the ingest_repo.py output; only
  the section headings, the lesson map, the provenance line, this section and the section order
  were edited. Re-running /ingest-course-repo overwrites these edits.

---

## Lesson Map

- (no notebook) → Lesson 1: Introduction
- (no notebook) → Lesson 2: What Are Tabular Foundation Models?
- L2/L2.ipynb → Lesson 3: Classification, Regression & Forecasting with TabPFN
- L3/L3.ipynb → Lesson 4: Interpreting TabPFN predictions
- L4/L4.ipynb → Lesson 5: Real-time inference with the KV cache
- (no notebook) → Lesson 6: Building a Data Science Agent
- (no notebook) → Lesson 7: Conclusion
- Appendix – Tips, Help, and Download/Appendix.ipynb → platform notebook, not a lesson
- MonitorSetup.ipynb → platform notebook, not a lesson
- ProxyTest.ipynb → platform notebook, not a lesson

> Generated from `https://github.com/https-deeplearning-ai/SC-Priorlabs-C1-Platform` @ default branch by ingest_repo.py, then renumbered by hand to the transcript lessons in `materials/transcripts/tabular-foundation-models-for-data-science-agents-transcripts.md`.

---

## Lesson 1: Introduction

No notebook in the repo for this lesson.

---

## Lesson 2: What Are Tabular Foundation Models?

No notebook in the repo for this lesson.

---

## Lesson 3: Classification, Regression & Forecasting with TabPFN — L2/L2.ipynb

[markdown] cell 0

# L2: Classification, Regresion & Forecasting with TabPFN

[markdown] cell 1

Make first predictions with TabPFN: classify heart-disease
patients, predict house prices, and read the full predictive
distribution behind every regression output.

[markdown] cell 2

## 1. Setup

[code] cell 3

import numpy as np
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    mean_absolute_error,
    precision_score,
    r2_score,
    recall_score,
)

from helper import (
    configure_lesson,
    init_tabpfn,
    load_co2,
    load_electricity,
    load_heart_disease_full,
    load_housing,
    plot_actual_vs_predicted,
    plot_co2,
    plot_electricity,
    plot_forecast_comparison,
    plot_predicted_distribution,
    plot_quantile_band,
)

configure_lesson(plots=True)

from tabpfn_client import TabPFNClassifier, TabPFNRegressor
init_tabpfn()

[markdown] cell 4

## 2. Classification: is this patient at risk?

- 920 patients pooled from four hospital studies (Cleveland,
  Hungary, Switzerland, Long Beach); 700 for training context,
  220 held out for testing.
- The target is binary: coronary disease or not.
- Two thirds of the records have missing measurements. TabPFN
  handles the gaps natively; there is nothing to impute.

[code] cell 5

X_train, X_test, y_train, y_test = load_heart_disease_full(
    train_size=700, test_size=220,
)

X_train.head(3)

[code] cell 6

y_train.head(3)

[markdown] cell 7

The interface is scikit-learn's, but the mechanics are not:

- TabPFN is a pretrained foundation model. `fit` does **no**
  training: it uploads the training table so the model can use
  it as context.
- All model compute happens at `predict`. The transformer reads
  the training rows and the new rows together and predicts in a
  single forward pass (in-context learning).
- Because the work happens at predict time, repeated requests
  re-encode the same context. L3 shows how a KV cache removes
  that cost.

No configuration needed: TabPFN detects which columns are
categorical, and its defaults are the tuned ones.

[code] cell 8

classifier = TabPFNClassifier()
classifier.fit(X_train, y_train)

[markdown] cell 9

### Predict one patient first

Before scoring anything, predict a single patient. `predict`
returns the label; `predict_proba` returns the calibrated
probability behind it, which is the number a clinic would
actually act on.

[code] cell 10

patient = X_test.iloc[[0]]
display(patient)

[code] cell 11

prediction = classifier.predict(patient)[0]


print(f"predicted: {prediction:.0f}   "
      f"actual: {y_test.iloc[0]:.0f}")

[code] cell 12

proba = classifier.predict_proba(patient)[0]
print(f"P(healthy: label=0) = {proba[0]:.2f}   "
      f"P(disease: label=1) = {proba[1]:.2f}")

[markdown] cell 13

### Evaluate on all 220 held-out patients

One patient tells a story; 220 tell us whether to trust it.
Instead of compressing everything into a single accuracy
number, keep the four possible outcomes apart with a
**confusion matrix**: each row is what was actually true, each
column is what the model said. The diagonal cells are correct
calls; the two off-diagonal cells are the two kinds of
mistakes, and in a clinic they are not equally bad.

[code] cell 14

predictions = classifier.predict(X_test)

ConfusionMatrixDisplay.from_predictions(
    y_test,
    predictions,
    display_labels=["no disease", "disease"],
    cmap="Blues",
    colorbar=False,
);

[markdown] cell 15

Two numbers summarize the two failure modes:

- **Precision**: of the patients the model flags as sick, how
  many really are. Low precision means false alarms and
  unnecessary follow-up tests.
- **Recall**: of the patients who really are sick, how many the
  model catches. Low recall means missed diseases, the costly
  mistake here.

[code] cell 16

precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)

print(f"precision: {precision:.2f}")
print(f"recall:    {recall:.2f}")

[markdown] cell 17

## 3. Regression: house price prediction

New table, continuous target: predict the sale price of houses
in Ames, Iowa from a handful of listing facts. The only change
on our side is the estimator class.

Note the `Neighborhood` column: it is text. No encoding, no
preprocessing; TabPFN handles mixed column types natively.

The data: the [Ames Housing dataset](https://www.openml.org/d/42165)
(De Cock, 2011) — 1,460 home sales from Ames, Iowa, 2006-2010.
We keep 9 of the original 80 columns.

[code] cell 18

X_train_h, X_test_h, y_train_h, y_test_h = load_housing(
    train_size=1300,
    test_size=160,
)
X_train_h.head(3)

[code] cell 19

y_train_h.head(3)

[code] cell 20

reg = TabPFNRegressor()
reg.fit(X_train_h, y_train_h)

[markdown] cell 21

### Predict the price of one house first

A classical regressor answers "what is this house worth?" with
one number. TabPFN answers a different question: "how likely is
each possible price?" Internally it chops the price range into
thousands of small bins and predicts a probability for each, so
every prediction is a full histogram over prices.

Everything `predict` can return is a summary of that histogram:

- the default output is its **mean**, the expected price;
- the **10th percentile** is the price the model gives the true
  value a 10% chance of falling below, the **90th** a 90%
  chance. Between the two sits 80% of the model's belief.

[code] cell 22

house_ind = 5
house = X_test_h.iloc[[house_ind]]
display(house)

[code] cell 23

mean_price = reg.predict(house)[0]
print(f"mean:            ${mean_price:,.0f}")
print(f"actual price:    ${y_test_h.iloc[house_ind]:,.0f}")


q10, q50, q90 = reg.predict(
    house,
    output_type="quantiles",
    quantiles=[0.1, 0.5, 0.9],
)

print(f"10th percentile: ${q10[0]:,.0f}")
print(f"median:          ${q50[0]:,.0f}")
print(f"90th percentile: ${q90[0]:,.0f}")

[markdown] cell 24

Read it as the model talking: "my best single guess is the
mean, but I'd bet 80% odds the real price lands between the
10th and the 90th percentile." Two houses can share the same
mean and mean completely different things: a tight band is a
confident model, a wide band is a model telling you it is
guessing. A point estimate hides that distinction entirely.

[markdown] cell 25

### Evaluate on the whole test set

For a continuous target, being "right" is a matter of distance,
not matching:

- **MAE** (mean absolute error): how far off the predictions are
  on average, in the target's own units, here dollars.
- **R²**: the share of house-to-house price variation the model
  explains. 1.0 is perfect; 0.0 means no better than always
  predicting the average price.

[code] cell 26

point = reg.predict(X_test_h)

comparison = pd.DataFrame(
    {
        "predicted ($1000s)": (point[:6] / 1000).round(0),
        "actual ($1000s)": (y_test_h.values[:6] / 1000),
    }
)
print(comparison)

[markdown] cell 27

##### Evaluating errors

[code] cell 28


mae = mean_absolute_error(y_test_h, point)
print(f"MAE: ${mae:,.0f}")
print(f"R2:  {r2_score(y_test_h, point):.2f}")

[markdown] cell 29

The same comparison as a picture: one dot per house, actual
price across, predicted price up. A perfect model would put
every dot on the diagonal; the vertical distance from the line
is that house's error.

[code] cell 30

plot_actual_vs_predicted(
    y_test_h / 1000,
    point / 1000,
    unit="sale price ($1000s)",
)

[markdown] cell 31

### Can you trust the band?

"80% of my belief" only means something if the model is
*calibrated*: across many predictions, the true value should
land inside the 10-90 band about 80% of the time. TabPFN is
generally well calibrated because it is pretrained on synthetic
tasks where the true noise is known, but the honest check is
empirical: measure the coverage on held-out data.

[code] cell 32

low, median, high = reg.predict(
    X_test_h,
    output_type="quantiles",
    quantiles=[0.1, 0.5, 0.9]
)

actual = y_test_h.values
inside = (actual >= low) & (actual <= high)
print(f"the 10-90 band covers {inside.mean():.0%} "
      f"of {len(actual)} test houses")

plot_quantile_band(
    actual / 1000,
    low / 1000,
    median / 1000,
    high / 1000,
    "Sale price ($1000s)",
    unit="test houses",
)

[markdown] cell 33

## 4. Time-series forecasting

TabPFN has no built-in notion of time. But a forecast is just a
table where some rows have no target yet, so we can treat it as
regression. The catch: the model can only use the context we put
in front of it, and how we encode time decides everything.

The data: two weeks of hourly German day-ahead electricity
prices. A strong daily cycle, a weekly rhythm, and the occasional
shock. We hold out the last 48 hours.

[code] cell 34

history, future = load_electricity(horizon=48)

print(f"history:  {len(history)} hours")
print(f"held out: {len(future)} hours")

plot_electricity(history)

[markdown] cell 35

#### Turn the calendar into features

[code] cell 36

history.head(3)

[markdown] cell 37

#### Prediction

[code] cell 38

history[["hour","price_eur"]].head(3)

[code] cell 39

reg_ts = TabPFNRegressor()

reg_ts.fit(history[["hour"]], history["price_eur"])
forecast_price = reg_ts.predict(future[["hour"]])

[code] cell 40

low_price, _, high_price = reg_ts.predict(future[["hour"]],
                                          output_type="quantiles", 
                                          quantiles=[0.1, 0.5, 0.9])

plot_forecast_comparison(
    history, future,
    {"forecast": forecast_price}, time_col="hour",
    target_col="price_eur", ylabel="price",
    title="48 hours of prices, forecast from the clock",
    band=(low_price, high_price),
)

[markdown] cell 41

### Turn the clock into features

The model needs columns, so we hand it the structure we already
know is in the series:

- `hour_of_day` places each row on the daily cycle,
- `day_of_week` separates weekdays from the weekend.

[code] cell 42

def add_calendar_features(df):
    out = df.copy()
    out["hour_of_day"] = out["hour"].dt.hour
    out["day_of_week"] = out["hour"].dt.dayofweek
    return out


FEATURES = ["hour_of_day", "day_of_week"]

history_cal = add_calendar_features(history)
future_cal = add_calendar_features(future)

reg_ts = TabPFNRegressor()
reg_ts.fit(history_cal[FEATURES], history_cal["price_eur"])

forecast_price = reg_ts.predict(future_cal[FEATURES])

[markdown] cell 43

And because every TabPFN regression is a distribution, the
forecast ships with its own uncertainty band, at no extra cost.

[code] cell 44

low_price, _, high_price = reg_ts.predict(future_cal[FEATURES],
                                          output_type="quantiles",
                                          quantiles=[0.1, 0.5, 0.9])

plot_forecast_comparison(
    history, future,
    {"calendar features": forecast_price}, time_col="hour",
    target_col="price_eur", ylabel="price",
    title="48 hours of prices, forecast from the clock",
    band=(low_price, high_price),
)

[markdown] cell 45

### Exercise: forecast with more than the clock

Prices follow demand and renewable supply, and the grid publishes
*forecasts* of both a day ahead, so they are known for the very
hours you want to predict. They are already in the table as
`load_forecast` and `renewables_forecast`. Your turn:

1. Add the two market columns to `FEATURES` and fit a second
   `TabPFNRegressor`.
2. Compare its MAE on `future["price_eur"]` with the
   calendar-only forecast above.
3. Plot both forecasts with `plot_forecast_comparison`.

[code] cell 46

# YOUR CODE HERE
#
# Hint: MARKET_FEATURES = FEATURES + ["load_forecast",
# "renewables_forecast"], fit a second TabPFNRegressor on
# history_cal[MARKET_FEATURES], predict future_cal, compare
# mean_absolute_error on future["price_eur"], then pass both
# forecasts to plot_forecast_comparison in one dict.

[markdown] cell 47

The model never changed; its context did. With a tabular
foundation model, feature engineering *is* context engineering:
you decide what the model gets to read before it answers.
Calendar features hand it the clock; exogenous columns hand it
the world. The `tabpfn-time-series` package automates exactly
this recipe.

[markdown] cell 48

## Recap

- One scikit-learn-style API covers classification and
  regression, with no tuning and no manual encoding.
- `fit` uploads context; the model computes at `predict`. Lesson 3
  caches that context for real-time serving.
- Regression outputs are full distributions: quantile bands and
  densities come for free, on test sets and forecasts alike.
- The right features put the right context in front of the
  model, and that is where the accuracy lives.

---

## Lesson 4: Interpreting TabPFN predictions — L3/L3.ipynb

[markdown] cell 0

# L3: Interpreting TabPFN Predictions

[markdown] cell 1

Use global and local interpretability to understand the model’s
predictions.

[markdown] cell 2

## 1. Setup

Load the interpretability tools and initialize the managed client.

[code] cell 3

import numpy as np
from sklearn.metrics import roc_auc_score

from tabpfn_client import TabPFNClassifier

from helper import (
    CONTINUOUS,
    N_ESTIMATORS,
    RANDOM_STATE,
    categorical_indices,
    configure_lesson,
    init_tabpfn,
    load_heart_disease,
    make_shap_explainer,
    plot_beeswarm,
    plot_partial_dependence,
    plot_patient_waterfall,
    quiet_client_call,
    top_continuous_features,
)

configure_lesson(plots=True)
init_tabpfn()

[markdown] cell 4

## 2. Load readable data

Keep plain-language feature names and categorical column indices for
every explanation.

[code] cell 5

X_train, X_test, y_train, y_test = load_heart_disease(
    train_size=200,
    test_size=70,
)

feature_names = list(X_train.columns)
cat_idx = categorical_indices(feature_names)

X_train.head(3)

[code] cell 6

y_train.head(3)

[markdown] cell 7

## 3. Fit the cached model

Cache the training context because interpretation requires many
repeated predictions.

[code] cell 8

clf = TabPFNClassifier(
    fit_mode="fit_with_cache",
    categorical_features_indices=cat_idx,
)
quiet_client_call(
    clf.fit, X_train.values, y_train.values
)

proba_test = quiet_client_call(
    clf.predict_proba, X_test.values
)[:, 1]
print(f"test AUC {roc_auc_score(y_test, proba_test):.3f}")

[markdown] cell 9

## 4. Compute SHAP values

- Explain 25 patients.
- The beeswarm ranks features by average impact.

[code] cell 10

explainer = make_shap_explainer(clf, X_train, y_train)

[code] cell 11

N_EXPLAIN = 10

X_explain = X_test.iloc[:N_EXPLAIN]
shap_values = explainer(
    X_explain,
    silent=False,
)
shap_values.display_data = X_explain.values

print(f"Explained {len(X_explain)} patients")

[markdown] cell 12

##### Explaining single predictions

[code] cell 13

predicted = shap_values.values.sum(axis=1) + shap_values.base_values
idx_high = int(np.argmax(predicted))
idx_borderline = int(np.argmin(np.abs(predicted - 0.5)))

[code] cell 14

plot_patient_waterfall(
    shap_values, idx_high, X_explain, feature_names, "Highest-risk patient",
)

[code] cell 15

plot_patient_waterfall(
    shap_values, idx_borderline, X_explain, feature_names, 
    "Borderline patient",
)

[markdown] cell 16

## 5. Feature importance

[code] cell 17

plot_beeswarm(shap_values, len(feature_names))

[markdown] cell 18

## 6. Partial dependence plots

- Sweep the strongest continuous features and compare their response
  curves.
- Shared axes make effect sizes comparable.

[code] cell 19

top_continuous = top_continuous_features(
    shap_values, feature_names, CONTINUOUS)

plot_partial_dependence(
    clf, X_train.values, top_continuous, feature_names,
)

[markdown] cell 20

## Recap

- SHAP gives attribution; partial dependence gives response shape.
- Waterfalls explain individual patient predictions.
- These are associations and sensitivities, not causal claims.

---

## Lesson 5: Real-time inference with the KV cache — L4/L4.ipynb

[markdown] cell 0

# L4: Real-time Inference with the KV-cache

[markdown] cell 1

Cache a fixed training context and measure how much server
prediction work it saves across repeated requests.

[markdown] cell 2

## 1. Setup

Use client 0.6.0 to read server timings alongside total
request latency. Both models below use TabPFN v3.5.

[code] cell 3

import os

print("TabPFN token available:", bool(os.getenv("TABPFN_TOKEN")))

[code] cell 4

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

from tabpfn_client import TabPFNClassifier

from helper import (
    N_ESTIMATORS, RANDOM_STATE,
    benchmark_cache_comparison, configure_lesson,
    init_tabpfn, show_fit_comparison,
    show_latency_comparison, show_split_summary,
    timed_client_call, display_precomputed
)

configure_lesson()
init_tabpfn()

[markdown] cell 5

## 2. Generate the data

Generate 30,000 synthetic rows with 20 numeric features.
Keep 20,000 rows for training and 10,000 for testing.
This larger training context gives the cache more work to save.
Use a fixed seed and a stratified split for reproducibility.

[code] cell 6

X, y = make_classification(
    n_samples=30_000, n_features=20, n_informative=10,
    n_redundant=5, random_state=RANDOM_STATE,
)
X = pd.DataFrame(X, columns=[f"x{i}" for i in range(20)])
y = pd.Series(y, name="target")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=10_000,
    stratify=y, random_state=RANDOM_STATE,
)
show_split_summary(X_train, X_test)
X_train.head(3)

[markdown] cell 7

## 3. No-cache baseline

`fit_preprocessors` prepares the data. Each prediction still
encodes the training context. Time the whole API call with
a local clock, then read `predict_s` from the server:
this is the time the worker spent predicting.

[code] cell 8

clf = TabPFNClassifier()

_, t_fit = timed_client_call(clf.fit, X_train.values, y_train.values)

print(f"Context ready in {t_fit:.2f} s")

[code] cell 9

proba, t_predict = timed_client_call(
    clf.predict_proba, X_test.values
)
server_time = clf.last_predict_timings["predict_s"]
proba = proba[:, 1]
auc = roc_auc_score(y_test, proba)

print("For 20K training rows and 10K test rows")
print(f"Server prediction: {server_time:.3f} s")
print(f"Whole request: {t_predict:.2f} s")
print(f"Test AUC: {auc:.3f}")

[markdown] cell 10

## 4. Using the KV-cache

`fit_with_cache` performs the context work once during fitting.
Prediction requests then attend to the stored context.

[code] cell 11

clf_cached = TabPFNClassifier(fit_mode="fit_with_cache",)

_, t_fit_cached = timed_client_call(
    clf_cached.fit, X_train.values, y_train.values
)
print(f"Context ready in {t_fit_cached:.2f} s")

[code] cell 12

proba_cached, t_predict_cached = timed_client_call(
    clf_cached.predict_proba, X_test.values
)
server_time_cached = clf_cached.last_predict_timings["predict_s"]
proba_cached = proba_cached[:, 1]
auc_cached = roc_auc_score(y_test, proba_cached)

print("For 20K training rows and 10K test rows")
print(f"Server prediction: {server_time_cached:.3f} s")
print(f"Whole request: {t_predict_cached:.2f} s")
print(f"Test AUC: {auc_cached:.3f}")

[code] cell 13

show_fit_comparison(
    [t_fit, t_fit_cached], [t_predict, t_predict_cached],
    [server_time, server_time_cached], n_rows=len(X_test),
)
difference = np.abs(proba - proba_cached).max()
print(f"Largest probability difference: {difference:.4f}")

[markdown] cell 14

## 5. Benchmark repeated requests

The first predictions score all 10,000 test rows.
For repeated requests, use smaller batches from that test set.
A single call does not establish a speedup.
The helper warms up both models, then sends the same fresh
1,000-row batches to each. It alternates request order
and records 20 calls per model.

Compare two clocks:

- **Server prediction:** time the worker spent predicting.
  This is where reusing the training context saves work.
- **Whole request:** time the caller waited, including
  uploads, preprocessing, network traffic, and queues.

Faster server predictions can coexist with similar total
request times. A ratio above 1 means caching was faster
for that measurement in this run.

[code] cell 15

run_benchmark = True
if run_benchmark:
    timings = benchmark_cache_comparison(
        clf, clf_cached, X_test,
        n_queries=20,
        rows_per_query=1_000,
    )
    show_latency_comparison(timings)
else:
    display_precomputed()

[markdown] cell 16

## When not to use the cache

- Refit whenever the training data changes.
- Skip caching for one fit followed by one prediction.
- Cached context consumes server-side storage.

[markdown] cell 17

## Recap

- Cache a fixed context when predictions repeat.
- Compare server prediction time and whole-request latency
  separately: queue and network delays also affect users.
- Use matched requests, warm-up calls, and latency medians.
- Caching changes execution, not the prediction task.

---

## Lesson 6: Building a Data Science Agent

No notebook in the repo for this lesson. The transcript's Claude Code demo (`.mcp.json`, the
TabPFN handoff skill, the fetch-data, baseline and evaluation scripts, the telco churn data) is not
in this repo snapshot.

---

## Lesson 7: Conclusion

No notebook in the repo for this lesson.

---

## Platform notebook (not a course lesson): Appendix — Appendix – Tips, Help, and Download/Appendix.ipynb

[markdown] cell 0

## 💻 &nbsp; Accessing Utils File and Helper Functions
In each notebook on the top menu:

**1:** &nbsp; Click on <em>"File"</em>

**2:** &nbsp; Then, click on <em>"Open"</em>

You will be able to see all the notebook files for the lesson, including any helper functions used in the notebook on the left sidebar. See the following image for the steps above.

<img width="450px" src="images/upload-file2.png" style="border-width:3px; border-color:#f5ecda; border-style:solid; border-radius:6px">

<hr style="height: 3px; background-color:#f0f0f0; border: none;">

[markdown] cell 1

## 💻 &nbsp; Downloading Notebooks
In each notebook on the top menu:

**1:** &nbsp; Click on <em>"File"</em>

**2:** &nbsp; Then, click on <em>"Download as"</em>

**3:** &nbsp; Then, click on <em>"Notebook (.ipynb)"</em>

<img width="450px" src="images/how-to-download-notebooks.png" style="border-width:3px; border-color:#f5ecda; border-style:solid; border-radius:6px">

<hr style="height: 3px; background-color:#f0f0f0; border: none;">

[markdown] cell 2

## 💻 &nbsp; Uploading Your Files
After following the steps shown in the previous section ("File" => "Open"), then click on <em>"Upload"</em> button to upload your files.

<img width="700px" src="images/upload-file-3.png" style="border-width:3px; border-color:#f5ecda; border-style:solid; border-radius:6px"></img>

<hr style="height: 3px; background-color:#f0f0f0; border: none;">

[markdown] cell 3

## 📗 &nbsp; See Your Progress
Once you enroll in this course—or any other short course on the DeepLearning.AI platform—and open it, you can click on 'My Learning' at the top right corner of the desktop view. There, you will be able to see all the short courses you have enrolled in and your progress in each one.

<img width="700px" src="images/progress-upper.png" style="border-width:3px; border-color:#f5ecda; border-style:solid; border-radius:6px"></img>

Additionally, your progress in each short course is displayed at the bottom-left corner of the learning page for each course (desktop view).

<img width="700px" src="images/progress-bottom.png" style="border-width:3px; border-color:#f5ecda; border-style:solid; border-radius:6px"></img>

<hr style="height: 3px; background-color:#f0f0f0; border: none;">

[markdown] cell 4

## 📱 &nbsp; Features to Use

**🎞 &nbsp; Adjust Video Speed:** Click on the gear icon (⚙) on the video and then from the <em>Speed</em> option, choose your desired video speed.

**🗣️ &nbsp; Captions (English and Spanish):** Click on the gear icon (⚙) on the video and then from the <em>Captions</em> option, choose to see the captions either in English or Spanish.

**🔅 &nbsp; Video Quality:** If you do not have access to high-speed internet, click on the gear icon (⚙) on the video and then from <em>Quality</em>, choose the quality that works the best for your Internet speed.

<img width="350px" src="images/options.png" style="border-width:3px; border-color:#f5ecda; border-style:solid; border-radius:6px"></img>

**🖥 &nbsp; Picture in Picture (PiP):** This feature allows you to continue watching the video when you switch to another browser tab or window. Click on the small rectangle shape on the video to go to <em>PiP</em> mode.

**✔ &nbsp; Hide and Unhide Lesson Navigation Menu:** If you do not have a large screen, you may click on the small hamburger icon beside the title of the course to hide the left-side navigation menu. You can then unhide it by clicking on the same icon again.

<hr style="height: 3px; background-color:#f0f0f0; border: none;">

[markdown] cell 5

## 🧑‍🎓 &nbsp; Efficient Learning Tips
The following tips can help you have an efficient learning experience with this short course and other courses.

**🧑‍🏫 &nbsp; Create a Dedicated Study Space:** Establish a quiet, organized workspace free from distractions. A dedicated learning environment can significantly improve concentration and overall learning efficiency.

**📅 &nbsp; Develop a Consistent Learning Schedule:**
Consistency is key to learning. Set out specific times in your day for study and make it a routine. Consistent study times help build a habit and improve information retention.

**Tip:** Set a recurring event and reminder in your calendar, with clear action items, to get regular notifications about your study plans and goals.

**☕ &nbsp; Take Regular Breaks:**
Include short breaks in your study sessions. The Pomodoro Technique, which involves studying for 25 minutes followed by a 5-minute break, can be particularly effective.

**💬 &nbsp; Engage with the Community:**
Participate in forums, discussions, and group activities. Engaging with peers can provide additional insights, create a sense of community, and make learning more enjoyable.

**✍ &nbsp; Practice Active Learning:**
Don't just read or run notebooks or watch the material. Engage actively by taking notes, summarizing what you learn, teaching the concept to someone else, or applying the knowledge in your practical projects.

<hr style="height: 3px; background-color:#f0f0f0; border: none;">

[markdown] cell 6

## 📚 &nbsp; Enroll in Other Short Courses
Keep learning by enrolling in other short courses. We add new short courses regularly. Visit DeepLearning.AI Short Courses page to see our latest courses and begin learning new topics. 👇

<b><a href="https://www.deeplearning.ai/courses/?utm_source=dlai-learn-platform&utm_medium=referral-sc&utm_campaign=appendix-tips-help">👉👉 🔗 DeepLearning.AI – All Short Courses [+]</a></b>

<hr style="height: 3px; background-color:#f0f0f0; border: none;">

[markdown] cell 7

## 🙂 &nbsp; Let Us Know What You Think
Your feedback helps us know what you liked and didn't like about the course. We read all your feedback and use them to improve this course and future courses. Please submit your feedback by clicking on <em>"Course Feedback"</em> option at the bottom of the lessons list menu (desktop view).

<img width="700px" src="images/feedback.png" style="border-width:3px; border-color:#f5ecda; border-style:solid; border-radius:6px"></img>

Also, you are more than welcome to join our community <a href="https://community.deeplearning.ai/">👉👉 🔗 DeepLearning.AI Forum</a>

<hr style="height: 3px; background-color:#f0f0f0; border: none;">

---

## Platform notebook (not a course lesson): MonitorSetup — MonitorSetup.ipynb

[code] cell 0

         1         2         3         4         5         6         7  
#23456789012345678901234567890123456789012345678901234567890123456789012

[code] cell 1

1

[code] cell 2

2

[code] cell 3

3

[code] cell 4

4

[code] cell 5

5

[code] cell 6

6

[code] cell 7

7

[code] cell 8

8

[code] cell 9

9

[code] cell 10

10

[code] cell 11

11

[code] cell 12

12

[code] cell 13

13

[code] cell 14

14

[code] cell 15

15

[code] cell 16

16

[code] cell 17

17

[code] cell 18

18

---

## Platform notebook (not a course lesson): OpenAI Model Availability Tester — ProxyTest.ipynb

[markdown] cell 0

# OpenAI Model Availability Tester

This script checks whether a list of OpenAI chat and embedding models are available through a configured proxy environment. It's primarily used to verify access permissions and connectivity via an internal proxy setup.

## Prerequisites

- `openai` Python package installed (`pip install openai`)

## Environment Variables

Before running the script, make sure to set the following three environment variables. These are essential for routing requests through the internal proxy and authenticating with the OpenAI service.

| Variable Name       | Description                                 | Example Value                                                                 |
|---------------------|---------------------------------------------|--------------------------------------------------------------------------------|
| `OPENAI_BASE_URL`   | Base URL for OpenAI requests (proxy route)  | `http://jupyter-api-proxy.stg.internal.dlai/rev-proxy/openai`                |
| `OPENAI_API_BASE`   | API base endpoint (typically same as above) | `http://jupyter-api-proxy.stg.internal.dlai/rev-proxy/openai`                |
| `OPENAI_API_KEY`    | Authentication token for OpenAI API         | (Insert your valid token here)                                                |


## What It Does

Once the environment variables are set, the script will:

1. Confirm that the proxy is enabled.
2. Test availability of the following **OpenAI chat/completion models**:
   - `o1-mini`
   - `o3-mini`
   - `o1`
   - `o1-pro`
   - `gpt-4o`
   - `gpt-4o-mini`
3. Test availability of the following **OpenAI embedding models**:
   - `text-embedding-3-small`
   - `text-embedding-3-large`

Each model will either be marked as:
- ✅ **available**
- ❌ **unavailable (Permission Denied)**
- ⚠️ **error** (with details)

## Running the Script

Run the cell below

[code] cell 1

import openai
from openai import OpenAI
from openai._exceptions import PermissionDeniedError, OpenAIError
import os

# Uncomment below to turn on proxy

# os.environ["OPENAI_BASE_URL"] = "http://jupyter-api-proxy.stg.internal.dlai/rev-proxy/openai"
# os.environ["OPENAI_API_BASE"] = "http://jupyter-api-proxy.stg.internal.dlai/rev-proxy/openai"
# os.environ["OPENAI_API_KEY"]  = "<redacted>"

# List of OpenAI models to test
openai_models_list = [
    "o1-mini",
    "o3-mini",
    "o1",
    "o1-pro",
    "gpt-4o",
    "gpt-4o-mini",
]

# List of OpenAI embeddings models to test
openai_embeddings_models = [
    "text-embedding-3-small",
    "text-embedding-3-large",
]

# Check base model access
try:
    os.environ["OPENAI_BASE_URL"]
    os.environ["OPENAI_API_BASE"]
    os.environ["OPENAI_API_KEY"]
except KeyError:
    print("NO PROXY ENABLED")
else:
    client = OpenAI()

    print("PROXY WORKING")
    print("-----------------------")
    print("OpenAI Completion Model Access")
    
    # Check models for completion response
    for m in openai_models_list:
        try:
            completion = client.chat.completions.create(
                model=m,
                messages=[
                    {
                        "role": "user",
                        "content": "Respond with 'yes'"
                    }
                ]
            )
            print(f"{m}: available")
        except PermissionDeniedError:
            print(f"{m}: unavailable (Permission Denied)")
        except OpenAIError as e:
            print(f"{m}: error - {type(e).__name__}: {e}")


    # Check embeddings models for embedding response
    text = "This is an example sentence for text embedding."

    print("\n\nOpenAI Embeddings Model Access")
    print("-----------------------")
    
    for m in openai_embeddings_models:
    
        try:
            response = openai.embeddings.create(
            model=m,
            input=text
        )
            print(f"{m}: available")
        except PermissionDeniedError:
            print(f"{m}: unavailable (Permission Denied)")
        except OpenAIError as e:
            print(f"{m}: error - {type(e).__name__}: {e}")

---

## Helper Module Context

_Extracted from: helper.py. (3 symlink(s) collapsed)._

_Top-level functions and classes, de-duplicated across helper files. Module-level constants are not included._

```python
def load_env():
    _ = load_dotenv(find_dotenv())
```

```python
def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key
```

```python
def load_heart_disease(train_size=200, test_size=70):
    """Load readable Heart Statlog features and a binary target."""
    df = pd.read_csv(DATA_PATH).rename(columns=RENAME)
    X = df.drop(columns="target")
    y = df["target"]
    return train_test_split(
        X,
        y,
        train_size=train_size,
        test_size=test_size,
        random_state=RANDOM_STATE,
        stratify=y,
    )
```

```python
def sample_heart_disease_rows(n_rows=8, *, rng=None):
    """Draw intact patient rows for an inference benchmark."""
    if n_rows < 1:
        raise ValueError("n_rows must be at least 1")

    rng = np.random.default_rng(rng)
    features = (
        pd.read_csv(DATA_PATH)
        .rename(columns=RENAME)
        .drop(columns="target")
    )
    positions = rng.choice(
        len(features),
        size=n_rows,
        replace=n_rows > len(features),
    )
    return features.iloc[positions].reset_index(drop=True)
```

```python
def categorical_indices(feature_names):
    """Return positions of categorical columns."""
    return [feature_names.index(column) for column in CATEGORICAL]
```

```python
def show_value(name, value):
    """Render a raw feature value as a human-readable label."""
    if name in DECODE:
        return DECODE[name].get(int(value), str(value))
    return f"{value:g}"
```

```python
def describe_patient(
    shap_row,
    patient,
    feature_names,
    label,
    top_k=5,
):
    """Print the top drivers behind one patient's predicted risk."""
    risk = float(shap_row.values.sum() + shap_row.base_values)
    base = float(shap_row.base_values)
    print(
        f"[{label}] predicted risk = {risk:.0%}  "
        f"(reference average {base:.0%})"
    )
    for index in np.argsort(-np.abs(shap_row.values))[:top_k]:
        name = feature_names[index]
        if shap_row.values[index] > 0:
            direction = "raises"
        else:
            direction = "lowers"
        value = show_value(name, patient.iloc[index])
        print(
            f"    {name:<18} = {value:<18} "
            f"{direction} risk by "
            f"{abs(shap_row.values[index]) * 100:4.1f} points"
        )
    print()
```

```python
def decoded_display_data(patient, feature_names):
    """Return human-readable feature values for SHAP plots."""
    return np.array(
        [
            show_value(name, patient.iloc[index])
            for index, name in enumerate(feature_names)
        ],
        dtype=object,
    )
```

```python
def use_lesson_style():
    """Use legible, high-contrast plotting defaults."""
    plt.rcParams.update(
        {
            "figure.figsize": (9, 5),
            "figure.dpi": 110,
            "font.size": 12,
            "axes.titlesize": 13,
            "axes.labelsize": 12,
            "axes.grid": True,
            "grid.alpha": 0.3,
            "legend.frameon": False,
        }
    )
```

```python
def configure_lesson(*, plots=False):
    """Apply compact display defaults shared by lesson notebooks."""
    from tabpfn_client.options import get_opts

    options = get_opts()
    if hasattr(options, "TABPFN_CLIENT_CI_MODE"):
        os.environ["TABPFN_CLIENT_CI_MODE"] = "true"
        options.TABPFN_CLIENT_CI_MODE = True
    for name in ("tabpfn_client", "tabpfn_client.client"):
        logging.getLogger(name).setLevel(logging.WARNING)
    pd.set_option("display.max_columns", 7)
    if plots:
        use_lesson_style()
```

```python
def quiet_client_call(method, *args, **kwargs):
    """Call the client without retaining animated spinner output."""
    with redirect_stdout(StringIO()):
        return method(*args, **kwargs)
```

```python
def timed_client_call(method, *args, **kwargs):
    """Return a quiet client result and its elapsed time."""
    start = time.perf_counter()
    result = quiet_client_call(method, *args, **kwargs)
    return result, time.perf_counter() - start
```

```python
def show_table(frame, caption, formats=None):
    """Display a consistently formatted lesson table."""
    styled = frame.style
    if formats:
        styled = styled.format(formats)
    display(styled.set_caption(caption))
```

```python
def show_split_summary(X_train, X_test):
    """Show the dimensions of the training and test tables."""
    summary = pd.DataFrame(
        {
            "rows": [len(X_train), len(X_test)],
            "features": [X_train.shape[1], X_test.shape[1]],
        },
        index=["training set", "test set"],
    )
    show_table(summary, "Training and test split")
```

```python
def show_fit_comparison(fit_times, predict_times, aucs, n_rows):
    """Display the measured timings and scores."""
    predict_label = f"request {n_rows} rows (s)"
    comparison = pd.DataFrame(
        {
            "fit (s)": fit_times,
            predict_label: predict_times,
            "test AUC": aucs,
        },
        index=["preprocessing only", "KV cache"],
    )
    formats = {
        "fit (s)": "{:.2f}",
        predict_label: "{:.2f}",
        "test AUC": "{:.3f}",
    }
    show_table(comparison, "One fit and one prediction", formats)
```

```python
def show_latency_comparison(timings):
    """Keep server computation and whole-request timing separate."""
    labels = ["preprocessing only", "KV cache"]
    for column, caption in [
        ("server_ms", "Server prediction (ms)"),
        ("request_ms", "Whole request (ms)"),
    ]:
        grouped = timings.groupby("model")[column]
        summary = pd.DataFrame({
            "median": grouped.median(),
            "25th percentile": grouped.quantile(0.25),
            "75th percentile": grouped.quantile(0.75),
        }).reindex(labels)
        show_table(summary, caption, "{:.0f}")
        baseline, cached = summary["median"]
        if np.isfinite([baseline, cached]).all() and cached > 0:
            ratio = baseline / cached
            print(f"{caption}: uncached / cached = {ratio:.2f}×")
        else:
            print(f"{caption}: timing unavailable")
```

```python
def benchmark_cache_comparison(
    baseline,
    cached,
    rows,
    n_queries=20,
    rows_per_query=8,
):
    """Compare warm models on matched batches; alternate order."""
    rng = np.random.default_rng(RANDOM_STATE)
    batches = [
        rows.iloc[
            rng.choice(len(rows), rows_per_query, replace=False)
        ].to_numpy()
        for _ in range(n_queries + 2)
    ]
    models = [("preprocessing only", baseline), ("KV cache", cached)]
    for _, model in models:
        for batch in batches[-2:]:
            quiet_client_call(model.predict_proba, batch)

    records = []
    for index in tqdm(
        range(n_queries), desc="Requests", leave=False
    ):
        order = models if index % 2 == 0 else models[::-1]
        for label, model in order:
            _, elapsed = timed_client_call(
                model.predict_proba, batches[index]
            )
            server = model.last_predict_timings or {}
            prediction = server.get("predict_s")
            queue = server.get("predict_queue_wait_s")
            records.append({
                "model": label,
                "query": index,
                "request_ms": elapsed * 1000,
                "server_ms": (
                    prediction * 1000
                    if prediction is not None else np.nan
                ),
                "queue_ms": (
                    queue * 1000 if queue is not None else np.nan
                ),
            })
    return pd.DataFrame(records)
```

```python
def make_shap_explainer(model, X_train, y_train):
    """Build the lesson's SHAP explainer with a fixed reference."""
    import shap

    background, _ = train_test_split(
        X_train,
        train_size=20,
        random_state=RANDOM_STATE,
        stratify=y_train,
    )

    def predict_risk(rows):
        probabilities = quiet_client_call(
            model.predict_proba, np.asarray(rows)
        )
        return probabilities[:, 1]

    return shap.PermutationExplainer(
        predict_risk, background, seed=RANDOM_STATE
    )
```

```python
def plot_beeswarm(shap_values, feature_count):
    """Draw the lesson's compact global SHAP summary."""
    import shap

    shap.plots.beeswarm(
        shap_values,
        max_display=feature_count,
        show=False,
    )
    figure = plt.gcf()
    figure.set_size_inches(9, 5.5)
    figure.suptitle(
        "Global drivers of coronary-disease risk\n"
        "right = toward disease; red = high feature value",
        fontsize=13,
    )
    figure.tight_layout()
    plt.show()
```

```python
def top_continuous_features(
    shap_values,
    feature_names,
    continuous,
    count=4,
):
    """Return indices of the strongest continuous features."""
    importance = np.abs(shap_values.values).mean(axis=0)
    ranking = np.argsort(-importance)
    return [
        index
        for index in ranking
        if feature_names[index] in continuous
    ][:count]
```

```python
def plot_partial_dependence(
    model,
    data,
    feature_indices,
    feature_names,
):
    """Draw compact partial-dependence panels on a shared scale."""
    with redirect_stdout(StringIO()):
        result = PartialDependenceDisplay.from_estimator(
            model,
            data,
            features=list(feature_indices),
            grid_resolution=12,
            kind="average",
            target=1,
            response_method="predict_proba",
            method="brute",
            n_cols=2,
        )

    figure = result.figure_
    figure.set_size_inches(9, 5.5)
    axes = [
        axis
        for axis in np.ravel(result.axes_)
        if axis is not None
    ]
    values = [
        line.get_ydata()
        for axis in axes
        for line in axis.get_lines()
    ]
    low = min(value.min() for value in values)
    high = max(value.max() for value in values)
    padding = 0.05 * (high - low)

    for position, (axis, index) in enumerate(
        zip(axes, feature_indices)
    ):
        axis.set_ylim(low - padding, high + padding)
        axis.set_xlabel(feature_names[index])
        label = "Predicted P(disease)" if position % 2 == 0 else ""
        axis.set_ylabel(label)

    figure.suptitle(
        "Average predicted risk by measurement\n"
        "panels share the same y-axis",
        fontsize=13,
    )
    figure.tight_layout()
    plt.show()
```

```python
def plot_patient_waterfall(
    shap_values,
    patient_index,
    patients,
    feature_names,
    label,
):
    """Describe one patient and draw a compact SHAP waterfall."""
    import shap

    row = shap_values[patient_index]
    patient = patients.iloc[patient_index]
    row.display_data = decoded_display_data(
        patient,
        feature_names,
    )
    describe_patient(row, patient, feature_names, label)
    predicted = row.values.sum() + row.base_values
    shap.plots.waterfall(row, show=False)
    figure = plt.gcf()
    figure.set_size_inches(9, 5)
    figure.suptitle(
        f"{label}: predicted risk {predicted:.0%}",
        fontsize=13,
    )
    figure.tight_layout()
    plt.show()
```

```python
def load_heart_disease_full(train_size=700, test_size=220):
    """Split the pooled four-hospital heart data (920 rows)."""
    df = pd.read_csv(HEART_FULL_PATH).rename(columns=RENAME)
    X = df.drop(columns="target")
    y = df["target"]
    return train_test_split(
        X,
        y,
        train_size=train_size,
        test_size=test_size,
        random_state=RANDOM_STATE,
        stratify=y,
    )
```

```python
def plot_actual_vs_predicted(y_true, y_pred, unit=""):
    """Scatter actual against predicted with the ideal line."""
    y = np.asarray(y_true, dtype=float)
    p = np.asarray(y_pred, dtype=float)
    low = min(y.min(), p.min())
    high = max(y.max(), p.max())
    pad = 0.04 * (high - low)
    ends = [low - pad, high + pad]

    plt.figure(figsize=(6.2, 6.2))
    plt.plot(
        ends,
        ends,
        color="gray",
        ls="--",
        lw=1.5,
        label="perfect prediction",
    )
    plt.scatter(y, p, s=18, alpha=0.6)
    plt.xlim(ends)
    plt.ylim(ends)
    plt.gca().set_aspect("equal")
    plt.xlabel(f"actual {unit}".strip())
    plt.ylabel(f"predicted {unit}".strip())
    plt.title("Closer to the diagonal is better")
    plt.legend()
    plt.tight_layout()
    plt.show()
```

```python
def init_tabpfn():
    """Authenticate the client, preferring a token in the env."""
    import tabpfn_client

    load_env()
    token = os.getenv("TABPFN_TOKEN")
    if token:
        tabpfn_client.set_access_token(token)
    elif hasattr(tabpfn_client, "interactive_login"):
        # tabpfn-client >= 0.6: init() no longer prompts for a login.
        # interactive_login() reuses a cached token or opens the browser.
        tabpfn_client.interactive_login()
    else:
        tabpfn_client.init()
```

```python
def load_housing(train_size=1200, test_size=260):
    """Split Ames houses to predict the sale price in dollars."""
    df = pd.read_csv(HOUSING_PATH)
    X = df.drop(columns="Sale price")
    y = df["Sale price"]
    return train_test_split(
        X,
        y,
        train_size=train_size,
        test_size=test_size,
        random_state=RANDOM_STATE,
    )
```

```python
def plot_quantile_band(
    y_true,
    lower,
    median,
    upper,
    ylabel,
    unit="test samples",
):
    """Plot actual values inside a predicted quantile band."""
    order = np.argsort(np.asarray(median))
    y = np.asarray(y_true)[order]
    low = np.asarray(lower)[order]
    mid = np.asarray(median)[order]
    high = np.asarray(upper)[order]
    inside = (y >= low) & (y <= high)
    x = np.arange(len(y))

    plt.figure()
    plt.fill_between(
        x,
        low,
        high,
        alpha=0.25,
        label="10th to 90th percentile",
    )
    plt.plot(x, mid, lw=1.5, label="predicted median")
    plt.scatter(
        x[inside], y[inside], s=18, label="actual, inside band"
    )
    plt.scatter(
        x[~inside],
        y[~inside],
        s=26,
        color="crimson",
        label="actual, outside band",
    )
    plt.xlabel(f"{unit}, sorted by predicted median")
    plt.ylabel(ylabel)
    plt.title(f"One uncertainty band per {unit.rstrip('s')}")
    plt.legend()
    plt.tight_layout()
    plt.show()
```

```python
def plot_predicted_distribution(
    full_output,
    row,
    actual,
    xlabel,
):
    """Draw the predicted density for one regression test row."""
    # The full output spans a huge support with log-probabilities
    # per bin; far-tail bins may arrive as NaN and carry no mass.
    logits = np.asarray(full_output["logits"])[row]
    borders = np.asarray(full_output["borders"])
    if borders.ndim > 1:
        borders = borders[row]

    probabilities = np.exp(np.nan_to_num(logits, nan=-np.inf))
    probabilities = probabilities / probabilities.sum()
    density = probabilities / np.diff(borders)
    window = np.ones(21) / 21
    density = np.convolve(density, window, mode="same")
    centers = (borders[:-1] + borders[1:]) / 2

    cdf = np.cumsum(probabilities)
    keep = (cdf > 0.001) & (cdf < 0.999)
    inner = (cdf > 0.1) & (cdf < 0.9)

    plt.figure()
    plt.fill_between(
        centers[keep],
        density[keep],
        color="tab:blue",
        alpha=0.2,
        label="predicted distribution",
    )
    plt.fill_between(
        centers[inner],
        density[inner],
        color="tab:blue",
        alpha=0.5,
        label="80% interval (10th to 90th)",
    )
    mean = float(np.asarray(full_output["mean"])[row])
    plt.axvline(
        mean,
        color="tab:blue",
        ls="--",
        label=f"mean {mean:,.0f}",
    )
    plt.axvline(
        actual,
        color="crimson",
        lw=2,
        label=f"actual {actual:,.0f}",
    )
    span = centers[keep]
    pad = 0.15 * (span.max() - span.min())
    plt.xlim(
        min(span.min(), actual) - pad,
        max(span.max(), actual) + pad,
    )
    plt.ylim(bottom=0)
    plt.xlabel(xlabel)
    plt.ylabel("density")
    plt.title("The model predicts a distribution, not a number")
    plt.legend()
    plt.tight_layout()
    plt.show()
```

```python
def _split_series(df, horizon):
    """Split one time series into history and held-out future."""
    history = df.iloc[:-horizon].reset_index(drop=True)
    future = df.iloc[-horizon:].reset_index(drop=True)
    return history.copy(), future.copy()
```

```python
def load_co2(horizon=24):
    """Return monthly CO2 history plus a held-out future."""
    df = pd.read_csv(CO2_PATH, parse_dates=["month"])
    return _split_series(df, horizon)
```

```python
def load_electricity(horizon=48):
    """Return hourly electricity prices plus a held-out future."""
    df = pd.read_csv(ELECTRICITY_PATH, parse_dates=["hour"])
    return _split_series(df, horizon)
```

```python
def plot_co2(history, months=120):
    """Plot the tail of the CO2 series."""
    recent = history.iloc[-months:]
    plt.figure()
    plt.plot(recent["month"], recent["co2_ppm"])
    plt.ylabel("CO2 (ppm)")
    plt.title("Monthly CO2 at Mauna Loa: trend plus seasonality")
    plt.tight_layout()
    plt.show()
```

```python
def plot_electricity(history, hours=336):
    """Plot the tail of the hourly electricity price series."""
    recent = history.iloc[-hours:]
    plt.figure()
    plt.plot(recent["hour"], recent["price_eur"])
    plt.ylabel("price (EUR/MWh)")
    plt.title("Hourly day-ahead electricity prices: a daily cycle")
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show()
```

```python
def plot_forecast_comparison(
    history,
    future,
    forecasts,
    time_col,
    target_col,
    ylabel,
    title,
    band=None,
    context=72,
):
    """Compare forecasts, optionally with a prediction band."""
    recent = history.iloc[-context:]
    plt.figure()
    plt.plot(
        recent[time_col],
        recent[target_col],
        color="gray",
        label="history",
    )
    plt.plot(
        future[time_col],
        future[target_col],
        color="black",
        lw=2,
        label="actual future",
    )
    for label, values in forecasts.items():
        plt.plot(
            future[time_col], values, "--", lw=2, label=label
        )
    if band is not None:
        low, high = band
        plt.fill_between(
            future[time_col],
            low,
            high,
            color="tab:blue",
            alpha=0.2,
            label="10th to 90th percentile",
        )
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show()
```

```python
def display_precomputed():
    """Show the precomputed benchmark numbers (no re-run needed)."""
    labels = ["preprocessing only", "KV cache"]
    formats = {
        "median": "{:.0f}",
        "25th percentile": "{:.0f}",
        "75th percentile": "{:.0f}",
    }

    model_pred = pd.DataFrame({
        "median": [2625, 272],
        "25th percentile": [2609, 270],
        "75th percentile": [2642, 276],
    }, index=labels)
    show_table(model_pred, "Model prediction (ms)", formats)
    print(f"Model prediction (ms): uncached / cached = {2625 / 272:.2f}x")

    whole_request = pd.DataFrame({
        "median": [3853, 1524],
        "25th percentile": [3827, 1482],
        "75th percentile": [3889, 1584],
    }, index=labels)
    show_table(whole_request, "Whole request (ms)", formats)
    print(f"Whole request (ms): uncached / cached = {3853 / 1524:.2f}x")
```
