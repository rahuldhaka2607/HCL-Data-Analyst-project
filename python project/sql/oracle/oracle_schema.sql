-- ====================================================================
-- Project No. 6: Loan Default Analysis and Risk Dashboard
-- File: sql/oracle/oracle_schema.sql (Oracle 19c/21c DDL)
-- Target: Oracle Enterprise Database Star Schema Warehouse
-- ====================================================================

-- Drop existing tables safely with cascade constraints
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE FACT_LOANS CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE DIM_CUSTOMER CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE DIM_DATE CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE DIM_LOAN_PURPOSE CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE DIM_LOAN_GRADE CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

-- --------------------------------------------------------------------
-- 1. Dimension Table: Customer Profile
-- --------------------------------------------------------------------
CREATE TABLE DIM_CUSTOMER (
    customer_id      VARCHAR2(20) PRIMARY KEY,
    age              NUMBER(3) NOT NULL CONSTRAINT chk_ora_age CHECK (age BETWEEN 18 AND 100),
    gender           VARCHAR2(10) NOT NULL,
    employment_type  VARCHAR2(25) NOT NULL,
    annual_income    NUMBER(12,2) NOT NULL CONSTRAINT chk_ora_inc CHECK (annual_income >= 0),
    credit_score     NUMBER(4) NOT NULL CONSTRAINT chk_ora_score CHECK (credit_score BETWEEN 300 AND 850),
    home_ownership   VARCHAR2(15) NOT NULL,
    existing_loans   NUMBER(2) NOT NULL CONSTRAINT chk_ora_loans CHECK (existing_loans >= 0)
);

-- --------------------------------------------------------------------
-- 2. Dimension Table: Calendar Origination Date
-- --------------------------------------------------------------------
CREATE TABLE DIM_DATE (
    date_id          VARCHAR2(10) PRIMARY KEY,
    full_date        DATE NOT NULL,
    day              NUMBER(2) NOT NULL,
    month            NUMBER(2) NOT NULL,
    month_name       VARCHAR2(15) NOT NULL,
    quarter          VARCHAR2(5) NOT NULL,
    year             NUMBER(4) NOT NULL,
    year_month       VARCHAR2(7) NOT NULL
);

-- --------------------------------------------------------------------
-- 3. Dimension Table: Loan Purpose Catalog
-- --------------------------------------------------------------------
CREATE TABLE DIM_LOAN_PURPOSE (
    purpose_id       NUMBER(5) PRIMARY KEY,
    purpose_name     VARCHAR2(50) UNIQUE NOT NULL
);

-- --------------------------------------------------------------------
-- 4. Dimension Table: Credit Risk Grade Master
-- --------------------------------------------------------------------
CREATE TABLE DIM_LOAN_GRADE (
    grade_id         VARCHAR2(5) PRIMARY KEY,
    grade_name       VARCHAR2(25) NOT NULL,
    base_risk_level  VARCHAR2(25) NOT NULL
);

-- --------------------------------------------------------------------
-- 5. Fact Table: Loan Performance and Repayments
-- --------------------------------------------------------------------
CREATE TABLE FACT_LOANS (
    loan_id               VARCHAR2(20) PRIMARY KEY,
    customer_id           VARCHAR2(20) NOT NULL,
    date_id               VARCHAR2(10) NOT NULL,
    purpose_id            NUMBER(5) NOT NULL,
    grade_id              VARCHAR2(5) NOT NULL,
    loan_amount           NUMBER(12,2) NOT NULL CONSTRAINT chk_ora_amt CHECK (loan_amount > 0),
    loan_term_months      NUMBER(3) NOT NULL CONSTRAINT chk_ora_term CHECK (loan_term_months IN (36, 60)),
    interest_rate         NUMBER(5,2) NOT NULL CONSTRAINT chk_ora_rate CHECK (interest_rate > 0),
    debt_to_income_ratio  NUMBER(5,2) NOT NULL CONSTRAINT chk_ora_dti CHECK (debt_to_income_ratio >= 0),
    loan_status           VARCHAR2(25) NOT NULL,
    total_payment         NUMBER(12,2) DEFAULT 0.0 NOT NULL,
    outstanding_balance   NUMBER(12,2) DEFAULT 0.0 NOT NULL,
    default_flag          NUMBER(1) NOT NULL CONSTRAINT chk_ora_def CHECK (default_flag IN (0, 1)),
    
    CONSTRAINT fk_ora_cust FOREIGN KEY (customer_id) REFERENCES DIM_CUSTOMER(customer_id),
    CONSTRAINT fk_ora_date FOREIGN KEY (date_id) REFERENCES DIM_DATE(date_id),
    CONSTRAINT fk_ora_purp FOREIGN KEY (purpose_id) REFERENCES DIM_LOAN_PURPOSE(purpose_id),
    CONSTRAINT fk_ora_grad FOREIGN KEY (grade_id) REFERENCES DIM_LOAN_GRADE(grade_id)
);

CREATE INDEX idx_ora_grade ON FACT_LOANS(grade_id);
CREATE INDEX idx_ora_date ON FACT_LOANS(date_id);
CREATE INDEX idx_ora_purpose ON FACT_LOANS(purpose_id);
CREATE INDEX idx_ora_status ON FACT_LOANS(loan_status);
CREATE INDEX idx_ora_default ON FACT_LOANS(default_flag);
