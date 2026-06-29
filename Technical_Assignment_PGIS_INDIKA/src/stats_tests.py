"""
src/stats_tests.py
Runs the 5 hypothesis tests required by the assignment (Section 5.1).
Prints a results table you can paste straight into your report.
Run: python src/stats_tests.py
"""
import pandas as pd
from scipy import stats
import numpy as np

PROCESSED_DIR = "data/processed"


def cohens_d(a, b):
    pooled_std = np.sqrt(((len(a) - 1) * a.std()**2 + (len(b) - 1) * b.std()**2) / (len(a) + len(b) - 2))
    return (a.mean() - b.mean()) / pooled_std


def h1_entire_home_vs_private(df):
    a = df[df["room_type"] == "Entire Home/Apt"]["price"].dropna()
    b = df[df["room_type"] == "Private Room"]["price"].dropna()
    t, p = stats.mannwhitneyu(a, b, alternative="greater")  # price likely non-normal -> nonparametric
    d = cohens_d(a, b)
    print(f"H1: Entire home vs private room price | U={t:.1f} p={p:.4g} Cohen's d={d:.2f}")
    print(f"    Means: entire={a.mean():.1f}, private={b.mean():.1f}")


def h2_superhost_review_scores(df):
    if "host_is_superhost" not in df.columns or "review_scores_rating" not in df.columns:
        print("H2: required columns missing, skipping")
        return
    a = df[df["host_is_superhost"] == "t"]["review_scores_rating"].dropna()
    b = df[df["host_is_superhost"] == "f"]["review_scores_rating"].dropna()
    t, p = stats.mannwhitneyu(a, b, alternative="greater")
    d = cohens_d(a, b)
    print(f"H2: Superhost vs non-superhost review scores | U={t:.1f} p={p:.4g} Cohen's d={d:.2f}")


def h3_reviews_threshold_price(df):
    a = df[df["number_of_reviews"] > 10]["price"].dropna()
    b = df[df["number_of_reviews"] <= 10]["price"].dropna()
    t, p = stats.mannwhitneyu(a, b)
    d = cohens_d(a, b)
    print(f"H3: >10 reviews vs <=10 reviews price | U={t:.1f} p={p:.4g} Cohen's d={d:.2f}")


def h4_neighbourhood_anova(df):
    groups = [g["price"].dropna() for _, g in df.groupby("neighbourhood_group_cleansed")]
    groups = [g for g in groups if len(g) > 5]
    f, p = stats.f_oneway(*groups)
    # eta-squared
    grand_mean = df["price"].mean()
    ss_between = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in groups)
    ss_total = sum((df["price"].dropna() - grand_mean) ** 2)
    eta_sq = ss_between / ss_total
    print(f"H4: Neighbourhood ANOVA | F={f:.2f} p={p:.4g} eta^2={eta_sq:.3f}")


def h5_weekend_weekday(calendar_df):
    a = calendar_df[calendar_df["is_weekend"]]["price"].dropna()
    b = calendar_df[~calendar_df["is_weekend"]]["price"].dropna()
    t, p = stats.mannwhitneyu(a, b, alternative="greater")
    d = cohens_d(a, b)
    print(f"H5: Weekend vs weekday price | U={t:.1f} p={p:.4g} Cohen's d={d:.2f}")
    print(f"    Means: weekend={a.mean():.1f}, weekday={b.mean():.1f}")


if __name__ == "__main__":
    listings = pd.read_csv(f"{PROCESSED_DIR}/listings_clean.csv")
    calendar = pd.read_csv(f"{PROCESSED_DIR}/calendar_clean.csv", parse_dates=["date"])

    print("=" * 70)
    h1_entire_home_vs_private(listings)
    h2_superhost_review_scores(listings)
    h3_reviews_threshold_price(listings)
    h4_neighbourhood_anova(listings)
    h5_weekend_weekday(calendar)
    print("=" * 70)
    print("NOTE: copy this output into Section 7 (Statistical Findings) of your report,")
    print("with one business-language sentence interpreting each result.")
