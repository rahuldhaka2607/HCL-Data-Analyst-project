-- ====================================================================
-- Project No. 6: Loan Default Analysis and Risk Dashboard
-- File: sql/oracle/oracle_queries.sql (Oracle-Compatible Analytics)
-- ====================================================================

-- 1. Default Rate by Grade
SELECT 
    g.grade_id AS loan_grade,
    g.grade_name,
    COUNT(f.loan_id) AS total_loans,
    SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END) AS eligible_closed_loans,
    SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) AS defaulted_loans,
    ROUND(
        100.0 * SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) / 
        NULLIF(SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END), 0), 
        2
    ) AS default_rate_pct,
    ROUND(AVG(f.interest_rate), 2) AS avg_interest_rate_pct,
    ROUND(AVG(f.loan_amount), 2) AS avg_loan_amount
FROM FACT_LOANS f
JOIN DIM_LOAN_GRADE g ON f.grade_id = g.grade_id
GROUP BY g.grade_id, g.grade_name
ORDER BY g.grade_id ASC;

-- 2. Monthly Trend with Oracle Window Functions
WITH MonthlyStats AS (
    SELECT 
        d.year_month,
        COUNT(f.loan_id) AS monthly_originations,
        ROUND(SUM(f.loan_amount), 2) AS total_originated_volume,
        SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END) AS closed_loans,
        SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) AS monthly_defaults
    FROM FACT_LOANS f
    JOIN DIM_DATE d ON f.date_id = d.date_id
    GROUP BY d.year_month
)
SELECT 
    year_month,
    monthly_originations,
    total_originated_volume,
    closed_loans,
    monthly_defaults,
    ROUND(100.0 * monthly_defaults / NULLIF(closed_loans, 0), 2) AS monthly_default_rate_pct,
    LAG(monthly_originations, 1) OVER (ORDER BY year_month) AS prev_month_originations,
    ROUND(
        100.0 * (monthly_originations - LAG(monthly_originations, 1) OVER (ORDER BY year_month)) / 
        NULLIF(LAG(monthly_originations, 1) OVER (ORDER BY year_month), 0),
        2
    ) AS mom_growth_pct
FROM MonthlyStats
ORDER BY year_month ASC;
