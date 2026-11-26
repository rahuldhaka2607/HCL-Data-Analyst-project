"""
Project No. 6: Loan Default Analysis and Risk Dashboard
Module: Data Dictionary Generator (P5)
Description: Inspects actual CSV dataset headers, data types, and sample records to produce
             docs/data_dictionary.md and docs/data_dictionary.xlsx using openpyxl.
"""

import os
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_data_dictionary():
    clean_csv_path = os.path.join(BASE_DIR, "data", "clean", "loans_clean.csv")
    md_path = os.path.join(BASE_DIR, "docs", "data_dictionary.md")
    xlsx_path = os.path.join(BASE_DIR, "docs", "data_dictionary.xlsx")
    
    if not os.path.exists(clean_csv_path):
        print(f"Error: {clean_csv_path} does not exist yet. Run cleaning pipeline first.")
        return
        
    with open(clean_csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        sample_row = next(reader)
        
    print(f"Inspecting dataset with {len(fieldnames)} columns. Sample loan_id: {sample_row.get('loan_id')}")
    
    metadata = {
        'loan_id': {
            'table': 'FACT_LOANS',
            'type': 'VARCHAR(20)',
            'desc': 'Unique alphanumeric identifier for each loan disbursement contract.',
            'nullability': 'No (Primary Key)',
            'units': 'Identifier',
            'rule': 'Must follow regex pattern LN-XXXXXX. Unique constraint.'
        },
        'customer_id': {
            'table': 'DIM_CUSTOMER',
            'type': 'VARCHAR(20)',
            'desc': 'Unique alphanumeric identifier representing an individual borrower.',
            'nullability': 'No (Foreign Key)',
            'units': 'Identifier',
            'rule': 'Must follow regex pattern CUST-XXXXX. Relates to DIM_CUSTOMER.'
        },
        'age': {
            'table': 'DIM_CUSTOMER',
            'type': 'INTEGER',
            'desc': 'Borrower chronological age at the time of loan approval.',
            'nullability': 'No',
            'units': 'Years',
            'rule': 'Integer between 18 and 75.'
        },
        'gender': {
            'table': 'DIM_CUSTOMER',
            'type': 'VARCHAR(10)',
            'desc': 'Borrower reported gender identity for fair lending compliance analysis.',
            'nullability': 'No',
            'units': 'Categorical',
            'rule': 'Permitted values: Male, Female, Other.'
        },
        'employment_type': {
            'table': 'DIM_CUSTOMER',
            'type': 'VARCHAR(25)',
            'desc': 'Primary source of borrower income and occupational status.',
            'nullability': 'No',
            'units': 'Categorical',
            'rule': 'Permitted values: Salaried, Self-Employed, Business, Contract.'
        },
        'annual_income': {
            'table': 'DIM_CUSTOMER',
            'type': 'NUMERIC(12,2)',
            'desc': 'Self-reported and verified annual gross earnings of the primary borrower.',
            'nullability': 'No (Imputed)',
            'units': 'USD ($)',
            'rule': 'Positive float >= $15,000. Missing values imputed via employment-grade median.'
        },
        'credit_score': {
            'table': 'DIM_CUSTOMER',
            'type': 'INTEGER',
            'desc': 'Three-digit standard FICO-scale credit score reflecting historical repayment behavior.',
            'nullability': 'No',
            'units': 'FICO Score Points',
            'rule': 'Valid range 300 to 850. Scores < 300 or > 850 quarantined.'
        },
        'loan_amount': {
            'table': 'FACT_LOANS',
            'type': 'NUMERIC(12,2)',
            'desc': 'Total principal currency amount disbursed to the borrower at origination.',
            'nullability': 'No',
            'units': 'USD ($)',
            'rule': 'Positive float $1,000 to $100,000. Outliers > $150,000 quarantined.'
        },
        'loan_term_months': {
            'table': 'FACT_LOANS',
            'type': 'INTEGER',
            'desc': 'Contractual loan repayment duration in calendar months.',
            'nullability': 'No',
            'units': 'Months',
            'rule': 'Restricted strictly to 36 or 60 months.'
        },
        'interest_rate': {
            'table': 'FACT_LOANS',
            'type': 'NUMERIC(5,2)',
            'desc': 'Fixed annual interest rate charged on the loan balance.',
            'nullability': 'No',
            'units': 'Percentage (%)',
            'rule': 'Float between 5.0% and 32.0%, calibrated to loan risk grade.'
        },
        'loan_purpose': {
            'table': 'DIM_LOAN_PURPOSE',
            'type': 'VARCHAR(30)',
            'desc': 'Designated commercial or personal expenditure purpose stated by borrower.',
            'nullability': 'No (Foreign Key)',
            'units': 'Categorical',
            'rule': 'Permitted: Debt Consolidation, Credit Card, Home Improvement, Small Business, Major Purchase, Medical, Car.'
        },
        'loan_grade': {
            'table': 'DIM_LOAN_GRADE',
            'type': 'CHAR(1)',
            'desc': 'Underwriting credit rating grade assigned based on credit risk tier.',
            'nullability': 'No (Foreign Key)',
            'units': 'Rating Letter',
            'rule': 'Single letter A, B, C, D, E, F, or G (A = lowest risk, G = highest risk).'
        },
        'debt_to_income_ratio': {
            'table': 'FACT_LOANS',
            'type': 'NUMERIC(5,2)',
            'desc': 'Borrower total monthly debt payments divided by gross monthly income.',
            'nullability': 'No',
            'units': 'Percentage (%)',
            'rule': 'Float between 2.0% and 60.0%.'
        },
        'existing_loans': {
            'table': 'DIM_CUSTOMER',
            'type': 'INTEGER',
            'desc': 'Number of active credit lines and loans currently held by borrower.',
            'nullability': 'No',
            'units': 'Count',
            'rule': 'Non-negative integer between 0 and 10.'
        },
        'home_ownership': {
            'table': 'DIM_CUSTOMER',
            'type': 'VARCHAR(15)',
            'desc': 'Residential housing occupancy and ownership status.',
            'nullability': 'No',
            'units': 'Categorical',
            'rule': 'Permitted values: MORTGAGE, RENT, OWN.'
        },
        'loan_issue_date': {
            'table': 'DIM_DATE',
            'type': 'DATE',
            'desc': 'Calendar date when loan funds were formally originated and released.',
            'nullability': 'No (Foreign Key)',
            'units': 'YYYY-MM-DD Date',
            'rule': 'Valid calendar date between 2021-01-01 and 2024-06-30.'
        },
        'loan_status': {
            'table': 'FACT_LOANS',
            'type': 'VARCHAR(25)',
            'desc': 'Current contractual performance status of the loan contract.',
            'nullability': 'No',
            'units': 'Categorical Status',
            'rule': 'Permitted: Fully Paid, Charged Off, Default, Current, In Grace Period.'
        },
        'total_payment': {
            'table': 'FACT_LOANS',
            'type': 'NUMERIC(12,2)',
            'desc': 'Cumulative gross monetary payments received from borrower to date.',
            'nullability': 'No',
            'units': 'USD ($)',
            'rule': 'Non-negative float. <= Total expected contractual repayment.'
        },
        'outstanding_balance': {
            'table': 'FACT_LOANS',
            'type': 'NUMERIC(12,2)',
            'desc': 'Remaining unpaid loan principal balance currently owed.',
            'nullability': 'No',
            'units': 'USD ($)',
            'rule': 'Non-negative float. Equals $0.00 for Fully Paid loans.'
        },
        'default_flag': {
            'table': 'FACT_LOANS',
            'type': 'INTEGER (0/1)',
            'desc': 'Binary indicator specifying whether the loan experienced severe delinquency/default.',
            'nullability': 'No',
            'units': 'Binary (0 or 1)',
            'rule': '1 if loan_status in ("Charged Off", "Default"); 0 otherwise.'
        }
    }
    
    rows = []
    for col in fieldnames:
        meta = metadata.get(col, {
            'table': 'FACT_LOANS',
            'type': 'VARCHAR(50)',
            'desc': 'General loan attribute',
            'nullability': 'No',
            'units': 'Standard',
            'rule': 'None'
        })
        sample_val = str(sample_row.get(col, ''))
        rows.append({
            'Table': meta['table'],
            'Column': col,
            'Data Type': meta['type'],
            'Description': meta['desc'],
            'Nullability': meta['nullability'],
            'Units': meta['units'],
            'Example / Rule': f"Example: {sample_val} | Rule: {meta['rule']}"
        })
        
    # Build Excel Workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Data_Dictionary"
    
    headers = ['Table', 'Column', 'Data Type', 'Description', 'Nullability', 'Units', 'Example / Rule']
    ws.append(headers)
    
    # Styling
    header_fill = PatternFill(start_color="0A192F", end_color="0A192F", fill_type="solid")
    header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Segoe UI", size=10)
    
    for col_num in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    for r in rows:
        ws.append([r['Table'], r['Column'], r['Data Type'], r['Description'], r['Nullability'], r['Units'], r['Example / Rule']])
        
    for row in ws.iter_rows(min_row=2, max_row=len(rows)+1, min_col=1, max_col=len(headers)):
        for cell in row:
            cell.font = data_font
            cell.alignment = Alignment(vertical="center")
            
    # Auto-adjust column widths
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = openpyxl.utils.get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = min(60, max(max_len + 3, 12))
        
    wb.save(xlsx_path)
    print(f"SUCCESS: Exported data dictionary Excel to {xlsx_path}")
    
    # Build Markdown Document
    with open(md_path, mode='w', encoding='utf-8') as f:
        f.write("# Data Dictionary: Loan Default Analysis and Risk Dashboard\n\n")
        f.write("This data dictionary specifies all 20 verified attributes present in the cleaned banking dataset (`data/clean/loans_clean.csv`). ")
        f.write("It includes business meanings, star-schema table mappings, data types, nullability, physical units, and validation rules.\n\n")
        f.write("| Table | Column | Data Type | Description | Nullability | Units | Example / Rule |\n")
        f.write("|:---|:---|:---:|:---|:---:|:---:|:---|\n")
        for r in rows:
            f.write(f"| **{r['Table']}** | `{r['Column']}` | `{r['Data Type']}` | {r['Description']} | {r['Nullability']} | {r['Units']} | {r['Example / Rule']} |\n")
            
    print(f"SUCCESS: Exported data dictionary Markdown to {md_path}")

if __name__ == "__main__":
    generate_data_dictionary()
