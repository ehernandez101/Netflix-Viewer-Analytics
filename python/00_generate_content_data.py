import pandas as pd
import numpy as np
from pathlib import Path

# =========================================================
# PATH SETUP
# =========================================================

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

INPUT_FILE = DATA / "anime-filtered.csv"
OUTPUT_FILE = DATA / "crunchyroll_anime_dataset.csv"

# =========================================================
# LOAD REAL ANIME DATASET
# =========================================================

df = pd.read_csv(INPUT_FILE)

print("\nLoading anime dataset...\n")

# =========================================================
# CLEAN DATA
# =========================================================

df.columns = df.columns.str.lower().str.strip()

# Try to identify anime title column automatically
possible_title_columns = [
    "name",
    "title",
    "anime",
    "anime_title"
]

anime_title_col = None

for col in possible_title_columns:
    if col in df.columns:
        anime_title_col = col
        break

if anime_title_col is None:
    raise Exception(
        f"Could not find anime title column. Columns found: {df.columns.tolist()}"
    )

# =========================================================
# BUILD ANALYTICS DATASET
# =========================================================

analytics_df = pd.DataFrame()

analytics_df["anime_title"] = df[anime_title_col].astype(str)

# Create fake streaming analytics metrics
np.random.seed(42)

analytics_df["user_id"] = np.random.randint(1000, 50000, len(df))

analytics_df["watch_minutes"] = np.random.randint(15, 240, len(df))

analytics_df["completion_rate"] = np.round(
    np.random.uniform(0.30, 1.00, len(df)),
    2
)

analytics_df["score"] = np.round(
    np.random.uniform(5.5, 10.0, len(df)),
    2
)

genres = [
    "Action",
    "Fantasy",
    "Adventure",
    "Comedy",
    "Drama",
    "Sci-Fi"
]

analytics_df["genre"] = np.random.choice(genres, len(df))

regions = [
    "North America",
    "Latin America",
    "Europe",
    "Asia Pacific"
]

analytics_df["region"] = np.random.choice(regions, len(df))

analytics_df["retained"] = np.random.choice(
    [0, 1],
    len(df),
    p=[0.35, 0.65]
)

analytics_df["churn_risk"] = np.random.choice(
    ["Low", "Medium", "High"],
    len(df),
    p=[0.60, 0.25, 0.15]
)

# =========================================================
# SAVE OUTPUT
# =========================================================

analytics_df.to_csv(OUTPUT_FILE, index=False)

print("===================================================")
print("Crunchyroll analytics dataset created successfully.")
print("===================================================")

print(f"\nRows created: {len(analytics_df):,}")
print(f"Output file: {OUTPUT_FILE}")

print("\nSample Data:\n")
print(analytics_df.head())