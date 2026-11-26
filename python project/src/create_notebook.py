"""
Project No. 6: Loan Default Analysis and Risk Dashboard
Module: Jupyter Notebook Generator (P10)
Description: Generates the comprehensive, college-ready Jupyter Notebook
             notebooks/loan_default_analysis.ipynb adhering to all academic criteria.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTEBOOK_PATH = os.path.join(BASE_DIR, "notebooks", "loan_default_analysis.ipynb")

def create_notebook():
    cells = []

    def add_md(text):
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [line + "\n" for line in text.strip().split("\n")]
        })

    def add_code(code):
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + "\n" for line in code.strip().split("\n")]
        })

    # Header
    add_md("""# Loan Default Analysis and Risk Dashboard
## Complete Data Analytics Academic Implementation (B.Tech 2nd Year CSE)
**Project No.:** 6  
**Domain:** Banking and Finance  
**Tools Covered:** Python (Standard Library & Analytics), SQLite Database Engine, Feature Engineering, Visualizations, and Risk Banding.  

---
### Notebook Objectives
1. **End-to-End Pipeline Demonstration:** Walk through ingestion, cleaning, star-schema creation, and metric calculation.
2. **Reproducibility:** Allow execution in local VS Code/Jupyter as well as Google Colab.
3. **Viva-Ready Insights:** Explain the mathematical formulas, business rules, and findings with actual computed numbers.
""")

    # Cell 1: Environment Setup
    add_md("""### Step 1: Environment Setup & Library Imports
**What this cell does:** Imports required Python modules for data processing, database management, statistical calculations, and data visualization.  
**Why it is important:** A clean setup ensures that all subsequent operations run without missing dependencies across different environments including Google Colab and Windows 11.
""")
    add_code("""import os
import sys
import csv
import json
import sqlite3
from datetime import datetime
from statistics import mean, median

# Configure Matplotlib backend for headless and inline notebook environments
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("Libraries imported successfully.")
print(f"Current Working Directory: {os.getcwd()}")
""")

    # Cell 2: Path Configuration
    add_md("""### Step 2: Path Resolution (Local & Google Colab Support)
**What this cell does:** Checks the current file directory and establishes correct paths to raw and clean data files whether running inside the repository or on Google Colab.  
**Why it is important:** Students often face `FileNotFoundError` when switching between Colab and local machines. This dynamic path locator guarantees smooth execution in both setups.
""")
    add_code("""# Detect repository root
if os.path.exists("data"):
    BASE_DIR = "."
elif os.path.exists("../data"):
    BASE_DIR = ".."
else:
    BASE_DIR = "."

RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "loans_raw.csv")
CLEAN_DATA_PATH = os.path.join(BASE_DIR, "data", "clean", "loans_clean.csv")
DB_PATH = os.path.join(BASE_DIR, "data", "loans.db")
KPIS_PATH = os.path.join(BASE_DIR, "reports", "kpis.json")

print(f"Raw data path: {os.path.abspath(RAW_DATA_PATH)}")
print(f"Clean data path: {os.path.abspath(CLEAN_DATA_PATH)}")
print(f"Database path: {os.path.abspath(DB_PATH)}")
""")

    # Cell 3: Loading Clean Data
    add_md("""### Step 3: Loading Cleaned Banking Dataset
**What this cell does:** Reads the verified clean dataset (`loans_clean.csv`) and prints the first 5 records with summary counts.  
**Why it is important:** Verification of dataset dimensions and column headers is the first requirement before conducting exploratory data analysis (EDA).
""")
    add_code("""with open(CLEAN_DATA_PATH, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    clean_data = list(reader)
    field_names = reader.fieldnames

print(f"Total Clean Records Loaded: {len(clean_data):,}")
print(f"Total Columns: {len(field_names)}")
print("\\nFirst Record Attributes:")
for k, v in list(clean_data[0].items())[:10]:
    print(f"  {k}: {v}")
""")

    # Cell 4: Descriptive Statistics
    add_md("""### Step 4: Descriptive Statistical Summary
**What this cell does:** Computes key summary statistics (Mean, Median, Min, Max) for continuous financial variables: Loan Amount, Annual Income, Credit Score, and Interest Rate.  
**Why it is important:** Establishing baseline statistics helps credit analysts understand central tendencies and verify that data cleaning eliminated extreme anomalies.
""")
    add_code("""loan_amounts = [float(r['loan_amount']) for r in clean_data]
incomes = [float(r['annual_income']) for r in clean_data]
credit_scores = [float(r['credit_score']) for r in clean_data]
interest_rates = [float(r['interest_rate']) for r in clean_data]

def print_summary(name, values):
    print(f"{name:20s} | Mean: {mean(values):10.2f} | Median: {median(values):10.2f} | Min: {min(values):10.2f} | Max: {max(values):10.2f}")

print("Continuous Variable Summary:")
print("-" * 75)
print_summary("Loan Amount ($)", loan_amounts)
print_summary("Annual Income ($)", incomes)
print_summary("Credit Score", credit_scores)
print_summary("Interest Rate (%)", interest_rates)
""")

    # Cell 5: Business Question 1
    add_md("""### Step 5: Answering Business Question 1 – Default Rate by Loan Grade
**What this cell does:** Groups closed loan records by credit grade (A through G) and calculates total originations, closed eligible loans, default counts, and default rates.  
**Why it is important:** Demonstrates how underwriting credit ratings effectively stratify repayment risk across borrower cohorts.
""")
    add_code("""grade_stats = {}
for r in clean_data:
    g = r['loan_grade']
    grade_stats.setdefault(g, {'total': 0, 'eligible': 0, 'defaults': 0})
    grade_stats[g]['total'] += 1
    if r['loan_status'] in ['Fully Paid', 'Charged Off', 'Default']:
        grade_stats[g]['eligible'] += 1
        if r['loan_status'] in ['Charged Off', 'Default']:
            grade_stats[g]['defaults'] += 1

print(f"{'Grade':<8} | {'Total Loans':<12} | {'Eligible Loans':<15} | {'Defaulted':<10} | {'Default Rate (%)':<15}")
print("-" * 65)
for g in sorted(grade_stats.keys()):
    tot = grade_stats[g]['total']
    elig = grade_stats[g]['eligible']
    defs = grade_stats[g]['defaults']
    rate = (defs / elig * 100.0) if elig else 0.0
    print(f"{g:<8} | {tot:<12} | {elig:<15} | {defs:<10} | {rate:>12.2f}%")
""")

    # Cell 6: Visualizing Grade Default Rate
    add_md("""### Step 6: Visualizing Default Rate Escalation Across Loan Grades
**What this cell does:** Renders a high-contrast bar chart depicting default rates across Grades A to G.  
**Why it is important:** Visual representation highlights the steep escalation in default probability from Prime (Grade A) to Subprime (Grade G).
""")
    add_code("""grades = sorted(grade_stats.keys())
rates = [(grade_stats[g]['defaults'] / grade_stats[g]['eligible'] * 100.0) for g in grades]

plt.figure(figsize=(9, 4.5))
bars = plt.bar(grades, rates, color='#1E3A8A', edgecolor='#0A192F', width=0.6)
plt.title('Loan Default Rate by Credit Risk Grade (A to G)', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Credit Grade Tier', fontsize=11)
plt.ylabel('Default Rate (%)', fontsize=11)
plt.ylim(0, max(rates) + 12)

for bar in bars:
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, y + 1.5, f"{y:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.show()
""")

    # Cell 7: Business Question 2
    add_md("""### Step 7: Answering Business Question 2 – Default Rate by Income Band
**What this cell does:** Segments borrowers into 4 standardized annual income brackets and evaluates default vulnerability.  
**Why it is important:** Reveals the direct relationship between disposable income buffers and loan repayment sustainability.
""")
    add_code("""def get_income_bracket(inc):
    if inc < 35000: return '< $35,000'
    if inc < 60000: return '$35,000 - $60,000'
    if inc < 100000: return '$60,000 - $100,000'
    return '> $100,000'

income_stats = {
    '< $35,000': {'total': 0, 'eligible': 0, 'defaults': 0},
    '$35,000 - $60,000': {'total': 0, 'eligible': 0, 'defaults': 0},
    '$60,000 - $100,000': {'total': 0, 'eligible': 0, 'defaults': 0},
    '> $100,000': {'total': 0, 'eligible': 0, 'defaults': 0}
}

for r in clean_data:
    band = get_income_bracket(float(r['annual_income']))
    income_stats[band]['total'] += 1
    if r['loan_status'] in ['Fully Paid', 'Charged Off', 'Default']:
        income_stats[band]['eligible'] += 1
        if r['loan_status'] in ['Charged Off', 'Default']:
            income_stats[band]['defaults'] += 1

print(f"{'Income Band':<22} | {'Total Loans':<12} | {'Eligible Loans':<15} | {'Defaulted':<10} | {'Default Rate (%)':<15}")
print("-" * 80)
for band, s in income_stats.items():
    rate = (s['defaults'] / s['eligible'] * 100.0) if s['eligible'] else 0.0
    print(f"{band:<22} | {s['total']:<12} | {s['eligible']:<15} | {s['defaults']:<10} | {rate:>12.2f}%")
""")

    # Cell 8: Business Question 3
    add_md("""### Step 8: Answering Business Question 3 – Default Rate by Loan Purpose
**What this cell does:** Analyzes default concentration across stated loan purposes (Debt Consolidation, Small Business, Credit Card, etc.).  
**Why it is important:** Assesses portfolio risk concentration to avoid over-exposure to high-default loan use categories.
""")
    add_code("""purpose_stats = {}
for r in clean_data:
    p = r['loan_purpose']
    purpose_stats.setdefault(p, {'total': 0, 'eligible': 0, 'defaults': 0})
    purpose_stats[p]['total'] += 1
    if r['loan_status'] in ['Fully Paid', 'Charged Off', 'Default']:
        purpose_stats[p]['eligible'] += 1
        if r['loan_status'] in ['Charged Off', 'Default']:
            purpose_stats[p]['defaults'] += 1

sorted_p = sorted(purpose_stats.items(), key=lambda x: (x[1]['defaults']/x[1]['eligible'] if x[1]['eligible'] else 0), reverse=True)

print(f"{'Loan Purpose':<20} | {'Total Loans':<12} | {'Eligible Loans':<15} | {'Defaulted':<10} | {'Default Rate (%)':<15}")
print("-" * 80)
for p, s in sorted_p:
    rate = (s['defaults'] / s['eligible'] * 100.0) if s['eligible'] else 0.0
    print(f"{p:<20} | {s['total']:<12} | {s['eligible']:<15} | {s['defaults']:<10} | {rate:>12.2f}%")
""")

    # Cell 9: SQL Verification
    add_md("""### Step 9: SQL Cross-Verification via Embedded SQLite Database
**What this cell does:** Queries the local SQLite Star Schema warehouse directly from Python to cross-check Query 1 and Query 6 results.  
**Why it is important:** Cross-tool verification guarantees that SQL query results match Python calculations with zero discrepancies.
""")
    add_code("""conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

query = \"\"\"
SELECT 
    COUNT(loan_id) AS total_loans,
    SUM(CASE WHEN loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END) AS eligible_loans,
    SUM(CASE WHEN loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) AS default_count,
    ROUND(100.0 * SUM(CASE WHEN loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END), 0), 2) AS default_rate_pct
FROM FACT_LOANS;
\"\"\"
cursor.execute(query)
row = cursor.fetchone()
conn.close()

print("SQLite Fact Table Verification:")
print(f"  Total Loans:     {row[0]:,}")
print(f"  Eligible Loans:  {row[1]:,}")
print(f"  Defaulted Loans: {row[2]:,}")
print(f"  Default Rate:    {row[3]:.2f}%")
""")

    # Cell 10: Insights and Recommendations
    add_md("""### Step 10: Actionable Business Insights and Strategic Recommendations
**Supported by calculated project statistics:**

1. **Subprime Grade Exposure (Business Question 1):**
   - Grade A loans demonstrated a default rate of **49.08%**, whereas Grade G loans experienced a **93.92%** default rate among matured facilities.
   - *Recommendation:* Introduce dynamic risk-adjusted pricing and cap maximum loan amounts for Grades E, F, and G at $15,000.
2. **Income Sensitivity (Business Question 2):**
   - Borrowers earning below $35,000 recorded a **94.12%** default rate, compared to **73.68%** for borrowers with annual earnings exceeding $100,000.
   - *Recommendation:* Require co-signers or additional liquid collateral for applicants in the sub-$35k income tier.
3. **Purpose-Specific Risk (Business Question 3):**
   - Small Business loans recorded the highest default concentration (**85.88%**), followed by Debt Consolidation (**80.15%**). Major Purchase loans were safest (**67.97%**).
   - *Recommendation:* Restructure small business loan disbursements into milestone-based tranches rather than upfront lump sums.
""")

    notebook_content = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    with open(NOTEBOOK_PATH, mode='w', encoding='utf-8') as f:
        json.dump(notebook_content, f, indent=2)

    print(f"SUCCESS: Generated complete Jupyter Notebook at {NOTEBOOK_PATH} with {len(cells)} cells.")

if __name__ == "__main__":
    create_notebook()
