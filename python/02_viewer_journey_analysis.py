import pandas as pd
import numpy as np

df = pd.read_csv("../data/crunchyroll_anime_dataset.csv")

np.random.seed(42)

# -----------------------------
# Simulate Viewer Journey
# -----------------------------

df["homepage_click"] = np.random.choice(
    [0, 1],
    size=len(df),
    p=[0.35, 0.65]
)

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

# -----------------------------
# Funnel Metrics
# -----------------------------

homepage_click_rate = df["homepage_click"].mean() * 100
start_rate = df["started_episode"].mean() * 100
completion_rate = df["completed_episode"].mean() * 100
return_rate = df["returned_next_day"].mean() * 100

print("\n=== VIEWER JOURNEY FUNNEL ===\n")

print(f"Homepage Click Rate: {homepage_click_rate:.2f}%")
print(f"Episode Start Rate: {start_rate:.2f}%")
print(f"Episode Completion Rate: {completion_rate:.2f}%")
print(f"Next-Day Return Rate: {return_rate:.2f}%")

# -----------------------------
# Anime Title Funnel Analysis
# -----------------------------

title_funnel = (
    df.groupby("anime_title")[
        [
            "homepage_click",
            "started_episode",
            "completed_episode",
            "returned_next_day"
        ]
    ]
    .mean()
    * 100
)

print("\n=== TITLE PERFORMANCE FUNNEL ===\n")
print(title_funnel.round(2))

# Save enriched dataset
df.to_csv("../data/crunchyroll_viewer_journey_dataset.csv", index=False)

print("\nViewer journey dataset created successfully.")
