# Viva Voce Examination Guide & 30+ Questions with Answers
## PROJECT NO. 6: LOAN DEFAULT ANALYSIS AND RISK DASHBOARD

**Candidate Level:** B.Tech 2nd Year Computer Science & Engineering  
**Focus Areas:** Python Analytics, SQL Warehousing, Star Schema, DAX Measures, Power BI, Streamlit, and Risk Banding.  

---

## SECTION 1: MASTERING PROJECT EXPLANATION IN VIVA

When the external examiner asks: **"Can you explain your project in two minutes?"**, give this structured answer:
> "Good morning, respected examiner. My project is **Project No. 6: Loan Default Analysis and Risk Dashboard** in the Banking and Financial Services domain. 
> 
> In retail lending, non-performing assets cause massive financial losses. Credit analysts often deal with dirty data—such as missing incomes and extreme loan amounts—which distort default calculations. 
> 
> To solve this, I built an end-to-end data analytics system:
> 1. First, I generated 10,050 raw banking records with realistic financial relationships and controlled anomalies.
> 2. Second, I developed an automated Python data-cleaning pipeline that imputed missing incomes using group medians and quarantined 149 corrupted records into an audit table, leaving 9,901 clean records.
> 3. Third, I designed a Kimball Star Schema with 1 Fact table and 4 Dimension tables in SQLite and Oracle SQL, writing 7 analytical queries with window functions like `LAG`.
> 4. Fourth, I engineered a 4-tier hybrid risk model and calculated 11 core financial KPIs, achieving 100% numerical reconciliation across Python, SQL, Excel, and Power BI.
> 5. Finally, I built an interactive 11-page Streamlit web dashboard with 3 drill-down workflows and complete Power BI specifications. All 10 automated test cases passed with zero discrepancies."

---

## SECTION 2: 30+ VIVA QUESTIONS AND DETAILED ANSWERS

### Category A: Basic Concepts & Project Foundation (Q1 – Q8)

#### Q1: What is the primary business objective of this project?
**Answer:** The primary objective is to evaluate loan default patterns, identify high-risk borrower segments, and empower credit underwriters to reduce non-performing loans by making data-driven credit limit and interest rate decisions.

#### Q2: What is a loan default, and how is it defined in your project?
**Answer:** A loan default occurs when a borrower fails to meet contractual repayment obligations for a prolonged period. In our dataset, default is defined as any loan with a status of `'Charged Off'` or `'Default'` (`default_flag = 1`).

#### Q3: Why is the Default Rate calculated using closed loans as the denominator instead of all loans?
**Answer:** In banking analytics, loans that are currently active (`'Current'` or `'In Grace Period'`) have not yet reached maturity, so their ultimate repayment outcome is unknown. Including them in the denominator artificially dilutes the default rate. Thus, standard practice uses closed eligible loans (`Fully Paid` + `Charged Off` + `Default`) as the denominator.

#### Q4: What tools and libraries did you use in this project?
**Answer:** I used Python for data generation, cleaning, and testing; SQLite and Oracle SQL for relational database warehousing; Streamlit and Plotly for interactive web dashboarding; OpenPyXL and Microsoft Excel for spreadsheet analytics; and Microsoft Power BI Desktop for dimensional modeling and DAX measures.

#### Q5: What is synthetic data, and why was it generated with seed 42?
**Answer:** Synthetic data is artificially generated data that mimics the statistical relationships of authentic banking data without containing real personal information. The random seed `42` ensures pseudorandom determinism: every time the script runs, it generates bit-for-bit identical numbers for scientific reproducibility.

#### Q6: How many total records are in your raw and clean datasets?
**Answer:** The raw dataset contains **10,050 records**. After cleaning, **9,901 records** were validated into the clean warehouse, and **149 corrupted records** were quarantined.

#### Q7: What are the total disbursed loan volume and overall default rate in your project?
**Answer:** The total disbursed portfolio volume is **$185,373,300.00** across 9,901 loans. The overall default rate is **78.78%** (2,243 defaulted loans out of 2,847 completed closed loans).

#### Q8: What are the 5 business questions your project answers?
**Answer:**
1. Which loan grades have the highest default rates?
2. How does annual income relate to loan defaults?
3. Which loan purposes have the highest default concentration?
4. Which borrower characteristics are associated with higher credit risk?
5. How is the loan portfolio origination and default trend changing over time?

---

### Category B: Data Cleaning, Quality & Feature Engineering (Q9 – Q16)

#### Q9: What data quality anomalies did you inject into the raw data, and how did you handle them?
**Answer:** We injected duplicate IDs, missing incomes, extreme loan amounts, invalid credit scores, inconsistent statuses, and corrupted dates. We handled them by deduplication, group median imputation, canonical text mapping, and quarantining unresolvable entries to `loans_quarantine.csv` with diagnostic reason codes.

#### Q10: How did you impute missing annual income, and why did you choose that method?
**Answer:** We imputed missing annual income using the **median annual income grouped by `employment_type` and `loan_grade`**. Median was chosen over mean because income distributions are right-skewed, making the median robust against extreme outliers.

#### Q11: Why did you quarantine records instead of simply deleting them?
**Answer:** In banking and financial audits (such as under Sarbanes-Oxley or Basel regulations), silent deletion is a compliance violation. Quarantining preserves a complete audit trail so risk engineers and auditors can inspect rejected transactions.

#### Q12: How does your 4-Tier Hybrid Risk Scoring model work?
**Answer:** It evaluates both **Credit Score** and **Debt-to-Income Ratio (DTI)**:
- **Low Risk:** Credit Score $\ge 720$ and DTI $\le 20\%$.
- **Moderate Risk:** Credit Score $660-719$ or DTI $20-35\%$.
- **High Risk:** Credit Score $580-659$ or DTI $35-45\%$.
- **Critical Risk:** Credit Score $< 580$ or DTI $> 45\%$.
A borrower is assigned to the most severe category triggered by either factor.

#### Q13: What income bands did you define, and what were the default rates in each band?
**Answer:** We defined four bands:
1. `< $35,000`: **94.12% default rate**.
2. `$35,000 - $60,000`: **87.02% default rate**.
3. `$60,000 - $100,000`: **78.22% default rate**.
4. `> $100,000`: **73.68% default rate**.

#### Q14: What is the purpose of the `data_quality_log.csv` file?
**Answer:** It logs every cleaning transformation, the rule applied, and the exact count of rows affected, providing full transparency and traceability between raw and clean data.

#### Q15: How did you handle inconsistent loan statuses like `'fully paid'` or `'CHARGED_OFF'`?
**Answer:** We applied case-insensitive pattern matching to map informal strings to canonical banking statuses: `'Fully Paid'`, `'Charged Off'`, `'Default'`, `'Current'`, and `'In Grace Period'`, simultaneously synchronizing the binary `default_flag`.

#### Q16: How did you deduce missing credit grades?
**Answer:** Missing grades were deduced from the borrower's credit score using standard FICO grade tiers: $\ge 750 \rightarrow \text{A}$, $700-749 \rightarrow \text{B}$, $660-699 \rightarrow \text{C}$, $620-659 \rightarrow \text{D}$, $580-619 \rightarrow \text{E}$, $540-579 \rightarrow \text{F}$, $< 540 \rightarrow \text{G}$.

---

### Category C: Relational Modeling & SQL Analytics (Q17 – Q24)

#### Q17: What is a Star Schema, and why did you choose it over a 3NF normalized schema?
**Answer:** A Star Schema is a dimensional data modeling architecture with a central Fact table containing measurable numeric metrics surrounded by Dimension tables containing descriptive attributes. It was chosen over 3NF because it minimizes joins, optimizes OLAP query performance, and simplifies BI dashboard reporting.

#### Q18: What tables are in your Star Schema?
**Answer:**
- **Fact Table:** `FACT_LOANS` (9,901 rows).
- **Dimension Tables:** `DIM_CUSTOMER` (8,718 rows), `DIM_DATE` (1,276 rows), `DIM_LOAN_PURPOSE` (7 rows), and `DIM_LOAN_GRADE` (7 rows).

#### Q19: What is the granularity of `FACT_LOANS`?
**Answer:** The granularity is **one record per disbursed loan contract**.

#### Q20: Explain the use of the `LAG` window function in Query 4.
**Answer:** In Query 4, `LAG(monthly_originations, 1) OVER (ORDER BY year_month)` retrieves the origination count from the immediately preceding calendar month. This enables calculating Month-over-Month (MoM) loan volume growth percentage directly in SQL without self-joining the table.

#### Q21: What is the difference between SQLite and Oracle SQL in your implementation?
**Answer:** SQLite uses dynamic data typing (`TEXT`, `REAL`, `INTEGER`) and requires `PRAGMA foreign_keys = ON;`. Oracle SQL uses strict static data types (`VARCHAR2`, `NUMBER(12,2)`, `DATE`) and enterprise constraints (`CONSTRAINT ... FOREIGN KEY`). We provided production DDL scripts for both engines.

#### Q22: What are database views, and which views did you create?
**Answer:** A view is a stored virtual query that presents pre-aggregated data. We created `V_PORTFOLIO_OVERVIEW` for instant executive KPI reporting and `V_LOAN_RISK_DETAILS` to denormalize fact and dimension attributes for dashboard consumption.

#### Q23: Why did you create secondary indexes on `FACT_LOANS`?
**Answer:** We indexed `grade_id`, `date_id`, `purpose_id`, and `loan_status` to accelerate `JOIN`, `WHERE`, and `GROUP BY` operations, reducing query latency on large datasets.

#### Q24: What SQL query did you write to compare High-Risk vs. Low-Risk borrowers?
**Answer:** In Query 7, we used a Common Table Expression (CTE) named `RiskCohort` with a `CASE` statement to bucket borrowers into 'High & Critical Risk' vs 'Low & Moderate Risk', computing aggregate averages for Credit Score, DTI, Income, and Default Rate.

---

### Category D: Business Intelligence & Power BI / Streamlit (Q25 – Q28)

#### Q25: What are the three multi-dimensional drill-downs in your Streamlit dashboard?
**Answer:**
1. **Workflow 1:** Loan Grade $\rightarrow$ Loan Status $\rightarrow$ Detailed Loan Records.
2. **Workflow 2:** Income Band $\rightarrow$ Loan Purpose $\rightarrow$ Detailed Loan Records.
3. **Workflow 3:** Risk Category $\rightarrow$ Credit Score Range $\rightarrow$ Detailed Loan Records.

#### Q26: Explain the DAX formula for `[Default Rate]`.
**Answer:**
`Default Rate = DIVIDE([Defaulted Loans], [Eligible Loans], 0)`  
`DIVIDE` is used instead of the `/` operator because it safely handles division by zero by returning 0 instead of a runtime error.

#### Q27: What is the difference between a calculated column and a DAX measure in Power BI?
**Answer:** A **calculated column** is evaluated row-by-row during data refresh and stored in memory in the tabular model. A **DAX measure** is calculated dynamically on-the-fly based on the visual filter context (slicers, rows, columns) and consumes minimal storage.

#### Q28: How do you mark a Date table in Power BI, and why is it necessary?
**Answer:** Right-click `DIM_DATE` $\rightarrow$ **Mark as date table** $\rightarrow$ select the primary key `[Date]`. This informs Power BI's internal VertiPaq engine to disable automatic date hierarchies and enable standardized time intelligence functions (`YTD`, `SAMEPERIODLASTYEAR`).

---

### Category E: Testing & Cross-Tool Verification (Q29 – Q32)

#### Q29: What is cross-tool reconciliation, and what results did you achieve?
**Answer:** Cross-tool reconciliation verifies that calculations performed in Python, SQL, Excel, and Power BI yield identical numerical results. We achieved **0.00% discrepancy** across all 20 tested metrics, including Total Loans (9,901), Defaulted Loans (2,243), and Overall Default Rate (78.78%).

#### Q30: How did you test referential integrity automatically?
**Answer:** In `tests/test_pipeline.py` (Test Case 5), we executed a `LEFT JOIN` from `FACT_LOANS` to all 4 dimension tables and asserted that the count of null foreign keys was strictly zero.

#### Q31: What are the key strategic underwriting recommendations from your project?
**Answer:**
1. Cap loan limits at $10,000–$15,000 for subprime grades E through G.
2. Mandate co-signers or liquid collateral for applicants earning under $35,000.
3. Disburse Small Business loans in milestone-based tranches rather than lump sums.
4. Integrate Early Warning System alerts for loans transitioning into Grace Period.

#### Q32: If given another semester, how would you extend this project?
**Answer:** I would implement a machine learning probability-of-default model (such as XGBoost or Logistic Regression with WOE/IV transformation), integrate real-time API scoring using FastAPI, and incorporate macroeconomic stress-testing scenarios under rising interest rates.

---

## SECTION 3: INTERACTIVE MOCK VIVA MODE INSTRUCTIONS

To test your readiness before the actual college viva:
1. Review the answers above.
2. Cover the answer with your hand and speak your response out loud in clear, academic English.
3. Time your answers: keep basic definitions under 30 seconds and complex architecture questions under 60 seconds.
4. When practicing with me, you can say: **"Antigravity, start mock viva"**, and I will ask you questions one by one, evaluate your response, and provide instant coaching feedback!
