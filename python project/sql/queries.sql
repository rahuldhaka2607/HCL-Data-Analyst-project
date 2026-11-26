-- ====================================================================
-- Project No. 6: Loan Default Analysis and Risk Dashboard
-- File: sql/queries.sql (SQLite Analytical Queries)
-- Description: 7 Core Business Intelligence & Risk Analysis Queries
-- ====================================================================

-- --------------------------------------------------------------------
-- QUERY 1: Default Rate by Loan Grade (Business Question 1)
-- --------------------------------------------------------------------
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

-- --------------------------------------------------------------------
-- QUERY 2: Default Rate by Income Band (Business Question 2)
-- --------------------------------------------------------------------
SELECT 
    CASE 
        WHEN c.annual_income < 35000 THEN '< $35,000'
        WHEN c.annual_income >= 35000 AND c.annual_income < 60000 THEN '$35,000 - $60,000'
        WHEN c.annual_income >= 60000 AND c.annual_income < 100000 THEN '$60,000 - $100,000'
        ELSE '> $100,000'
    END AS income_band,
    COUNT(f.loan_id) AS total_loans,
    SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END) AS eligible_closed_loans,
    SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) AS defaulted_loans,
    ROUND(
        100.0 * SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) / 
        NULLIF(SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END), 0), 
        2
    ) AS default_rate_pct,
    ROUND(AVG(c.annual_income), 2) AS avg_income_in_band,
    ROUND(AVG(f.debt_to_income_ratio), 2) AS avg_dti_ratio
FROM FACT_LOANS f
JOIN DIM_CUSTOMER c ON f.customer_id = c.customer_id
GROUP BY income_band
ORDER BY 
    CASE income_band
        WHEN '< $35,000' THEN 1
        WHEN '$35,000 - $60,000' THEN 2
        WHEN '$60,000 - $100,000' THEN 3
        ELSE 4
    END;

-- --------------------------------------------------------------------
-- QUERY 3: Default Rate by Loan Purpose (Business Question 3)
-- --------------------------------------------------------------------
SELECT 
    p.purpose_name AS loan_purpose,
    COUNT(f.loan_id) AS total_loans,
    SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END) AS eligible_closed_loans,
    SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) AS defaulted_loans,
    ROUND(
        100.0 * SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) / 
        NULLIF(SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END), 0), 
        2
    ) AS default_rate_pct,
    ROUND(SUM(f.loan_amount), 2) AS total_volume_disbursed,
    ROUND(AVG(f.interest_rate), 2) AS avg_interest_rate
FROM FACT_LOANS f
JOIN DIM_LOAN_PURPOSE p ON f.purpose_id = p.purpose_id
GROUP BY p.purpose_name
ORDER BY default_rate_pct DESC;

-- --------------------------------------------------------------------
-- QUERY 4: Monthly Default Trends with LAG Window Function (Business Question 5)
-- --------------------------------------------------------------------
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
    ) AS mom_origination_growth_pct
FROM MonthlyStats
ORDER BY year_month ASC;

-- --------------------------------------------------------------------
-- QUERY 5: 4-Tier Risk Category Distribution (Business Question 4)
-- --------------------------------------------------------------------
SELECT 
    CASE 
        WHEN c.credit_score < 580 OR f.debt_to_income_ratio > 45.0 THEN 'Critical Risk'
        WHEN c.credit_score < 660 OR f.debt_to_income_ratio > 35.0 THEN 'High Risk'
        WHEN c.credit_score < 720 OR f.debt_to_income_ratio > 20.0 THEN 'Moderate Risk'
        ELSE 'Low Risk'
    END AS risk_category,
    COUNT(f.loan_id) AS total_borrowers,
    ROUND(SUM(f.loan_amount), 2) AS total_capital_exposure,
    ROUND(SUM(f.outstanding_balance), 2) AS current_outstanding_exposure,
    SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END) AS eligible_closed_loans,
    SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) AS defaulted_loans,
    ROUND(
        100.0 * SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) / 
        NULLIF(SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END), 0), 
        2
    ) AS default_rate_pct
FROM FACT_LOANS f
JOIN DIM_CUSTOMER c ON f.customer_id = c.customer_id
GROUP BY risk_category
ORDER BY 
    CASE risk_category
        WHEN 'Low Risk' THEN 1
        WHEN 'Moderate Risk' THEN 2
        WHEN 'High Risk' THEN 3
        ELSE 4
    END;

-- --------------------------------------------------------------------
-- QUERY 6: Executive Portfolio Summary & Health KPIs
-- --------------------------------------------------------------------
SELECT 
    COUNT(f.loan_id) AS total_loans,
    COUNT(DISTINCT f.customer_id) AS total_unique_borrowers,
    ROUND(SUM(f.loan_amount), 2) AS total_portfolio_volume,
    ROUND(AVG(f.loan_amount), 2) AS avg_loan_size,
    ROUND(AVG(f.interest_rate), 2) AS avg_portfolio_interest_rate,
    ROUND(SUM(f.total_payment), 2) AS total_cumulative_repayments,
    ROUND(SUM(f.outstanding_balance), 2) AS total_outstanding_balance,
    SUM(CASE WHEN f.loan_status = 'Current' THEN 1 ELSE 0 END) AS active_current_loans,
    SUM(CASE WHEN f.loan_status = 'In Grace Period' THEN 1 ELSE 0 END) AS active_grace_period_loans,
    SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END) AS total_closed_eligible_loans,
    SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) AS total_defaulted_loans,
    ROUND(
        100.0 * SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) / 
        NULLIF(SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END), 0), 
        2
    ) AS overall_default_rate_pct
FROM FACT_LOANS f;

-- --------------------------------------------------------------------
-- QUERY 7: Deep Comparison: High-Risk vs. Low-Risk Cohort Profile
-- --------------------------------------------------------------------
WITH RiskCohort AS (
    SELECT 
        f.loan_id,
        f.loan_amount,
        f.interest_rate,
        f.debt_to_income_ratio,
        f.loan_status,
        c.credit_score,
        c.annual_income,
        c.existing_loans,
        c.home_ownership,
        CASE 
            WHEN c.credit_score < 580 OR f.debt_to_income_ratio > 45.0 THEN 'High & Critical Risk'
            WHEN c.credit_score < 660 OR f.debt_to_income_ratio > 35.0 THEN 'High & Critical Risk'
            ELSE 'Low & Moderate Risk'
        END AS risk_cohort
    FROM FACT_LOANS f
    JOIN DIM_CUSTOMER c ON f.customer_id = c.customer_id
)
SELECT 
    risk_cohort,
    COUNT(loan_id) AS loan_count,
    ROUND(AVG(credit_score), 1) AS avg_credit_score,
    ROUND(AVG(annual_income), 2) AS avg_annual_income,
    ROUND(AVG(debt_to_income_ratio), 2) AS avg_dti,
    ROUND(AVG(interest_rate), 2) AS avg_interest_rate_charged,
    ROUND(AVG(existing_loans), 1) AS avg_existing_credit_lines,
    SUM(CASE WHEN loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END) AS eligible_loans,
    SUM(CASE WHEN loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) AS default_count,
    ROUND(
        100.0 * SUM(CASE WHEN loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) / 
        NULLIF(SUM(CASE WHEN loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END), 0), 
        2
    ) AS default_rate_pct
FROM RiskCohort
GROUP BY risk_cohort;
