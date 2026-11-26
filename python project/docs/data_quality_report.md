# Data Quality & Pipeline Audit Report

**Execution Timestamp:** 2026-11-26 12:22:45  
**Raw Dataset Input:** `C:\Users\rahul\Desktop\HCL PROJECT\loan-default-analysis-risk-dashboard\data\raw\loans_raw.csv` (10,050 records)  
**Clean Dataset Output:** `C:\Users\rahul\Desktop\HCL PROJECT\loan-default-analysis-risk-dashboard\data\clean\loans_clean.csv` (9,901 records)  
**Quarantined Records:** `C:\Users\rahul\Desktop\HCL PROJECT\loan-default-analysis-risk-dashboard\data\clean\loans_quarantine.csv` (149 records)  

## 1. Data Quality Issues & Transformations Log

| Issue Identified | Cleaning Rule Applied | Rows Affected |
|:---|:---|:---:|
| **Duplicate Loan IDs** | Removed duplicate loan records while retaining the first valid entry. | 50 |
| **Inconsistent Text Formatting** | Stripped whitespace and standardized text casing across gender, employment, and home ownership. | 99 |
| **Missing Loan Grades** | Deduce and impute missing credit grade from borrower credit score using standard FICO grade tiers. | 50 |
| **Missing Annual Income** | Imputed missing annual income values with the group median based on employment type and loan grade. | 200 |
| **Inconsistent Loan Status** | Mapped non-standard status strings to canonical banking statuses and synchronized default flags. | 60 |
| **Invalid Credit Scores** | Quarantined records with credit scores outside the valid 300 to 850 range. | 40 |
| **Extreme Loan Amounts** | Quarantined loans with negative amounts, zero amounts, or unrealistic outlier values exceeding $150,000. | 30 |
| **Invalid Issue Dates** | Quarantined unparseable and calendar-invalid date strings. | 29 |

## 2. Before vs. After Data Health Comparison

| Quality Metric | Raw Dataset | Cleaned Dataset | Resolution Status |
|:---|:---:|:---:|:---:|
| **Total Record Count** | 10,050 | 9,901 | Validated |
| **Duplicate Loan IDs** | 50 | 0 | 100% Resolved |
| **Missing Annual Income** | 200 | 0 | Imputed via Group Median |
| **Missing Credit Grades** | 50 | 0 | Deduced via FICO Tiers |
| **Invalid Credit Scores (<300 or >850)** | 40 | 0 | Quarantined |
| **Extreme Loan Amounts (Outliers/Negative)** | 30 | 0 | Quarantined |
| **Invalid Date Formats** | 29 | 0 | Quarantined |
| **Inconsistent Status Labels** | 60 | 0 | Standardized Canonical |

## 3. Quarantined Records Summary

To ensure complete regulatory auditability, unresolvable records were not silently deleted. A total of **149** records were isolated into `C:\Users\rahul\Desktop\HCL PROJECT\loan-default-analysis-risk-dashboard\data\clean\loans_quarantine.csv` with designated diagnostic reason codes for audit review.
