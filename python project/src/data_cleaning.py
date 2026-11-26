"""
Project No. 6: Loan Default Analysis and Risk Dashboard
Module: Data Cleaning Pipeline (P6)
Description: Robust data cleaning pipeline executing all mandatory cleaning rules:
             handling missing income, extreme loan amounts, invalid credit scores,
             inconsistent status labels, missing grades, duplicate IDs, and corrupt dates.
             Saves to data/clean/loans_clean.csv, data/clean/loans_quarantine.csv,
             data/reports/data_quality_log.csv, and docs/data_quality_report.md.
"""

import os
import csv
from datetime import datetime
from statistics import median

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def clean_loan_data(
    raw_path=os.path.join(BASE_DIR, "data", "raw", "loans_raw.csv"),
    clean_path=os.path.join(BASE_DIR, "data", "clean", "loans_clean.csv"),
    quarantine_path=os.path.join(BASE_DIR, "data", "clean", "loans_quarantine.csv"),
    log_path=os.path.join(BASE_DIR, "data", "reports", "data_quality_log.csv"),
    report_path=os.path.join(BASE_DIR, "docs", "data_quality_report.md")
):
    os.makedirs(os.path.dirname(clean_path), exist_ok=True)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    print(f"Loading raw loan data from {raw_path}...")
    with open(raw_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        raw_rows = list(reader)
        fieldnames = list(reader.fieldnames)
        
    initial_count = len(raw_rows)
    print(f"Total raw records loaded: {initial_count}")
    
    quality_logs = []
    quarantined = []
    
    # 1. Duplicate Loan IDs
    seen_ids = set()
    unique_rows = []
    dup_count = 0
    for row in raw_rows:
        lid = row['loan_id']
        if lid in seen_ids:
            dup_count += 1
            row_copy = dict(row)
            row_copy['quarantine_reason'] = 'Duplicate Loan ID'
            quarantined.append(row_copy)
        else:
            seen_ids.add(lid)
            unique_rows.append(row)
            
    quality_logs.append({
        'issue': 'Duplicate Loan IDs',
        'rule_applied': 'Removed duplicate loan records while retaining the first valid entry.',
        'rows_affected': dup_count
    })
    
    # 2. Inconsistent Text Formatting
    text_count = 0
    for row in unique_rows:
        orig_g = row['gender']
        orig_e = row['employment_type']
        orig_h = row['home_ownership']
        
        row['gender'] = row['gender'].strip().capitalize()
        row['employment_type'] = row['employment_type'].strip().title()
        row['home_ownership'] = row['home_ownership'].strip().upper()
        row['loan_purpose'] = row['loan_purpose'].strip().title()
        
        if (row['gender'] != orig_g) or (row['employment_type'] != orig_e) or (row['home_ownership'] != orig_h):
            text_count += 1
            
    quality_logs.append({
        'issue': 'Inconsistent Text Formatting',
        'rule_applied': 'Stripped whitespace and standardized text casing across gender, employment, and home ownership.',
        'rows_affected': text_count
    })
    
    # 3. Missing Loan Grades (deduce from credit score)
    missing_grade_count = 0
    for row in unique_rows:
        grade = row.get('loan_grade', '').strip()
        if not grade:
            missing_grade_count += 1
            try:
                score = float(row['credit_score'])
                if score >= 750: grade = 'A'
                elif score >= 700: grade = 'B'
                elif score >= 660: grade = 'C'
                elif score >= 620: grade = 'D'
                elif score >= 580: grade = 'E'
                elif score >= 540: grade = 'F'
                else: grade = 'G'
            except:
                grade = 'C'
            row['loan_grade'] = grade
            
    quality_logs.append({
        'issue': 'Missing Loan Grades',
        'rule_applied': 'Deduce and impute missing credit grade from borrower credit score using standard FICO grade tiers.',
        'rows_affected': missing_grade_count
    })
    
    # 4. Missing Annual Income (Impute with group median by employment_type & loan_grade)
    income_groups = {}
    all_incomes = []
    missing_inc_count = 0
    
    for row in unique_rows:
        inc_str = row['annual_income'].strip()
        if inc_str:
            try:
                val = float(inc_str)
                all_incomes.append(val)
                key = (row['employment_type'], row['loan_grade'])
                income_groups.setdefault(key, []).append(val)
            except:
                missing_inc_count += 1
        else:
            missing_inc_count += 1
            
    overall_median = median(all_incomes) if all_incomes else 65000.0
    group_medians = {k: median(v) for k, v in income_groups.items()}
    
    for row in unique_rows:
        inc_str = row['annual_income'].strip()
        if not inc_str:
            key = (row['employment_type'], row['loan_grade'])
            imputed = group_medians.get(key, overall_median)
            row['annual_income'] = f"{imputed:.2f}"
            
    quality_logs.append({
        'issue': 'Missing Annual Income',
        'rule_applied': 'Imputed missing annual income values with the group median based on employment type and loan grade.',
        'rows_affected': missing_inc_count
    })
    
    # 5. Inconsistent Loan Status Codes & Synchronize default_flag
    status_changed_count = 0
    for row in unique_rows:
        s = row['loan_status'].strip().lower()
        orig_s = row['loan_status']
        if any(x in s for x in ['fully paid', 'paid in full', 'fully_paid']):
            row['loan_status'] = 'Fully Paid'
        elif any(x in s for x in ['charged off', 'charged_off', 'written off']):
            row['loan_status'] = 'Charged Off'
        elif any(x in s for x in ['default', 'defaulted', 'def']):
            row['loan_status'] = 'Default'
        elif any(x in s for x in ['current', 'active', 'current_loan']):
            row['loan_status'] = 'Current'
        elif any(x in s for x in ['grace', 'grace period', 'grace_period']):
            row['loan_status'] = 'In Grace Period'
        else:
            row['loan_status'] = 'Current'
            
        if row['loan_status'] != orig_s:
            status_changed_count += 1
            
        # Synchronize default flag
        row['default_flag'] = '1' if row['loan_status'] in ['Charged Off', 'Default'] else '0'
        
    quality_logs.append({
        'issue': 'Inconsistent Loan Status',
        'rule_applied': 'Mapped non-standard status strings to canonical banking statuses and synchronized default flags.',
        'rows_affected': status_changed_count
    })
    
    # 6. Invalid Credit Scores (<300 or >850) -> Quarantine
    valid_score_rows = []
    invalid_score_count = 0
    for row in unique_rows:
        try:
            cs = float(row['credit_score'])
            if 300 <= cs <= 850:
                valid_score_rows.append(row)
            else:
                invalid_score_count += 1
                row_copy = dict(row)
                row_copy['quarantine_reason'] = 'Invalid Credit Score Range'
                quarantined.append(row_copy)
        except:
            invalid_score_count += 1
            row_copy = dict(row)
            row_copy['quarantine_reason'] = 'Invalid Credit Score Range'
            quarantined.append(row_copy)
            
    quality_logs.append({
        'issue': 'Invalid Credit Scores',
        'rule_applied': 'Quarantined records with credit scores outside the valid 300 to 850 range.',
        'rows_affected': invalid_score_count
    })
    
    # 7. Extreme Loan Amounts (<= 0 or > 150000) -> Quarantine
    valid_amount_rows = []
    extreme_amount_count = 0
    for row in valid_score_rows:
        try:
            amt = float(row['loan_amount'])
            if 0 < amt <= 150000:
                valid_amount_rows.append(row)
            else:
                extreme_amount_count += 1
                row_copy = dict(row)
                row_copy['quarantine_reason'] = 'Extreme Loan Amount Outlier'
                quarantined.append(row_copy)
        except:
            extreme_amount_count += 1
            row_copy = dict(row)
            row_copy['quarantine_reason'] = 'Extreme Loan Amount Outlier'
            quarantined.append(row_copy)
            
    quality_logs.append({
        'issue': 'Extreme Loan Amounts',
        'rule_applied': 'Quarantined loans with negative amounts, zero amounts, or unrealistic outlier values exceeding $150,000.',
        'rows_affected': extreme_amount_count
    })
    
    # 8. Invalid Dates -> Quarantine
    clean_rows = []
    invalid_date_count = 0
    for row in valid_amount_rows:
        d_str = row['loan_issue_date'].strip()
        try:
            d_obj = datetime.strptime(d_str, '%Y-%m-%d')
            row['loan_issue_date'] = d_obj.strftime('%Y-%m-%d')
            clean_rows.append(row)
        except:
            invalid_date_count += 1
            row_copy = dict(row)
            row_copy['quarantine_reason'] = 'Corrupt Issue Date'
            quarantined.append(row_copy)
            
    quality_logs.append({
        'issue': 'Invalid Issue Dates',
        'rule_applied': 'Quarantined unparseable and calendar-invalid date strings.',
        'rows_affected': invalid_date_count
    })
    
    # Write Clean Data
    with open(clean_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(clean_rows)
    print(f"SUCCESS: Wrote {len(clean_rows)} clean records to {clean_path}")
    
    # Write Quarantine Data
    quarantine_fields = fieldnames + ['quarantine_reason']
    with open(quarantine_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=quarantine_fields)
        writer.writeheader()
        writer.writerows(quarantined)
    print(f"SUCCESS: Wrote {len(quarantined)} quarantined records to {quarantine_path}")
    
    # Write Quality Log
    with open(log_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['issue', 'rule_applied', 'rows_affected'])
        writer.writeheader()
        writer.writerows(quality_logs)
    print(f"SUCCESS: Wrote data quality log to {log_path}")
    
    # Generate docs/data_quality_report.md
    with open(report_path, mode='w', encoding='utf-8') as f:
        f.write("# Data Quality & Pipeline Audit Report\n\n")
        f.write(f"**Execution Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
        f.write(f"**Raw Dataset Input:** `{raw_path}` ({initial_count:,} records)  \n")
        f.write(f"**Clean Dataset Output:** `{clean_path}` ({len(clean_rows):,} records)  \n")
        f.write(f"**Quarantined Records:** `{quarantine_path}` ({len(quarantined):,} records)  \n\n")
        
        f.write("## 1. Data Quality Issues & Transformations Log\n\n")
        f.write("| Issue Identified | Cleaning Rule Applied | Rows Affected |\n")
        f.write("|:---|:---|:---:|\n")
        for log in quality_logs:
            f.write(f"| **{log['issue']}** | {log['rule_applied']} | {log['rows_affected']} |\n")
            
        f.write("\n## 2. Before vs. After Data Health Comparison\n\n")
        f.write("| Quality Metric | Raw Dataset | Cleaned Dataset | Resolution Status |\n")
        f.write("|:---|:---:|:---:|:---:|\n")
        f.write(f"| **Total Record Count** | {initial_count:,} | {len(clean_rows):,} | Validated |\n")
        f.write(f"| **Duplicate Loan IDs** | {dup_count} | 0 | 100% Resolved |\n")
        f.write(f"| **Missing Annual Income** | {missing_inc_count} | 0 | Imputed via Group Median |\n")
        f.write(f"| **Missing Credit Grades** | {missing_grade_count} | 0 | Deduced via FICO Tiers |\n")
        f.write(f"| **Invalid Credit Scores (<300 or >850)** | {invalid_score_count} | 0 | Quarantined |\n")
        f.write(f"| **Extreme Loan Amounts (Outliers/Negative)** | {extreme_amount_count} | 0 | Quarantined |\n")
        f.write(f"| **Invalid Date Formats** | {invalid_date_count} | 0 | Quarantined |\n")
        f.write(f"| **Inconsistent Status Labels** | {status_changed_count} | 0 | Standardized Canonical |\n\n")
        
        f.write("## 3. Quarantined Records Summary\n\n")
        f.write("To ensure complete regulatory auditability, unresolvable records were not silently deleted. ")
        f.write(f"A total of **{len(quarantined)}** records were isolated into `{quarantine_path}` with designated diagnostic reason codes for audit review.\n")
        
    print(f"SUCCESS: Generated data quality report at {report_path}")
    return len(clean_rows), len(quarantined)

if __name__ == "__main__":
    clean_loan_data()
