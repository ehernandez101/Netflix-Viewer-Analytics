"""
Netflix Viewer Analytics
02_netflix_kpi_analysis.py

Purpose:
Create business KPIs and Tableau-ready analytical datasets from the
cleaned Netflix user behavior dataset.

Outputs are written to:
data/processed/tableau/
"""

from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# 1. PROJECT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

PROCESSED_DIR = ROOT / "data" / "processed"
TABLEAU_DIR = PROCESSED_DIR / "tableau"

TABLEAU_DIR.mkdir(parents=True, exist_ok=True)

BEHAVIOR_FILE = PROCESSED_DIR / "netflix_user_behavior_clean.csv"


print("=" * 75)
print("NETFLIX VIEWER ANALYTICS")
print("KPI & BUSINESS ANALYSIS")
print("=" * 75)

print(f"\nProject folder:\n{ROOT}")
print(f"\nInput file:\n{BEHAVIOR_FILE}")
print(f"\nTableau output folder:\n{TABLEAU_DIR}")


# ============================================================
# 2. LOAD CLEAN DATA
# ============================================================

if not BEHAVIOR_FILE.exists():
    raise FileNotFoundError(
        "\nClean user behavior file was not found.\n"
        "Run 01_netflix_data_cleaning.py first.\n"
        f"Expected file:\n{BEHAVIOR_FILE}"
    )

df = pd.read_csv(BEHAVIOR_FILE)

print("\nClean user behavior dataset loaded successfully.")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns):,}")


# ============================================================
# 3. STANDARDIZE CHURN FIELD
# ============================================================

# Convert churn values into a numeric flag:
# 1 = churned
# 0 = retained

df["churn_flag"] = (
    df["churned"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map(
        {
            "yes": 1,
            "no": 0,
            "true": 1,
            "false": 0,
            "1": 1,
            "0": 0,
        }
    )
)

if df["churn_flag"].isna().any():
    print(
        "\nWARNING: Some churn values could not be converted "
        "to churn_flag."
    )

df["customer_status"] = np.where(
    df["churn_flag"] == 1,
    "Churned",
    "Retained"
)


# ============================================================
# 4. REVENUE METRICS
# ============================================================

df["estimated_monthly_revenue"] = df["monthly_fee"]

df["revenue_at_risk"] = np.where(
    df["churn_flag"] == 1,
    df["monthly_fee"],
    0
)


# ============================================================
# 5. EXECUTIVE KPIs
# ============================================================

total_users = len(df)

churned_users = int(df["churn_flag"].sum())

retained_users = total_users - churned_users

churn_rate = df["churn_flag"].mean() * 100

retention_rate = 100 - churn_rate

monthly_revenue = df["monthly_fee"].sum()

annualized_revenue = monthly_revenue * 12

monthly_revenue_at_risk = df["revenue_at_risk"].sum()

annualized_revenue_at_risk = monthly_revenue_at_risk * 12

avg_monthly_fee = df["monthly_fee"].mean()

avg_watch_time = df["avg_watch_time_minutes"].mean()

avg_completion_rate = df["completion_rate"].mean()

avg_rating = df["rating_given"].mean()

avg_binge_sessions = df["binge_watch_sessions"].mean()

avg_recommendation_ctr = df["recommendation_click_rate"].mean()

avg_days_since_login = df["days_since_last_login"].mean()

avg_content_interactions = df["content_interactions"].mean()


executive_kpis = pd.DataFrame(
    {
        "kpi": [
            "Total Users",
            "Retained Users",
            "Churned Users",
            "Churn Rate (%)",
            "Retention Rate (%)",
            "Estimated Monthly Revenue",
            "Annualized Revenue",
            "Monthly Revenue At Risk",
            "Annualized Revenue At Risk",
            "Average Monthly Fee",
            "Average Watch Time (Minutes)",
            "Average Completion Rate (%)",
            "Average Rating",
            "Average Binge Sessions",
            "Average Recommendation Click Rate (%)",
            "Average Days Since Last Login",
            "Average Content Interactions",
        ],
        "value": [
            total_users,
            retained_users,
            churned_users,
            round(churn_rate, 2),
            round(retention_rate, 2),
            round(monthly_revenue, 2),
            round(annualized_revenue, 2),
            round(monthly_revenue_at_risk, 2),
            round(annualized_revenue_at_risk, 2),
            round(avg_monthly_fee, 2),
            round(avg_watch_time, 2),
            round(avg_completion_rate, 2),
            round(avg_rating, 2),
            round(avg_binge_sessions, 2),
            round(avg_recommendation_ctr, 2),
            round(avg_days_since_login, 2),
            round(avg_content_interactions, 2),
        ],
    }
)


# ============================================================
# 6. HELPER FUNCTION
# ============================================================

def build_segment_analysis(column_name):
    """
    Create an aggregated business analysis table for a category.
    """

    result = (
        df.groupby(column_name, dropna=False)
        .agg(
            users=("user_id", "count"),
            churned_users=("churn_flag", "sum"),
            churn_rate=("churn_flag", "mean"),
            estimated_monthly_revenue=(
                "estimated_monthly_revenue",
                "sum"
            ),
            revenue_at_risk=("revenue_at_risk", "sum"),
            avg_watch_time_minutes=(
                "avg_watch_time_minutes",
                "mean"
            ),
            avg_completion_rate=("completion_rate", "mean"),
            avg_rating=("rating_given", "mean"),
            avg_binge_sessions=("binge_watch_sessions", "mean"),
            avg_content_interactions=(
                "content_interactions",
                "mean"
            ),
            avg_recommendation_click_rate=(
                "recommendation_click_rate",
                "mean"
            ),
            avg_days_since_last_login=(
                "days_since_last_login",
                "mean"
            ),
        )
        .reset_index()
    )

    result["churn_rate"] = result["churn_rate"] * 100

    numeric_columns = result.select_dtypes(
        include=[np.number]
    ).columns

    result[numeric_columns] = result[numeric_columns].round(2)

    return result


# ============================================================
# 7. COUNTRY ANALYSIS
# ============================================================

country_analysis = build_segment_analysis("country")

country_analysis = country_analysis.sort_values(
    "users",
    ascending=False
)


# ============================================================
# 8. SUBSCRIPTION ANALYSIS
# ============================================================

subscription_analysis = build_segment_analysis(
    "subscription_type"
)

subscription_analysis = subscription_analysis.sort_values(
    "users",
    ascending=False
)


# ============================================================
# 9. DEVICE ANALYSIS
# ============================================================

device_analysis = build_segment_analysis("primary_device")

device_analysis = device_analysis.sort_values(
    "users",
    ascending=False
)


# ============================================================
# 10. GENRE ANALYSIS
# ============================================================

genre_analysis = build_segment_analysis("favorite_genre")

genre_analysis = genre_analysis.sort_values(
    "users",
    ascending=False
)


# ============================================================
# 11. PAYMENT METHOD ANALYSIS
# ============================================================

payment_analysis = build_segment_analysis("payment_method")

payment_analysis = payment_analysis.sort_values(
    "users",
    ascending=False
)


# ============================================================
# 12. CHURNED VS RETAINED ANALYSIS
# ============================================================

churn_analysis = (
    df.groupby("customer_status")
    .agg(
        users=("user_id", "count"),
        estimated_monthly_revenue=(
            "estimated_monthly_revenue",
            "sum"
        ),
        avg_monthly_fee=("monthly_fee", "mean"),
        avg_watch_time_minutes=(
            "avg_watch_time_minutes",
            "mean"
        ),
        avg_watch_sessions_per_week=(
            "watch_sessions_per_week",
            "mean"
        ),
        avg_binge_sessions=(
            "binge_watch_sessions",
            "mean"
        ),
        avg_completion_rate=(
            "completion_rate",
            "mean"
        ),
        avg_rating=("rating_given", "mean"),
        avg_content_interactions=(
            "content_interactions",
            "mean"
        ),
        avg_recommendation_click_rate=(
            "recommendation_click_rate",
            "mean"
        ),
        avg_days_since_last_login=(
            "days_since_last_login",
            "mean"
        ),
        avg_account_age_months=(
            "account_age_months",
            "mean"
        ),
    )
    .reset_index()
)

numeric_columns = churn_analysis.select_dtypes(
    include=[np.number]
).columns

churn_analysis[numeric_columns] = (
    churn_analysis[numeric_columns].round(2)
)


# ============================================================
# 13. AGE GROUP ANALYSIS
# ============================================================

age_bins = [0, 24, 34, 44, 54, 64, 200]

age_labels = [
    "18-24",
    "25-34",
    "35-44",
    "45-54",
    "55-64",
    "65+",
]

df["age_group"] = pd.cut(
    df["age"],
    bins=age_bins,
    labels=age_labels,
    include_lowest=True,
)

age_analysis = build_segment_analysis("age_group")


# ============================================================
# 14. ENGAGEMENT SEGMENT
# ============================================================

watch_median = df["avg_watch_time_minutes"].median()

df["engagement_segment"] = np.where(
    df["avg_watch_time_minutes"] >= watch_median,
    "High Engagement",
    "Low Engagement"
)

engagement_analysis = build_segment_analysis(
    "engagement_segment"
)


# ============================================================
# 15. BINGE WATCHING SEGMENT
# ============================================================

binge_median = df["binge_watch_sessions"].median()

df["binge_segment"] = np.where(
    df["binge_watch_sessions"] >= binge_median,
    "High Binge Activity",
    "Low Binge Activity"
)

binge_analysis = build_segment_analysis("binge_segment")


# ============================================================
# 16. LOGIN ACTIVITY SEGMENT
# ============================================================

df["login_activity_segment"] = pd.cut(
    df["days_since_last_login"],
    bins=[-1, 7, 14, 30, 60, np.inf],
    labels=[
        "0-7 Days",
        "8-14 Days",
        "15-30 Days",
        "31-60 Days",
        "60+ Days",
    ],
)

login_activity_analysis = build_segment_analysis(
    "login_activity_segment"
)


# ============================================================
# 17. EXPORT TABLEAU FILES
# ============================================================

outputs = {
    "executive_kpis.csv": executive_kpis,
    "churn_analysis.csv": churn_analysis,
    "country_analysis.csv": country_analysis,
    "subscription_analysis.csv": subscription_analysis,
    "device_analysis.csv": device_analysis,
    "genre_analysis.csv": genre_analysis,
    "payment_analysis.csv": payment_analysis,
    "age_analysis.csv": age_analysis,
    "engagement_analysis.csv": engagement_analysis,
    "binge_analysis.csv": binge_analysis,
    "login_activity_analysis.csv": login_activity_analysis,
}


print("\n" + "=" * 75)
print("EXPORTING TABLEAU DATASETS")
print("=" * 75)

for filename, dataframe in outputs.items():

    output_path = TABLEAU_DIR / filename

    dataframe.to_csv(
        output_path,
        index=False
    )

    print(
        f"Created: {filename} "
        f"({len(dataframe):,} rows)"
    )


# Also export the enriched user-level dataset.
# This gives Tableau maximum flexibility for additional analysis.

tableau_user_file = (
    TABLEAU_DIR / "netflix_user_analytics.csv"
)

df.to_csv(
    tableau_user_file,
    index=False
)

print(
    f"Created: netflix_user_analytics.csv "
    f"({len(df):,} rows)"
)


# ============================================================
# 18. PRINT EXECUTIVE SUMMARY
# ============================================================

print("\n" + "=" * 75)
print("EXECUTIVE KPI SUMMARY")
print("=" * 75)

print(f"\nTotal Users: {total_users:,}")

print(
    f"Retained Users: "
    f"{retained_users:,}"
)

print(
    f"Churned Users: "
    f"{churned_users:,}"
)

print(
    f"Churn Rate: "
    f"{churn_rate:.2f}%"
)

print(
    f"Retention Rate: "
    f"{retention_rate:.2f}%"
)

print(
    f"Estimated Monthly Revenue: "
    f"${monthly_revenue:,.2f}"
)

print(
    f"Annualized Revenue: "
    f"${annualized_revenue:,.2f}"
)

print(
    f"Monthly Revenue At Risk: "
    f"${monthly_revenue_at_risk:,.2f}"
)

print(
    f"Annualized Revenue At Risk: "
    f"${annualized_revenue_at_risk:,.2f}"
)

print(
    f"Average Watch Time: "
    f"{avg_watch_time:.2f} minutes"
)

print(
    f"Average Completion Rate: "
    f"{avg_completion_rate:.2f}%"
)

print(
    f"Average Rating: "
    f"{avg_rating:.2f}"
)


# ============================================================
# 19. IDENTIFY HIGH-LEVEL BUSINESS FINDINGS
# ============================================================

highest_churn_subscription = (
    subscription_analysis
    .sort_values("churn_rate", ascending=False)
    .iloc[0]
)

highest_churn_genre = (
    genre_analysis
    .sort_values("churn_rate", ascending=False)
    .iloc[0]
)

highest_churn_device = (
    device_analysis
    .sort_values("churn_rate", ascending=False)
    .iloc[0]
)

highest_revenue_country = (
    country_analysis
    .sort_values(
        "estimated_monthly_revenue",
        ascending=False
    )
    .iloc[0]
)


print("\n" + "=" * 75)
print("INITIAL BUSINESS FINDINGS")
print("=" * 75)

print(
    "\nSubscription tier with highest churn rate:"
)

print(
    f"{highest_churn_subscription['subscription_type']} "
    f"({highest_churn_subscription['churn_rate']:.2f}%)"
)

print(
    "\nFavorite genre with highest churn rate:"
)

print(
    f"{highest_churn_genre['favorite_genre']} "
    f"({highest_churn_genre['churn_rate']:.2f}%)"
)

print(
    "\nPrimary device with highest churn rate:"
)

print(
    f"{highest_churn_device['primary_device']} "
    f"({highest_churn_device['churn_rate']:.2f}%)"
)

print(
    "\nCountry with highest estimated monthly revenue:"
)

print(
    f"{highest_revenue_country['country']} "
    f"(${highest_revenue_country['estimated_monthly_revenue']:,.2f})"
)


print("\n" + "=" * 75)
print("KPI ANALYSIS COMPLETE")
print("=" * 75)

print(
    "\nTableau-ready files are located at:"
)

print(TABLEAU_DIR)

print(
    "\nNext step: Build the Netflix Executive Analytics "
    "Dashboard in Tableau."
)
