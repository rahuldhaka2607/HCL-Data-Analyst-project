# Public Loan Datasets Review and Benchmark Analysis

**Project No. 6:** Loan Default Analysis and Risk Dashboard  
**Domain:** Banking & Financial Services  

---

## 1. Executive Summary

To ground our analytical design in authentic industry standards, we reviewed three premier publicly available retail banking loan datasets. While these repositories provide real-world credit patterns, academic environments and institutional firewalls often face download rate limits, missing schema updates, and irregular licence restrictions. Therefore, in accordance with the project guidelines, we benchmark our architecture against these public datasets and produce an automated, 10,000-record synthetic banking dataset with controlled real-world data quality anomalies for transparent testing, learning, and viva demonstration.

---

## 2. Public Dataset Benchmark Analysis

### Dataset 1: LendingClub Loan Data (2007–2018Q4)
- **Dataset Name:** Lending Club Loan Dataset
- **Direct Working Link:** [https://www.kaggle.com/datasets/wordsforthewise/lending-club](https://www.kaggle.com/datasets/wordsforthewise/lending-club)
- **Source / Platform:** Kaggle / LendingClub Financial Peer-to-Peer Marketplace
- **Licence / Usage Terms:** Open Data Commons Public Domain Dedication and License (PDDL) / CC0 1.0 Universal
- **Available Key Columns:** `id`, `loan_amnt`, `term`, `int_rate`, `installment`, `grade`, `sub_grade`, `emp_length`, `home_ownership`, `annual_inc`, `verification_status`, `issue_d`, `loan_status`, `purpose`, `dti`, `earliest_cr_line`, `open_acc`, `pub_rec`, `revol_bal`, `total_pymnt`, `recoveries`.
- **Advantages:**
  - Enormous historical sample size (> 2.2 million loan records).
  - Authentic FICO grade classification (A through G) and historical default indicators (`Charged Off`, `Default`).
  - Widely accepted benchmark across peer-reviewed finance literature.
- **Limitations:**
  - Massive uncompressed file size (> 1.6 GB CSV), making it difficult to process quickly on student laptops during a 10-minute viva.
  - Excessive feature sparsity (> 145 raw columns, many with > 80% null values).
  - Uneven reporting across regulatory reporting regimes (2007 vs 2018).
- **Suitability for This Project:** **Very High (Architectural Model)**. Our synthetic dataset fields, grading tiers (A–G), and status codes (`Fully Paid`, `Charged Off`, `Current`) are directly modeled after LendingClub standards.

---

### Dataset 2: Bank Marketing & Term Deposit Default Dataset (UCI Machine Learning Repository)
- **Dataset Name:** Bank Marketing Dataset
- **Direct Working Link:** [https://archive.ics.uci.edu/dataset/222/bank+marketing](https://archive.ics.uci.edu/dataset/222/bank+marketing)
- **Source / Platform:** UC Irvine Machine Learning Repository (Donated by S. Moro, P. Cortez, P. Rita)
- **Licence / Usage Terms:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Available Key Columns:** `age`, `job`, `marital`, `education`, `default` (credit in default: yes/no), `balance`, `housing` (housing loan), `loan` (personal loan), `contact`, `day`, `month`, `duration`, `campaign`, `pdays`, `previous`, `poutcome`, `y`.
- **Advantages:**
  - Clean, peer-reviewed academic benchmark with 45,211 instances.
  - Realistic European retail customer demographic variables.
  - Light storage footprint (< 5 MB).
- **Limitations:**
  - Primarily centered on telemarketing conversion rather than multi-installment loan performance over time.
  - Lacks loan amounts, loan grades, credit score scales, and debt-to-income (DTI) metrics.
- **Suitability for This Project:** **Moderate**. Useful for validating customer demographic distributions (age, employment type), but lacks core credit underwriting attributes.

---

### Dataset 3: Home Credit Default Risk Dataset
- **Dataset Name:** Home Credit Default Risk
- **Direct Working Link:** [https://www.kaggle.com/c/home-credit-default-risk/data](https://www.kaggle.com/c/home-credit-default-risk/data)
- **Source / Platform:** Kaggle / Home Credit Group
- **Licence / Usage Terms:** Competition Open Data Terms (Permitted for academic research and educational demonstration)
- **Available Key Columns:** `SK_ID_CURR`, `TARGET` (1 = default, 0 = non-default), `NAME_CONTRACT_TYPE`, `CODE_GENDER`, `FLAG_OWN_CAR`, `FLAG_OWN_REALTY`, `CNT_CHILDREN`, `AMT_INCOME_TOTAL`, `AMT_CREDIT`, `AMT_ANNUITY`, `NAME_INCOME_TYPE`, `NAME_EDUCATION_TYPE`, `DAYS_BIRTH`, `DAYS_EMPLOYED`, `EXT_SOURCE_1/2/3`.
- **Advantages:**
  - Tailored specifically to unbanked and underserved borrowers with rich risk telemetry.
  - Captures complex repayment dynamics and alternative data points.
- **Limitations:**
  - Multi-table relational complexity (7 distinct CSV files joined by foreign keys) requiring significant data wrangling.
  - Lacks standardized A–G credit rating grades and standard 36/60-month loan terms.
- **Suitability for This Project:** **High (Comparative Reference)**. Great for understanding alternative credit factors, but less suited for standard credit grade and risk-band educational modeling.

---

## 3. Synthetic Dataset Strategy & Academic Labeling Notice

> [!IMPORTANT]
> **SYNTHETIC DATASET DISCLOSURE:**  
> The primary dataset utilized throughout this project (`data/raw/loans_raw.csv` and `data/clean/loans_clean.csv`) is an authentic synthetic dataset generated using Python with fixed pseudorandom seed `42`. It accurately models real-world credit dynamics (FICO distributions, LendingClub grade structures, risk-premium interest rates, and loan default correlations).  
> **Under no circumstances is this synthetic data to be represented as actual personally identifiable banking or customer financial records.** It is formulated solely for software engineering, relational database modeling, BI dashboard development, and university examination purposes.
