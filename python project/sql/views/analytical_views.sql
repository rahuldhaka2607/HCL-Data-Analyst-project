-- ====================================================================
-- Project No. 6: Loan Default Analysis and Risk Dashboard
-- File: sql/views/analytical_views.sql
-- Description: Pre-aggregated database views for BI reporting
-- ====================================================================

-- 1. View: Executive Portfolio Overview
CREATE VIEW IF NOT EXISTS V_PORTFOLIO_OVERVIEW AS
SELECT 
    COUNT(f.loan_id) AS total_loans,
    COUNT(DISTINCT f.customer_id) AS total_borrowers,
    ROUND(SUM(f.loan_amount), 2) AS total_loan_volume,
    ROUND(AVG(f.loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(f.interest_rate), 2) AS avg_interest_rate,
    ROUND(SUM(f.outstanding_balance), 2) AS total_outstanding,
    SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END) AS eligible_closed_loans,
    SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) AS defaulted_loans,
    ROUND(
        100.0 * SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) / 
        NULLIF(SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END), 0), 
        2
    ) AS default_rate_pct
FROM FACT_LOANS f;

-- 2. View: Comprehensive Loan Risk Details
CREATE VIEW IF NOT EXISTS V_LOAN_RISK_DETAILS AS
SELECT 
    f.loan_id,
    f.customer_id,
    c.age,
    c.gender,
    c.employment_type,
    c.annual_income,
    c.credit_score,
    c.home_ownership,
    c.existing_loans,
    f.date_id AS issue_date,
    d.year,
    d.month_name,
    d.quarter,
    d.year_month,
    p.purpose_name AS loan_purpose,
    g.grade_id AS loan_grade,
    g.base_risk_level,
    f.loan_amount,
    f.loan_term_months,
    f.interest_rate,
    f.debt_to_income_ratio,
    f.loan_status,
    f.total_payment,
    f.outstanding_balance,
    f.default_flag,
    CASE 
        WHEN c.credit_score < 580 OR f.debt_to_income_ratio > 45.0 THEN 'Critical Risk'
        WHEN c.credit_score < 660 OR f.debt_to_income_ratio > 35.0 THEN 'High Risk'
        WHEN c.credit_score < 720 OR f.debt_to_income_ratio > 20.0 THEN 'Moderate Risk'
        ELSE 'Low Risk'
    END AS risk_category,
    CASE 
        WHEN c.annual_income < 35000 THEN '< $35,000'
        WHEN c.annual_income >= 35000 AND c.annual_income < 60000 THEN '$35,000 - $60,000'
        WHEN c.annual_income >= 60000 AND c.annual_income < 100000 THEN '$60,000 - $100,000'
        ELSE '> $100,000'
    END AS income_band
FROM FACT_LOANS f
JOIN DIM_CUSTOMER c ON f.customer_id = c.customer_id
JOIN DIM_DATE d ON f.date_id = d.date_id
JOIN DIM_LOAN_PURPOSE p ON f.purpose_id = p.purpose_id
JOIN DIM_LOAN_GRADE g ON f.grade_id = g.grade_id;
