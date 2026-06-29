# Decisions & Assumptions Log

Fill this in as you go — don't try to reconstruct it at the end, you'll forget the reasoning.
Each entry: what you decided, why, what you gave up.

## Scoping decisions

- **Single city (NYC), not multi-city.** Chosen because [X amount of time available];
  the brief itself states depth on one city outperforms shallow multi-city work.
  Trade-off: no cross-market comparative insight.

- **Skipped: cloud deployment, Docker, dbt, RAG/agentic AI.** These are weighted lowest
  in the rubric (AI/ML Experimentation = 10) relative to the time they'd cost.
  Discussed conceptually in the report instead of implemented.

## Data decisions

- **Price field parsing:** stripped `$` and `,`, cast to float. Rows with price <= 0 or
  > $10,000/night dropped as likely data entry errors or non-representative luxury outliers
  — [state how many rows this affected once you run it].

- **Lat/long validation:** restricted to NYC bounding box (40.4–41.0 lat, -74.3 to -73.6 lon)
  to drop obvious geocoding errors.

- **Missing `reviews_per_month`:** filled with 0 rather than imputed, because a missing value
  here plausibly means "no reviews yet," not "unknown" — an explicit, defensible assumption.

- **No separate hosts table exists in Inside Airbnb** — host attributes are derived from the
  listings table itself (one row per listing, not per host). Documented as a data limitation,
  not engineered around.

## Modeling decisions

- **Model families chosen:** Linear Regression (interpretable baseline), Random Forest,
  XGBoost — covers linear, bagged-tree, and boosted-tree approaches as required.

- **Evaluation metric:** MAE prioritized over RMSE for stakeholder communication (easier to
  explain as "average dollar error per night") while still reporting RMSE/MAPE as required.

- **SHAP over LIME:** chosen for consistency with prior tree-based-model explainability work
  and native TreeExplainer support for XGBoost.

## What I would do with more time

- [Fill in: multi-city, NLP sentiment on reviews, dashboard, cloud architecture, etc.]
