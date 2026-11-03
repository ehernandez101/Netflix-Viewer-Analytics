-- 01_monthly_rating_summary.sql
-- Question: how has the average app rating changed month by month?
--
-- Input table : reviews(review_id, score, review_date)   one row per Google Play review
-- Output      : one row per month with at least 300 reviews
--
-- Why HAVING COUNT(*) >= 300: months with only a handful of reviews (8-23 in
-- the data) produce averages that swing wildly and show fake dips on the chart.
--
-- Dialect: written for SQLite (used to verify the numbers).
-- Oracle equivalents: TO_CHAR(review_date, 'YYYY-MM') for the month, and
-- ROUND(AVG(score), 2) works unchanged.

SELECT
    SUBSTR(review_date, 1, 7)                                   AS review_month,
    COUNT(*)                                                    AS reviews,
    ROUND(AVG(score), 2)                                        AS avg_score,
    ROUND(100.0 * SUM(CASE WHEN score = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_1star,
    ROUND(100.0 * SUM(CASE WHEN score = 5 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_5star
FROM reviews
GROUP BY SUBSTR(review_date, 1, 7)
HAVING COUNT(*) >= 300
ORDER BY review_month;
