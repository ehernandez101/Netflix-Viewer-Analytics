"""
Netflix Viewer Analytics
03_review_summary.py

Purpose:
Build the two summary tables behind the review dashboard:
  1. review_monthly_summary.csv   - monthly review count and average rating
  2. review_complaint_themes.csv  - complaint theme shares with 95% Wilson intervals

Inputs:
  --reviews  Raw Google Play reviews CSV (download from Kaggle, see data/README.md).
             Not stored in this repository because of its license.
  --labels   data/processed/reviews/review_sample_labels.csv
             300 random English-language 1-2 star reviews with one primary theme
             each (assigned by an LLM, validated on a 30-review hand check).

Usage:
  python python/03_review_summary.py --reviews data/netflix_reviews.csv
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

Z = 1.96  # 95% confidence


def wilson_interval(k, n, z=Z):
    """95% Wilson score interval for a proportion k/n, returned as percentages."""
    p = k / n
    centre = (p + z**2 / (2 * n)) / (1 + z**2 / n)
    half = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / (1 + z**2 / n)
    return 100 * (centre - half), 100 * (centre + half)


def monthly_summary(reviews_path):
    # Read only what is needed. Review text and user names are never loaded.
    df = pd.read_csv(reviews_path, usecols=["score", "at"], parse_dates=["at"])
    df["month"] = df["at"].dt.to_period("M").dt.to_timestamp()

    out = (
        df.groupby("month")
        .agg(
            reviews=("score", "size"),
            avg_score=("score", "mean"),
            pct_1star=("score", lambda s: 100 * (s == 1).mean()),
            pct_5star=("score", lambda s: 100 * (s == 5).mean()),
        )
        .reset_index()
    )
    out[["avg_score"]] = out[["avg_score"]].round(2)
    out[["pct_1star", "pct_5star"]] = out[["pct_1star", "pct_5star"]].round(1)

    # The last month is partial if the data stops before that month ends.
    last_date = df["at"].max()
    last_month = out["month"].max()
    month_end = last_month + pd.offsets.MonthEnd(0)
    out["partial_month"] = np.where(
        (out["month"] == last_month) & (last_date.normalize() < month_end), "Yes", "No"
    )
    out["month"] = out["month"].dt.strftime("%Y-%m-%d")
    return out


def theme_shares(labels_path):
    labels = pd.read_csv(labels_path)
    n = len(labels)
    counts = labels["theme"].value_counts().rename_axis("theme").reset_index(name="reviews")
    counts["share_pct"] = (100 * counts["reviews"] / n).round(1)
    bounds = counts["reviews"].apply(lambda k: wilson_interval(k, n))
    counts["ci_low_pct"] = bounds.apply(lambda b: b[0]).round(1)
    counts["ci_high_pct"] = bounds.apply(lambda b: b[1]).round(1)
    return counts.sort_values(["reviews", "theme"], ascending=[False, True])


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--reviews", required=True, type=Path)
    parser.add_argument("--labels", type=Path,
                        default=root / "data/processed/reviews/review_sample_labels.csv")
    parser.add_argument("--out", type=Path, default=root / "data/processed/reviews")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    monthly_summary(args.reviews).to_csv(args.out / "review_monthly_summary.csv", index=False)
    theme_shares(args.labels).to_csv(args.out / "review_complaint_themes.csv", index=False)
    print(f"Wrote summary tables to {args.out}")


if __name__ == "__main__":
    main()
