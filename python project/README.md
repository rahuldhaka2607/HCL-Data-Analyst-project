# LOAN INTELLIGENCE: Loan Default Analysis and Risk Dashboard
## Complete Data Analytics Academic & Industry Project (Project No. 6)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Database-SQLite3-lightgrey](https://img.shields.io/badge/Database-SQLite3%20%7C%20Oracle%20Compatible-orange.svg)](https://www.sqlite.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Interactive%20UI-FF4B4B.svg)](https://streamlit.io/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Star%20Schema%20%2B%20DAX-F2C811.svg)](https://powerbi.microsoft.com/)
[![Tests-10%2F10%20Pass-brightgreen](https://img.shields.io/badge/Tests-10%2F10%20PASS-brightgreen.svg)](tests/test_pipeline.py)
[![Academic Evaluation](https://img.shields.io/badge/Target-B.Tech%202nd%20Year%20CSE-purple.svg)]()

---

## 1. Problem Statement

Retail lending institutions face substantial non-performing asset (NPA) losses due to the lack of transparent, automated monitoring of borrower credit profiles and repayment behavior. Credit analysts and risk managers struggle with fragmented data quality issues, such as missing income figures and extreme loan outliers, which distort default rate calculations across loan grades and customer demographics. This project establishes an end-to-end analytics pipeline and multi-tier risk dashboard that cleans dirty loan data, segments borrower default propensity, and empowers financial officers to take preemptive credit mitigation actions.

---

## 2. Measurable Project Objectives

1. **Automated Data Quality & Hygiene:** Ingest and sanitize 10,000 multi-attribute loan records containing controlled real-world anomalies (missing incomes, extreme outliers, invalid credit scores, duplicate IDs, corrupt dates), quarantining unresolvable entries to achieve 100% warehouse integrity.
2. **Standardized Star Schema Warehouse:** Construct a Kimball-methodology Star Schema comprising 1 Fact table (`FACT_LOANS`) and 4 Dimension tables (`DIM_CUSTOMER`, `DIM_DATE`, `DIM_LOAN_PURPOSE`, `DIM_LOAN_GRADE`) with explicit referential integrity and SQLite/Oracle DDL scripts.
3. **Cross-Tool Financial Reconciliation:** Compute 11 core financial performance indicators and guarantee 100% numerical reconciliation (0.00% variance) across Python, SQL, Excel, and Power BI.
4. **Interactive Multi-Level BI Dashboards:** Deliver an 11-page interactive Streamlit web dashboard and complete Power BI specifications featuring 3 functional drill-down workflows and dynamic filtering.

---

## 3. Technology Stack

- **Core Analytics & Scripting:** Python (Standard Library, SQLite3, Matplotlib, Plotly, Streamlit, OpenPyXL, Pytest).
- **Database Architecture:** Embedded SQLite 3.x and Oracle 19c/21c Enterprise DDL & Analytical Queries.
- **Business Intelligence:** Microsoft Power BI Desktop (Power Query M, DAX Measure Engine, Star Schema).
- **Spreadsheet Analytics:** Microsoft Excel (Formulas, PivotTables, Multi-sheet Dashboard).
- **Version Control & Docs:** Git, GitHub, Markdown, Draw.io ER diagrams.

---

## 4. Key Verified Project Metrics

| Executive Financial KPI | Calculated Production Metric | Verification Notes |
|:---|:---:|:---|
| **Total Originated Loans** | **9,901** | Post-cleaning clean warehouse records |
| **Total Disbursed Volume** | **$185,373,300.00** | Principal disbursed across active & closed loans |
| **Total Unique Borrowers** | **8,718** | Distinct customer accounts |
| **Eligible Closed Loans** | **2,847** | Closed portfolio denominator (`Fully Paid` + `Charged Off` + `Default`) |
| **Total Defaulted Loans** | **2,243** | Severely delinquent contracts (`default_flag = 1`) |
| **Overall Default Rate** | **78.78%** | Defaulted / Closed Eligible Loans (100% reconciled) |
| **Average Loan Amount** | **$18,722.68** | Mean principal per loan contract |
| **Average Credit Score** | **683.1** | Mean FICO credit score across borrowers |
| **Total Outstanding Balance** | **$118,836,026.27** | Active uncollected capital at risk |
| **Grade A vs. Grade G Default** | **49.08% vs. 93.92%** | Clear risk escalation across underwriting tiers |

---

## 5. Repository Structure

```
loan-default-analysis-risk-dashboard/
│
├── app/
│   └── streamlit_app.py               # 11-page interactive Streamlit web dashboard
│
├── data/
│   ├── raw/
│   │   └── loans_raw.csv              # Synthetic raw dataset with injected anomalies (10,050 rows)
│   ├── clean/
│   │   ├── loans_clean.csv            # Cleaned, standardized warehouse dataset (9,901 rows)
│   │   └── loans_quarantine.csv       # Quarantined unrecoverable records with diagnostic reason (149 rows)
│   ├── reports/
│   │   ├── data_quality_log.csv       # Transformation audit log
│   │   ├── query_1_grade_default_rate.csv
│   │   ├── query_2_income_band_default_rate.csv
│   │   ├── query_3_purpose_default_rate.csv
│   │   ├── query_4_monthly_default_trends.csv
│   │   ├── query_5_risk_category_distribution.csv
│   │   ├── query_6_portfolio_summary.csv
│   │   └── query_7_risk_cohort_comparison.csv
│   └── loans.db                       # Local SQLite 3 star schema database
│
├── src/
│   ├── data_generator.py              # Synthetic data generation with seed 42
│   ├── data_cleaning.py               # Rule-based cleaning and quarantine engine
│   ├── feature_engineering.py         # Risk banding and income segment calculator
│   ├── database.py                    # Star-schema builder and SQL analytics runner
│   ├── kpi_calculations.py            # KPI calculation and chart export engine
│   ├── reconciliation.py              # Cross-tool reconciliation verification
│   ├── generate_data_dictionary.py    # Auto-generation of data dictionary (MD and XLSX)
│   └── create_excel_dashboard.py      # Multi-sheet Excel workbook generator
│
├── notebooks/
│   └── loan_default_analysis.ipynb    # Complete academic Jupyter Notebook (Colab compatible)
│
├── sql/
│   ├── schema.sql                     # SQLite Star Schema DDL
│   ├── queries.sql                    # 7 Analytical SQL Queries (JOIN, GROUP BY, LAG, CASE)
│   ├── oracle/
│   │   ├── oracle_schema.sql          # Oracle 19c/21c DDL with static constraints
│   │   └── oracle_queries.sql         # Oracle SQL queries with analytical functions
│   └── views/
│       └── analytical_views.sql       # Pre-aggregated analytical database views
│
├── powerbi/
│   ├── dax_measures.dax               # 12 DAX measure formulas with plain-English definitions
│   ├── data_model.md                  # Star schema ER diagrams and draw.io guide
│   └── setup_guide.md                 # 4-page Power BI Desktop setup instructions
│
├── excel/
│   └── loan_analysis_dashboard.xlsx   # 6-sheet workbook with Dashboard, Data, and Pivot Analysis
│
├── reports/
│   ├── kpis.json                      # Machine-readable JSON summary of KPIs
│   ├── test_results.csv               # 10-point automated test execution log (10/10 PASS)
│   └── reconciliation_report.csv      # Cross-tool verification matrix (0.00% variance)
│
├── docs/
│   ├── problem_statement.md           # Formal project scope and 5 business questions
│   ├── synopsis.md                    # Academic project synopsis
│   ├── srs.md                         # Complete Software Requirements Specification
│   ├── data_dictionary.md             # Markdown data dictionary
│   ├── data_dictionary.xlsx           # Excel data dictionary
│   ├── risk_band_documentation.md     # 4-tier risk band methodology
│   ├── data_quality_report.md         # Before/after data quality audit report
│   ├── public_datasets_review.md      # Review of LendingClub, UCI, and Home Credit
│   ├── insights_summary.md            # Actionable business insights
│   ├── final_report.md                # 18-section academic project report
│   └── viva_questions.md              # 30+ Viva Voce questions and answers
│
├── tests/
│   └── test_pipeline.py               # 10 automated test cases with pytest support
│
├── assets/
│   └── screenshots/
│       ├── default_rate_by_grade.png
│       ├── default_rate_by_income_band.png
│       ├── default_rate_by_purpose.png
│       └── monthly_default_trend.png
│
├── requirements.txt                   # Project Python dependencies
└── README.md                          # Master documentation guide
```

---

## 6. How to Run in Five Simple Steps

### Step 1: Clone or Navigate to the Workspace
```bash
git clone https://github.com/<your-username>/loan-default-analysis-risk-dashboard.git
cd loan-default-analysis-risk-dashboard
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Data Generation and Cleaning Pipeline
```bash
python src/data_generator.py
python src/data_cleaning.py
python src/generate_data_dictionary.py
```

### Step 4: Build the SQLite Database and Compute Metrics
```bash
python src/database.py
python src/kpi_calculations.py
python src/create_excel_dashboard.py
python src/reconciliation.py
```

### Step 5: Launch the Interactive Streamlit Web Dashboard
```bash
streamlit run app/streamlit_app.py
```
*The web dashboard will launch automatically in your browser at `http://localhost:8501`.*

---

## 7. Automated Test Suite Verification

Run the automated verification suite to validate all 10 acceptance criteria:
```bash
python tests/test_pipeline.py
```
**Output Summary:**
```text
[PASS] TC-01: No Duplicate Primary Keys (9,901 unique IDs)
[PASS] TC-02: No Missing Required Fields (0 missing values)
[PASS] TC-03: Valid Value Ranges (FICO 300-850, Loan > $0, Age 18-100)
[PASS] TC-04: Python Total Equals SQL Total (9,901 rows matched)
[PASS] TC-05: Referential Integrity Verified (0 orphaned foreign keys)
[PASS] TC-06: Default Rate Calculation Rigor (78.78% verified)
[PASS] TC-07: Risk Band Dual-Trigger Classification (4/4 scenarios verified)
[PASS] TC-08: Missing Income Imputation (0 nulls remaining)
[PASS] TC-09: Extreme Loan Amounts Quarantined (30 outliers isolated)
[PASS] TC-10: Invalid Loan Status Standardization (0 unmapped codes)
```

---

## 8. Five Core Business Questions Answered

### BQ1: Which loan grades have the highest default rates?
- **Finding:** Default rate escalates dramatically across credit rating tiers: **Grade A (49.08%)**, **Grade B (67.23%)**, **Grade C (74.82%)**, **Grade D (84.47%)**, **Grade E (89.05%)**, **Grade F (94.41%)**, and **Grade G (93.92%)**.
- **Underwriting Action:** Cap total loan amounts at $15,000 for subprime grades E through G and adjust risk-premium interest rates.

### BQ2: How does annual income relate to loan defaults?
- **Finding:** Lower-income borrowers experience higher default rates: **< $35k (94.12%)**, **$35k-$60k (87.02%)**, **$60k-$100k (78.22%)**, and **> $100k (73.68%)**.
- **Underwriting Action:** Require co-signers or verifiable liquid cash reserves for borrowers earning under $35,000.

### BQ3: Which loan purposes have the highest default rates?
- **Finding:** **Small Business** loans exhibited the highest default rate (**85.88%**), followed by **Debt Consolidation** (**80.15%**) and **Car** loans (**78.57%**). **Major Purchase** loans had the lowest default rate (**67.97%**).
- **Underwriting Action:** Disburse small business loans in progress-based milestones rather than immediate lump sums.

### BQ4: Which borrower characteristics are associated with higher risk?
- **Finding:** Borrowers classified in the **Critical Risk** cohort (Credit Score < 580 or DTI > 45%) exhibited an overwhelming concentration of portfolio charge-offs and account for over 45% of outstanding capital exposure.

### BQ5: How is the loan portfolio and default trend changing over time?
- **Finding:** Monthly originations remained steady at 200–280 loans per month, but default rates showed seasonal peaks following holiday expenditure quarters, reinforcing the need for proactive loan restructuring.

---

## 9. Assumptions and Limitations

### Assumptions:
1. Loan performance is finalized once a contract reaches `'Fully Paid'`, `'Charged Off'`, or `'Default'`.
2. Median income imputation preserves customer demographic distributions without introducing artificial variance.
3. The 4-tier hybrid risk model conservatively assigns a borrower to the highest risk band triggered by either Credit Score or DTI.

### Limitations:
1. The dataset is synthetic and designed specifically for educational modeling and algorithm validation.
2. Macroeconomic factors (inflation, central bank benchmark rates, regional unemployment) are held static.

---

## 10. AI Usage Disclosure & Academic Integrity

This project utilized AI assistance (Antigravity by Google DeepMind) as an architectural mentor for code scaffolding, test case structuring, and documentation drafting. All data cleaning rules, SQL queries, DAX formulas, mathematical reconciliations, and academic analyses were verified, executed, and tested by the student for practical evaluation.

---

## 11. Demonstration Video & GitHub Setup

- **GitHub Repository:** `https://github.com/<your-username>/loan-default-analysis-risk-dashboard`
- **Video Walkthrough (5 Mins):** *[Insert YouTube / Loom Walkthrough Link Here]*
- **Author:** Rahul (B.Tech 2nd Year Computer Science & Engineering)  
- **Academic Mentor:** Senior Data Analyst & Course Evaluator
