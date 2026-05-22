import pandas as pd
import numpy as np
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

INPUT_FILE = DATA / "final_animedataset.csv"
OUTPUT_FILE = DATA / "crunchyroll_anime_dataset.csv"

# -----------------------------
# Load real anime dataset
# -----------------------------
df = pd.read_csv(INPUT_FILE)

print("Loaded real anime dataset:")
print(df.head())
print("\nColumns:")
print(df.columns)

# -----------------------------
# Standardize column names
# -----------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

# -----------------------------
# Try to find useful columns
# -----------------------------
title_col = "name" if "name" in df.columns else df.columns[0]
genre_col = "genres" if "genres" in df.columns else None
score_col = "score" if "score" in df.columns else None
episodes_col = "episodes" if "episodes" in df.columns else None
members_col = "members" if "members" in df.columns else None
popularity_col = "popularity" if "popularity" in df.columns else None

# -----------------------------
# Build clean analytics dataset
# -----------------------------
analytics_df = pd.DataFrame()

analytics_df["anime_title"] = df[title_col].astype(str)

if genre_col:
    analytics_df["genre"] = df[genre_col].astype(str).str.split(",").str[0].str.strip()
else:
    analytics_df["genre"] = np.random.choice(
        ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Romance"],
        size=len(df)
    )

if score_col:
    analytics_df["score"] = pd.to_numeric(df[score_col], errors="coerce")
else:
    analytics_df["score"] = np.random.uniform(6.0, 9.5, size=len(df)).round(2)

if episodes_col:
    analytics_df["episodes"] = pd.to_numeric(df[episodes_col], errors="coerce")
else:
    analytics_df["episodes"] = np.random.randint(1, 26, size=len(df))

if members_col:
    analytics_df["members"] = pd.to_numeric(df[members_col], errors="coerce")
else:
    analytics_df["members"] = np.random.randint(10000, 1000000, size=len(df))

if popularity_col:
    analytics_df["popularity"] = pd.to_numeric(df[popularity_col], errors="coerce")
else:
    analytics_df["popularity"] = analytics_df["members"].rank(ascending=False)

# -----------------------------
# Clean missing values
# -----------------------------
analytics_df = analytics_df.dropna(subset=["anime_title"])
analytics_df["score"] = analytics_df["score"].fillna(analytics_df["score"].median())
analytics_df["episodes"] = analytics_df["episodes"].fillna(analytics_df["episodes"].median())
analytics_df["members"] = analytics_df["members"].fillna(analytics_df["members"].median())
analytics_df["genre"] = analytics_df["genre"].replace("nan", "Unknown").fillna("Unknown")

# -----------------------------
# Simulate streaming analytics fields from real metadata
# -----------------------------
np.random.seed(42)

analytics_df["user_id"] = range(1, len(analytics_df) + 1)

analytics_df["region"] = np.random.choice(
    ["North America", "Europe", "Latin America", "Asia"],
    size=len(analytics_df),
    p=[0.35, 0.25, 0.20, 0.20]
)

analytics_df["watch_minutes"] = (
    analytics_df["score"] * 15
    + np.random.normal(20, 15, size=len(analytics_df))
).clip(10).round(1)

analytics_df["episodes_completed"] = (
    analytics_df["episodes"] * np.random.uniform(0.25, 0.95, size=len(analytics_df))
).clip(1).round().astype(int)

analytics_df["completion_rate"] = (
    analytics_df["episodes_completed"] / analytics_df["episodes"]
).clip(0, 1)

analytics_df["days_inactive"] = np.random.randint(0, 60, size=len(analytics_df))
analytics_df["subscription_months"] = np.random.randint(1, 48, size=len(analytics_df))
analytics_df["ad_clicks"] = np.random.randint(0, 20, size=len(analytics_df))

# -----------------------------
# Retention and churn logic
# -----------------------------
analytics_df["engagement_score"] = (
    analytics_df["watch_minutes"] * 0.35
    + analytics_df["completion_rate"] * 100 * 0.35
    + analytics_df["score"] * 10 * 0.30
).round(2)

analytics_df["retained"] = np.where(
    (analytics_df["engagement_score"] >= analytics_df["engagement_score"].median())
    & (analytics_df["days_inactive"] < 30),
    1,
    0
)

analytics_df["churn_risk"] = np.where(
    (analytics_df["days_inactive"] > 30)
    & (analytics_df["engagement_score"] < analytics_df["engagement_score"].median()),
    "High",
    "Low"
)

# -----------------------------
# Save final analytics dataset
# -----------------------------
analytics_df.to_csv(OUTPUT_FILE, index=False)

print("\nReal-data analytics dataset created successfully.")
print(f"Saved to: {OUTPUT_FILE}")
print("\nPreview:")
print(analytics_df.head())
print("\nRows:", len(analytics_df))