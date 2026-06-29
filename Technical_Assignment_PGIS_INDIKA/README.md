# NYC Airbnb Market Intelligence — Data Engineering Assignment

## Project Overview
Analysis of New York City Airbnb market using Inside Airbnb public dataset.

## Dataset
- Source: Inside Airbnb (https://insideairbnb.com/)
- City: New York City
- Scrape Date: 2026-06-23

## Project Structure
airbnb-analysis/
├── data/
│   └── raw/
│       ├── listings.csv.gz
│       ├── calendar.csv.gz
│       ├── reviews.csv
│       └── neighbourhoods.csv
├── notebooks/
│   └── 01_dataset_familiarization.ipynb
├── README.md
└── requirements.txt

## How to Run
1. Install dependencies: pip install -r requirements.txt
2. Download data from https://insideairbnb.com/get-the-data/
3. Place files in data/raw/
4. Open notebooks/01_dataset_familiarization.ipynb
5. Run all cells top to bottom

## What Has Been Completed
- Section 2: Dataset Familiarization (fully completed)
  - Schema documentation
  - Primary and foreign key relationships
  - Columns requiring special interpretation
  - Dataset limitations
  - Assumptions about ambiguous fields
  - Business domain context

## What Has Not Been Completed
- Section 3: Data Engineering Challenges (in progress)
- Section 4: Exploratory Data Analysis (not started)
- Sections 5-8: Statistical, ML and AI analysis (not started)

Prioritization rationale: Focused on depth and completeness of
Section 2 before moving to engineering tasks.

## AI Tools Used
- Claude (Anthropic) — assisted with code structure and markdown writing
- All outputs verified and validated manually by running the code