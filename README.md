# NYC Airbnb Market Intelligence — Data Engineering Technical Assignment

**Candidate:** PGIS Indika  
**Organisation:** Expernetic (Pvt) Ltd — Talent Assessment Program  
**Role:** Data Engineer Intern  
**Dataset:** Inside Airbnb — New York City (Scrape Date: 2026-06-23)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Repository Structure](#2-repository-structure)
3. [What Has Been Completed](#3-what-has-been-completed)
4. [What Has Not Been Completed & Why](#4-what-has-not-been-completed--why)
5. [Setup & Reproducibility Instructions](#5-setup--reproducibility-instructions)
6. [How to Review This Submission](#6-how-to-review-this-submission)
7. [Key Deliverables Index](#7-key-deliverables-index)
8. [AI Tools Used](#8-ai-tools-used)
9. [Data Source](#9-data-source)

---

## 1. Project Overview

This repository contains the technical assignment submission for the **Data Engineer Intern** role at Expernetic (Pvt) Ltd. The objective was to act as a Data Engineer and Analyst for a hypothetical Airbnb market intelligence consultancy, transforming publicly available short-term rental data into engineering artefacts, analytical insights, and business recommendations.

**City selected:** New York City, USA  
**Prioritisation rationale:** Single-city analysis was chosen to allow maximum depth across sections 02, 03, and 04, consistent with the assignment's design philosophy that depth on one city outperforms shallow multi-city coverage.

---

## 2. Repository Structure

```
Technical_Assignment_PGIS_INDIKA/
│
├── 01_dataset_familiarization.ipynb       # Section 02 — Dataset Familiarization
├── 03_Data_Engineering_Challenges.ipynb   # Section 03 — Data Engineering Pipeline
├── 04_Exploratory_Data_Analysis .ipynb    # Section 04 — Exploratory Data Analysis
│
├── src/
│   ├── clean.py                           # Data cleaning helper functions
│   ├── eda.py                             # EDA helper functions
│   ├── model.py                           # (Scaffolded, not executed)
│   └── stats_tests.py                     # (Scaffolded, not executed)
│
├── sql/
│   └── star_schema.sql                    # Star schema DDL for the DuckDB warehouse
│
├── data/
│   ├── raw/
│   │   ├── listings.csv.gz                # Core listings — 30,259 rows × 90 columns
│   │   ├── listings.csv                   # Detailed listings (full metadata)
│   │   ├── listings(1).csv                # Alternate listings snapshot
│   │   ├── calendar.csv.gz                # Daily availability data — 11.2M rows
│   │   ├── reviews.csv                    # Guest reviews — 990,170 rows
│   │   └── neighbourhoods.csv             # Neighbourhood groupings — 230 rows
│   └── processed/
│       ├── airbnb_warehouse.duckdb        # DuckDB star-schema warehouse (6 tables)
│       ├── nyc_enriched_listing_master.csv  # Cleaned & enriched master listing table
│       └── pipeline_metadata.db           # SQLite pipeline run & lineage metadata
│
├── figures/                               # All EDA visualisation outputs (27 figures)
│   ├── fig01_price_distribution_overall.png
│   ├── fig02_price_by_borough.png
│   ├── fig03_price_by_room_type.png
│   ├── fig04_price_by_property_type.png
│   ├── fig05_host_power_law.png
│   ├── fig06_review_score_distributions.png
│   ├── fig07_rating_inflation.png
│   ├── fig08_availability_distributions.png
│   ├── fig10_availability_by_borough.png
│   ├── fig11_listing_density.png
│   ├── fig12_price_distance_gradient.png
│   ├── fig13_review_scores_spatial.png
│   ├── fig14_clustering_by_type.png
│   ├── fig15_demand_by_month.png
│   ├── fig16_review_volume_trend.png
│   ├── fig17_price_by_host_tenure.png
│   ├── fig18_min_nights_by_month.png
│   ├── fig19_host_segmentation.png
│   ├── fig20_price_by_host_segment.png
│   ├── fig21_superhost_vs_nonsuper.png
│   ├── fig23_lorenz_supply_concentration.png
│   ├── fig24_review_count_score_price.png
│   ├── fig25_review_frequency_demand.png
│   ├── fig26_high_demand_low_quality.png
│   └── fig27_subdimension_analysis.png
│
├── logs/
│   └── pipeline.log                       # Structured pipeline execution log
│
├── docs/
│   ├── ai_usage_disclosure.md             # AI tool usage log
│   ├── decisions_log.md                   # Engineering & data decision log
│   └── report_outline.md                  # Report planning notes
│
├── Documentations/
│   ├── Data_Engineering_Technical_Report.pdf  # ★ Primary report — start here
│   ├── AI_Usage_Disclosure.pdf
│   ├── Assumptions_and_Decision_Log.pdf
│   ├── Completed_Work.pdf
│   ├── Incompleted_Work.pdf
│   └── Reproducibility_Instructions.pdf
│
├── requirements.txt                       # Python dependencies
└── README.md                              # This file
```

---

## 3. What Has Been Completed

### Section 02 — Dataset Familiarization (`01_dataset_familiarization.ipynb`)

All tasks in Section 02 were fully completed.

- **Schema documentation** — column names, data types, ranges, and sample values for all four files (listings, calendar, reviews, neighbourhoods)
- **Primary and foreign key relationships** — `listings.id` as primary key; `calendar.listing_id` and `reviews.listing_id` as foreign keys; orphaned record counts documented (296 in calendar, 239 in reviews)
- **Columns requiring special interpretation** — detailed table covering 100% null scraping failures (`host_since`, `instant_bookable`, `host_response_rate`, etc.), partially missing fields (`license` 82.5% null, `bedrooms` 36.3%, `price` 28.9%), and non-obvious fields (`available` as `t`/`f` strings, `reviews_per_month` as Inside Airbnb's derived field)
- **Dataset limitations** — 9 documented limitations including scraping failures, orphaned records, COVID-19 distortion in 2020 review volumes, price outliers ($4.58–$30,972.96), and single-snapshot nature of the data
- **Assumptions log** — documented before any analysis, including treating null `license` as "no license" (not unknown), treating null review scores as "no reviews" (not imputation candidates), and relying on `neighbourhood_cleansed` over the raw `neighbourhood` column
- **Business domain context** — entity descriptions for Listing (30,259 listings, $4.58–$30,972.96 price range), Host (16,474 unique hosts, host data embedded in listings with no separate file), and Review (990,170 reviews spanning 2009–2026, used as the only proxy for booking demand)

---

### Section 03 — Data Engineering Challenges (`03_Data_Engineering_Challenges.ipynb`)

#### 3.1 Data Ingestion & Profiling
- Repeatable ingestion pipeline with skip-if-present logic (downloads only if the file is not on disk)
- Full dataset profiling: row counts, column cardinality, null rates, data type distributions for all four files
- Structured data quality report with a weighted quality score (Grade B: 84.9/100) and per-column severity classification (DEAD / CRITICAL / HIGH / MODERATE / LOW / COMPLETE)
- Duplicate detection: deterministic check (0 exact duplicates) plus fuzzy matching using host ID + neighbourhood + room type + price tolerance + name similarity score — 5,075 near-duplicate candidate pairs found, 1,646 classified as HIGH confidence
- Completeness assessment with documented business implications for each missing-data finding
- Outlier report for price (max $30,972.96; 12 listings above $10,000), availability, and review count
- Domain validation: all listings pass price ≥ 0, lat/lon within NYC bounding box, availability within 0–365, minimum nights ≥ 1; 27 listings outside strict bounding box flagged (not dropped)

#### 3.2 Data Cleaning & Standardisation
- Price columns: stripped `$` and `,`, cast to float; `price_quote_*` fields confirmed already numeric
- Date fields: all date columns in listings, calendar, and reviews parsed to `datetime64` with sanity checks against scrape date
- Free-text normalisation: `t`/`f` flags converted to nullable boolean; `room_type` whitespace and casing standardised; `property_type` (69 unique values) mapped to a 5-group `property_group` derived column
- Missing value handling: 12 always-null columns dropped; `has_reviews` flag added; `bedrooms`, `bathrooms`, `beds` imputed using group-median by `(room_type, accommodates)` with `*_was_missing` transparency flags; review score columns left as NaN (missing-not-at-random)
- Validation flags: `flag_outside_city_bbox` and `flag_long_min_stay` added as soft flags; records with `price < 0` hard-dropped (none found)
- Geographic standardisation: coordinates rounded to 5 decimal places; `neighbourhood_cleansed` and `neighbourhood_group_cleansed` whitespace-stripped and title-cased; `city` column added for future multi-city pipeline compatibility

#### 3.3 Data Enrichment & Joining
- Listings joined with aggregated review summary (review count, first/last date, unique reviewers, average comment length) from `reviews.csv`
- Calendar integrated to compute per-listing occupancy rate and revenue estimate (nights booked × current price)
- Neighbourhood-level aggregates appended directly via `transform`: median price, listing count, average rating per neighbourhood
- Derived calculated fields: `host_tenure_years` (from Inside Airbnb's pre-derived field, since `host_since` was 100% null), `review_frequency` (review count ÷ months hosting), `price_per_bedroom` (price ÷ bedrooms, with studio safety guard)
- Multi-city scaffold: `CITY_MASTER_FRAMES` dictionary ready for a second city to be added with automatic schema harmonisation
- Enriched master saved to `data/processed/nyc_enriched_listing_master.csv`

#### 3.4 Data Modeling
- Star schema designed and implemented in DuckDB with 4 dimension tables and 2 fact tables:
  - `dim_date` — 365 calendar dates with year, month, day, day of week, is_weekend
  - `dim_host` — one row per host (16,474 hosts) with superhost status, identity verification, tenure
  - `dim_neighbourhood` — one row per neighbourhood (221 neighbourhoods) with pre-computed aggregates
  - `dim_property_type` — one row per (property_type, property_group, room_type) combination
  - `fact_listing` — one row per listing with FK references to all four dimensions, plus price, occupancy, revenue estimate, derived metrics
  - `fact_calendar` — one row per listing per date (11.2M rows) with FK to `dim_date`, is_booked flag
- 6 analytical SQL queries demonstrated: revenue by room type, top neighbourhoods by price, weekday vs. weekend booking rate, monthly seasonality, top multi-listing hosts by portfolio revenue, host tenure vs. rating/price
- Trade-offs documented: denormalisation choice, SCD omission (single-snapshot data), surrogate key strategy, omission of a separate `dim_listing`, constraint enforcement decision

#### 3.5 Pipeline Design & Automation
- Structured logging with dual-channel output (console at INFO, file at DEBUG) written to `logs/pipeline.log`
- Exponential back-off retry logic for downloads (max 3 attempts, base delay 2s, cap 60s)
- City-configurable pipeline via a `CITY_CONFIG` dictionary — change only this dict to target any Inside Airbnb city with no code modification
- Incremental processing using MD5 checksums: files are only re-downloaded and re-processed when a content change is detected
- Metadata management layer in SQLite (`pipeline_metadata.db`) with three tables — `pipeline_runs`, `file_events`, `validation_events` — tracking ingestion timestamps, file hashes, row counts, and validation outcomes per run
- Data lineage documented for all 11 output tables/files, tracing source → transformation → sink; lineage records also written to the `lineage` table in `pipeline_metadata.db`

---

### Section 04 — Exploratory Data Analysis (`04_Exploratory_Data_Analysis .ipynb`)

All five EDA sub-sections were fully completed. Every visualisation is accompanied by a plain-English business interpretation as required.

#### 4.1 Summary Statistics & Distributions
- Descriptive statistics table for 14 key numerical variables with skewness and kurtosis
- **Fig 01** — NYC nightly price distribution (linear and log scale)
- **Fig 02** — Median price and IQR box by borough (Manhattan highest, Bronx lowest)
- **Fig 03** — Violin plot and summary table by room type (Entire home ~2–3× private room)
- **Fig 04** — Price box plot by top 10 property types (boats, villas, boutique hotels at premium)
- **Fig 05** — Power law host portfolio analysis: log-log plot, pie chart of listing share by segment, host count vs. listings controlled; casual hosts (1 listing) are the majority of hosts but control only 37.2% of listings
- **Fig 06** — Review score distributions for all sub-dimensions; strong left-skew confirming rating inflation
- **Fig 07** — Rating inflation breakdown: percentage of listings with perfect 5.0, 4.5–5.0, below 4.5, below 4.0
- **Fig 08 & 10** — Availability distribution (bimodal pattern) and availability by borough

#### 4.2 Geographic & Spatial Analysis
- **Fig 11** — Listing density map across neighbourhoods
- **Fig 12** — Geographic pricing gradient: listings closer to Manhattan city centre command higher prices
- **Fig 13** — Review scores mapped spatially to identify high- and low-rated neighbourhood clusters
- **Fig 14** — Geographic clustering of property and room types across boroughs

#### 4.3 Temporal & Seasonal Trends
- **Fig 15** — Demand seasonality by month derived from calendar data
- **Fig 16** — Review volume trend from 2009–2026; COVID-19 impact visible in 2020 dip
- **Fig 17** — Price by host tenure bucket (0–2 years, 2–5 years, 5+ years)
- **Fig 18** — Minimum night policy shifts across calendar months

#### 4.4 Host & Supply-Side Analysis
- **Fig 19** — Host segmentation (casual / small / medium / professional / commercial) by portfolio size
- **Fig 20** — Pricing strategy differences between casual and professional hosts
- **Fig 21** — Superhost vs. non-superhost listing performance comparison
- **Fig 23** — Lorenz curve demonstrating supply concentration (small number of commercial hosts controls disproportionate inventory)

#### 4.5 Review & Demand-Side Analysis
- **Fig 24** — Relationship between review count, review score, and price for 15,131 listings
- **Fig 25** — Review frequency as a proxy for booking demand across 15,283 listings
- **Fig 26** — Characterisation of the "high review count + low score" friction zone
- **Fig 27** — Sub-dimension score analysis across all 6 review dimensions (cleanliness, location, communication, check-in, accuracy, value) for 15,437 listings

---

## 4. What Has Not Been Completed & Why

| Section | What Was Skipped | Reason |
|---------|-----------------|--------|
| 03.6 | Advanced & Cloud-Native Topics | Architectural concepts (Docker, CDC, cloud) discussed in the written report rather than implemented. Rubric weight is lowest (AI/ML Experimentation = 10) relative to the time investment required. |
| 05 | Statistical Analysis | `src/stats_tests.py` scaffolded with function stubs. Not executed within the one-week window after prioritising depth in sections 02–04. |
| 06 | Data Science / ML | `src/model.py` scaffolded with Linear Regression, Random Forest, and XGBoost stubs. Not executed. |
| 07 | AI & LLM Opportunities | Not attempted. |
| 08 | Open Innovation Challenge | Not attempted. |

The assignment brief explicitly states that depth in chosen sections outperforms shallow coverage of all sections. Sections 02, 03, and 04 carry the highest combined rubric weight and were completed in full.

---

## 5. Setup & Reproducibility Instructions

### Prerequisites

- Python 3.10 or higher
- Git
- ~2 GB free disk space

### Step 1 — Clone the repository

```bash
git clone https://github.com/isashashini/PGIS_Indika_Technical_Assignment.git
cd PGIS_Indika_Technical_Assignment/Technical_Assignment_PGIS_INDIKA
```

### Step 2 — Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

| Package | Purpose |
|---------|---------|
| `pandas` | Core data manipulation |
| `numpy` | Numerical computation |
| `matplotlib` / `seaborn` | Visualisations |
| `scipy` | Statistical functions |
| `scikit-learn` | ML preprocessing |
| `xgboost` | Gradient boosting (scaffolded) |
| `shap` | Model explainability (scaffolded) |
| `duckdb` | Embedded analytical warehouse |
| `folium` | Interactive geospatial maps |
| `geopandas` | Spatial data |
| `jupyter` | Notebook environment |

### Step 4 — Data files

Raw data files are already included in `data/raw/`. If you need to re-download them:

1. Go to [https://insideairbnb.com/get-the-data/](https://insideairbnb.com/get-the-data/)
2. Select **New York City, New York, United States — scrape date 2026-06-23**
3. Download and place in `data/raw/`: `listings.csv.gz`, `calendar.csv.gz`, `reviews.csv`, `neighbourhoods.csv`

Alternatively, the ingestion pipeline in `03_Data_Engineering_Challenges.ipynb` (Section 3.1.1) will download files automatically if they are not on disk.

### Step 5 — Run notebooks in order

```bash
jupyter notebook
```

Run in this exact order:

1. `01_dataset_familiarization.ipynb`
2. `03_Data_Engineering_Challenges.ipynb` ← produces `nyc_enriched_listing_master.csv` and `airbnb_warehouse.duckdb`
3. `04_Exploratory_Data_Analysis .ipynb` ← reads from processed data; produces all figures

Each notebook is self-contained with markdown cells explaining every decision.

---

## 6. How to Review This Submission

| Step | Artefact | Why |
|------|----------|-----|
| 1 | `Documentations/Data_Engineering_Technical_Report.pdf` | Start here — the primary written deliverable |
| 2 | `01_dataset_familiarization.ipynb` | Section 02 — schema, relationships, limitations, assumptions, domain context |
| 3 | `03_Data_Engineering_Challenges.ipynb` | Full pipeline: ingestion → profiling → cleaning → enrichment → star schema → automation |
| 4 | `04_Exploratory_Data_Analysis .ipynb` | All 27 EDA figures with business interpretations |
| 5 | `figures/` | All saved visualisation outputs (fig01–fig27) |
| 6 | `sql/star_schema.sql` | Star schema DDL |
| 7 | `data/processed/airbnb_warehouse.duckdb` | Live DuckDB warehouse with all 6 tables |
| 8 | `logs/pipeline.log` | Pipeline execution log |
| 9 | `docs/decisions_log.md` | Engineering decision log with trade-offs |
| 10 | `Documentations/AI_Usage_Disclosure.pdf` | Full AI usage disclosure per Section 10 |
| 11 | `Documentations/Assumptions_and_Decision_Log.pdf` | All data and modelling assumptions |

---

## 7. Key Deliverables Index

| Deliverable | Location | Status |
|-------------|----------|--------|
| Source Code | `src/`, all notebooks | ✅ |
| Reproducibility Instructions | `Documentations/Reproducibility_Instructions.pdf` | ✅ |
| Professional PDF Report | `Documentations/Data_Engineering_Technical_Report.pdf` | ✅ |
| Assumptions & Decisions Log | `Documentations/Assumptions_and_Decision_Log.pdf`, `docs/decisions_log.md` | ✅ |
| Summary: Completed Work | `Documentations/Completed_Work.pdf` | ✅ |
| Summary: Incomplete Work | `Documentations/Incompleted_Work.pdf` | ✅ |
| AI Usage Disclosure | `Documentations/AI_Usage_Disclosure.pdf`, `docs/ai_usage_disclosure.md` | ✅ |
| Enriched Master Dataset | `data/processed/nyc_enriched_listing_master.csv` | ✅ |
| DuckDB Warehouse | `data/processed/airbnb_warehouse.duckdb` | ✅ |
| Pipeline Metadata | `data/processed/pipeline_metadata.db` | ✅ |
| Star Schema SQL | `sql/star_schema.sql` | ✅ |
| EDA Figures (27 charts) | `figures/` | ✅ |
| Pipeline Log | `logs/pipeline.log` | ✅ |

---

## 8. AI Tools Used

AI tools were used in accordance with the assignment's AI Tools Usage Policy (Section 10). Full disclosure is in `Documentations/AI_Usage_Disclosure.pdf` and `docs/ai_usage_disclosure.md`.

| Tool | How It Was Used |
|------|----------------|
| Claude (Anthropic) | Code structure guidance, markdown writing, decision log drafting |

All AI-generated outputs were reviewed, tested by running the code, and modified where necessary. No AI output was accepted without manual validation.

---

## 9. Data Source

All data sourced exclusively from **Inside Airbnb** (public, independent dataset).

- **Homepage:** [https://insideairbnb.com/](https://insideairbnb.com/)
- **Data Download:** [https://insideairbnb.com/get-the-data/](https://insideairbnb.com/get-the-data/)
- **Data Dictionary:** [Google Sheets](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/)
- **Methodology:** [https://insideairbnb.com/behind-the-data/](https://insideairbnb.com/behind-the-data/)

---

*Expernetic (Pvt) Ltd — Talent Assessment Program · Confidential & For Candidate Use Only*
