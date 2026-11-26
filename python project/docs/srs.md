# Software Requirements Specification (SRS)
## Project No. 6: Loan Default Analysis and Risk Dashboard

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) details the complete functional and non-functional requirements for the **Loan Default Analysis and Risk Dashboard** project. It specifies the architecture, data processing standards, database schemas, visualization modules, testing mechanisms, and acceptance criteria required for academic evaluation (B.Tech 2nd Year CSE) and professional analytics demonstration.

### 1.2 Project Scope
The software system ingests raw multi-attribute retail loan data, detects and repairs data quality issues, transforms records into a Star Schema data warehouse, executes analytical SQL queries, generates descriptive and diagnostic KPIs, and presents actionable insights through an 11-page Streamlit application, Power BI specifications, and an Excel dashboard.

### 1.3 Definitions, Acronyms, and Abbreviations
- **DTI:** Debt-to-Income Ratio (percentage of monthly debt obligations divided by gross monthly income).
- **FICO:** Fair Isaac Corporation credit score metric (ranging from 300 to 850).
- **NPA:** Non-Performing Asset.
- **DAX:** Data Analysis Expressions (used in Microsoft Power BI).
- **KPI:** Key Performance Indicator.
- **SRS:** Software Requirements Specification.
- **FR / NFR:** Functional Requirement / Non-Functional Requirement.

### 1.4 References
- Basel II / Basel III Credit Risk Management Frameworks.
- LendingClub Public Loan Data Documentation.
- Microsoft Power BI DAX & Star Schema Best Practices.

---

## 2. Overall Description

### 2.1 Product Perspective
The product is a self-contained, multi-tier data analytics and business intelligence solution designed to run locally on Windows 11 without requiring paid cloud infrastructure or commercial database instances. It incorporates SQLite for local embedded relational persistence and provides Oracle-compatible scripts for enterprise database portability.

### 2.2 Product Functions
- Synthetic data generation with controlled, reproducible real-world anomalies.
- Automated data hygiene logging and quarantine of corrupted rows.
- Feature engineering of risk bands (`Low`, `Moderate`, `High`, `Critical Risk`) and income brackets.
- Star schema dimensional mapping and relational query execution.
- Web-based interactive visual analytics with three-level drill-down workflows.
- Cross-platform numerical verification across Python, SQL, Excel, and Power BI.

### 2.3 User Characteristics
- **B.Tech Student / Developer:** Executes pipelines, inspects source code, tests SQL queries, and analyzes findings.
- **College Viva Examiner:** Evaluates methodology, relational constraints, DAX logic, and cross-tool consistency.
- **Credit Underwriter / Risk Analyst:** Uses dashboards to monitor default rates, identify risky segments, and review loan distributions.

### 2.4 Operating Environment
- **Operating System:** Windows 11 (64-bit).
- **Python Version:** Python 3.10+ (specifically Python 3.15 compatible).
- **Database:** SQLite 3 (built-in) and Oracle 19c/21c DDL compatibility.
- **BI Software:** Streamlit 1.28+, Microsoft Power BI Desktop, Microsoft Excel 2016+.

---

## 3. Assumptions and Constraints

### 3.1 Assumptions
1. Synthetic records accurately reflect real-world credit risk distributions (e.g., lower credit scores correlate with higher default probabilities).
2. The loan default status is established once a loan reaches `'Charged Off'` or `'Default'` status.
3. The user has administrative rights on the local Windows 11 machine to run Python scripts and launch local web servers via localhost.

### 3.2 Constraints
1. No paid software, proprietary external APIs, or cloud database subscriptions are required.
2. All file paths must be relative to the repository root directory.
3. Random seed for data generation is fixed at `42` to guarantee reproducibility.

---

## 4. Functional Requirements

| Req ID | Requirement Title | Detailed Description | Priority |
|:---|:---|:---|:---:|
| **FR1** | Synthetic Data Generation | System must generate $\ge 10,000$ synthetic loan records with 20 attributes and inject controlled errors (missing values, extreme outliers, invalid credit scores, duplicate IDs, corrupt dates). | High |
| **FR2** | Data Hygiene & Cleaning Pipeline | Ingest raw CSV data, impute missing income with group medians, quarantine unrecoverable records, format dates, and output clean CSV files to `data/clean/`. | High |
| **FR3** | Data Quality Audit Logging | Maintain an audit log (`data_quality_log.csv`) recording issue description, applied rule, and exact rows affected for every transformation. | High |
| **FR4** | Data Dictionary Generation | Auto-inspect generated datasets and output a comprehensive data dictionary in Markdown and Excel formats (`docs/data_dictionary.md`, `docs/data_dictionary.xlsx`). | Medium |
| **FR5** | Star Schema Relational Modeling | Create and maintain 1 Fact Table (`FACT_LOANS`) and 4 Dimension Tables (`DIM_CUSTOMER`, `DIM_DATE`, `DIM_LOAN_PURPOSE`, `DIM_LOAN_GRADE`) with explicit Primary and Foreign Keys. | High |
| **FR6** | SQL Relational Analytics | Implement SQLite and Oracle-compatible DDL/queries executing at least 7 analytical queries addressing business questions (including `GROUP BY`, `CASE`, `LAG`, and subqueries). | High |
| **FR7** | Financial KPI Computation | Calculate 11 mandatory financial KPIs (Total Originated Volume, Total Borrowers, Defaulted Loans, Eligible Closed Loans, Default Rate, Avg Credit Score, Avg Loan Amount, Outstanding Balance, and Default Rates by Grade, Income Band, and Purpose) and export to `reports/kpis.json`. | High |
| **FR8** | Interactive Streamlit Dashboard | Deliver an 11-page interactive Streamlit web dashboard styled with Navy/Teal banking aesthetics, dynamic global filters, KPI tiles, Plotly charts, and searchable loan tables. | High |
| **FR9** | Multi-Level Drill-Downs | Support three distinct functional drill-down workflows in the UI: (1) Grade → Status → Details, (2) Income Band → Purpose → Details, (3) Risk Category → Credit Range → Details. | High |
| **FR10** | Power BI Model & DAX Library | Provide a complete Power BI desktop setup guide, dimensional data model diagram, and 12 DAX measure formulas. | High |
| **FR11** | Microsoft Excel Analytics Route | Provide an Excel workbook (`excel/loan_analysis_dashboard.xlsx`) with raw/clean data sheets, Power Query steps, PivotTables, and dynamic dashboard sheets. | Medium |
| **FR12** | Automated Testing Suite | Execute a comprehensive testing script (`tests/test_pipeline.py`) validating primary keys, ranges, referential integrity, and cross-tool reconciliation, outputting PASS/FAIL to `reports/test_results.csv`. | High |

---

## 5. Non-Functional Requirements

| Req ID | NFR Category | Requirement Specification | Measurable Verification Method |
|:---|:---|:---|:---|
| **NFR1** | **Accuracy & Reconciliation** | The default count and overall default rate calculated in Python, SQL, Excel, and Power BI must be 100% numerically identical. | Run `src/reconciliation.py`; difference must equal 0.00% across all shared metrics in `reports/reconciliation_report.csv`. |
| **NFR2** | **Performance & Latency** | Streamlit web application pages and chart renders must complete in $< 2.0$ seconds on standard laptop hardware. | Measure page execution time using Python `time.perf_counter()` during local browser navigation. |
| **NFR3** | **Data Integrity** | Cleaned warehouse fact table must have 0% orphaned foreign keys and 0 duplicate primary keys. | Automated test assertion `test_referential_integrity()` in `tests/test_pipeline.py` returning PASS. |
| **NFR4** | **Reproducibility** | Data generation script executed multiple times must produce bit-for-bit identical datasets. | Compare SHA-256 hash of `data/raw/loans_raw.csv` across independent runs with seed `42`. |
| **NFR5** | **Portability** | Pipeline must run seamlessly on Windows 11 without requiring Unix-specific shell utilities or administrative virtualization. | Execute entire pipeline via standard Windows PowerShell without syntax or path delimiter errors. |
| **NFR6** | **Usability** | The Streamlit dashboard must have a contrast ratio $\ge 4.5:1$ adhering to WCAG 2.1 AA standards for professional data visualization. | Inspect UI color palette (Dark Navy `#0A192F`, White `#FFFFFF`, Teal `#00B4D8`, Coral `#EF476F`). |
| **NFR7** | **Maintainability** | All Python modules must feature PEP 8 compliant docstrings, type hints, and modular separation of concerns. | Automated static linting check or test pass with clean module imports. |
| **NFR8** | **Auditability** | Every data cleaning action and record exclusion must be documented in human-readable and tabular format. | Inspect `data/reports/data_quality_log.csv` and verify all dropped/imputed rows match reported totals. |

---

## 6. Data Requirements

The system must handle 20 standardized attributes:
1. `loan_id` (String / Integer - Unique Identifier)
2. `customer_id` (String / Integer - Customer Identifier)
3. `age` (Integer: 18 - 75)
4. `gender` (Categorical: Male, Female, Other)
5. `employment_type` (Categorical: Salaried, Self-Employed, Business, Contract)
6. `annual_income` (Float: 15,000 - 300,000; includes missing values in raw)
7. `credit_score` (Integer: 300 - 850; includes out-of-range anomalies in raw)
8. `loan_amount` (Float: 1,000 - 100,000; includes extreme outliers in raw)
9. `loan_term_months` (Integer: 36 or 60)
10. `interest_rate` (Float: 5.0% - 28.0%)
11. `loan_purpose` (Categorical: Debt Consolidation, Credit Card, Home Improvement, Small Business, Medical, Education, Major Purchase)
12. `loan_grade` (Categorical: A, B, C, D, E, F, G)
13. `debt_to_income_ratio` (Float: 2.0% - 60.0%)
14. `existing_loans` (Integer: 0 - 10)
15. `home_ownership` (Categorical: RENT, OWN, MORTGAGE)
16. `loan_issue_date` (Date: YYYY-MM-DD; includes corrupted formats in raw)
17. `loan_status` (Categorical: Fully Paid, Charged Off, Default, Current, In Grace Period)
18. `total_payment` (Float: Repayment amount to date)
19. `outstanding_balance` (Float: Remaining balance)
20. `default_flag` (Binary: 1 = Defaulted / Charged Off, 0 = Non-Defaulted)

---

## 7. Acceptance Criteria

- **AC1 (Grade Default Rate Accuracy):** Default rate strictly increases from Grade A (lowest, typically $< 5\%$) to Grade G (highest, typically $> 30\%$).
- **AC2 (Income Band Default Rate Accuracy):** Lower income tiers ($< \$35,000$) show higher default rates than affluent tiers ($> \$100,000$).
- **AC3 (Purpose Default Rate Accuracy):** High-risk purposes such as Small Business and Debt Consolidation exhibit higher default rates than secured Home Improvement loans.
- **AC4 (Documented Risk Bands):** Risk tiers (`Low`, `Moderate`, `High`, `Critical`) are mathematically defined and documented with dual-trigger credit score and DTI criteria.
- **AC5 (Interactive Drill-Downs):** At least 3 interactive drill-downs operate without runtime errors and dynamically filter loan detail records in the Streamlit web dashboard.
