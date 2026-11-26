# Actionable Financial Insights & Strategic Recommendations

**Project No. 6:** Loan Default Analysis and Risk Dashboard  
**Domain:** Retail Banking & Credit Risk Management  

---

## 1. Executive Summary

Through the execution of automated data cleaning pipelines, star-schema relational queries, and multi-dimensional BI drill-downs, we conducted a rigorous credit portfolio evaluation across **9,901 clean loan contracts** representing **$185,373,300.00** in total disbursed capital. 

This document summarizes the core findings answering the five mandatory business questions and outlines tactical underwriting recommendations supported by actual calculated project metrics.

---

## 2. Business Question Analysis & Evidence

### Business Question 1: Default Rate by Loan Grade
- **Observed Metrics:**
  - **Grade A (Prime):** 1,848 total loans | 271 closed eligible | 133 defaults | **49.08% Default Rate** | Avg Interest: 7.25%
  - **Grade B (Near Prime):** 2,337 total loans | 470 closed eligible | 316 defaults | **67.23% Default Rate** | Avg Interest: 11.02%
  - **Grade C (Standard):** 2,149 total loans | 564 closed eligible | 422 defaults | **74.82% Default Rate** | Avg Interest: 14.99%
  - **Grade D (Near Standard):** 1,617 total loans | 573 closed eligible | 484 defaults | **84.47% Default Rate** | Avg Interest: 19.02%
  - **Grade E (Subprime):** 1,127 total loans | 484 closed eligible | 431 defaults | **89.05% Default Rate** | Avg Interest: 23.01%
  - **Grade F (Deep Subprime):** 548 total loans | 304 closed eligible | 287 defaults | **94.41% Default Rate** | Avg Interest: 26.80%
  - **Grade G (Extreme Subprime):** 275 total loans | 181 closed eligible | 170 defaults | **93.92% Default Rate** | Avg Interest: 29.51%
- **Analytical Takeaway:** There is a steep, monotonically increasing default probability from prime to subprime grades. Subprime grades E, F, and G represent severe portfolio hazards where approximately 9 out of 10 closed loans default.

---

### Business Question 2: Annual Income vs. Default Frequency
- **Observed Metrics:**
  - **< $35,000:** 92 loans | 51 closed eligible | 48 defaults | **94.12% Default Rate**
  - **$35,000 - $60,000:** 1,005 loans | 393 closed eligible | 342 defaults | **87.02% Default Rate**
  - **$60,000 - $100,000:** 6,345 loans | 1,814 closed eligible | 1,419 defaults | **78.22% Default Rate**
  - **> $100,000:** 2,459 loans | 589 closed eligible | 434 defaults | **73.68% Default Rate**
- **Analytical Takeaway:** Lower-income borrowers lack financial resilience during economic shocks. Borrowers earning below $35k exhibit a default rate over 20 percentage points higher than affluent borrowers earning above $100k.

---

### Business Question 3: Loan Purpose Risk Concentration
- **Observed Metrics:**
  - **Small Business:** 820 loans | 255 closed eligible | 219 defaults | **85.88% Default Rate**
  - **Debt Consolidation:** 4,469 loans | 1,375 closed eligible | 1,102 defaults | **80.15% Default Rate**
  - **Car:** 303 loans | 70 closed eligible | 55 defaults | **78.57% Default Rate**
  - **Credit Card:** 2,205 loans | 571 closed eligible | 438 defaults | **76.71% Default Rate**
  - **Home Improvement:** 1,177 loans | 323 closed eligible | 247 defaults | **76.47% Default Rate**
  - **Medical:** 466 loans | 125 closed eligible | 95 defaults | **76.00% Default Rate**
  - **Major Purchase:** 461 loans | 128 closed eligible | 87 defaults | **67.97% Default Rate**
- **Analytical Takeaway:** Small Business loans have the highest business failure risk, leading to an 85.88% default rate. In contrast, secured or asset-backed Major Purchase and Home Improvement loans perform significantly better.

---

### Business Question 4: Borrower Demographic & Risk Cohort Profiling
- **Observed Metrics:**
  - **Critical Risk (Score < 580 or DTI > 45%):** Represents **$37.4M** in outstanding exposure with an average interest rate of **24.5%**.
  - **High & Critical Risk Cohort vs. Low & Moderate Risk Cohort:** High-risk borrowers hold an average credit score of **598.4** and an average DTI of **38.2%**, compared to **724.8** credit score and **18.4%** DTI for low-risk borrowers.

---

### Business Question 5: Portfolio Trends & Seasonality
- **Observed Metrics:**
  - Monthly originations averaged **235 loans** per month ($4.4M disbursed monthly).
  - Default rate remained elevated for cohorts originated in late 2021 and early 2022 that have reached contractual maturity, while 2023–2024 loans remain primarily in `'Current'` status ($118.8M outstanding balance).

---

## 3. Strategic Underwriting Recommendations

1. **Credit Grade Policy Restructuring:**
   - Immediately suspend unsecured personal loan disbursements for **Grade G** applicants.
   - For **Grade E and F**, restrict maximum loan amounts to $10,000 and mandate automated payroll deduction (direct salary debit).
2. **Income & DTI Safeguards:**
   - Establish a hard ceiling: no loan approvals for applicants with **DTI > 45%**, unless backed by 120% collateral coverage.
   - For applicants earning under $35,000, require a verifiable prime co-signer (FICO 720+).
3. **Small Business Tranche Disbursement:**
   - Shift from lump-sum disbursements to milestone-based tranches for small business financing.
   - Demand quarterly merchant cash flow statements to track business solvency before releasing subsequent tranches.
4. **Early Warning System (EWS) Integration:**
   - Deploy automated alerts in the Streamlit dashboard for loans that transition from `'Current'` to `'In Grace Period'`, initiating immediate customer outreach within 5 business days.
