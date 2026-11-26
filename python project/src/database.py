"""
Project No. 6: Loan Default Analysis and Risk Dashboard
Module: Database Pipeline & SQL Analytics Runner (P8)
Description: Builds local SQLite star-schema database, ingests cleaned CSV records,
             populates dimensions and fact tables, and executes all 7 analytical queries,
             saving query result CSVs to data/reports/.
"""

import os
import sqlite3
import csv
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def setup_database():
    db_path = os.path.join(BASE_DIR, "data", "loans.db")
    schema_path = os.path.join(BASE_DIR, "sql", "schema.sql")
    views_path = os.path.join(BASE_DIR, "sql", "views", "analytical_views.sql")
    clean_csv = os.path.join(BASE_DIR, "data", "clean", "loans_clean.csv")
    queries_path = os.path.join(BASE_DIR, "sql", "queries.sql")
    reports_dir = os.path.join(BASE_DIR, "data", "reports")
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    
    print(f"Connecting to SQLite database: {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. Execute Schema DDL
    print(f"Executing schema DDL from {schema_path}...")
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    print("Star schema tables created successfully.")
    
    # 2. Ingest Cleaned Data
    print(f"Reading cleaned records from {clean_csv}...")
    with open(clean_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        records = list(reader)
        
    print(f"Loaded {len(records)} clean records for dimensional population.")
    
    # Collect unique entities
    customers = {}
    dates = {}
    purposes = {}
    purpose_id_counter = 1
    
    # Standard grade master
    grade_master = {
        'A': ('Grade A Prime', 'Very Low Risk'),
        'B': ('Grade B Near Prime', 'Low Risk'),
        'C': ('Grade C Standard', 'Moderate Risk'),
        'D': ('Grade D Near Standard', 'Medium Risk'),
        'E': ('Grade E Subprime', 'High Risk'),
        'F': ('Grade F Deep Subprime', 'Very High Risk'),
        'G': ('Grade G Extreme Subprime', 'Critical Risk'),
    }
    
    for r in records:
        # Customer
        cid = r['customer_id']
        if cid not in customers:
            customers[cid] = (
                cid,
                int(r['age']),
                r['gender'],
                r['employment_type'],
                float(r['annual_income']),
                int(float(r['credit_score'])),
                r['home_ownership'],
                int(r['existing_loans'])
            )
            
        # Date
        d_str = r['loan_issue_date']
        if d_str not in dates:
            d_obj = datetime.strptime(d_str, '%Y-%m-%d')
            dates[d_str] = (
                d_str,
                d_str,
                d_obj.day,
                d_obj.month,
                d_obj.strftime('%B'),
                f"Q{(d_obj.month - 1) // 3 + 1}",
                d_obj.year,
                d_obj.strftime('%Y-%m')
            )
            
        # Purpose
        p_name = r['loan_purpose']
        if p_name not in purposes:
            purposes[p_name] = purpose_id_counter
            purpose_id_counter += 1
            
    # Insert DIM_CUSTOMER
    print(f"Populating DIM_CUSTOMER ({len(customers)} rows)...")
    cursor.executemany("""
        INSERT INTO DIM_CUSTOMER (customer_id, age, gender, employment_type, annual_income, credit_score, home_ownership, existing_loans)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, list(customers.values()))
    
    # Insert DIM_DATE
    print(f"Populating DIM_DATE ({len(dates)} rows)...")
    cursor.executemany("""
        INSERT INTO DIM_DATE (date_id, full_date, day, month, month_name, quarter, year, year_month)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, list(dates.values()))
    
    # Insert DIM_LOAN_PURPOSE
    print(f"Populating DIM_LOAN_PURPOSE ({len(purposes)} rows)...")
    cursor.executemany("""
        INSERT INTO DIM_LOAN_PURPOSE (purpose_id, purpose_name)
        VALUES (?, ?);
    """, [(pid, name) for name, pid in purposes.items()])
    
    # Insert DIM_LOAN_GRADE
    print(f"Populating DIM_LOAN_GRADE ({len(grade_master)} rows)...")
    cursor.executemany("""
        INSERT INTO DIM_LOAN_GRADE (grade_id, grade_name, base_risk_level)
        VALUES (?, ?, ?);
    """, [(gid, name, risk) for gid, (name, risk) in grade_master.items()])
    
    # Insert FACT_LOANS
    print(f"Populating FACT_LOANS ({len(records)} rows)...")
    fact_rows = []
    for r in records:
        fact_rows.append((
            r['loan_id'],
            r['customer_id'],
            r['loan_issue_date'],
            purposes[r['loan_purpose']],
            r['loan_grade'],
            float(r['loan_amount']),
            int(r['loan_term_months']),
            float(r['interest_rate']),
            float(r['debt_to_income_ratio']),
            r['loan_status'],
            float(r['total_payment']),
            float(r['outstanding_balance']),
            int(r['default_flag'])
        ))
        
    cursor.executemany("""
        INSERT INTO FACT_LOANS (
            loan_id, customer_id, date_id, purpose_id, grade_id,
            loan_amount, loan_term_months, interest_rate, debt_to_income_ratio,
            loan_status, total_payment, outstanding_balance, default_flag
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, fact_rows)
    
    conn.commit()
    print("Database tables and indexes populated successfully.")
    
    # 3. Create Analytical Views
    if os.path.exists(views_path):
        print(f"Creating analytical views from {views_path}...")
        with open(views_path, 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())
        conn.commit()
        print("Views created successfully.")
        
    # 4. Execute and Export Analytical Queries
    print("Executing analytical SQL queries...")
    
    queries = {
        'query_1_grade_default_rate.csv': """
            SELECT 
                g.grade_id AS loan_grade,
                g.grade_name,
                COUNT(f.loan_id) AS total_loans,
                SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END) AS eligible_closed_loans,
                SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) AS defaulted_loans,
                ROUND(
                    100.0 * SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) / 
                    NULLIF(SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END), 0), 
                    2
                ) AS default_rate_pct,
                ROUND(AVG(f.interest_rate), 2) AS avg_interest_rate_pct,
                ROUND(AVG(f.loan_amount), 2) AS avg_loan_amount
            FROM FACT_LOANS f
            JOIN DIM_LOAN_GRADE g ON f.grade_id = g.grade_id
            GROUP BY g.grade_id, g.grade_name
            ORDER BY g.grade_id ASC;
        """,
        'query_2_income_band_default_rate.csv': """
            SELECT 
                CASE 
                    WHEN c.annual_income < 35000 THEN '< $35,000'
                    WHEN c.annual_income >= 35000 AND c.annual_income < 60000 THEN '$35,000 - $60,000'
                    WHEN c.annual_income >= 60000 AND c.annual_income < 100000 THEN '$60,000 - $100,000'
                    ELSE '> $100,000'
                END AS income_band,
                COUNT(f.loan_id) AS total_loans,
                SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END) AS eligible_closed_loans,
                SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) AS defaulted_loans,
                ROUND(
                    100.0 * SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) / 
                    NULLIF(SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END), 0), 
                    2
                ) AS default_rate_pct,
                ROUND(AVG(c.annual_income), 2) AS avg_income_in_band,
                ROUND(AVG(f.debt_to_income_ratio), 2) AS avg_dti_ratio
            FROM FACT_LOANS f
            JOIN DIM_CUSTOMER c ON f.customer_id = c.customer_id
            GROUP BY income_band
            ORDER BY 
                CASE income_band
                    WHEN '< $35,000' THEN 1
                    WHEN '$35,000 - $60,000' THEN 2
                    WHEN '$60,000 - $100,000' THEN 3
                    ELSE 4
                END;
        """,
        'query_3_purpose_default_rate.csv': """
            SELECT 
                p.purpose_name AS loan_purpose,
                COUNT(f.loan_id) AS total_loans,
                SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END) AS eligible_closed_loans,
                SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) AS defaulted_loans,
                ROUND(
                    100.0 * SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) / 
                    NULLIF(SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END), 0), 
                    2
                ) AS default_rate_pct,
                ROUND(SUM(f.loan_amount), 2) AS total_volume_disbursed,
                ROUND(AVG(f.interest_rate), 2) AS avg_interest_rate
            FROM FACT_LOANS f
            JOIN DIM_LOAN_PURPOSE p ON f.purpose_id = p.purpose_id
            GROUP BY p.purpose_name
            ORDER BY default_rate_pct DESC;
        """,
        'query_4_monthly_default_trends.csv': """
            WITH MonthlyStats AS (
                SELECT 
                    d.year_month,
                    COUNT(f.loan_id) AS monthly_originations,
                    ROUND(SUM(f.loan_amount), 2) AS total_originated_volume,
                    SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END) AS closed_loans,
                    SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) AS monthly_defaults
                FROM FACT_LOANS f
                JOIN DIM_DATE d ON f.date_id = d.date_id
                GROUP BY d.year_month
            )
            SELECT 
                year_month,
                monthly_originations,
                total_originated_volume,
                closed_loans,
                monthly_defaults,
                ROUND(100.0 * monthly_defaults / NULLIF(closed_loans, 0), 2) AS monthly_default_rate_pct,
                LAG(monthly_originations, 1) OVER (ORDER BY year_month) AS prev_month_originations,
                ROUND(
                    100.0 * (monthly_originations - LAG(monthly_originations, 1) OVER (ORDER BY year_month)) / 
                    NULLIF(LAG(monthly_originations, 1) OVER (ORDER BY year_month), 0),
                    2
                ) AS mom_origination_growth_pct
            FROM MonthlyStats
            ORDER BY year_month ASC;
        """,
        'query_5_risk_category_distribution.csv': """
            SELECT 
                CASE 
                    WHEN c.credit_score < 580 OR f.debt_to_income_ratio > 45.0 THEN 'Critical Risk'
                    WHEN c.credit_score < 660 OR f.debt_to_income_ratio > 35.0 THEN 'High Risk'
                    WHEN c.credit_score < 720 OR f.debt_to_income_ratio > 20.0 THEN 'Moderate Risk'
                    ELSE 'Low Risk'
                END AS risk_category,
                COUNT(f.loan_id) AS total_borrowers,
                ROUND(SUM(f.loan_amount), 2) AS total_capital_exposure,
                ROUND(SUM(f.outstanding_balance), 2) AS current_outstanding_exposure,
                SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END) AS eligible_closed_loans,
                SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) AS defaulted_loans,
                ROUND(
                    100.0 * SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) / 
                    NULLIF(SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END), 0), 
                    2
                ) AS default_rate_pct
            FROM FACT_LOANS f
            JOIN DIM_CUSTOMER c ON f.customer_id = c.customer_id
            GROUP BY risk_category
            ORDER BY 
                CASE risk_category
                    WHEN 'Low Risk' THEN 1
                    WHEN 'Moderate Risk' THEN 2
                    WHEN 'High Risk' THEN 3
                    ELSE 4
                END;
        """,
        'query_6_portfolio_summary.csv': """
            SELECT 
                COUNT(f.loan_id) AS total_loans,
                COUNT(DISTINCT f.customer_id) AS total_unique_borrowers,
                ROUND(SUM(f.loan_amount), 2) AS total_portfolio_volume,
                ROUND(AVG(f.loan_amount), 2) AS avg_loan_size,
                ROUND(AVG(f.interest_rate), 2) AS avg_portfolio_interest_rate,
                ROUND(SUM(f.total_payment), 2) AS total_cumulative_repayments,
                ROUND(SUM(f.outstanding_balance), 2) AS total_outstanding_balance,
                SUM(CASE WHEN f.loan_status = 'Current' THEN 1 ELSE 0 END) AS active_current_loans,
                SUM(CASE WHEN f.loan_status = 'In Grace Period' THEN 1 ELSE 0 END) AS active_grace_period_loans,
                SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END) AS total_closed_eligible_loans,
                SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) AS total_defaulted_loans,
                ROUND(
                    100.0 * SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) / 
                    NULLIF(SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END), 0), 
                    2
                ) AS overall_default_rate_pct
            FROM FACT_LOANS f;
        """,
        'query_7_risk_cohort_comparison.csv': """
            WITH RiskCohort AS (
                SELECT 
                    f.loan_id,
                    f.loan_amount,
                    f.interest_rate,
                    f.debt_to_income_ratio,
                    f.loan_status,
                    c.credit_score,
                    c.annual_income,
                    c.existing_loans,
                    c.home_ownership,
                    CASE 
                        WHEN c.credit_score < 580 OR f.debt_to_income_ratio > 45.0 THEN 'High & Critical Risk'
                        WHEN c.credit_score < 660 OR f.debt_to_income_ratio > 35.0 THEN 'High & Critical Risk'
                        ELSE 'Low & Moderate Risk'
                    END AS risk_cohort
                FROM FACT_LOANS f
                JOIN DIM_CUSTOMER c ON f.customer_id = c.customer_id
            )
            SELECT 
                risk_cohort,
                COUNT(loan_id) AS loan_count,
                ROUND(AVG(credit_score), 1) AS avg_credit_score,
                ROUND(AVG(annual_income), 2) AS avg_annual_income,
                ROUND(AVG(debt_to_income_ratio), 2) AS avg_dti,
                ROUND(AVG(interest_rate), 2) AS avg_interest_rate_charged,
                ROUND(AVG(existing_loans), 1) AS avg_existing_credit_lines,
                SUM(CASE WHEN loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END) AS eligible_loans,
                SUM(CASE WHEN loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) AS default_count,
                ROUND(
                    100.0 * SUM(CASE WHEN loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) / 
                    NULLIF(SUM(CASE WHEN loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END), 0), 
                    2
                ) AS default_rate_pct
            FROM RiskCohort
            GROUP BY risk_cohort;
        """
    }
    
    for filename, sql in queries.items():
        cursor.execute(sql)
        cols = [d[0] for d in cursor.description]
        rows = cursor.fetchall()
        out_path = os.path.join(reports_dir, filename)
        with open(out_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            writer.writerows(rows)
        print(f"SUCCESS: Exported {filename} ({len(rows)} rows)")
        
    conn.close()
    print("Database pipeline completed successfully.")

if __name__ == "__main__":
    setup_database()
