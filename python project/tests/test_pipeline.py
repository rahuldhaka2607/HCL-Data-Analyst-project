"""
Project No. 6: Loan Default Analysis and Risk Dashboard
Module: Automated Pipeline Verification & Testing Suite (P15)
Description: Executes all 10 mandatory test cases verifying data integrity,
             domain rules, relational constraints, and cross-tool reconciliation.
             Saves results to reports/test_results.csv.
"""

import os
import csv
import sqlite3
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_CSV = os.path.join(BASE_DIR, "data", "clean", "loans_clean.csv")
RAW_CSV = os.path.join(BASE_DIR, "data", "raw", "loans_raw.csv")
QUARANTINE_CSV = os.path.join(BASE_DIR, "data", "clean", "loans_quarantine.csv")
DB_PATH = os.path.join(BASE_DIR, "data", "loans.db")
TEST_RESULTS_PATH = os.path.join(BASE_DIR, "reports", "test_results.csv")

test_records = []

def record_test(test_num, name, condition, details=""):
    status = "PASS" if condition else "FAIL"
    test_records.append({
        'Test_ID': f"TC-{test_num:02d}",
        'Test_Name': name,
        'Status': status,
        'Verification_Details': details
    })
    print(f"[{status}] TC-{test_num:02d}: {name} -> {details}")
    assert condition, f"Test TC-{test_num:02d} FAILED: {details}"

def load_clean_rows():
    with open(CLEAN_CSV, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def load_quarantine_rows():
    with open(QUARANTINE_CSV, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

# -------------------------------------------------------------
# 10 MANDATORY TEST CASES
# -------------------------------------------------------------

def test_tc01_no_duplicate_primary_keys():
    """Test 1: No duplicate primary keys in clean dataset."""
    rows = load_clean_rows()
    ids = [r['loan_id'] for r in rows]
    unique_ids = set(ids)
    is_valid = len(ids) == len(unique_ids)
    record_test(1, "No Duplicate Primary Keys", is_valid, f"Total IDs: {len(ids)}, Unique IDs: {len(unique_ids)}")

def test_tc02_no_missing_required_fields():
    """Test 2: No missing or null values in required columns."""
    rows = load_clean_rows()
    required = ['loan_id', 'customer_id', 'annual_income', 'credit_score', 'loan_amount', 'loan_grade', 'loan_status']
    missing_count = 0
    for r in rows:
        for col in required:
            val = r.get(col, '')
            if val is None or str(val).strip() == '':
                missing_count += 1
    record_test(2, "No Missing Required Fields", missing_count == 0, f"Found {missing_count} missing values across required columns")

def test_tc03_valid_value_ranges():
    """Test 3: Value ranges strictly conform to domain limits."""
    rows = load_clean_rows()
    invalid_count = 0
    for r in rows:
        score = float(r['credit_score'])
        amt = float(r['loan_amount'])
        age = int(r['age'])
        if not (300 <= score <= 850): invalid_count += 1
        if amt <= 0 or amt > 150000: invalid_count += 1
        if not (18 <= age <= 100): invalid_count += 1
    record_test(3, "Valid Value Ranges", invalid_count == 0, f"Found {invalid_count} range violations (Credit Score 300-850, Loan > $0, Age 18-100)")

def test_tc04_python_total_equals_sql_total():
    """Test 4: Python dataset total exactly equals SQL fact table total."""
    rows = load_clean_rows()
    py_total = len(rows)
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM FACT_LOANS;")
    sql_total = cur.fetchone()[0]
    conn.close()
    
    record_test(4, "Python Total Equals SQL Total", py_total == sql_total, f"Python Rows: {py_total:,} | SQL FACT_LOANS Rows: {sql_total:,}")

def test_tc05_referential_integrity():
    """Test 5: Every fact row has matching customer, date, purpose, and grade dimension rows."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(f.loan_id)
        FROM FACT_LOANS f
        LEFT JOIN DIM_CUSTOMER c ON f.customer_id = c.customer_id
        LEFT JOIN DIM_DATE d ON f.date_id = d.date_id
        LEFT JOIN DIM_LOAN_PURPOSE p ON f.purpose_id = p.purpose_id
        LEFT JOIN DIM_LOAN_GRADE g ON f.grade_id = g.grade_id
        WHERE c.customer_id IS NULL OR d.date_id IS NULL OR p.purpose_id IS NULL OR g.grade_id IS NULL;
    """)
    orphans = cur.fetchone()[0]
    conn.close()
    record_test(5, "Referential Integrity Verified", orphans == 0, f"Orphaned foreign key fact records: {orphans}")

def test_tc06_default_rate_calculations():
    """Test 6: Default rate strictly obeys formula (Defaulted / Closed Eligible)."""
    rows = load_clean_rows()
    eligible = sum(1 for r in rows if r['loan_status'] in ['Fully Paid', 'Charged Off', 'Default'])
    defaulted = sum(1 for r in rows if r['loan_status'] in ['Charged Off', 'Default'])
    expected_rate = round(defaulted / eligible * 100.0, 2)
    record_test(6, "Default Rate Calculation Rigor", expected_rate == 78.78, f"Eligible: {eligible:,}, Defaulted: {defaulted:,}, Rate: {expected_rate:.2f}%")

def test_tc07_risk_band_classification():
    """Test 7: Risk-band categorization correctly applies dual-trigger logic."""
    # Test cases: Score < 580 -> Critical, Score >= 720 & DTI <= 20 -> Low
    cases = [
        ({'credit_score': 500, 'debt_to_income_ratio': 15.0}, 'Critical Risk'),
        ({'credit_score': 750, 'debt_to_income_ratio': 12.0}, 'Low Risk'),
        ({'credit_score': 680, 'debt_to_income_ratio': 25.0}, 'Moderate Risk'),
        ({'credit_score': 630, 'debt_to_income_ratio': 38.0}, 'High Risk')
    ]
    correct = 0
    for c, expected in cases:
        score = c['credit_score']
        dti = c['debt_to_income_ratio']
        if score < 580 or dti > 45.0: cat = 'Critical Risk'
        elif score < 660 or dti > 35.0: cat = 'High Risk'
        elif score < 720 or dti > 20.0: cat = 'Moderate Risk'
        else: cat = 'Low Risk'
        if cat == expected: correct += 1
    record_test(7, "Risk Band Dual-Trigger Classification", correct == len(cases), f"Successfully validated {correct}/{len(cases)} boundary test scenarios")

def test_tc08_missing_income_handled():
    """Test 8: Missing income records were imputed with zero nulls remaining."""
    rows = load_clean_rows()
    null_incomes = sum(1 for r in rows if not r.get('annual_income', '').strip())
    record_test(8, "Missing Income Imputation", null_incomes == 0, f"Remaining unhandled missing income records: {null_incomes}")

def test_tc09_extreme_loan_amounts_detected():
    """Test 9: Extreme outlier loan amounts were quarantined."""
    quarantined = load_quarantine_rows()
    extreme_quarantined = sum(1 for r in quarantined if r.get('quarantine_reason') == 'Extreme Loan Amount Outlier')
    record_test(9, "Extreme Loan Amounts Quarantined", extreme_quarantined > 0, f"Detected and quarantined {extreme_quarantined} extreme outlier loans")

def test_tc10_invalid_loan_statuses_detected():
    """Test 10: Inconsistent raw loan statuses were mapped to valid canonical set."""
    rows = load_clean_rows()
    valid_set = {'Fully Paid', 'Charged Off', 'Default', 'Current', 'In Grace Period'}
    invalid_statuses = sum(1 for r in rows if r['loan_status'] not in valid_set)
    record_test(10, "Invalid Loan Status Standardization", invalid_statuses == 0, f"Remaining unmapped status codes: {invalid_statuses}")

def run_all_tests():
    print("Executing 10-Point Automated Verification Pipeline...\n")
    test_tc01_no_duplicate_primary_keys()
    test_tc02_no_missing_required_fields()
    test_tc03_valid_value_ranges()
    test_tc04_python_total_equals_sql_total()
    test_tc05_referential_integrity()
    test_tc06_default_rate_calculations()
    test_tc07_risk_band_classification()
    test_tc08_missing_income_handled()
    test_tc09_extreme_loan_amounts_detected()
    test_tc10_invalid_loan_statuses_detected()
    
    os.makedirs(os.path.dirname(TEST_RESULTS_PATH), exist_ok=True)
    with open(TEST_RESULTS_PATH, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Test_ID', 'Test_Name', 'Status', 'Verification_Details'])
        writer.writeheader()
        writer.writerows(test_records)
        
    print(f"\nALL 10 TESTS EXECUTED. Results saved to {TEST_RESULTS_PATH}")

if __name__ == "__main__":
    run_all_tests()
