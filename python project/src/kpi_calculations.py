"""
Project No. 6: Loan Default Analysis and Risk Dashboard
Module: KPI Calculations & Visualizations Engine (P9)
Description: Computes the 11 core financial KPIs from the cleaned dataset,
             exports reports/kpis.json, and generates 4 professional banking charts.
"""

import os
import csv
import json
import tempfile

os.environ['MPLCONFIGDIR'] = tempfile.gettempdir()
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def calculate_kpis():
    clean_csv = os.path.join(BASE_DIR, "data", "clean", "loans_clean.csv")
    kpis_json_path = os.path.join(BASE_DIR, "reports", "kpis.json")
    screenshots_dir = os.path.join(BASE_DIR, "assets", "screenshots")
    
    os.makedirs(os.path.dirname(kpis_json_path), exist_ok=True)
    os.makedirs(screenshots_dir, exist_ok=True)
    
    print(f"Reading cleaned dataset from {clean_csv}...")
    with open(clean_csv, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        records = list(reader)
        
    total_loans = len(records)
    unique_borrowers = len(set(r['customer_id'] for r in records))
    total_loan_amount = sum(float(r['loan_amount']) for r in records)
    total_outstanding = sum(float(r['outstanding_balance']) for r in records)
    total_payment = sum(float(r['total_payment']) for r in records)
    
    avg_loan_amount = total_loan_amount / total_loans if total_loans else 0
    avg_credit_score = sum(float(r['credit_score']) for r in records) / total_loans if total_loans else 0
    
    # Eligible closed loans vs Defaulted loans
    # Closed loans: Fully Paid, Charged Off, Default
    eligible_loans = sum(1 for r in records if r['loan_status'] in ['Fully Paid', 'Charged Off', 'Default'])
    defaulted_loans = sum(1 for r in records if r['loan_status'] in ['Charged Off', 'Default'])
    overall_default_rate = (defaulted_loans / eligible_loans * 100.0) if eligible_loans else 0.0
    
    # 1. Default Rate by Grade
    grade_data = {}
    for r in records:
        g = r['loan_grade']
        grade_data.setdefault(g, {'total': 0, 'eligible': 0, 'defaulted': 0, 'amount': 0.0})
        grade_data[g]['total'] += 1
        grade_data[g]['amount'] += float(r['loan_amount'])
        if r['loan_status'] in ['Fully Paid', 'Charged Off', 'Default']:
            grade_data[g]['eligible'] += 1
            if r['loan_status'] in ['Charged Off', 'Default']:
                grade_data[g]['defaulted'] += 1
                
    default_rate_by_grade = {}
    for g in sorted(grade_data.keys()):
        e = grade_data[g]['eligible']
        d = grade_data[g]['defaulted']
        rate = (d / e * 100.0) if e else 0.0
        default_rate_by_grade[g] = {
            'total_loans': grade_data[g]['total'],
            'eligible_loans': e,
            'defaulted_loans': d,
            'default_rate_pct': round(rate, 2),
            'total_volume': round(grade_data[g]['amount'], 2)
        }
        
    # 2. Default Rate by Income Band
    def get_income_band(inc):
        if inc < 35000: return '< $35,000'
        if inc < 60000: return '$35,000 - $60,000'
        if inc < 100000: return '$60,000 - $100,000'
        return '> $100,000'
        
    income_data = {
        '< $35,000': {'total': 0, 'eligible': 0, 'defaulted': 0},
        '$35,000 - $60,000': {'total': 0, 'eligible': 0, 'defaulted': 0},
        '$60,000 - $100,000': {'total': 0, 'eligible': 0, 'defaulted': 0},
        '> $100,000': {'total': 0, 'eligible': 0, 'defaulted': 0}
    }
    for r in records:
        band = get_income_band(float(r['annual_income']))
        income_data[band]['total'] += 1
        if r['loan_status'] in ['Fully Paid', 'Charged Off', 'Default']:
            income_data[band]['eligible'] += 1
            if r['loan_status'] in ['Charged Off', 'Default']:
                income_data[band]['defaulted'] += 1
                
    default_rate_by_income_band = {}
    for band, val in income_data.items():
        e = val['eligible']
        d = val['defaulted']
        rate = (d / e * 100.0) if e else 0.0
        default_rate_by_income_band[band] = {
            'total_loans': val['total'],
            'eligible_loans': e,
            'defaulted_loans': d,
            'default_rate_pct': round(rate, 2)
        }
        
    # 3. Default Rate by Purpose
    purpose_data = {}
    for r in records:
        p = r['loan_purpose']
        purpose_data.setdefault(p, {'total': 0, 'eligible': 0, 'defaulted': 0})
        purpose_data[p]['total'] += 1
        if r['loan_status'] in ['Fully Paid', 'Charged Off', 'Default']:
            purpose_data[p]['eligible'] += 1
            if r['loan_status'] in ['Charged Off', 'Default']:
                purpose_data[p]['defaulted'] += 1
                
    default_rate_by_purpose = {}
    for p, val in sorted(purpose_data.items()):
        e = val['eligible']
        d = val['defaulted']
        rate = (d / e * 100.0) if e else 0.0
        default_rate_by_purpose[p] = {
            'total_loans': val['total'],
            'eligible_loans': e,
            'defaulted_loans': d,
            'default_rate_pct': round(rate, 2)
        }
        
    # 4. Monthly Trend Data
    monthly_data = {}
    for r in records:
        ym = r['loan_issue_date'][:7]
        monthly_data.setdefault(ym, {'originations': 0, 'volume': 0.0, 'eligible': 0, 'defaults': 0})
        monthly_data[ym]['originations'] += 1
        monthly_data[ym]['volume'] += float(r['loan_amount'])
        if r['loan_status'] in ['Fully Paid', 'Charged Off', 'Default']:
            monthly_data[ym]['eligible'] += 1
            if r['loan_status'] in ['Charged Off', 'Default']:
                monthly_data[ym]['defaults'] += 1
                
    kpis = {
        'total_loans': total_loans,
        'total_loan_amount': round(total_loan_amount, 2),
        'total_borrowers': unique_borrowers,
        'eligible_loans': eligible_loans,
        'defaulted_loans': defaulted_loans,
        'default_rate_pct': round(overall_default_rate, 2),
        'average_loan_amount': round(avg_loan_amount, 2),
        'average_credit_score': round(avg_credit_score, 1),
        'total_outstanding_balance': round(total_outstanding, 2),
        'total_repayment': round(total_payment, 2),
        'default_rate_by_grade': default_rate_by_grade,
        'default_rate_by_income_band': default_rate_by_income_band,
        'default_rate_by_purpose': default_rate_by_purpose
    }
    
    with open(kpis_json_path, mode='w', encoding='utf-8') as f:
        json.dump(kpis, f, indent=4)
    print(f"SUCCESS: Exported KPIs JSON to {kpis_json_path}")
    
    # ==========================================
    # Matplotlib Professional Banking Visualizations
    # ==========================================
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    # Chart 1: Default Rate by Grade
    plt.figure(figsize=(9, 5))
    grades = list(default_rate_by_grade.keys())
    rates = [default_rate_by_grade[g]['default_rate_pct'] for g in grades]
    colors = ['#2EC4B6', '#3A86FF', '#FFBE0B', '#FB5607', '#FF006E', '#8338EC', '#D90429']
    
    bars = plt.bar(grades, rates, color=colors, edgecolor='#0A192F', width=0.6)
    plt.title('Loan Default Rate by Credit Risk Grade (A to G)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Loan Grade Tier (Prime to Deep Subprime)', fontsize=11)
    plt.ylabel('Default Rate (%)', fontsize=11)
    plt.ylim(0, max(rates) + 12)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f"{yval:.1f}%", ha='center', va='bottom', fontsize=10, fontweight='bold')
        
    plt.tight_layout()
    chart1_path = os.path.join(screenshots_dir, 'default_rate_by_grade.png')
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"SUCCESS: Saved {chart1_path}")
    
    # Chart 2: Default Rate by Income Band
    plt.figure(figsize=(9, 5))
    bands = list(default_rate_by_income_band.keys())
    inc_rates = [default_rate_by_income_band[b]['default_rate_pct'] for b in bands]
    
    bars2 = plt.bar(bands, inc_rates, color=['#EF476F', '#F78C6B', '#FFD166', '#06D6A0'], edgecolor='#0A192F', width=0.55)
    plt.title('Loan Default Rate Across Annual Income Segments', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Annual Income Tier (USD)', fontsize=11)
    plt.ylabel('Default Rate (%)', fontsize=11)
    plt.ylim(0, max(inc_rates) + 12)
    
    for bar in bars2:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f"{yval:.1f}%", ha='center', va='bottom', fontsize=10, fontweight='bold')
        
    plt.tight_layout()
    chart2_path = os.path.join(screenshots_dir, 'default_rate_by_income_band.png')
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"SUCCESS: Saved {chart2_path}")
    
    # Chart 3: Default Rate by Loan Purpose
    plt.figure(figsize=(10, 5))
    sorted_purposes = sorted(default_rate_by_purpose.items(), key=lambda x: x[1]['default_rate_pct'], reverse=True)
    p_names = [x[0] for x in sorted_purposes]
    p_rates = [x[1]['default_rate_pct'] for x in sorted_purposes]
    
    bars3 = plt.barh(p_names[::-1], p_rates[::-1], color='#118AB2', edgecolor='#073B4C', height=0.6)
    plt.title('Default Concentration by Stated Loan Purpose', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Default Rate (%)', fontsize=11)
    plt.ylabel('Loan Purpose Category', fontsize=11)
    plt.xlim(0, max(p_rates) + 12)
    
    for bar in bars3:
        wval = bar.get_width()
        plt.text(wval + 1.0, bar.get_y() + bar.get_height()/2.0, f"{wval:.1f}%", ha='left', va='center', fontsize=9, fontweight='bold')
        
    plt.tight_layout()
    chart3_path = os.path.join(screenshots_dir, 'default_rate_by_purpose.png')
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    print(f"SUCCESS: Saved {chart3_path}")
    
    # Chart 4: Monthly Default Trend
    sorted_months = sorted(monthly_data.keys())
    m_rates = [(monthly_data[m]['defaults'] / monthly_data[m]['eligible'] * 100.0) if monthly_data[m]['eligible'] else 0.0 for m in sorted_months]
    
    plt.figure(figsize=(12, 5))
    plt.plot(sorted_months, m_rates, marker='o', color='#E63946', linewidth=2, markersize=5, label='Monthly Default Rate (%)')
    plt.title('Monthly Loan Default Rate Trajectory (2021 - 2024)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Origination Year-Month', fontsize=11)
    plt.ylabel('Default Rate (%)', fontsize=11)
    plt.xticks(sorted_months[::3], rotation=45, fontsize=9)
    plt.ylim(0, 100)
    plt.legend(frameon=True)
    plt.tight_layout()
    
    chart4_path = os.path.join(screenshots_dir, 'monthly_default_trend.png')
    plt.savefig(chart4_path, dpi=300)
    plt.close()
    print(f"SUCCESS: Saved {chart4_path}")
    
    return kpis

if __name__ == "__main__":
    calculate_kpis()
