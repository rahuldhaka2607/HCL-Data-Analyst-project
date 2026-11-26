"""
Project No. 6: Loan Default Analysis and Risk Dashboard
Module: Excel Workbook & Analytics Dashboard Generator (P14)
Description: Builds the complete multi-sheet Microsoft Excel workbook
             excel/loan_analysis_dashboard.xlsx using openpyxl with formatted tables,
             KPI summaries, Pivot analyses, and cross-checking formulas.
"""

import os
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_excel_dashboard():
    raw_csv = os.path.join(BASE_DIR, "data", "raw", "loans_raw.csv")
    clean_csv = os.path.join(BASE_DIR, "data", "clean", "loans_clean.csv")
    log_csv = os.path.join(BASE_DIR, "data", "reports", "data_quality_log.csv")
    excel_path = os.path.join(BASE_DIR, "excel", "loan_analysis_dashboard.xlsx")
    
    os.makedirs(os.path.dirname(excel_path), exist_ok=True)
    
    print("Creating Excel workbook...")
    wb = openpyxl.Workbook()
    
    # Common Palette Styles
    navy_fill = PatternFill(start_color="0A192F", end_color="0A192F", fill_type="solid")
    teal_fill = PatternFill(start_color="00B4D8", end_color="00B4D8", fill_type="solid")
    header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    soft_gray = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    
    white_bold = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    white_title = Font(name="Segoe UI", size=14, bold=True, color="FFFFFF")
    navy_bold = Font(name="Segoe UI", size=11, bold=True, color="0A192F")
    standard_font = Font(name="Segoe UI", size=10)
    
    thin_border = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )

    # -------------------------------------------------------------
    # SHEET 1: Dashboard (Executive Summary)
    # -------------------------------------------------------------
    ws_dash = wb.active
    ws_dash.title = "Dashboard"
    ws_dash.views.sheetView[0].showGridLines = True
    
    # Header Banner
    ws_dash.merge_cells("A1:H2")
    banner = ws_dash["A1"]
    banner.value = "LOAN INTELLIGENCE — Executive Credit Risk Dashboard"
    banner.font = white_title
    banner.fill = navy_fill
    banner.alignment = Alignment(horizontal="center", vertical="center")
    
    # KPI Blocks
    kpis = [
        ("TOTAL LOANS", "=COUNTA('Cleaned Data'!A2:A10000)", "$#,##0"),
        ("TOTAL PORTFOLIO ($)", "=SUM('Cleaned Data'!H2:H10000)", "$#,##0"),
        ("ELIGIBLE LOANS", "=COUNTIF('Cleaned Data'!Q2:Q10000, \"Fully Paid\") + COUNTIF('Cleaned Data'!Q2:Q10000, \"Charged Off\") + COUNTIF('Cleaned Data'!Q2:Q10000, \"Default\")", "#,##0"),
        ("DEFAULTED LOANS", "=COUNTIF('Cleaned Data'!T2:T10000, 1)", "#,##0"),
        ("DEFAULT RATE (%)", "=E4/C4", "0.00%"),
        ("AVG LOAN AMOUNT", "=AVERAGE('Cleaned Data'!H2:H10000)", "$#,##0.00"),
        ("AVG CREDIT SCORE", "=AVERAGE('Cleaned Data'!G2:G10000)", "0.0"),
        ("TOTAL OUTSTANDING", "=SUM('Cleaned Data'!S2:S10000)", "$#,##0")
    ]
    
    # Write KPI Tiles
    row_starts = [4, 7]
    col_starts = [("B", "C"), ("D", "E"), ("F", "G"), ("H", "I")]
    
    for idx, (label, formula, num_format) in enumerate(kpis[:4]):
        c1 = col_starts[idx][0]
        ws_dash[f"{c1}4"] = label
        ws_dash[f"{c1}4"].font = navy_bold
        ws_dash[f"{c1}4"].fill = soft_gray
        ws_dash[f"{c1}4"].alignment = Alignment(horizontal="center")
        
        ws_dash[f"{c1}5"] = formula
        ws_dash[f"{c1}5"].font = Font(name="Segoe UI", size=14, bold=True, color="00B4D8")
        ws_dash[f"{c1}5"].number_format = num_format
        ws_dash[f"{c1}5"].alignment = Alignment(horizontal="center")
        
    for idx, (label, formula, num_format) in enumerate(kpis[4:]):
        c1 = col_starts[idx][0]
        ws_dash[f"{c1}7"] = label
        ws_dash[f"{c1}7"].font = navy_bold
        ws_dash[f"{c1}7"].fill = soft_gray
        ws_dash[f"{c1}7"].alignment = Alignment(horizontal="center")
        
        ws_dash[f"{c1}8"] = formula
        ws_dash[f"{c1}8"].font = Font(name="Segoe UI", size=14, bold=True, color="EF476F" if "DEFAULT" in label else "0A192F")
        ws_dash[f"{c1}8"].number_format = num_format
        ws_dash[f"{c1}8"].alignment = Alignment(horizontal="center")

    # Add quick navigation note
    ws_dash["B11"] = "Navigation Guide:"
    ws_dash["B11"].font = Font(name="Segoe UI", size=11, bold=True, color="1E3A8A")
    ws_dash["B12"] = "• Sheet 'Cleaned Data': Full 20-attribute cleansed warehouse dataset."
    ws_dash["B13"] = "• Sheet 'Raw Data': Sample original ingested records showing simulated anomalies."
    ws_dash["B14"] = "• Sheet 'Data Quality': Audit remediation log with rules and row counts."
    ws_dash["B15"] = "• Sheet 'Pivot Analysis': Deep dive default tables across Grade, Income, Purpose, and Trends."
    ws_dash["B16"] = "• Sheet 'KPI Summary': Reconciled cross-check totals matching Python and SQL."

    # -------------------------------------------------------------
    # SHEET 2: Cleaned Data
    # -------------------------------------------------------------
    print("Writing Cleaned Data sheet...")
    ws_clean = wb.create_sheet(title="Cleaned Data")
    with open(clean_csv, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for r_idx, row in enumerate(reader, start=1):
            # Parse numeric cells
            parsed_row = []
            for c_idx, val in enumerate(row):
                if r_idx == 1:
                    parsed_row.append(val)
                else:
                    try:
                        if '.' in val:
                            parsed_row.append(float(val))
                        else:
                            parsed_row.append(int(val))
                    except:
                        parsed_row.append(val)
            ws_clean.append(parsed_row)
            
    # Format header
    for cell in ws_clean[1]:
        cell.fill = navy_fill
        cell.font = white_bold
        cell.alignment = Alignment(horizontal="center")

    # -------------------------------------------------------------
    # SHEET 3: Raw Data (Sample first 200 rows)
    # -------------------------------------------------------------
    print("Writing Raw Data sheet...")
    ws_raw = wb.create_sheet(title="Raw Data")
    with open(raw_csv, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for r_idx, row in enumerate(reader, start=1):
            if r_idx > 250:  # Write first 250 rows for demonstration
                break
            ws_raw.append(row)
            
    for cell in ws_raw[1]:
        cell.fill = header_fill
        cell.font = white_bold
        cell.alignment = Alignment(horizontal="center")

    # -------------------------------------------------------------
    # SHEET 4: Data Quality Log
    # -------------------------------------------------------------
    print("Writing Data Quality sheet...")
    ws_qual = wb.create_sheet(title="Data Quality")
    with open(log_csv, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            ws_qual.append(row)
            
    for cell in ws_qual[1]:
        cell.fill = navy_fill
        cell.font = white_bold
        cell.alignment = Alignment(horizontal="center")
        
    for row in ws_qual.iter_rows(min_row=2, max_col=3):
        for cell in row:
            cell.font = standard_font
            cell.border = thin_border

    # -------------------------------------------------------------
    # SHEET 5: Pivot Analysis (Tabular Formulations)
    # -------------------------------------------------------------
    print("Writing Pivot Analysis sheet...")
    ws_pivot = wb.create_sheet(title="Pivot Analysis")
    
    # 1. Default Rate by Grade Table
    ws_pivot["A1"] = "Analysis 1: Default Rate by Loan Grade"
    ws_pivot["A1"].font = Font(name="Segoe UI", size=12, bold=True, color="0A192F")
    
    headers_g = ["Grade", "Total Loans", "Eligible Closed Loans", "Defaulted Loans", "Default Rate (%)"]
    ws_pivot.append(headers_g)
    for c_idx, h in enumerate(headers_g, start=1):
        cell = ws_pivot.cell(row=2, column=c_idx)
        cell.fill = navy_fill
        cell.font = white_bold
        cell.alignment = Alignment(horizontal="center")
        
    grades = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    for idx, g in enumerate(grades, start=3):
        ws_pivot[f"A{idx}"] = g
        ws_pivot[f"B{idx}"] = f"=COUNTIF('Cleaned Data'!$L$2:$L$10000, A{idx})"
        ws_pivot[f"C{idx}"] = f"=COUNTIFS('Cleaned Data'!$L$2:$L$10000, A{idx}, 'Cleaned Data'!$Q$2:$Q$10000, \"Fully Paid\") + COUNTIFS('Cleaned Data'!$L$2:$L$10000, A{idx}, 'Cleaned Data'!$Q$2:$Q$10000, \"Charged Off\") + COUNTIFS('Cleaned Data'!$L$2:$L$10000, A{idx}, 'Cleaned Data'!$Q$2:$Q$10000, \"Default\")"
        ws_pivot[f"D{idx}"] = f"=COUNTIFS('Cleaned Data'!$L$2:$L$10000, A{idx}, 'Cleaned Data'!$T$2:$T$10000, 1)"
        ws_pivot[f"E{idx}"] = f"=D{idx}/C{idx}"
        ws_pivot[f"E{idx}"].number_format = "0.00%"
        
    # 2. Default Rate by Income Band Table
    ws_pivot["A12"] = "Analysis 2: Default Rate by Annual Income Band"
    ws_pivot["A12"].font = Font(name="Segoe UI", size=12, bold=True, color="0A192F")
    
    headers_inc = ["Income Band", "Total Loans", "Eligible Closed Loans", "Defaulted Loans", "Default Rate (%)"]
    ws_pivot.cell(row=13, column=1, value=headers_inc[0])
    for c_idx, h in enumerate(headers_inc, start=1):
        cell = ws_pivot.cell(row=13, column=c_idx, value=h)
        cell.fill = header_fill
        cell.font = white_bold
        cell.alignment = Alignment(horizontal="center")
        
    income_rows = [
        ("< $35,000", "<35000", "<=0"),
        ("$35,000 - $60,000", ">=35000", "<60000"),
        ("$60,000 - $100,000", ">=60000", "<100000"),
        ("> $100,000", ">=100000", "")
    ]
    
    ws_pivot["A14"] = "< $35,000"
    ws_pivot["B14"] = "=COUNTIF('Cleaned Data'!$F$2:$F$10000, \"<35000\")"
    ws_pivot["C14"] = "=COUNTIFS('Cleaned Data'!$F$2:$F$10000, \"<35000\", 'Cleaned Data'!$Q$2:$Q$10000, \"Fully Paid\") + COUNTIFS('Cleaned Data'!$F$2:$F$10000, \"<35000\", 'Cleaned Data'!$Q$2:$Q$10000, \"Charged Off\") + COUNTIFS('Cleaned Data'!$F$2:$F$10000, \"<35000\", 'Cleaned Data'!$Q$2:$Q$10000, \"Default\")"
    ws_pivot["D14"] = "=COUNTIFS('Cleaned Data'!$F$2:$F$10000, \"<35000\", 'Cleaned Data'!$T$2:$T$10000, 1)"
    ws_pivot["E14"] = "=D14/C14"
    ws_pivot["E14"].number_format = "0.00%"

    ws_pivot["A15"] = "$35,000 - $60,000"
    ws_pivot["B15"] = "=COUNTIFS('Cleaned Data'!$F$2:$F$10000, \">=35000\", 'Cleaned Data'!$F$2:$F$10000, \"<60000\")"
    ws_pivot["C15"] = "=COUNTIFS('Cleaned Data'!$F$2:$F$10000, \">=35000\", 'Cleaned Data'!$F$2:$F$10000, \"<60000\", 'Cleaned Data'!$T$2:$T$10000, 0) + COUNTIFS('Cleaned Data'!$F$2:$F$10000, \">=35000\", 'Cleaned Data'!$F$2:$F$10000, \"<60000\", 'Cleaned Data'!$T$2:$T$10000, 1)"
    ws_pivot["D15"] = "=COUNTIFS('Cleaned Data'!$F$2:$F$10000, \">=35000\", 'Cleaned Data'!$F$2:$F$10000, \"<60000\", 'Cleaned Data'!$T$2:$T$10000, 1)"
    ws_pivot["E15"] = "=D15/C15"
    ws_pivot["E15"].number_format = "0.00%"

    ws_pivot["A16"] = "$60,000 - $100,000"
    ws_pivot["B16"] = "=COUNTIFS('Cleaned Data'!$F$2:$F$10000, \">=60000\", 'Cleaned Data'!$F$2:$F$10000, \"<100000\")"
    ws_pivot["C16"] = "=COUNTIFS('Cleaned Data'!$F$2:$F$10000, \">=60000\", 'Cleaned Data'!$F$2:$F$10000, \"<100000\", 'Cleaned Data'!$T$2:$T$10000, 0) + COUNTIFS('Cleaned Data'!$F$2:$F$10000, \">=60000\", 'Cleaned Data'!$F$2:$F$10000, \"<100000\", 'Cleaned Data'!$T$2:$T$10000, 1)"
    ws_pivot["D16"] = "=COUNTIFS('Cleaned Data'!$F$2:$F$10000, \">=60000\", 'Cleaned Data'!$F$2:$F$10000, \"<100000\", 'Cleaned Data'!$T$2:$T$10000, 1)"
    ws_pivot["E16"] = "=D16/C16"
    ws_pivot["E16"].number_format = "0.00%"

    ws_pivot["A17"] = "> $100,000"
    ws_pivot["B17"] = "=COUNTIF('Cleaned Data'!$F$2:$F$10000, \">=100000\")"
    ws_pivot["C17"] = "=COUNTIFS('Cleaned Data'!$F$2:$F$10000, \">=100000\", 'Cleaned Data'!$T$2:$T$10000, 0) + COUNTIFS('Cleaned Data'!$F$2:$F$10000, \">=100000\", 'Cleaned Data'!$T$2:$T$10000, 1)"
    ws_pivot["D17"] = "=COUNTIFS('Cleaned Data'!$F$2:$F$10000, \">=100000\", 'Cleaned Data'!$T$2:$T$10000, 1)"
    ws_pivot["E17"] = "=D17/C17"
    ws_pivot["E17"].number_format = "0.00%"

    # 3. Default Rate by Purpose Table
    ws_pivot["A20"] = "Analysis 3: Default Rate by Loan Purpose"
    ws_pivot["A20"].font = Font(name="Segoe UI", size=12, bold=True, color="0A192F")
    
    headers_p = ["Loan Purpose", "Total Loans", "Eligible Closed Loans", "Defaulted Loans", "Default Rate (%)"]
    for c_idx, h in enumerate(headers_p, start=1):
        cell = ws_pivot.cell(row=21, column=c_idx, value=h)
        cell.fill = navy_fill
        cell.font = white_bold
        cell.alignment = Alignment(horizontal="center")
        
    purposes = ['Debt Consolidation', 'Credit Card', 'Home Improvement', 'Small Business', 'Major Purchase', 'Medical', 'Car']
    for idx, p in enumerate(purposes, start=22):
        ws_pivot[f"A{idx}"] = p
        ws_pivot[f"B{idx}"] = f"=COUNTIF('Cleaned Data'!$K$2:$K$10000, A{idx})"
        ws_pivot[f"C{idx}"] = f"=COUNTIFS('Cleaned Data'!$K$2:$K$10000, A{idx}, 'Cleaned Data'!$Q$2:$Q$10000, \"Fully Paid\") + COUNTIFS('Cleaned Data'!$K$2:$K$10000, A{idx}, 'Cleaned Data'!$Q$2:$Q$10000, \"Charged Off\") + COUNTIFS('Cleaned Data'!$K$2:$K$10000, A{idx}, 'Cleaned Data'!$Q$2:$Q$10000, \"Default\")"
        ws_pivot[f"D{idx}"] = f"=COUNTIFS('Cleaned Data'!$K$2:$K$10000, A{idx}, 'Cleaned Data'!$T$2:$T$10000, 1)"
        ws_pivot[f"E{idx}"] = f"=D{idx}/C{idx}"
        ws_pivot[f"E{idx}"].number_format = "0.00%"

    # -------------------------------------------------------------
    # SHEET 6: KPI Summary
    # -------------------------------------------------------------
    print("Writing KPI Summary sheet...")
    ws_kpi = wb.create_sheet(title="KPI Summary")
    
    ws_kpi["A1"] = "Executive Financial Metric"
    ws_kpi["B1"] = "Formulated Excel Calculation"
    ws_kpi["C1"] = "Verification Target"
    for c in ["A1", "B1", "C1"]:
        ws_kpi[c].fill = navy_fill
        ws_kpi[c].font = white_bold
        ws_kpi[c].alignment = Alignment(horizontal="center")
        
    summary_items = [
        ("Total Originated Loans", "=COUNTA('Cleaned Data'!A2:A10000)", "9,901"),
        ("Total Disbursed Volume ($)", "=SUM('Cleaned Data'!H2:H10000)", "$185,373,300.00"),
        ("Eligible Closed Loans", "=COUNTIF('Cleaned Data'!Q2:Q10000, \"Fully Paid\") + COUNTIF('Cleaned Data'!Q2:Q10000, \"Charged Off\") + COUNTIF('Cleaned Data'!Q2:Q10000, \"Default\")", "2,847"),
        ("Total Defaulted Loans", "=COUNTIF('Cleaned Data'!T2:T10000, 1)", "2,243"),
        ("Overall Default Rate (%)", "=B5/B4", "78.78%"),
        ("Average Loan Size ($)", "=AVERAGE('Cleaned Data'!H2:H10000)", "$18,722.68"),
        ("Average Credit Score", "=AVERAGE('Cleaned Data'!G2:G10000)", "683.1"),
        ("Total Outstanding Balance ($)", "=SUM('Cleaned Data'!S2:S10000)", "$118,836,026.27")
    ]
    
    for r_idx, (m_name, m_form, m_target) in enumerate(summary_items, start=2):
        ws_kpi[f"A{r_idx}"] = m_name
        ws_kpi[f"B{r_idx}"] = m_form
        ws_kpi[f"C{r_idx}"] = m_target
        ws_kpi[f"A{r_idx}"].font = navy_bold
        ws_kpi[f"B{r_idx}"].font = standard_font
        ws_kpi[f"C{r_idx}"].font = Font(name="Segoe UI", size=10, bold=True, color="00B4D8")
        
        # Format types
        if "$" in m_target:
            ws_kpi[f"B{r_idx}"].number_format = "$#,##0.00"
        elif "%" in m_target:
            ws_kpi[f"B{r_idx}"].number_format = "0.00%"
        else:
            ws_kpi[f"B{r_idx}"].number_format = "#,##0"

    # Adjust all column widths
    for ws in [ws_dash, ws_clean, ws_raw, ws_qual, ws_pivot, ws_kpi]:
        for col in ws.columns:
            col_letter = get_column_letter(col[0].column)
            max_len = max(len(str(cell.value or '')) for cell in col[:50])
            ws.column_dimensions[col_letter].width = min(45, max(max_len + 3, 12))

    wb.save(excel_path)
    print(f"SUCCESS: Saved multi-sheet Excel analytical workbook to {excel_path}")

if __name__ == "__main__":
    generate_excel_dashboard()
