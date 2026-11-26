# Data Dictionary: Loan Default Analysis and Risk Dashboard

This data dictionary specifies all 20 verified attributes present in the cleaned banking dataset (`data/clean/loans_clean.csv`). It includes business meanings, star-schema table mappings, data types, nullability, physical units, and validation rules.

| Table | Column | Data Type | Description | Nullability | Units | Example / Rule |
|:---|:---|:---:|:---|:---:|:---:|:---|
| **FACT_LOANS** | `loan_id` | `VARCHAR(20)` | Unique alphanumeric identifier for each loan disbursement contract. | No (Primary Key) | Identifier | Example: LN-100001 | Rule: Must follow regex pattern LN-XXXXXX. Unique constraint. |
| **DIM_CUSTOMER** | `customer_id` | `VARCHAR(20)` | Unique alphanumeric identifier representing an individual borrower. | No (Foreign Key) | Identifier | Example: CUST-10002 | Rule: Must follow regex pattern CUST-XXXXX. Relates to DIM_CUSTOMER. |
| **DIM_CUSTOMER** | `age` | `INTEGER` | Borrower chronological age at the time of loan approval. | No | Years | Example: 22 | Rule: Integer between 18 and 75. |
| **DIM_CUSTOMER** | `gender` | `VARCHAR(10)` | Borrower reported gender identity for fair lending compliance analysis. | No | Categorical | Example: Male | Rule: Permitted values: Male, Female, Other. |
| **DIM_CUSTOMER** | `employment_type` | `VARCHAR(25)` | Primary source of borrower income and occupational status. | No | Categorical | Example: Salaried | Rule: Permitted values: Salaried, Self-Employed, Business, Contract. |
| **DIM_CUSTOMER** | `annual_income` | `NUMERIC(12,2)` | Self-reported and verified annual gross earnings of the primary borrower. | No (Imputed) | USD ($) | Example: 87312.77 | Rule: Positive float >= $15,000. Missing values imputed via employment-grade median. |
| **DIM_CUSTOMER** | `credit_score` | `INTEGER` | Three-digit standard FICO-scale credit score reflecting historical repayment behavior. | No | FICO Score Points | Example: 697 | Rule: Valid range 300 to 850. Scores < 300 or > 850 quarantined. |
| **FACT_LOANS** | `loan_amount` | `NUMERIC(12,2)` | Total principal currency amount disbursed to the borrower at origination. | No | USD ($) | Example: 22900.0 | Rule: Positive float $1,000 to $100,000. Outliers > $150,000 quarantined. |
| **FACT_LOANS** | `loan_term_months` | `INTEGER` | Contractual loan repayment duration in calendar months. | No | Months | Example: 36 | Rule: Restricted strictly to 36 or 60 months. |
| **FACT_LOANS** | `interest_rate` | `NUMERIC(5,2)` | Fixed annual interest rate charged on the loan balance. | No | Percentage (%) | Example: 14.69 | Rule: Float between 5.0% and 32.0%, calibrated to loan risk grade. |
| **DIM_LOAN_PURPOSE** | `loan_purpose` | `VARCHAR(30)` | Designated commercial or personal expenditure purpose stated by borrower. | No (Foreign Key) | Categorical | Example: Credit Card | Rule: Permitted: Debt Consolidation, Credit Card, Home Improvement, Small Business, Major Purchase, Medical, Car. |
| **DIM_LOAN_GRADE** | `loan_grade` | `CHAR(1)` | Underwriting credit rating grade assigned based on credit risk tier. | No (Foreign Key) | Rating Letter | Example: C | Rule: Single letter A, B, C, D, E, F, or G (A = lowest risk, G = highest risk). |
| **FACT_LOANS** | `debt_to_income_ratio` | `NUMERIC(5,2)` | Borrower total monthly debt payments divided by gross monthly income. | No | Percentage (%) | Example: 30.54 | Rule: Float between 2.0% and 60.0%. |
| **DIM_CUSTOMER** | `existing_loans` | `INTEGER` | Number of active credit lines and loans currently held by borrower. | No | Count | Example: 2 | Rule: Non-negative integer between 0 and 10. |
| **DIM_CUSTOMER** | `home_ownership` | `VARCHAR(15)` | Residential housing occupancy and ownership status. | No | Categorical | Example: RENT | Rule: Permitted values: MORTGAGE, RENT, OWN. |
| **DIM_DATE** | `loan_issue_date` | `DATE` | Calendar date when loan funds were formally originated and released. | No (Foreign Key) | YYYY-MM-DD Date | Example: 2023-05-10 | Rule: Valid calendar date between 2021-01-01 and 2024-06-30. |
| **FACT_LOANS** | `loan_status` | `VARCHAR(25)` | Current contractual performance status of the loan contract. | No | Categorical Status | Example: Current | Rule: Permitted: Fully Paid, Charged Off, Default, Current, In Grace Period. |
| **FACT_LOANS** | `total_payment` | `NUMERIC(12,2)` | Cumulative gross monetary payments received from borrower to date. | No | USD ($) | Example: 8876.84 | Rule: Non-negative float. <= Total expected contractual repayment. |
| **FACT_LOANS** | `outstanding_balance` | `NUMERIC(12,2)` | Remaining unpaid loan principal balance currently owed. | No | USD ($) | Example: 16242.37 | Rule: Non-negative float. Equals $0.00 for Fully Paid loans. |
| **FACT_LOANS** | `default_flag` | `INTEGER (0/1)` | Binary indicator specifying whether the loan experienced severe delinquency/default. | No | Binary (0 or 1) | Example: 0 | Rule: 1 if loan_status in ("Charged Off", "Default"); 0 otherwise. |
