"""
src/clean.py
Loads and cleans Inside Airbnb listings + calendar data.
Run standalone: python src/clean.py
"""
import pandas as pd
import numpy as np
import os

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"


def load_listings(path=f"{RAW_DIR}/listings.csv.gz"):
    df = pd.read_csv(path, low_memory=False)
    return df


def clean_listings(df):
    df = df.copy()

    # --- price: strip $ and commas, cast to float ---
    if df["price"].dtype == object:
        df["price"] = (
            df["price"].astype(str).str.replace(r"[$,]", "", regex=True)
        )
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # --- validation rules ---
    before = len(df)
    df = df[(df["price"] > 0) & (df["price"] < 10000)]  # drop negative/zero/absurd prices
    print(f"[clean] dropped {before - len(df)} rows on price validation")

    # lat/long sanity check (NYC bounding box roughly)
    df = df[df["latitude"].between(40.4, 41.0) & df["longitude"].between(-74.3, -73.6)]

    # --- categorical standardization ---
    df["room_type"] = df["room_type"].astype(str).str.strip().str.title()
    if "property_type" in df.columns:
        df["property_type"] = df["property_type"].astype(str).str.strip()

    # --- dates ---
    for col in ["host_since", "first_review", "last_review"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # --- derived fields ---
    if "host_since" in df.columns:
        df["host_tenure_years"] = (
            (pd.Timestamp.today() - df["host_since"]).dt.days / 365.25
        )

    if "bedrooms" in df.columns:
        df["price_per_bedroom"] = df["price"] / df["bedrooms"].replace(0, np.nan)

    # --- missing value handling: explicit nulls, document rather than impute blindly ---
    df["reviews_per_month"] = df["reviews_per_month"].fillna(0)

    return df


def load_calendar(path=f"{RAW_DIR}/calendar.csv.gz"):
    df = pd.read_csv(path, low_memory=False)
    df["date"] = pd.to_datetime(df["date"])
    if df["price"].dtype == object:
        df["price"] = df["price"].astype(str).str.replace(r"[$,]", "", regex=True)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["available"] = df["available"].map({"t": True, "f": False})
    df["is_weekend"] = df["date"].dt.dayofweek >= 5
    return df


def data_quality_report(df, name="listings"):
    report = pd.DataFrame({
        "dtype": df.dtypes,
        "null_count": df.isnull().sum(),
        "null_pct": (df.isnull().mean() * 100).round(2),
        "n_unique": df.nunique(),
    })
    out_path = f"{PROCESSED_DIR}/dq_report_{name}.csv"
    report.to_csv(out_path)
    print(f"[clean] data quality report saved -> {out_path}")
    return report


if __name__ == "__main__":
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    listings = load_listings()
    data_quality_report(listings, "listings_raw")

    listings_clean = clean_listings(listings)
    listings_clean.to_csv(f"{PROCESSED_DIR}/listings_clean.csv", index=False)
    print(f"[clean] saved {len(listings_clean)} clean listings")

    calendar = load_calendar()
    calendar.to_csv(f"{PROCESSED_DIR}/calendar_clean.csv", index=False)
    print(f"[clean] saved {len(calendar)} calendar rows")
