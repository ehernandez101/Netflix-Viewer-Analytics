-- 02_complaint_theme_shares.sql
-- Question: what share of 1-2 star reviews does each complaint theme account for?
--
-- Input table : review_sample_labels(review_id, score, review_month, theme)
--               300 random English-language 1-2 star reviews (Jan 2025 - Jun 2026),
--               each with one primary theme assigned by an LLM and validated
--               on a 30-review hand check (24 of 30 agreed).
-- Output      : one row per theme, largest first.
--
-- The window function SUM(COUNT(*)) OVER () gives the sample total (300)
-- without a second query, so each share is count / total.
--
-- Dialect: standard SQL; runs unchanged in SQLite and Oracle.

SELECT
    theme,
    COUNT(*)                                                    AS reviews,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)          AS share_pct
FROM review_sample_labels
GROUP BY theme
ORDER BY reviews DESC, theme;
