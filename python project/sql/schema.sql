-- ====================================================================
-- Project No. 6: Loan Default Analysis and Risk Dashboard
-- File: sql/schema.sql (SQLite DDL)
-- Target: SQLite 3.x Star Schema Warehouse
-- ====================================================================

PRAGMA foreign_keys = ON;

-- Drop tables in reverse dependency order
DROP TABLE IF EXISTS FACT_LOANS;
DROP TABLE IF EXISTS DIM_CUSTOMER;
DROP TABLE IF EXISTS DIM_DATE;
DROP TABLE IF EXISTS DIM_LOAN_PURPOSE;
DROP TABLE IF EXISTS DIM_LOAN_GRADE;

-- --------------------------------------------------------------------
-- 1. Dimension Table: Customer Profile
-- --------------------------------------------------------------------
CREATE TABLE DIM_CUSTOMER (
    customer_id      TEXT PRIMARY KEY,
    age              INTEGER NOT NULL CHECK(age BETWEEN 18 AND 100),
    gender           TEXT NOT NULL,
    employment_type  TEXT NOT NULL,
    annual_income    REAL NOT NULL CHECK(annual_income >= 0),
    credit_score     INTEGER NOT NULL CHECK(credit_score BETWEEN 300 AND 850),
    home_ownership   TEXT NOT NULL,
    existing_loans   INTEGER NOT NULL CHECK(existing_loans >= 0)
);

-- --------------------------------------------------------------------
-- 2. Dimension Table: Origination Calendar Date
-- --------------------------------------------------------------------
CREATE TABLE DIM_DATE (
    date_id          TEXT PRIMARY KEY,  -- Formatted YYYY-MM-DD
    full_date        TEXT NOT NULL,
    day              INTEGER NOT NULL,
    month            INTEGER NOT NULL,
    month_name       TEXT NOT NULL,
    quarter          TEXT NOT NULL,
    year             INTEGER NOT NULL,
    year_month       TEXT NOT NULL
);

-- --------------------------------------------------------------------
-- 3. Dimension Table: Loan Purpose Catalog
-- --------------------------------------------------------------------
CREATE TABLE DIM_LOAN_PURPOSE (
    purpose_id       INTEGER PRIMARY KEY,
    purpose_name     TEXT UNIQUE NOT NULL
);

-- --------------------------------------------------------------------
-- 4. Dimension Table: Credit Risk Grade Master
-- --------------------------------------------------------------------
CREATE TABLE DIM_LOAN_GRADE (
    grade_id         TEXT PRIMARY KEY,
    grade_name       TEXT NOT NULL,
    base_risk_level  TEXT NOT NULL
);

-- --------------------------------------------------------------------
-- 5. Fact Table: Loan Performance and Repayments
-- --------------------------------------------------------------------
CREATE TABLE FACT_LOANS (
    loan_id               TEXT PRIMARY KEY,
    customer_id           TEXT NOT NULL,
    date_id               TEXT NOT NULL,
    purpose_id            INTEGER NOT NULL,
    grade_id              TEXT NOT NULL,
    loan_amount           REAL NOT NULL CHECK(loan_amount > 0),
    loan_term_months      INTEGER NOT NULL CHECK(loan_term_months IN (36, 60)),
    interest_rate         REAL NOT NULL CHECK(interest_rate > 0),
    debt_to_income_ratio  REAL NOT NULL CHECK(debt_to_income_ratio >= 0),
    loan_status           TEXT NOT NULL,
    total_payment         REAL NOT NULL DEFAULT 0.0,
    outstanding_balance   REAL NOT NULL DEFAULT 0.0,
    default_flag          INTEGER NOT NULL CHECK(default_flag IN (0, 1)),
    
    FOREIGN KEY (customer_id) REFERENCES DIM_CUSTOMER(customer_id),
    FOREIGN KEY (date_id) REFERENCES DIM_DATE(date_id),
    FOREIGN KEY (purpose_id) REFERENCES DIM_LOAN_PURPOSE(purpose_id),
    FOREIGN KEY (grade_id) REFERENCES DIM_LOAN_GRADE(grade_id)
);

-- Create analytical indexes for high performance querying
CREATE INDEX idx_fact_grade ON FACT_LOANS(grade_id);
CREATE INDEX idx_fact_date ON FACT_LOANS(date_id);
CREATE INDEX idx_fact_purpose ON FACT_LOANS(purpose_id);
CREATE INDEX idx_fact_status ON FACT_LOANS(loan_status);
CREATE INDEX idx_fact_default ON FACT_LOANS(default_flag);
