import pandas as pd 

df = pd.read_csv("../data/crunchyroll_anime_dataset.csv")

print("\n=== CONTENT KPI SUMMARY ===\n")

total_users = df["user_id"].nunique()
avg_watch = df["watch_minutes"].mean()
retention_rate = df["retained"].mean() * 100

print(f"Total Users: {total_users}")
print(f"Average Watch Minutes: {avg_watch:.2f}")
print(f"Retention Rate: {retention_rate:.2f}%")

print("\n=== TOP ANIME TITLES ===\n")

top_titles = (
    df.groupby("anime_title")["watch_minutes"]
    .mean()
    .sort_values(ascending=False)
)

print(top_titles)

print("\n=== REGION ENGAGEMENT ===\n")

region_stats = (
    df.groupby("region")["watch_minutes"]
    .mean()
)

print(region_stats)

print("\n=== CHURN RISK DISTRIBUTION ===\n")

print(df["churn_risk"].value_counts())
