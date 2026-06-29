# AI Usage Disclosure

## AI Tools Used
- Claude (Sonnet 4.6) — used for: project scoping/planning, code scaffolding for the
  data pipeline (src/clean.py, src/eda.py, src/stats_tests.py, src/model.py), and
  drafting this disclosure template.
- [Add any others: ChatGPT, GitHub Copilot, etc.]

## AI-Assisted Sections
- **Pipeline code structure** (ingestion, cleaning, EDA, stats, modeling): scaffolded
  with AI assistance, then reviewed, run against actual NYC data, and modified based on
  real output (column names actually present, actual row-drop counts, etc.)
- **Report structure/outline**: AI-assisted skeleton based on the assignment's required
  15-section structure; all analytical content, interpretation, and writing is my own.
- **Executive summary / business interpretations**: written by me; optionally drafted
  a first pass with AI and then rewritten substantially — [be honest about how much you
  changed].

## Key Prompts Used (example — replace with your actual prompts)
1. "Help me scope a 1-week NYC Airbnb data engineering assignment down to what's
   achievable in 1 day, prioritizing the highest-weighted rubric items."
2. "Write a Python cleaning script for Inside Airbnb listings.csv: parse price,
   validate lat/long, standardize room_type, derive host_tenure_years."
3. [Add your real prompts as you use them today]

## Output Validation
- All AI-generated code was run against the actual downloaded NYC dataset, not assumed
  to work — column names, row counts, and figures were checked against real output.
- [Note any code that errored and how you fixed it]

## Modifications Made
- [e.g., "Changed the bounding box values after checking actual NYC listing lat/long
  ranges" / "Removed a feature column the AI assumed existed but wasn't in this dataset"]

## Critical Assessment (cases where AI output was rejected or substantially changed)
- [This is explicitly checked for by graders — include at least one real example.
  e.g., "AI's first cleaning script imputed missing prices with the mean; I rejected this
  because it would bias the price-prediction model, and dropped those rows instead with
  documentation in the decisions log."]
