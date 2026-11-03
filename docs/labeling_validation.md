# Complaint theme labeling and validation

## Sample
- 300 reviews drawn at random from English-language 1-2 star reviews written between Jan 2025 and Jun 2026.
- Each review has **one primary theme**, the main thing the reviewer is complaining about. Reviews that mention several issues are labeled by the most prominent one.
- The sample and its labels are in `data/processed/reviews/review_sample_labels.csv` (review ID, score, month, theme). Review text is not included.

## Themes
Playback/bugs, Catalog/content, Price/billing, Login/account, App features/UX, Household/sharing (account sharing limits, device and location restrictions), Other/vague, Ads, Support.

## How labels were assigned
Labels were assigned with an LLM against the fixed theme list above, then checked by the author.

## Validation
- The author reviewed **30 random labels** and agreed with **24 (80%)**.
- With a sample of 30, the plausible range for the true agreement rate is roughly 63% to 90% (95% Wilson interval).
- The six disagreements were between neighboring themes (for example price vs. account sharing, vague vs. playback, login vs. price), not between unrelated ones.

## What this means for the results
- The top theme (Playback/bugs, 28.3%) is well ahead of the second (Catalog/content, 16.7%), so its rank should survive this much label noise.
- Catalog/content (16.7%), Price/billing (15.3%) and the themes just below them are close enough that their order should not be read as precise.
- Theme shares carry sampling error of about +/-4 to 6 points (see `review_complaint_themes.csv`).

## Not done
- No second human rater, so inter-rater agreement has not been measured.
- A larger hand-labeled sample would tighten the validation estimate.
