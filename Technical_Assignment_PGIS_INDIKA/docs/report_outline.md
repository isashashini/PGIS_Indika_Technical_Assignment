# Final Report Outline (fill this in, then convert to PDF)

Follow this exact structure — it matches Section 12 of the assignment brief. Keep each
section honest and concise rather than padded; for a 1-day scope, aim for ~12-15 pages,
not the full 20 — note in your Reflection that page count was traded for depth/time.

## 1. Executive Summary (1 page)
- 3-4 headline findings (e.g., price drivers, borough differences, model accuracy)
- 2-3 actionable recommendations
- One line on scope: single city (NYC), 1-day assessment window

## 2. Objectives & Scope
- What you set out to do
- Why NYC was chosen
- Explicit statement of what was deprioritized and why (multi-city, dashboard, NLP, cloud)

## 3. Dataset Overview
- Inside Airbnb description, files used (listings, calendar)
- Known limitations (scrape-based, no separate hosts table, etc. — see docs/decisions_log.md)
- Key assumptions made

## 4. Methodology
- Overall analytical approach: clean -> EDA -> stats -> ML
- Why nonparametric tests were used for price comparisons (skewed distribution)

## 5. Engineering Approach
- Pipeline: ingestion -> cleaning -> validation -> star schema (DuckDB)
- Reference sql/star_schema.sql; explain fact/dimension design briefly
- Note: production considerations (incremental loads, orchestration) discussed but not built

## 6. EDA Findings
- Insert Figures 1-5 from reports/figures/, each with a numbered caption AND a
  2-3 sentence plain-English business interpretation (mandatory per brief)

## 7. Statistical Findings
- Table: H1-H5, test used, statistic, p-value, effect size
- One business-language sentence per hypothesis

## 8. Data Science Experiments
- Model comparison table (Linear / RF / XGBoost - MAE, RMSE, MAPE)
- Figure 6: SHAP summary plot + interpretation of top 3 price drivers
- Residual discussion (1 paragraph: any systematic errors by borough/room type?)

## 9. AI/ML Experiments
- Honest: state this was deprioritized given the 1-day window
- If you did anything (e.g. a quick sentiment check), describe it; otherwise describe
  what you WOULD do (sentiment analysis on reviews, LLM-generated insight summaries)
  and why it was cut

## 10. Visualizations
- Can consolidate with Section 6 if using the same figures - just ensure each is
  numbered and captioned

## 11. Business Recommendations
- 3-5 concrete, actionable items derived from your actual findings
  (e.g., "Entire-home listings in [borough] are underpriced relative to demand signals")

## 12. Cross-City Comparisons
- N/A - single city scope. State this explicitly rather than leaving the section blank.

## 13. Limitations & Caveats
- Data: scrape snapshot, not full booking data; no official host table
- Model: no cross-validation across boroughs tested; small feature set given time
- Scope: single city, 1-day window

## 14. Future Improvements
- Multi-city expansion, NLP on reviews, deployed dashboard, cloud-native pipeline,
  automated retraining

## 15. Reflection
- How you prioritized (reference rubric weights), what you cut and why,
  what you'd do differently with more time, key lessons

## Appendix A: AI Usage Disclosure
- Paste contents of docs/ai_usage_disclosure.md
