"""
Project No. 6: Loan Default Analysis and Risk Dashboard
Module: Data Generator (P4)
Description: Generates realistic synthetic retail loan data (10,000+ records)
             with authentic financial relationships and injected data quality anomalies.
Fixed Seed: 42 for complete scientific reproducibility.
"""

import os
import random
import csv
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_synthetic_loans(
    num_records=10000,
    output_path=os.path.join(BASE_DIR, "data", "raw", "loans_raw.csv"),
    seed=42
):
    random.seed(seed)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Domain configuration and distribution parameters
    grades = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    grade_weights = [0.18, 0.24, 0.22, 0.16, 0.11, 0.06, 0.03]
    
    # Financial relationship profiles per grade
    # (score_min, score_max, int_rate_min, int_rate_max, base_default_prob)
    grade_profiles = {
        'A': (750, 850, 5.5, 9.0, 0.04),
        'B': (700, 749, 9.0, 13.0, 0.09),
        'C': (660, 699, 13.0, 17.0, 0.17),
        'D': (620, 659, 17.0, 21.0, 0.25),
        'E': (580, 619, 21.0, 25.0, 0.34),
        'F': (540, 579, 25.0, 28.5, 0.44),
        'G': (300, 539, 28.0, 31.0, 0.55),
    }
    
    purposes = [
        'Debt Consolidation', 'Credit Card', 'Home Improvement',
        'Small Business', 'Major Purchase', 'Medical', 'Car'
    ]
    purpose_weights = [0.45, 0.22, 0.12, 0.08, 0.05, 0.05, 0.03]
    
    employment_types = ['Salaried', 'Self-Employed', 'Business', 'Contract']
    emp_weights = [0.55, 0.25, 0.12, 0.08]
    
    home_ownerships = ['MORTGAGE', 'RENT', 'OWN']
    home_weights = [0.48, 0.40, 0.12]
    
    genders = ['Male', 'Female', 'Other']
    gender_weights = [0.52, 0.46, 0.02]
    
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2024, 6, 30)
    total_days = (end_date - start_date).days
    
    records = []
    customer_id_counter = 10001
    
    for i in range(1, num_records + 1):
        loan_id = f"LN-{100000 + i}"
        customer_id = f"CUST-{customer_id_counter + (i % 8800)}"  # Some repeat borrowers
        
        # Demographic profile
        age = random.choices(
            [random.randint(21, 29), random.randint(30, 45), random.randint(46, 65)],
            weights=[0.30, 0.50, 0.20]
        )[0]
        gender = random.choices(genders, weights=gender_weights)[0]
        emp_type = random.choices(employment_types, weights=emp_weights)[0]
        home_own = random.choices(home_ownerships, weights=home_weights)[0]
        
        # Credit profile & Loan Grade
        grade = random.choices(grades, weights=grade_weights)[0]
        p = grade_profiles[grade]
        credit_score = random.randint(p[0], p[1])
        interest_rate = round(random.uniform(p[2], p[3]), 2)
        
        # Income generation correlated with age, grade and employment
        base_inc = 32000 + (credit_score - 300) * 110 + (age - 21) * 600
        if emp_type == 'Business':
            base_inc *= 1.25
        elif emp_type == 'Contract':
            base_inc *= 0.85
        annual_income = round(max(18000.0, random.gauss(base_inc, 16000)), 2)
        
        # Loan purpose & terms
        purpose = random.choices(purposes, weights=purpose_weights)[0]
        term_months = random.choice([36, 60])
        
        # Loan amount correlated with income and grade
        max_allowable = min(40000.0, annual_income * 0.45)
        min_amount = 2000.0
        loan_amount = round(random.uniform(min_amount, max(min_amount + 1000, max_allowable)), -2)
        if loan_amount < 1000:
            loan_amount = 1000.0
            
        # Debt-to-income ratio (DTI)
        base_dti = round(random.uniform(8.0, 32.0) + (850 - credit_score) * 0.035, 2)
        dti = min(58.0, max(4.0, base_dti))
        
        existing_loans = random.choices([0, 1, 2, 3, 4, 5], weights=[0.25, 0.35, 0.22, 0.12, 0.04, 0.02])[0]
        
        # Origination date
        random_days = random.randint(0, total_days)
        issue_date = start_date + timedelta(days=random_days)
        issue_date_str = issue_date.strftime("%Y-%m-%d")
        
        # Default probability calculation with compounding risk factors
        default_prob = p[4]
        if dti > 35.0:
            default_prob += 0.08
        if annual_income < 35000:
            default_prob += 0.06
        if purpose in ['Small Business', 'Debt Consolidation']:
            default_prob += 0.04
        if home_own == 'RENT':
            default_prob += 0.03
        default_prob = max(0.01, min(0.85, default_prob))
        
        is_default = 1 if random.random() < default_prob else 0
        
        # Status assignment
        if is_default == 1:
            status = random.choices(['Charged Off', 'Default'], weights=[0.85, 0.15])[0]
            # Defaulted loans recover only partial payments
            recovery_rate = random.uniform(0.10, 0.45)
            total_payment = round(loan_amount * recovery_rate, 2)
            outstanding_balance = round(loan_amount - total_payment, 2)
        else:
            # For non-defaulted, determine if completed or ongoing based on issue date
            loan_age_months = (datetime(2024, 7, 1) - issue_date).days // 30
            if loan_age_months >= term_months:
                status = 'Fully Paid'
                total_payment = round(loan_amount * (1 + (interest_rate / 100) * (term_months / 24)), 2)
                outstanding_balance = 0.0
            else:
                # Active loan portfolio
                status = random.choices(['Current', 'In Grace Period'], weights=[0.94, 0.06])[0]
                elapsed_ratio = min(0.95, loan_age_months / term_months)
                total_payment = round(loan_amount * elapsed_ratio * (1 + interest_rate / 200), 2)
                outstanding_balance = round(max(0.0, loan_amount - (total_payment * 0.75)), 2)
        
        records.append({
            'loan_id': loan_id,
            'customer_id': customer_id,
            'age': age,
            'gender': gender,
            'employment_type': emp_type,
            'annual_income': annual_income,
            'credit_score': credit_score,
            'loan_amount': loan_amount,
            'loan_term_months': term_months,
            'interest_rate': interest_rate,
            'loan_purpose': purpose,
            'loan_grade': grade,
            'debt_to_income_ratio': dti,
            'existing_loans': existing_loans,
            'home_ownership': home_own,
            'loan_issue_date': issue_date_str,
            'loan_status': status,
            'total_payment': total_payment,
            'outstanding_balance': outstanding_balance,
            'default_flag': is_default
        })
        
    print(f"Generated {len(records)} clean base records. Injecting controlled data quality issues...")
    
    # ==========================================
    # Controlled Data Quality Issue Injections
    # ==========================================
    
    # 1. Duplicate rows (~50 records)
    duplicate_indices = random.sample(range(len(records)), 50)
    for idx in duplicate_indices:
        records.append(dict(records[idx]))  # Exact clone
        
    # 2. Missing annual income (~200 records)
    missing_inc_indices = random.sample(range(len(records)), 200)
    for idx in missing_inc_indices:
        records[idx]['annual_income'] = ""
        
    # 3. Extreme loan amounts (~30 records)
    extreme_indices = random.sample(range(len(records)), 30)
    for i, idx in enumerate(extreme_indices):
        if i % 2 == 0:
            records[idx]['loan_amount'] = random.choice([250000.0, 500000.0, 1000000.0]) # Outlier
        else:
            records[idx]['loan_amount'] = random.choice([-5000.0, -10000.0, 0.0]) # Impossible negative
            
    # 4. Invalid credit scores (~40 records)
    invalid_score_indices = random.sample(range(len(records)), 40)
    for i, idx in enumerate(invalid_score_indices):
        if i % 2 == 0:
            records[idx]['credit_score'] = random.randint(900, 999) # Above 850
        else:
            records[idx]['credit_score'] = random.randint(100, 290) # Below 300
            
    # 5. Inconsistent loan status (~60 records)
    inconsistent_status_indices = random.sample(range(len(records)), 60)
    for idx in inconsistent_status_indices:
        curr = records[idx]['loan_status']
        if curr == 'Fully Paid':
            records[idx]['loan_status'] = random.choice(['fully paid', 'FULLY_PAID', 'paid in full'])
        elif curr == 'Charged Off':
            records[idx]['loan_status'] = random.choice(['charged off', 'CHARGED_OFF', 'written off'])
        elif curr == 'Default':
            records[idx]['loan_status'] = random.choice(['defaulted', 'DEFAULT', 'def'])
        elif curr == 'Current':
            records[idx]['loan_status'] = random.choice(['current_loan', 'CURRENT', 'active'])
        elif curr == 'In Grace Period':
            records[idx]['loan_status'] = random.choice(['grace period', 'GRACE_PERIOD'])
            
    # 6. Invalid date formats (~30 records)
    invalid_date_indices = random.sample(range(len(records)), 30)
    for idx in invalid_date_indices:
        records[idx]['loan_issue_date'] = random.choice(['99/99/9999', '2023-02-31', 'INVALID_DATE', '0000-00-00'])
        
    # 7. Missing loan grades (~50 records)
    missing_grade_indices = random.sample(range(len(records)), 50)
    for idx in missing_grade_indices:
        records[idx]['loan_grade'] = ""
        
    # 8. Inconsistent text values (trailing spaces, lowercase in gender / employment / home_ownership)
    inconsistent_text_indices = random.sample(range(len(records)), 100)
    for idx in inconsistent_text_indices:
        records[idx]['gender'] = records[idx]['gender'].lower() + "  "
        records[idx]['employment_type'] = "  " + records[idx]['employment_type'].upper()
        records[idx]['home_ownership'] = records[idx]['home_ownership'].lower()

    # Write out raw CSV
    fieldnames = [
        'loan_id', 'customer_id', 'age', 'gender', 'employment_type',
        'annual_income', 'credit_score', 'loan_amount', 'loan_term_months',
        'interest_rate', 'loan_purpose', 'loan_grade', 'debt_to_income_ratio',
        'existing_loans', 'home_ownership', 'loan_issue_date', 'loan_status',
        'total_payment', 'outstanding_balance', 'default_flag'
    ]
    
    with open(output_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
        
    print(f"SUCCESS: Raw dataset saved to {output_path} with {len(records)} total records.")
    return len(records)

if __name__ == "__main__":
    generate_synthetic_loans()
