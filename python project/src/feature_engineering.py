"""
Project No. 6: Loan Default Analysis and Risk Dashboard
Module: Feature Engineering (P6/P7)
Description: Generates standard banking risk bands, income segments,
             credit score ranges, and temporal attributes.
"""

import pandas as pd
import numpy as np

def apply_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies banking domain feature engineering to clean loan dataframe.
    """
    df = df.copy()
    
    # 1. Income Bands (< $35k, $35k-$60k, $60k-$100k, > $100k)
    income_bins = [0, 35000, 60000, 100000, float('inf')]
    income_labels = ['< $35,000', '$35,000 - $60,000', '$60,000 - $100,000', '> $100,000']
    df['income_band'] = pd.cut(df['annual_income'], bins=income_bins, labels=income_labels, right=False)
    
    # 2. 4-Tier Hybrid Risk Category
    # Criteria:
    # Critical Risk: Credit Score < 580 OR DTI > 45.0%
    # High Risk: Credit Score < 660 OR DTI > 35.0%
    # Moderate Risk: Credit Score < 720 OR DTI > 20.0%
    # Low Risk: Credit Score >= 720 AND DTI <= 20.0%
    conditions = [
        (df['credit_score'] < 580) | (df['debt_to_income_ratio'] > 45.0),
        (df['credit_score'] < 660) | (df['debt_to_income_ratio'] > 35.0),
        (df['credit_score'] < 720) | (df['debt_to_income_ratio'] > 20.0)
    ]
    choices = ['Critical Risk', 'High Risk', 'Moderate Risk']
    df['risk_category'] = np.select(conditions, choices, default='Low Risk')
    
    # 3. Credit Score FICO Ranges
    score_bins = [300, 580, 660, 720, 800, 851]
    score_labels = ['300-579 (Very Poor)', '580-659 (Fair)', '660-719 (Good)', '720-799 (Very Good)', '800-850 (Exceptional)']
    df['credit_score_range'] = pd.cut(df['credit_score'], bins=score_bins, labels=score_labels, right=False)
    
    # 4. Eligible Closed Loan Indicator (for Default Rate denominator)
    # Closed loans: 'Fully Paid', 'Charged Off', 'Default'
    df['is_eligible_loan'] = df['loan_status'].isin(['Fully Paid', 'Charged Off', 'Default']).astype(int)
    
    # 5. Temporal Attributes
    df['loan_issue_date'] = pd.to_datetime(df['loan_issue_date'], errors='coerce')
    df['issue_year'] = df['loan_issue_date'].dt.year
    df['issue_month'] = df['loan_issue_date'].dt.month
    df['year_month'] = df['loan_issue_date'].dt.strftime('%Y-%m')
    df['issue_quarter'] = 'Q' + df['loan_issue_date'].dt.quarter.astype(str)
    
    return df
