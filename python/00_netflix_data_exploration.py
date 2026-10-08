# ============================================================
# Netflix Viewer Analytics
# 00_netflix_data_exploration.py
#
# Purpose:
# Explore the Netflix datasets before performing analysis
# and building the Tableau dashboard.
# ============================================================

from pathlib import Path
import pandas as pd


# ------------------------------------------------------------
# 1. PROJECT PATHS
# ------------------------------------------------------------

# Finds the main Netflix-Viewer-Analytics project folder
ROOT = Path(__file__).resolve().parents[1]

# Data folder
DATA = ROOT / "data"

# Dataset locations
REVIEWS_FILE = DATA / "netflix_reviews.csv"
BEHAVIOR_FILE = DATA / "netflix_user_behavior_dataset.csv"


# ------------------------------------------------------------
# 2. DISPLAY SETTINGS
# ------------------------------------------------------------

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", 50)


# ------------------------------------------------------------
# 3. HELPER FUNCTION
# ------------------------------------------------------------

def explore_dataset(df, dataset_name):
    """
    Prints important information about a dataset so we can
    understand its structure before performing analysis.
    """

    print("\n")
    print("=" * 80)
    print(f"DATASET: {dataset_name}")
    print("=" * 80)

    # Dataset dimensions
    print("\n1. DATASET SIZE")
    print("-" * 80)
    print(f"Rows:    {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]:,}")

    # Column names
    print("\n2. COLUMN NAMES")
    print("-" * 80)

    for number, column in enumerate(df.columns, start=1):
        print(f"{number}. {column}")

    # Data types
    print("\n3. DATA TYPES")
    print("-" * 80)
    print(df.dtypes)

    # Missing values
    print("\n4. MISSING VALUES")
    print("-" * 80)

    missing = df.isnull().sum()
    missing_percent = (missing / len(df) * 100).round(2)

    missing_report = pd.DataFrame({
        "Missing Values": missing,
        "Missing Percent": missing_percent
    })

    print(missing_report)

    # Duplicate records
    print("\n5. DUPLICATE ROWS")
    print("-" * 80)

    duplicate_count = df.duplicated().sum()

    print(f"Duplicate rows: {duplicate_count:,}")

    if len(df) > 0:
        duplicate_percent = (duplicate_count / len(df)) * 100
        print(f"Duplicate percentage: {duplicate_percent:.2f}%")

    # Sample records
    print("\n6. FIRST 5 ROWS")
    print("-" * 80)
    print(df.head())

    # Numerical statistics
    print("\n7. NUMERICAL SUMMARY")
    print("-" * 80)

    numeric_columns = df.select_dtypes(include="number")

    if not numeric_columns.empty:
        print(numeric_columns.describe().T)
    else:
        print("No numeric columns found.")

    # Text/category summary
    print("\n8. TEXT / CATEGORY SUMMARY")
    print("-" * 80)

    text_columns = df.select_dtypes(include=["object", "string"])

    if not text_columns.empty:

        for column in text_columns.columns:

            unique_count = df[column].nunique(dropna=True)

            print(f"\nColumn: {column}")
            print(f"Unique values: {unique_count:,}")

            # Only show most common values for columns that
            # don't contain extremely high-cardinality data.
            if unique_count <= 100:

                print("Most common values:")

                print(
                    df[column]
                    .value_counts(dropna=False)
                    .head(10)
                )

            else:
                print("High-cardinality column - top values not displayed.")

    else:
        print("No text/category columns found.")

    print("\n")
    print("=" * 80)
    print(f"END OF {dataset_name}")
    print("=" * 80)


# ------------------------------------------------------------
# 4. MAIN PROGRAM
# ------------------------------------------------------------

def main():

    print("\nNETFLIX VIEWER ANALYTICS")
    print("DATA EXPLORATION REPORT")

    print("\nProject folder:")
    print(ROOT)

    print("\nData folder:")
    print(DATA)

    # --------------------------------------------------------
    # Check that files exist
    # --------------------------------------------------------

    if not REVIEWS_FILE.exists():
        print("\nERROR:")
        print(f"Could not find: {REVIEWS_FILE}")
        return

    if not BEHAVIOR_FILE.exists():
        print("\nERROR:")
        print(f"Could not find: {BEHAVIOR_FILE}")
        return

    print("\nBoth datasets found successfully.")

    # --------------------------------------------------------
    # Load datasets
    # --------------------------------------------------------

    print("\nLoading Netflix reviews dataset...")

    reviews = pd.read_csv(
        REVIEWS_FILE,
        low_memory=False
    )

    print("Reviews dataset loaded.")

    print("\nLoading Netflix user behavior dataset...")

    behavior = pd.read_csv(
        BEHAVIOR_FILE,
        low_memory=False
    )

    print("User behavior dataset loaded.")

    # --------------------------------------------------------
    # Explore datasets
    # --------------------------------------------------------

    explore_dataset(
        reviews,
        "Netflix Reviews"
    )

    explore_dataset(
        behavior,
        "Netflix User Behavior"
    )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print("\n")
    print("=" * 80)
    print("EXPLORATION COMPLETE")
    print("=" * 80)

    print("\nNetflix Reviews:")
    print(f"{reviews.shape[0]:,} rows x {reviews.shape[1]:,} columns")

    print("\nNetflix User Behavior:")
    print(f"{behavior.shape[0]:,} rows x {behavior.shape[1]:,} columns")

    print("\nNext step:")
    print("Review the columns and determine which KPIs can be used")
    print("for the Netflix Tableau analytics dashboard.")


# ------------------------------------------------------------
# 5. RUN PROGRAM
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
