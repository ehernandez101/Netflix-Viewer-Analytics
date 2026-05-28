import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

df = pd.read_csv(DATA / "crunchyroll_anime_dataset.csv")

np.random.seed(42)

df["homepage_click"] = np.random.choice([0, 1], size=len(df), p=[0.35, 0.65])

df["started_episode"] = np.where(
    df["homepage_click"] == 1,
    np.random.choice([0, 1], size=len(df), p=[0.25, 0.75]),
    0
)

df["completed_episode"] = np.where(
    df["started_episode"] == 1,
    np.random.choice([0, 1], size=len(df), p=[0.30, 0.70]),
    0
)

df["returned_next_day"] = np.where(
    df["completed_episode"] == 1,
    np.random.choice([0, 1], size=len(df), p=[0.40, 0.60]),
    0
)

print("\n=== VIEWER JOURNEY FUNNEL ===\n")
print(f"Homepage Click Rate: {df['homepage_click'].mean():.2%}")
print(f"Episode Start Rate: {df['started_episode'].mean():.2%}")
print(f"Episode Completion Rate: {df['completed_episode'].mean():.2%}")
print(f"Next-Day Return Rate: {df['returned_next_day'].mean():.2%}")

title_funnel = (
    df.groupby("anime_title")[["homepage_click", "started_episode", "completed_episode", "returned_next_day"]]
    .mean()
    .mul(100)
    .round(2)
)

print("\n=== TITLE PERFORMANCE FUNNEL ===\n")
print(title_funnel.head(15))

df.to_csv(DATA / "crunchyroll_viewer_journey_dataset.csv", index=False)

print("\nViewer journey dataset created successfully.")