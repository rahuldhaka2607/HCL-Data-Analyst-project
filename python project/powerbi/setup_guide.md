# Microsoft Power BI Desktop: Complete Implementation & Setup Guide

**Project No. 6:** Loan Default Analysis and Risk Dashboard  
**Academic Target:** B.Tech 2nd Year CSE Evaluation & Viva Defense  

---

## 1. Overview and Prerequisites
This setup guide provides step-by-step instructions to construct the official 4-page Power BI Dashboard for Project No. 6 using **Microsoft Power BI Desktop**.

### Prerequisites:
- Microsoft Power BI Desktop (Free download from Microsoft Store or official website).
- Cleaned dataset file: `data/clean/loans_clean.csv`.
- DAX measures file: `powerbi/dax_measures.dax`.
- Dimensional Architecture: `powerbi/data_model.md`.

---

## 2. Step 1: Data Ingestion via Power Query

1. Launch **Power BI Desktop**.
2. On the Home ribbon, click **Get Data** $\rightarrow$ **Text/CSV**.
3. Navigate to `loan-default-analysis-risk-dashboard/data/clean/loans_clean.csv` and click **Open**.
4. In the preview dialog, click **Transform Data** to open the **Power Query Editor**.
5. Verify column data types in the Applied Steps:
   - `loan_id`, `customer_id`, `gender`, `employment_type`, `home_ownership`, `loan_purpose`, `loan_grade`, `loan_status`: **Text**.
   - `age`, `credit_score`, `loan_term_months`, `existing_loans`, `default_flag`: **Whole Number** (`Int64.Type`).
   - `annual_income`, `loan_amount`, `interest_rate`, `debt_to_income_ratio`, `total_payment`, `outstanding_balance`: **Decimal Number** (`type number`).
   - `loan_issue_date`: **Date** (`type date`).
6. Click **Close & Apply** to load the dataset into the Power BI Data Model.

---

## 3. Step 2: Creating Dimension Tables and Star Schema

To implement the industry-standard Star Schema:

### Creating the Date Dimension (`DIM_DATE`):
On the Modeling ribbon, click **New Table** and paste the following DAX:
```dax
DIM_DATE = 
ADDCOLUMNS(
    CALENDAR(MIN(loans_clean[loan_issue_date]), MAX(loans_clean[loan_issue_date])),
    "Date_ID", FORMAT([Date], "YYYY-MM-DD"),
    "Year", YEAR([Date]),
    "Month_Number", MONTH([Date]),
    "Month_Name", FORMAT([Date], "MMMM"),
    "Year_Month", FORMAT([Date], "YYYY-MM"),
    "Quarter", "Q" & FORMAT([Date], "Q")
)
```
Mark `DIM_DATE` as a Date Table: Right-click `DIM_DATE` $\rightarrow$ **Mark as date table** $\rightarrow$ select `[Date]`.

### Creating Relationships in Model View:
1. Switch to **Model View** (icon on the left navigation bar).
2. Create single-direction 1-to-Many relationships:
   - Drag `DIM_DATE[Date]` to `loans_clean[loan_issue_date]` (1 to *).
3. Confirm active cardinality is `1 to Many` with filter direction set to `Single`.

---

## 4. Step 3: DAX Measures Implementation

1. In the Report View, click **Enter Data** on the Home ribbon to create a dedicated measure container named `_Measures`.
2. Right-click `_Measures` $\rightarrow$ **New Measure**, and copy each measure from `powerbi/dax_measures.dax`:
   - `Total Loans`
   - `Total Loan Amount`
   - `Total Borrowers`
   - `Defaulted Loans`
   - `Eligible Loans`
   - `Default Rate` (Format as **Percentage** with 2 decimals)
   - `Average Loan Amount` (Format as **Currency**)
   - `Average Credit Score` (Format as **Decimal**)
   - `Outstanding Balance` (Format as **Currency**)
   - `Default Rate by Grade`
   - `Default Rate by Income Band`
   - `Default Rate by Purpose`

---

## 5. Step 4: 4-Page Report Design & Visual Layout

### PAGE 1: Executive Overview
- **Header:** Title: "LOAN INTELLIGENCE - Executive Overview".
- **Top Cards Row (4 KPI Cards):**
  1. Card: `[Total Loans]` with subtitle `[Total Loan Amount]`.
  2. Card: `[Default Rate]` formatted in red `#EF476F`.
  3. Card: `[Average Credit Score]` formatted in dark navy `#0A192F`.
  4. Card: `[Outstanding Balance]` formatted in teal `#00B4D8`.
- **Visual 1 (Donut Chart):** `loans_clean[loan_status]` by `[Total Loans]` (Shows composition of Fully Paid, Charged Off, Current).
- **Visual 2 (Clustered Column Chart):** `loans_clean[loan_grade]` on X-axis, `[Default Rate]` on Y-axis.
- **Visual 3 (Line Chart):** `DIM_DATE[Year_Month]` on X-axis, `[Default Rate]` and `[Total Loan Amount]` on Y-axis.
- **Slicers Panel:** Dropdown slicers for `loan_grade`, `loan_purpose`, and `loan_issue_date` range.

### PAGE 2: Default Analysis
- **Visual 1 (Bar Chart):** Default Rate by Loan Grade (A to G).
- **Visual 2 (Column Chart):** Default Rate by Income Band (`< $35,000`, `$35,000 - $60,000`, etc.).
- **Visual 3 (Horizontal Bar Chart):** Default Rate by Loan Purpose (Small Business, Debt Consolidation, etc.).
- **Visual 4 (Matrix Table):** Rows: `loan_grade`, Columns: `loan_purpose`, Values: `[Default Rate]`, with conditional formatting data bars.

### PAGE 3: Borrower Risk Analysis
- **Visual 1 (Treemap):** Grouped by `risk_category` (`Low`, `Moderate`, `High`, `Critical Risk`), size by `[Total Loan Amount]`, color by `[Default Rate]`.
- **Visual 2 (Scatter Plot):** X-axis: `credit_score`, Y-axis: `debt_to_income_ratio`, bubble size: `loan_amount`, color: `default_flag`.
- **Visual 3 (Table / Detail View):** High-risk borrower roster showing `loan_id`, `customer_id`, `credit_score`, `dti`, `loan_amount`, and `status`.

### PAGE 4: Portfolio and Data Quality
- **Visual 1 (Stacked Area Chart):** Cumulative Repayments vs. Outstanding Balances over time.
- **Visual 2 (Card Metrics):** Raw Records (10,050), Clean Records (9,901), Quarantined (149).
- **Visual 3 (Table):** Summary of data quality remediation rules from `data_quality_log.csv`.

---

## 6. Step 5: Configuring Drill-Down & Drill-Through

1. **Drill-Down Hierarchy on Page 2:**
   - In the Bar Chart visual, add `loan_grade` as level 1, `loan_status` as level 2, and `loan_id` as level 3 in the Axis field well.
   - Click the **Drill Down** double arrow icon on the visual header to test hierarchical navigation.
2. **Drill-Through Page:**
   - Create a new tab named `Loan_Detail_Drillthrough`.
   - In the Format pane, set **Page Type** $\rightarrow$ **Drillthrough**.
   - Drag `loans_clean[loan_grade]` into the Drillthrough fields well.
   - Now, right-clicking any grade on Page 1 or 2 allows selecting **Drill through $\rightarrow$ Loan_Detail_Drillthrough** to view loan-level contracts.

---

## 7. Step 6: Professional Color Palette & Accessibility Guidance

- **Primary Dark Navy:** `#0A192F` (Headers, titles, primary cards).
- **Secondary Slate Blue:** `#1E3A8A` (Axis titles, standard bars).
- **Accent Teal:** `#00B4D8` (Low risk, performing assets).
- **Warning Amber:** `#FFD166` (Moderate risk, watch list).
- **Alert Red / Coral:** `#EF476F` (Defaulted loans, critical risk).
- **Background Canvas:** `#F8F9FA` (Clean, professional neutral contrast).
