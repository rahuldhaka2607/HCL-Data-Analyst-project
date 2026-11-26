# Risk Band Documentation & Methodology

**Project:** Loan Default Analysis and Risk Dashboard  
**Domain:** Credit Risk Analytics & Portfolio Management  

---

## 1. Overview of Risk Banding

Risk banding is a fundamental credit risk management technique used by commercial and retail banks to segment borrowers into clear, actionable risk tiers based on their creditworthiness and repayment capacity. 

In this project, we implement a **4-Tier Hybrid Risk Scoring Model** combining:
1. **Credit Score (FICO-style range 300 to 850):** Reflects historical credit discipline and repayment reliability.
2. **Debt-to-Income Ratio (DTI %):** Reflects current debt burden relative to monthly gross earnings.

---

## 2. Risk Band Definitions & Criteria

| Risk Tier | Risk Label | Credit Score Range | Debt-to-Income (DTI) Threshold | Business Meaning & Underwriting Action |
|:---|:---:|:---:|:---:|:---|
| **Tier 1** | **Low Risk** | $\ge 720$ | $\le 20.0\%$ | Prime borrowers with excellent credit history and low debt burden. Eligible for prime interest rates and instant approval. |
| **Tier 2** | **Moderate Risk** | $660 \le \text{Score} < 720$ | $\le 35.0\%$ | Near-prime borrowers with steady financial behavior. Standard underwriting, standard interest rates. |
| **Tier 3** | **High Risk** | $580 \le \text{Score} < 660$ | $35.0\% < \text{DTI} \le 45.0\%$ | Subprime borrowers or borrowers with strained cash flows. Requires additional collateral, guarantor, or risk-premium interest rate. |
| **Tier 4** | **Critical Risk** | $< 580$ | $> 45.0\%$ | Deep subprime or severely over-leveraged borrowers. High default probability; subject to rejection or strict restructuring. |

*Note on Hybrid Logic:* A borrower is assigned to the most severe risk category triggered by either their Credit Score or their DTI, enforcing conservative banking risk practices.

---

## 3. Mathematical & Logical Implementation

### Python Logic (Pandas Vectorized)
```python
def assign_risk_category(df):
    conditions = [
        (df['credit_score'] < 580) | (df['debt_to_income_ratio'] > 45.0),
        (df['credit_score'] < 660) | (df['debt_to_income_ratio'] > 35.0),
        (df['credit_score'] < 720) | (df['debt_to_income_ratio'] > 20.0)
    ]
    choices = ['Critical Risk', 'High Risk', 'Moderate Risk']
    return np.select(conditions, choices, default='Low Risk')
```

### SQL Implementation (`CASE` Statement)
```sql
CASE
    WHEN credit_score < 580 OR debt_to_income_ratio > 45.0 THEN 'Critical Risk'
    WHEN credit_score < 660 OR debt_to_income_ratio > 35.0 THEN 'High Risk'
    WHEN credit_score < 720 OR debt_to_income_ratio > 20.0 THEN 'Moderate Risk'
    ELSE 'Low Risk'
END AS risk_category
```

### Power BI DAX Calculated Column
```dax
Risk_Category = 
SWITCH(
    TRUE(),
    DIM_CUSTOMER[credit_score] < 580 || FACT_LOANS[debt_to_income_ratio] > 45.0, "Critical Risk",
    DIM_CUSTOMER[credit_score] < 660 || FACT_LOANS[debt_to_income_ratio] > 35.0, "High Risk",
    DIM_CUSTOMER[credit_score] < 720 || FACT_LOANS[debt_to_income_ratio] > 20.0, "Moderate Risk",
    "Low Risk"
)
```

---

## 4. Default Definition & Denominator Standard

To ensure consistency across Python, SQL, Excel, and Power BI:
- **Defaulted Loans (`default_flag = 1`):** Loans marked with `loan_status` in `('Charged Off', 'Default')`.
- **Non-Defaulted Closed Loans (`default_flag = 0`):** Loans marked as `'Fully Paid'`.
- **Eligible Loans Denominator:** All completed/closed loan agreements (`Fully Paid` + `Charged Off` + `Default`).
- **Active Portfolio (`Current`, `In Grace Period`):** Tracked separately in active portfolio KPI cards and excluded from historical default rate calculations to prevent artificial default rate dilution.
