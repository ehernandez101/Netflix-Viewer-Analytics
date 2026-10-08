# ============================================================
# Netflix Viewer Analytics
# 01_netflix_data_cleaning.py
#
# Purpose:
# Clean and prepare the Netflix datasets for analysis,
# SQL work, and Tableau visualization.
#
# IMPORTANT:
# This script DOES NOT modify the original raw CSV files.
# It creates new cleaned files in data/processed/.
# ============================================================

from pathlib import Path
import pandas as pd


# ------------------------------------------------------------
# 1. PROJECT PATHS
# ------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

DATA = ROOT / "data"
PROCESSED = DATA / "processed"

REVIEWS_FILE = DATA / "netflix_reviews.csv"
BEHAVIOR_FILE = DATA / "netflix_user_behavior_dataset.csv"

CLEAN_REVIEWS_FILE = PROCESSED / "netflix_reviews_clean.csv"
CLEAN_BEHAVIOR_FILE = PROCESSED / "netflix_user_behavior_clean.csv"


# ------------------------------------------------------------
# 2. HELPER FUNCTIONS
# ------------------------------------------------------------

def print_section(title):
    print("\n")
    print("=" * 80)
    print(title)
    print("=" * 80)


def standardize_text(series):
    """
    Removes leading/trailing spaces from text fields.
    Missing values remain missing.
    """
    return series.astype("string").str.strip()


# ------------------------------------------------------------
# 3. CLEAN NETFLIX REVIEWS
# ------------------------------------------------------------

def clean_reviews():

    print_section("CLEANING NETFLIX REVIEWS")

    print("\nLoading:")
    print(REVIEWS_FILE)

    reviews = pd.read_csv(
        REVIEWS_FILE,
        low_memory=False
    )

    original_rows = len(reviews)

    print(f"\nOriginal rows: {original_rows:,}")
    print(f"Original columns: {reviews.shape[1]}")

    # --------------------------------------------------------
    # Remove exact duplicate rows
    # --------------------------------------------------------

    duplicate_rows = reviews.duplicated().sum()

    print(f"\nExact duplicate rows found: {duplicate_rows:,}")

    reviews = reviews.drop_duplicates().copy()

    print(
        f"Rows after removing exact duplicates: "
        f"{len(reviews):,}"
    )

    # --------------------------------------------------------
    # Clean text columns
    # --------------------------------------------------------

    text_columns = [
        "reviewId",
        "userName",
        "content",
        "reviewCreatedVersion",
        "appVersion"
    ]

    for column in text_columns:

        if column in reviews.columns:
            reviews[column] = standardize_text(
                reviews[column]
            )

    # --------------------------------------------------------
    # Convert score to numeric
    # --------------------------------------------------------

    if "score" in reviews.columns:

        reviews["score"] = pd.to_numeric(
            reviews["score"],
            errors="coerce"
        )

        invalid_scores = (
            reviews["score"].notna()
            & ~reviews["score"].between(1, 5)
        )

        invalid_score_count = invalid_scores.sum()

        print(
            f"\nInvalid review scores outside 1-5: "
            f"{invalid_score_count:,}"
        )

        # Invalid values become missing rather than being
        # silently included in analysis.
        reviews.loc[invalid_scores, "score"] = pd.NA

    # --------------------------------------------------------
    # Convert thumbsUpCount to numeric
    # --------------------------------------------------------

    if "thumbsUpCount" in reviews.columns:

        reviews["thumbsUpCount"] = pd.to_numeric(
            reviews["thumbsUpCount"],
            errors="coerce"
        )

        negative_thumbs = (
            reviews["thumbsUpCount"].notna()
            & (reviews["thumbsUpCount"] < 0)
        )

        print(
            f"Negative thumbs-up counts: "
            f"{negative_thumbs.sum():,}"
        )

        reviews.loc[
            negative_thumbs,
            "thumbsUpCount"
        ] = pd.NA

    # --------------------------------------------------------
    # Convert review date
    # --------------------------------------------------------

    if "at" in reviews.columns:

        reviews["review_date"] = pd.to_datetime(
            reviews["at"],
            errors="coerce"
        )

        invalid_dates = reviews["review_date"].isna().sum()

        print(
            f"Invalid/missing review dates: "
            f"{invalid_dates:,}"
        )

        # Tableau-friendly date dimensions
        reviews["review_year"] = (
            reviews["review_date"].dt.year
        )

        reviews["review_month"] = (
            reviews["review_date"].dt.month
        )

        reviews["review_month_name"] = (
            reviews["review_date"].dt.month_name()
        )

        reviews["review_year_month"] = (
            reviews["review_date"]
            .dt.to_period("M")
            .astype("string")
        )

    # --------------------------------------------------------
    # Add rating categories
    # --------------------------------------------------------

    if "score" in reviews.columns:

        reviews["rating_category"] = pd.cut(
            reviews["score"],
            bins=[0, 2, 3, 5],
            labels=[
                "Negative",
                "Neutral",
                "Positive"
            ]
        )

    # --------------------------------------------------------
    # Add review engagement category
    # --------------------------------------------------------

    if "thumbsUpCount" in reviews.columns:

        reviews["review_engagement"] = pd.cut(
            reviews["thumbsUpCount"],
            bins=[
                -1,
                0,
                5,
                25,
                float("inf")
            ],
            labels=[
                "No Engagement",
                "Low",
                "Medium",
                "High"
            ]
        )

    # --------------------------------------------------------
    # Final review summary
    # --------------------------------------------------------

    removed_rows = original_rows - len(reviews)

    print("\nREVIEWS CLEANING SUMMARY")
    print("-" * 80)

    print(f"Original rows: {original_rows:,}")
    print(f"Final rows:    {len(reviews):,}")
    print(f"Rows removed:  {removed_rows:,}")

    print("\nMissing values after cleaning:")
    print(reviews.isna().sum())

    return reviews


# ------------------------------------------------------------
# 4. CLEAN USER BEHAVIOR DATA
# ------------------------------------------------------------

def clean_behavior():

    print_section("CLEANING NETFLIX USER BEHAVIOR")

    print("\nLoading:")
    print(BEHAVIOR_FILE)

    behavior = pd.read_csv(
        BEHAVIOR_FILE,
        low_memory=False
    )

    original_rows = len(behavior)

    print(f"\nOriginal rows: {original_rows:,}")
    print(f"Original columns: {behavior.shape[1]}")

    # --------------------------------------------------------
    # Remove exact duplicate rows
    # --------------------------------------------------------

    duplicate_rows = behavior.duplicated().sum()

    print(
        f"\nExact duplicate rows found: "
        f"{duplicate_rows:,}"
    )

    behavior = behavior.drop_duplicates().copy()

    # --------------------------------------------------------
    # Clean text/category columns
    # --------------------------------------------------------

    text_columns = [
        "user_id",
        "gender",
        "country",
        "subscription_type",
        "payment_method",
        "primary_device",
        "favorite_genre",
        "churned"
    ]

    for column in text_columns:

        if column in behavior.columns:

            behavior[column] = standardize_text(
                behavior[column]
            )

    # --------------------------------------------------------
    # Standardize known categorical values
    # --------------------------------------------------------

    if "gender" in behavior.columns:

        behavior["gender"] = (
            behavior["gender"]
            .str.title()
        )

    if "country" in behavior.columns:

        behavior["country"] = (
            behavior["country"]
            .str.strip()
        )

    if "subscription_type" in behavior.columns:

        behavior["subscription_type"] = (
            behavior["subscription_type"]
            .str.title()
        )

    if "payment_method" in behavior.columns:

        behavior["payment_method"] = (
            behavior["payment_method"]
            .str.title()
        )

    if "primary_device" in behavior.columns:

        behavior["primary_device"] = (
            behavior["primary_device"]
            .str.title()
        )

    if "favorite_genre" in behavior.columns:

        behavior["favorite_genre"] = (
            behavior["favorite_genre"]
            .str.title()
        )

    # --------------------------------------------------------
    # Standardize churn values
    # --------------------------------------------------------

    if "churned" in behavior.columns:

        behavior["churned"] = (
            behavior["churned"]
            .str.title()
        )

        print("\nChurn values:")
        print(
            behavior["churned"]
            .value_counts(dropna=False)
        )

        valid_churn_values = [
            "Yes",
            "No"
        ]

        invalid_churn = ~behavior[
            "churned"
        ].isin(valid_churn_values)

        invalid_churn_count = invalid_churn.sum()

        print(
            f"Invalid churn values: "
            f"{invalid_churn_count:,}"
        )

        behavior.loc[
            invalid_churn,
            "churned"
        ] = pd.NA

        # Numeric version useful in Tableau
        behavior["churn_flag"] = (
            behavior["churned"]
            .map({
                "Yes": 1,
                "No": 0
            })
            .astype("Int64")
        )

    # --------------------------------------------------------
    # Validate numeric columns
    # --------------------------------------------------------

    numeric_columns = [
        "age",
        "account_age_months",
        "monthly_fee",
        "devices_used",
        "avg_watch_time_minutes",
        "watch_sessions_per_week",
        "binge_watch_sessions",
        "completion_rate",
        "rating_given",
        "content_interactions",
        "recommendation_click_rate",
        "days_since_last_login"
    ]

    for column in numeric_columns:

        if column in behavior.columns:

            behavior[column] = pd.to_numeric(
                behavior[column],
                errors="coerce"
            )

    # --------------------------------------------------------
    # Validate percentage/rate columns
    # --------------------------------------------------------

    rate_columns = [
        "completion_rate",
        "recommendation_click_rate"
    ]

    for column in rate_columns:

        if column in behavior.columns:

            invalid = (
                behavior[column].notna()
                & ~behavior[column].between(0, 100)
            )

            print(
                f"Invalid {column} values: "
                f"{invalid.sum():,}"
            )

            behavior.loc[
                invalid,
                column
            ] = pd.NA

    # --------------------------------------------------------
    # Validate ratings
    # --------------------------------------------------------

    if "rating_given" in behavior.columns:

        invalid_rating = (
            behavior["rating_given"].notna()
            & ~behavior["rating_given"].between(1, 5)
        )

        print(
            f"Invalid rating_given values: "
            f"{invalid_rating.sum():,}"
        )

        behavior.loc[
            invalid_rating,
            "rating_given"
        ] = pd.NA

    # --------------------------------------------------------
    # Validate values that should not be negative
    # --------------------------------------------------------

    non_negative_columns = [
        "account_age_months",
        "monthly_fee",
        "devices_used",
        "avg_watch_time_minutes",
        "watch_sessions_per_week",
        "binge_watch_sessions",
        "content_interactions",
        "days_since_last_login"
    ]

    for column in non_negative_columns:

        if column in behavior.columns:

            negative_values = (
                behavior[column].notna()
                & (behavior[column] < 0)
            )

            print(
                f"Negative {column} values: "
                f"{negative_values.sum():,}"
            )

            behavior.loc[
                negative_values,
                column
            ] = pd.NA

    # --------------------------------------------------------
    # Age validation
    # --------------------------------------------------------

    if "age" in behavior.columns:

        invalid_age = (
            behavior["age"].notna()
            & ~behavior["age"].between(13, 100)
        )

        print(
            f"Invalid age values: "
            f"{invalid_age.sum():,}"
        )

        behavior.loc[
            invalid_age,
            "age"
        ] = pd.NA

    # --------------------------------------------------------
    # Create age groups for Tableau
    # --------------------------------------------------------

    if "age" in behavior.columns:

        behavior["age_group"] = pd.cut(
            behavior["age"],
            bins=[
                12,
                17,
                24,
                34,
                44,
                54,
                64,
                100
            ],
            labels=[
                "13-17",
                "18-24",
                "25-34",
                "35-44",
                "45-54",
                "55-64",
                "65+"
            ]
        )

    # --------------------------------------------------------
    # Create engagement segments
    # --------------------------------------------------------

    if "avg_watch_time_minutes" in behavior.columns:

        behavior["watch_time_segment"] = pd.cut(
            behavior["avg_watch_time_minutes"],
            bins=[
                -1,
                60,
                120,
                180,
                float("inf")
            ],
            labels=[
                "Low",
                "Moderate",
                "High",
                "Very High"
            ]
        )

    # --------------------------------------------------------
    # Create login-risk segments
    # --------------------------------------------------------

    if "days_since_last_login" in behavior.columns:

        behavior["login_activity_segment"] = pd.cut(
            behavior["days_since_last_login"],
            bins=[
                -1,
                7,
                14,
                30,
                float("inf")
            ],
            labels=[
                "Active",
                "Recently Active",
                "At Risk",
                "Inactive"
            ]
        )

    # --------------------------------------------------------
    # Monthly revenue estimate
    # --------------------------------------------------------

    if "monthly_fee" in behavior.columns:

        behavior["monthly_revenue"] = (
            behavior["monthly_fee"]
        )

    # --------------------------------------------------------
    # Annualized revenue estimate
    # --------------------------------------------------------

    if "monthly_fee" in behavior.columns:

        behavior["annualized_revenue"] = (
            behavior["monthly_fee"] * 12
        )

    # --------------------------------------------------------
    # Revenue-at-risk field
    # --------------------------------------------------------

    if (
        "monthly_fee" in behavior.columns
        and "churn_flag" in behavior.columns
    ):

        behavior["monthly_revenue_at_risk"] = (
            behavior["monthly_fee"]
            * behavior["churn_flag"]
        )

    # --------------------------------------------------------
    # Final behavior summary
    # --------------------------------------------------------

    removed_rows = original_rows - len(behavior)

    print("\nUSER BEHAVIOR CLEANING SUMMARY")
    print("-" * 80)

    print(f"Original rows: {original_rows:,}")
    print(f"Final rows:    {len(behavior):,}")
    print(f"Rows removed:  {removed_rows:,}")

    print("\nMissing values after cleaning:")
    print(behavior.isna().sum())

    return behavior


# ------------------------------------------------------------
# 5. SAVE CLEAN DATASETS
# ------------------------------------------------------------

def save_datasets(reviews, behavior):

    print_section("SAVING TABLEAU-READY DATA")

    # Create processed folder if it does not exist
    PROCESSED.mkdir(
        parents=True,
        exist_ok=True
    )

    reviews.to_csv(
        CLEAN_REVIEWS_FILE,
        index=False
    )

    behavior.to_csv(
        CLEAN_BEHAVIOR_FILE,
        index=False
    )

    print("\nClean reviews saved to:")
    print(CLEAN_REVIEWS_FILE)

    print("\nClean user behavior saved to:")
    print(CLEAN_BEHAVIOR_FILE)


# ------------------------------------------------------------
# 6. FINAL QUALITY CHECK
# ------------------------------------------------------------

def final_quality_check(reviews, behavior):

    print_section("FINAL DATA QUALITY CHECK")

    print("\nNETFLIX REVIEWS")
    print("-" * 80)

    print(
        f"Rows: {len(reviews):,}"
    )

    print(
        f"Columns: {reviews.shape[1]}"
    )

    print(
        f"Duplicate rows: "
        f"{reviews.duplicated().sum():,}"
    )

    if "score" in reviews.columns:

        print(
            f"Average review score: "
            f"{reviews['score'].mean():.2f}"
        )

    print("\nNETFLIX USER BEHAVIOR")
    print("-" * 80)

    print(
        f"Rows: {len(behavior):,}"
    )

    print(
        f"Columns: {behavior.shape[1]}"
    )

    print(
        f"Duplicate rows: "
        f"{behavior.duplicated().sum():,}"
    )

    if "churn_flag" in behavior.columns:

        churn_rate = (
            behavior["churn_flag"].mean()
            * 100
        )

        print(
            f"Churn rate: "
            f"{churn_rate:.2f}%"
        )

    if "avg_watch_time_minutes" in behavior.columns:

        print(
            f"Average watch time: "
            f"{behavior['avg_watch_time_minutes'].mean():.2f} minutes"
        )

    if "completion_rate" in behavior.columns:

        print(
            f"Average completion rate: "
            f"{behavior['completion_rate'].mean():.2f}%"
        )

    if "rating_given" in behavior.columns:

        print(
            f"Average rating: "
            f"{behavior['rating_given'].mean():.2f}"
        )

    if "monthly_fee" in behavior.columns:

        print(
            f"Estimated monthly revenue: "
            f"${behavior['monthly_fee'].sum():,.2f}"
        )

    if "monthly_revenue_at_risk" in behavior.columns:

        print(
            f"Monthly revenue associated with churned users: "
            f"${behavior['monthly_revenue_at_risk'].sum():,.2f}"
        )


# ------------------------------------------------------------
# 7. MAIN PROGRAM
# ------------------------------------------------------------

def main():

    print_section(
        "NETFLIX VIEWER ANALYTICS - DATA CLEANING"
    )

    print("\nProject folder:")
    print(ROOT)

    # Check source files
    if not REVIEWS_FILE.exists():

        print("\nERROR:")
        print(
            f"Could not find {REVIEWS_FILE}"
        )

        return

    if not BEHAVIOR_FILE.exists():

        print("\nERROR:")
        print(
            f"Could not find {BEHAVIOR_FILE}"
        )

        return

    # Clean datasets
    reviews = clean_reviews()

    behavior = clean_behavior()

    # Save outputs
    save_datasets(
        reviews,
        behavior
    )

    # Quality check
    final_quality_check(
        reviews,
        behavior
    )

    print_section(
        "DATA CLEANING COMPLETE"
    )

    print(
        "\nYour original raw CSV files were NOT modified."
    )

    print(
        "\nTableau-ready datasets are now located in:"
    )

    print(PROCESSED)

    print(
        "\nNext step: KPI and business analysis."
    )


# ------------------------------------------------------------
# 8. RUN PROGRAM
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
