"""
src/eda.py
Generates the core EDA charts as PNGs into reports/figures/.
Each chart is saved with a numbered filename matching the figure numbers
you'll use in the report. Run: python src/eda.py
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

PROCESSED_DIR = "data/processed"
FIG_DIR = "reports/figures"

sns.set_theme(style="whitegrid")


def fig_price_by_room_type(df):
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x="room_type", y="price", showfliers=False)
    plt.title("Fig 1. Price Distribution by Room Type")
    plt.ylabel("Price (USD)")
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/fig1_price_by_room_type.png", dpi=150)
    plt.close()


def fig_listings_per_host(df):
    counts = df["host_id"].value_counts()
    plt.figure(figsize=(8, 5))
    sns.histplot(counts, bins=50, log_scale=(False, True))
    plt.title("Fig 2. Distribution of Listings per Host (log scale y-axis)")
    plt.xlabel("Listings per host")
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/fig2_listings_per_host.png", dpi=150)
    plt.close()

    top_pct = (counts[counts > 1].sum() / counts.sum()) * 100
    print(f"[eda] hosts with >1 listing control {top_pct:.1f}% of all listings")


def fig_price_vs_distance_proxy(df):
    # crude proxy: distance from Manhattan center if no proper geocoding available
    center_lat, center_lon = 40.7580, -73.9855
    df = df.copy()
    df["dist_to_center"] = (
        (df["latitude"] - center_lat) ** 2 + (df["longitude"] - center_lon) ** 2
    ) ** 0.5
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df.sample(min(3000, len(df))), x="dist_to_center", y="price", alpha=0.3)
    plt.ylim(0, df["price"].quantile(0.95))
    plt.title("Fig 3. Price vs. Distance from City Center (proxy)")
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/fig3_price_vs_distance.png", dpi=150)
    plt.close()


def fig_review_score_vs_price(df):
    score_col = "review_scores_rating" if "review_scores_rating" in df.columns else None
    if not score_col:
        print("[eda] no review_scores_rating column found, skipping")
        return
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df.sample(min(3000, len(df))), x=score_col, y="price", alpha=0.3)
    plt.ylim(0, df["price"].quantile(0.95))
    plt.title("Fig 4. Review Score vs. Price")
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/fig4_reviewscore_vs_price.png", dpi=150)
    plt.close()


def fig_monthly_price_trend(calendar_df):
    monthly = calendar_df.dropna(subset=["price"]).groupby(calendar_df["date"].dt.month)["price"].mean()
    plt.figure(figsize=(8, 5))
    monthly.plot(kind="line", marker="o")
    plt.title("Fig 5. Average Listed Price by Month")
    plt.xlabel("Month")
    plt.ylabel("Average Price (USD)")
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/fig5_monthly_price_trend.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    os.makedirs(FIG_DIR, exist_ok=True)
    listings = pd.read_csv(f"{PROCESSED_DIR}/listings_clean.csv")
    calendar = pd.read_csv(f"{PROCESSED_DIR}/calendar_clean.csv", parse_dates=["date"])

    fig_price_by_room_type(listings)
    fig_listings_per_host(listings)
    fig_price_vs_distance_proxy(listings)
    fig_review_score_vs_price(listings)
    fig_monthly_price_trend(calendar)
    print("[eda] all figures saved to reports/figures/")
