# Data sources

| File | Source | License |
|---|---|---|
| netflix_user_behavior_dataset.csv | [Netflix User Watching Behavior Dataset](https://www.kaggle.com/datasets/rhythmghai/netflix-user-watching-behavior-dataset) (Kaggle, rhythmghai) | Apache 2.0. **Synthetic data**, not real Netflix users. |
| netflix_reviews.csv (not included) | [Netflix Reviews, Play Store](https://www.kaggle.com/datasets/ashishkumarak/netflix-reviews-playstore-daily-updated) (Kaggle, ashishkumarak) | CC BY-NC-SA 4.0 |

## Reproducing the review analysis

The raw reviews file is not stored in this repository because of its
non-commercial, share-alike license. To reproduce the analysis, download
`netflix_reviews.csv` from the Kaggle page above and place it in this folder.
My analysis used a snapshot with reviews through October 6, 2026. The dataset
is refreshed daily, so newer downloads will differ.

## Files in this repository derived from the reviews

All derived files contain no review text and no user names.

| File | What it is |
|---|---|
| processed/reviews/review_monthly_summary.csv | Monthly review count and average rating, built by `python/03_review_summary.py` |
| processed/reviews/review_complaint_themes.csv | Theme shares with 95% Wilson intervals, built from the sample labels |
| processed/reviews/review_sample_labels.csv | 300 sampled 1-2 star reviews: review ID, score, month, theme (no text) |
| processed/tableau/churn_whatif_inputs.csv | Three summary numbers from the synthetic user-behavior data, used as defaults in the what-if model |
