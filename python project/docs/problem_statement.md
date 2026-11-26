# Project Definition: Loan Default Analysis and Risk Dashboard

**Project Number:** Project No. 6  
**Domain:** Banking and Finance  
**Target Audience:** Academic Evaluation (B.Tech 2nd Year CSE), Viva Voce, and Industry Portfolio  

---

## 1. Problem Statement

Retail lending institutions face substantial non-performing asset (NPA) losses due to the lack of transparent, automated monitoring of borrower credit profiles and repayment behavior. Credit analysts and risk managers struggle with fragmented data quality issues, such as missing income figures and extreme loan outliers, which distort default rate calculations across loan grades and customer demographics. This project establishes an end-to-end analytics pipeline and multi-tier risk dashboard that cleans dirty loan data, segments borrower default propensity, and empowers financial officers to take preemptive credit mitigation actions.

---

## 2. Four Measurable Objectives

1. **Data Ingestion & Hygiene Assurance:** Ingest, inspect, and clean 10,000 multi-attribute loan records containing controlled anomalies (missing income, extreme amounts, corrupted status flags, invalid credit scores), ensuring 100% data integrity with zero unresolved records in the clean warehouse.
2. **Standardized Financial KPI Engine:** Formulate and automate 11 core financial KPIs (Total Originated Volume, Total Borrowers, Defaulted Loans, Eligible Closed Loans, Default Rate, Average Credit Score, Average Loan Amount, Total Outstanding Balance, and Default Rates broken down by Grade, Income Band, and Loan Purpose).
3. **Cross-Tool Financial Reconciliation:** Achieve 100% numerical reconciliation of all critical metrics across Python (Pandas), SQL (SQLite and Oracle DDL/Queries), Microsoft Excel (PivotTables), and Microsoft Power BI (DAX measures) with zero discrepancy.
4. **Interactive Multi-Level Drill-Down Dashboard:** Construct an 11-page Streamlit web dashboard and a production-grade 4-page Power BI report featuring dynamic slicers and three dedicated drill-down hierarchies (Grade → Status → Loan Details; Income Band → Purpose → Loan Details; Risk Category → Credit Range → Loan Details).

---

## 3. Five Core Business Questions

| BQ # | Business Question | Measurable Formulation & Required Fields |
|:---:|:---|:---|
| **BQ1** | Which loan grades have the highest default rates? | $\text{Default Rate} = \frac{\sum \text{default\_flag}}{\text{Count of Closed Loans}}$ grouped by `loan_grade` (Grades A to G). |
| **BQ2** | How does annual income relate to loan defaults? | Default frequency and proportion grouped by segmented `income_band` (`< $35,000`, `$35,000 - $60,000`, `$60,000 - $100,000`, `> $100,000`). |
| **BQ3** | Which loan purposes have the highest default rates? | $\text{Default Rate}$ calculated per categorized `loan_purpose` (e.g., Debt Consolidation, Small Business, Credit Card, Medical, Home Improvement). |
| **BQ4** | Which borrower characteristics are associated with higher risk? | Multi-variable cross-tabulation of `credit_score`, `debt_to_income_ratio` (DTI), `home_ownership`, and `employment_type` against `default_flag` and `risk_category`. |
| **BQ5** | How is the loan portfolio and default trend changing over time? | Monthly time-series aggregation of total loan originations, disbursed loan amount, defaulted count, and default percentage grouped by `loan_issue_date` (Year-Month). |

---

## 4. Project Scope

### In-Scope
- Synthetic generation of 10,000 realistic banking records with controlled dirty data (outliers, nulls, invalid categories, duplicates).
- Data cleaning pipeline with automatic logging (`data_quality_log.csv`) and quarantine of corrupted rows.
- Star schema dimensional model (1 Fact Table: `FACT_LOANS`, 4 Dimension Tables: `DIM_CUSTOMER`, `DIM_DATE`, `DIM_LOAN_PURPOSE`, `DIM_LOAN_GRADE`).
- SQLite local database pipeline and production-ready Oracle SQL DDL, queries, and analytical views.
- Python KPI calculation engine and publication of `kpis.json`.
- 11-page interactive Streamlit web dashboard with Navy/Teal banking UI and 3 drill-downs.
- Complete Power BI setup guide, dimensional data model, and 12 DAX measures.
- Fully formulated Excel workbook with Power Query steps, PivotTables, and Dashboard.
- Automated testing suite (`tests/test_pipeline.py`) verifying constraints and calculations.
- Comprehensive academic documentation, final project report, and 30+ viva questions with answers.

### Out-of-Scope
- Machine learning black-box predictive deployment (focus is on descriptive, diagnostic, and risk-segmentation analytics).
- Real-time online banking transactional APIs (batch loan data processing is adopted).
- Paid third-party enterprise BI server licenses or proprietary cloud connectors.

---

## 5. Intended Users

1. **Credit Risk Officers & Underwriters:** To evaluate portfolio health, identify high-risk segments, and calibrate underwriting thresholds.
2. **Chief Financial Officer (CFO) & Executive Leadership:** To track capital exposure, non-performing loans, and monthly portfolio growth.
3. **Academic Examiners & Viva Evaluators:** To assess software engineering discipline, SQL fluency, data modeling rigor, and statistical reasoning for B.Tech degree requirements.
4. **Data Analytics Students:** As an open-source, reproducible reference implementation for full-stack data analytics.

---

## 6. Expected Business Value

- **Capital Loss Mitigation:** Early detection of high-risk borrower clusters (subprime grades E-G and DTI > 35%) reduces unexpected charge-offs by up to 18%.
- **Streamlined Underwriting Policies:** Real-time visibility into purpose-specific default rates prevents over-concentration in vulnerable loan categories (e.g., high-risk small business or debt consolidation).
- **Audit & Governance Compliance:** Complete traceability from dirty raw data to cleaned star-schema warehouses ensures regulatory reporting accuracy and eliminates manual reconciliation errors.
