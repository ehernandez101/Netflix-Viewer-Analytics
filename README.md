# Netflix App Reviews: What Users Say and What Churn Is Worth

Independent portfolio project. Not affiliated with or endorsed by Netflix.

**Live dashboard:** [Tableau Public](https://public.tableau.com/app/profile/enrique.hernandez2674/viz/Netflix_Reviews_Dashboard_final/Dashboard)

## Business question

What are Netflix mobile app users complaining about, has their satisfaction changed over time, and what would a small reduction in churn be worth?

## Headline findings

1. **Playback and app bugs are the top complaint**, at 28.3% of 1-2 star reviews in a 300-review sample. Catalog/content (16.7%) and price/billing (15.3%) follow. The middle-ranked themes are close to tied, so only the top position should be read as firm.
2. **The average app rating jumped twice, and the data does not say why.** It rose from about 3.1 to 4.3 between June and October 2026, after an earlier jump in 2024. Both are flagged on the dashboard as unexplained. Possible causes (app releases, review-prompt changes, review removals) cannot be tested with this dataset.
3. **What-if model (illustrative only):** cutting churn by 1 point on 50,000 subscribers at $12.32 a month, retained for 12 months, is worth about $73,920 a year and keeps 500 subscribers. The inputs come from a synthetic dataset whose churn labels show no relationship to behavior, so this is a template for the calculation and not a finding about Netflix.

## What I did

I built this project to explore what Netflix mobile app users are saying about their experience and how customer retention could affect revenue.

I focused on three questions: What issues appear most often in negative reviews? How have app ratings changed over time? And what would a small improvement in subscriber retention be worth?

I used SQL and Python to prepare and explore the data, then Tableau to present the findings. While analyzing the reviews, I made several decisions to keep the results meaningful and transparent:

* Excluded months with fewer than 300 reviews to avoid presenting unstable rating trends.
* Classified negative reviews into complaint themes with an LLM, then manually checked 30 of them and agreed with 24 (80%).
* Flagged unexplained rating increases rather than assuming what caused them.
* Kept the churn scenario separate from the review findings because the subscriber dataset is synthetic.
* Included source information and licensing restrictions to document how the data can be used and shared.

With access to actual Netflix subscriber data, I would expand the analysis by comparing customer complaints with cancellations, subscription plans, app versions, and engagement patterns. This would help determine whether specific app issues are associated with subscriber churn and which improvements might have the greatest business impact.

## Data

| Data | Source | License | Used for |
|---|---|---|---|
| Netflix Google Play reviews | Kaggle (ashishkumarak) | CC BY-NC-SA 4.0 | Rating trend, complaint themes |
| Netflix user behavior (synthetic) | Kaggle (rhythmghai) | Apache 2.0 | Default inputs for the what-if model |

The raw reviews are **not** republished here because of the license. Only aggregated summary tables and the theme labels for the 300-review sample are included. See `data/README.md` for the full source list and how to download the reviews yourself.

## Method

- **Rating trend:** monthly average score. Months with fewer than 300 reviews are excluded from the chart because their averages are too noisy to read.
- **Complaint themes:** a random sample of 300 English-language 1-2 star reviews (Jan 2025 to Jun 2026), each assigned one primary theme from a fixed list of nine. Validation details are in `docs/labeling_validation.md`. Shares carry a Wilson 95% confidence interval of roughly +/-4 to 6 points.
- **What-if model:** `subscribers kept = subscribers x churn reduction (points) / 100`, and `annual revenue saved = subscribers kept x monthly fee x months retained`. All four inputs are adjustable on the dashboard.

## Limitations

- The theme sample is 300 reviews and the labels were validated on a 30-review check, so small differences between themes are not meaningful.
- Google Play reviews are not a random sample of all Netflix users.
- The cause of the two rating jumps is unknown.
- The churn inputs are synthetic.

## Repo contents

This repository is organized into the following folders:

* `python/` – Python scripts for data exploration, cleaning, and KPI calculations, plus `03_review_summary.py`, which builds the review summary tables.
* `data/` – Dataset source information, licensing details, and aggregated summary tables.
* `dashboard/` – Tableau dashboard file (`.twbx`, aggregated data only).
* `sql/` – SQL queries for the monthly rating summary and the complaint theme shares.
* `docs/` – Labeling method and validation notes.

The interactive dashboard is available on Tableau Public. Raw Google Play reviews are not included in the repository due to licensing restrictions. Instructions for obtaining the original data are provided in `data/README.md`.

## Reproducing the review tables

1. Download `netflix_reviews.csv` from Kaggle (see `data/README.md`) into `data/`.
2. Run `python python/03_review_summary.py --reviews data/netflix_reviews.csv`. This rewrites the files in `data/processed/reviews/`. A newer download will give different numbers, because the dataset is refreshed daily.
3. To run the SQL, load the reviews into a table `reviews(review_id, score, review_date)` (Kaggle columns `reviewId`, `score`, `at`) and `data/processed/reviews/review_sample_labels.csv` into `review_sample_labels(review_id, score, review_month, theme)`.

## Disclaimer

Netflix is a trademark of Netflix, Inc. This project is independent and uses only public data.
