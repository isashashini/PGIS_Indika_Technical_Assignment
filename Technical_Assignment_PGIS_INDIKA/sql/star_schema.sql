-- sql/star_schema.sql
-- Minimal star schema for analytical queries on the NYC listing dataset.
-- Designed to run in DuckDB against the cleaned CSVs.
-- Run e.g.: duckdb < sql/star_schema.sql   (or paste into a DuckDB Python connection)

-- DIMENSION: listings
CREATE OR REPLACE TABLE dim_listing AS
SELECT
    id AS listing_id,
    host_id,
    room_type,
    property_type,
    neighbourhood_group_cleansed AS borough,
    neighbourhood_cleansed AS neighbourhood,
    latitude,
    longitude,
    accommodates,
    bedrooms,
    bathrooms
FROM read_csv_auto('data/processed/listings_clean.csv');

-- DIMENSION: hosts (derived — no separate host file exists, this is a known limitation)
CREATE OR REPLACE TABLE dim_host AS
SELECT DISTINCT
    host_id,
    host_since,
    host_tenure_years,
    host_is_superhost
FROM read_csv_auto('data/processed/listings_clean.csv');

-- FACT: daily price/availability from calendar
CREATE OR REPLACE TABLE fact_listing_day AS
SELECT
    listing_id,
    date,
    price,
    available,
    is_weekend
FROM read_csv_auto('data/processed/calendar_clean.csv');

-- Example analytical queries (Section 3.4 requirement: demonstrate use cases)

-- 1. Median price by borough and room type
SELECT borough, room_type, MEDIAN(price) AS median_price, COUNT(*) AS n
FROM dim_listing l
JOIN (SELECT listing_id, AVG(price) AS price FROM fact_listing_day GROUP BY listing_id) p
  ON l.listing_id = p.listing_id
GROUP BY borough, room_type
ORDER BY borough, median_price DESC;

-- 2. Occupancy rate per listing (share of days NOT available = booked/blocked)
SELECT listing_id,
       1.0 - AVG(CASE WHEN available THEN 1.0 ELSE 0.0 END) AS occupancy_rate
FROM fact_listing_day
GROUP BY listing_id
ORDER BY occupancy_rate DESC
LIMIT 20;

-- 3. Weekend vs weekday average price
SELECT is_weekend, AVG(price) AS avg_price
FROM fact_listing_day
GROUP BY is_weekend;
