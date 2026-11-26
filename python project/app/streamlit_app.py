"""
LOAN INTELLIGENCE - Loan Default Analysis & Risk Dashboard
Project No.: 6 | Domain: Banking and Finance
Framework: Streamlit + Plotly + SQLite / CSV
"""

import os
import csv
import json
import sqlite3
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------------------------------------------------------
# Configuration and Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="LOAN INTELLIGENCE | Risk Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Banking CSS (Navy, Teal, Clean Light Theme)
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0A192F;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4A5568;
        margin-bottom: 25px;
    }
    .kpi-card {
        background: white;
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(10, 25, 47, 0.08);
        border-left: 5px solid #00B4D8;
        margin-bottom: 15px;
    }
    .kpi-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748B;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0A192F;
        margin-top: 5px;
        margin-bottom: 2px;
    }
    .kpi-sub {
        font-size: 0.8rem;
        color: #64748B;
    }
    .badge-critical {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    .badge-low {
        background-color: #DCFCE7;
        color: #166534;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    .css-1d391kg {
        background-color: #0A192F;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Data Loading & Caching
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_DATA_PATH = os.path.join(BASE_DIR, "data", "clean", "loans_clean.csv")
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "loans_raw.csv")
DB_PATH = os.path.join(BASE_DIR, "data", "loans.db")
QUALITY_LOG_PATH = os.path.join(BASE_DIR, "data", "reports", "data_quality_log.csv")

@st.cache_data
def load_clean_data():
    if not os.path.exists(CLEAN_DATA_PATH):
        return []
    with open(CLEAN_DATA_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        records = list(reader)
    
    # Pre-parse numeric and date attributes
    for r in records:
        r['loan_amount_val'] = float(r['loan_amount'])
        r['annual_income_val'] = float(r['annual_income'])
        r['credit_score_val'] = float(r['credit_score'])
        r['interest_rate_val'] = float(r['interest_rate'])
        r['dti_val'] = float(r['debt_to_income_ratio'])
        r['outstanding_val'] = float(r['outstanding_balance'])
        r['total_pymnt_val'] = float(r['total_payment'])
        r['default_flag_val'] = int(r['default_flag'])
        r['year_month'] = r['loan_issue_date'][:7]
        r['year'] = int(r['loan_issue_date'][:4])
        
        # Risk Category
        score = r['credit_score_val']
        dti = r['dti_val']
        if score < 580 or dti > 45.0:
            r['risk_category'] = 'Critical Risk'
        elif score < 660 or dti > 35.0:
            r['risk_category'] = 'High Risk'
        elif score < 720 or dti > 20.0:
            r['risk_category'] = 'Moderate Risk'
        else:
            r['risk_category'] = 'Low Risk'
            
        # Income Band
        inc = r['annual_income_val']
        if inc < 35000:
            r['income_band'] = '< $35,000'
        elif inc < 60000:
            r['income_band'] = '$35,000 - $60,000'
        elif inc < 100000:
            r['income_band'] = '$60,000 - $100,000'
        else:
            r['income_band'] = '> $100,000'
            
        # Credit Score Range
        if score < 580:
            r['credit_score_range'] = '300-579 (Very Poor)'
        elif score < 660:
            r['credit_score_range'] = '580-659 (Fair)'
        elif score < 720:
            r['credit_score_range'] = '660-719 (Good)'
        elif score < 800:
            r['credit_score_range'] = '720-799 (Very Good)'
        else:
            r['credit_score_range'] = '800-850 (Exceptional)'
            
        r['is_eligible'] = 1 if r['loan_status'] in ['Fully Paid', 'Charged Off', 'Default'] else 0
        
    return records

records_all = load_clean_data()

# -----------------------------------------------------------------------------
# Sidebar Navigation & Global Filters
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='color: white; margin-bottom: 0px;'>LOAN INTELLIGENCE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00B4D8; font-size: 0.85rem; margin-bottom: 20px;'>Risk Analytics Platform</p>", unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation Menu",
        [
            "1. Executive Overview",
            "2. Loan Portfolio Analysis",
            "3. Default Analysis",
            "4. Borrower Risk Analysis",
            "5. Income and Loan Analysis",
            "6. Loan Purpose Analysis",
            "7. Risk Segmentation",
            "8. Data Quality Monitor",
            "9. SQL Analytics",
            "10. Dataset Explorer",
            "11. Project Information"
        ]
    )
    
    st.markdown("---")
    st.markdown("<h4 style='color: white;'>Global Portfolio Filters</h4>", unsafe_allow_html=True)
    
    # Unique values for filters
    all_grades = sorted(list(set(r['loan_grade'] for r in records_all)))
    all_purposes = sorted(list(set(r['loan_purpose'] for r in records_all)))
    all_statuses = sorted(list(set(r['loan_status'] for r in records_all)))
    all_emp = sorted(list(set(r['employment_type'] for r in records_all)))
    all_risk = ['Low Risk', 'Moderate Risk', 'High Risk', 'Critical Risk']
    all_income_bands = ['< $35,000', '$35,000 - $60,000', '$60,000 - $100,000', '> $100,000']
    
    sel_grades = st.multiselect("Loan Grade", all_grades, default=all_grades)
    sel_purposes = st.multiselect("Loan Purpose", all_purposes, default=all_purposes)
    sel_statuses = st.multiselect("Loan Status", all_statuses, default=all_statuses)
    sel_emp = st.multiselect("Employment Type", all_emp, default=all_emp)
    sel_risk = st.multiselect("Risk Category", all_risk, default=all_risk)
    sel_income = st.multiselect("Income Band", all_income_bands, default=all_income_bands)

# Apply Filters
filtered = [
    r for r in records_all
    if (r['loan_grade'] in sel_grades) and
       (r['loan_purpose'] in sel_purposes) and
       (r['loan_status'] in sel_statuses) and
       (r['employment_type'] in sel_emp) and
       (r['risk_category'] in sel_risk) and
       (r['income_band'] in sel_income)
]

# Helper KPI Aggregation
def compute_kpis(data):
    total = len(data)
    if total == 0:
        return {"total_loans": 0, "volume": 0.0, "avg_loan": 0.0, "avg_score": 0.0,
                "eligible": 0, "defaults": 0, "default_rate": 0.0, "outstanding": 0.0}
    volume = sum(r['loan_amount_val'] for r in data)
    avg_loan = volume / total
    avg_score = sum(r['credit_score_val'] for r in data) / total
    eligible = sum(r['is_eligible'] for r in data)
    defaults = sum(r['default_flag_val'] for r in data)
    rate = (defaults / eligible * 100.0) if eligible else 0.0
    outstanding = sum(r['outstanding_val'] for r in data)
    return {
        "total_loans": total,
        "volume": volume,
        "avg_loan": avg_loan,
        "avg_score": avg_score,
        "eligible": eligible,
        "defaults": defaults,
        "default_rate": rate,
        "outstanding": outstanding
    }

k = compute_kpis(filtered)

# -----------------------------------------------------------------------------
# PAGE 1: EXECUTIVE OVERVIEW
# -----------------------------------------------------------------------------
if page == "1. Executive Overview":
    st.markdown('<div class="main-header">Executive Credit Risk Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">High-level portfolio health, non-performing assets, and loan default indicators.</div>', unsafe_allow_html=True)
    
    # 4 Dynamic KPI Tiles
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #00B4D8;">
            <div class="kpi-title">Total Loans / Volume</div>
            <div class="kpi-value">{k['total_loans']:,}</div>
            <div class="kpi-sub">${k['volume']/1e6:.2f}M Disbursed</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #EF476F;">
            <div class="kpi-title">Overall Default Rate</div>
            <div class="kpi-value">{k['default_rate']:.2f}%</div>
            <div class="kpi-sub">{k['defaults']:,} Defaulted of {k['eligible']:,} Closed</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #FFD166;">
            <div class="kpi-title">Average Credit Score</div>
            <div class="kpi-value">{k['avg_score']:.1f}</div>
            <div class="kpi-sub">FICO Benchmark (300-850)</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #06D6A0;">
            <div class="kpi-title">Total Outstanding Balance</div>
            <div class="kpi-value">${k['outstanding']/1e6:.2f}M</div>
            <div class="kpi-sub">Active Capital at Risk</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("### Portfolio Visual Telemetry")
    ch_col1, ch_col2 = st.columns(2)
    
    with ch_col1:
        # Default Rate by Grade
        grades_list = sorted(list(set(r['loan_grade'] for r in filtered)))
        g_rates = []
        for g in grades_list:
            sub = [r for r in filtered if r['loan_grade'] == g]
            sub_k = compute_kpis(sub)
            g_rates.append(sub_k['default_rate'])
            
        fig_grade = go.Figure(go.Bar(
            x=grades_list,
            y=g_rates,
            marker_color='#00B4D8',
            text=[f"{v:.1f}%" for v in g_rates],
            textposition='outside'
        ))
        fig_grade.update_layout(
            title="Default Rate by Credit Grade (Prime to Subprime)",
            xaxis_title="Loan Grade",
            yaxis_title="Default Rate (%)",
            plot_bgcolor='rgba(0,0,0,0)',
            height=360
        )
        st.plotly_chart(fig_grade, use_container_width=True)
        
    with ch_col2:
        # Status Distribution Pie Chart
        statuses = {}
        for r in filtered:
            statuses[r['loan_status']] = statuses.get(r['loan_status'], 0) + 1
        fig_pie = px.pie(
            names=list(statuses.keys()),
            values=list(statuses.values()),
            title="Loan Status Composition",
            color_discrete_sequence=['#00B4D8', '#EF476F', '#FFD166', '#06D6A0', '#118AB2'],
            hole=0.45
        )
        fig_pie.update_layout(height=360)
        st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 2: LOAN PORTFOLIO ANALYSIS
# -----------------------------------------------------------------------------
elif page == "2. Loan Portfolio Analysis":
    st.markdown('<div class="main-header">Loan Portfolio Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Disbursement volume distribution, term lengths, and interest rates.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        # Term distribution
        terms = {}
        for r in filtered:
            terms[f"{r['loan_term_months']} Months"] = terms.get(f"{r['loan_term_months']} Months", 0) + 1
        fig_term = px.bar(
            x=list(terms.keys()),
            y=list(terms.values()),
            title="Loan Originations by Term Duration",
            labels={'x': 'Contract Term', 'y': 'Number of Loans'},
            color_discrete_sequence=['#1E3A8A']
        )
        fig_term.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=380)
        st.plotly_chart(fig_term, use_container_width=True)
        
    with col2:
        # Average Interest Rate by Grade
        g_rates_avg = []
        for g in all_grades:
            sub = [r for r in filtered if r['loan_grade'] == g]
            avg_int = (sum(r['interest_rate_val'] for r in sub) / len(sub)) if sub else 0
            g_rates_avg.append(avg_int)
        fig_int = go.Figure(go.Scatter(
            x=all_grades,
            y=g_rates_avg,
            mode='lines+markers',
            line=dict(color='#EF476F', width=3),
            marker=dict(size=8)
        ))
        fig_int.update_layout(
            title="Calibrated Interest Rate Premium by Credit Grade",
            xaxis_title="Loan Grade",
            yaxis_title="Average Interest Rate (%)",
            plot_bgcolor='rgba(0,0,0,0)',
            height=380
        )
        st.plotly_chart(fig_int, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 3: DEFAULT ANALYSIS
# -----------------------------------------------------------------------------
elif page == "3. Default Analysis":
    st.markdown('<div class="main-header">Default Analysis & Macro Trends</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Monthly default rate trajectories and historical performance.</div>', unsafe_allow_html=True)
    
    # Monthly trend calculation
    months = sorted(list(set(r['year_month'] for r in filtered)))
    m_rates = []
    m_vol = []
    for m in months:
        sub = [r for r in filtered if r['year_month'] == m]
        sub_k = compute_kpis(sub)
        m_rates.append(sub_k['default_rate'])
        m_vol.append(sub_k['volume'] / 1e6)
        
    fig_month = go.Figure()
    fig_month.add_trace(go.Scatter(
        x=months, y=m_rates, name="Default Rate (%)",
        line=dict(color='#EF476F', width=3)
    ))
    fig_month.add_trace(go.Bar(
        x=months, y=m_vol, name="Volume ($ Millions)",
        yaxis='y2', opacity=0.35, marker_color='#00B4D8'
    ))
    fig_month.update_layout(
        title="Monthly Default Rate Trajectory vs. Origination Volume",
        xaxis_title="Origination Month",
        yaxis=dict(title="Default Rate (%)", side='left'),
        yaxis2=dict(title="Volume ($M)", overlaying='y', side='right', showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)',
        height=450,
        legend=dict(x=0.01, y=0.99)
    )
    st.plotly_chart(fig_month, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 4: BORROWER RISK ANALYSIS
# -----------------------------------------------------------------------------
elif page == "4. Borrower Risk Analysis":
    st.markdown('<div class="main-header">Borrower Credit Risk Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Correlation between Credit Scores, Debt-to-Income (DTI), and Defaults.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        # Credit Score Range Default Rates
        score_ranges = ['300-579 (Very Poor)', '580-659 (Fair)', '660-719 (Good)', '720-799 (Very Good)', '800-850 (Exceptional)']
        s_rates = []
        for sr in score_ranges:
            sub = [r for r in filtered if r['credit_score_range'] == sr]
            s_k = compute_kpis(sub)
            s_rates.append(s_k['default_rate'])
        fig_score = px.bar(
            x=score_ranges, y=s_rates,
            title="Default Rate by FICO Credit Score Tiers",
            labels={'x': 'Credit Score Range', 'y': 'Default Rate (%)'},
            color_discrete_sequence=['#FF006E']
        )
        fig_score.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=380)
        st.plotly_chart(fig_score, use_container_width=True)
        
    with col2:
        # Home Ownership vs Default
        home_types = sorted(list(set(r['home_ownership'] for r in filtered)))
        h_rates = []
        for h in home_types:
            sub = [r for r in filtered if r['home_ownership'] == h]
            h_k = compute_kpis(sub)
            h_rates.append(h_k['default_rate'])
        fig_home = px.bar(
            x=home_types, y=h_rates,
            title="Default Propensity by Home Ownership Status",
            labels={'x': 'Residential Status', 'y': 'Default Rate (%)'},
            color_discrete_sequence=['#3A86FF']
        )
        fig_home.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=380)
        st.plotly_chart(fig_home, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 5: INCOME AND LOAN ANALYSIS
# -----------------------------------------------------------------------------
elif page == "5. Income and Loan Analysis":
    st.markdown('<div class="main-header">Income and Loan Amount Dynamics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluating default sensitivity across borrower earning segments.</div>', unsafe_allow_html=True)
    
    inc_bands = ['< $35,000', '$35,000 - $60,000', '$60,000 - $100,000', '> $100,000']
    inc_rates = []
    inc_counts = []
    for b in inc_bands:
        sub = [r for r in filtered if r['income_band'] == b]
        sub_k = compute_kpis(sub)
        inc_rates.append(sub_k['default_rate'])
        inc_counts.append(sub_k['total_loans'])
        
    col1, col2 = st.columns(2)
    with col1:
        fig_inc = go.Figure(go.Bar(
            x=inc_bands, y=inc_rates,
            marker_color=['#EF476F', '#FB5607', '#FFBE0B', '#06D6A0'],
            text=[f"{v:.1f}%" for v in inc_rates],
            textposition='outside'
        ))
        fig_inc.update_layout(
            title="Default Rate Across Annual Income Bands",
            xaxis_title="Income Segment (USD)",
            yaxis_title="Default Rate (%)",
            plot_bgcolor='rgba(0,0,0,0)',
            height=380
        )
        st.plotly_chart(fig_inc, use_container_width=True)
        
    with col2:
        fig_pie_inc = px.pie(
            names=inc_bands, values=inc_counts,
            title="Portfolio Volume Share by Income Tier",
            color_discrete_sequence=px.colors.sequential.Teal
        )
        fig_pie_inc.update_layout(height=380)
        st.plotly_chart(fig_pie_inc, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 6: LOAN PURPOSE ANALYSIS
# -----------------------------------------------------------------------------
elif page == "6. Loan Purpose Analysis":
    st.markdown('<div class="main-header">Loan Purpose Risk Concentration</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluating default rates across stated borrower expenditure intentions.</div>', unsafe_allow_html=True)
    
    p_names = sorted(list(set(r['loan_purpose'] for r in filtered)))
    p_rates = []
    p_vols = []
    for p in p_names:
        sub = [r for r in filtered if r['loan_purpose'] == p]
        sub_k = compute_kpis(sub)
        p_rates.append(sub_k['default_rate'])
        p_vols.append(sub_k['volume'] / 1e6)
        
    sorted_pairs = sorted(zip(p_names, p_rates, p_vols), key=lambda x: x[1], reverse=True)
    
    fig_purp = go.Figure(go.Bar(
        y=[x[0] for x in sorted_pairs][::-1],
        x=[x[1] for x in sorted_pairs][::-1],
        orientation='h',
        marker_color='#118AB2',
        text=[f"{x[1]:.1f}%" for x in sorted_pairs][::-1],
        textposition='outside'
    ))
    fig_purp.update_layout(
        title="Default Rate by Loan Purpose Category",
        xaxis_title="Default Rate (%)",
        yaxis_title="Purpose",
        plot_bgcolor='rgba(0,0,0,0)',
        height=450
    )
    st.plotly_chart(fig_purp, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 7: RISK SEGMENTATION & 3 DRILL-DOWN WORKFLOWS
# -----------------------------------------------------------------------------
elif page == "7. Risk Segmentation":
    st.markdown('<div class="main-header">Risk Segmentation & Functional Drill-Downs</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Interactive 3-tier deep-dive hierarchies for credit risk officers.</div>', unsafe_allow_html=True)
    
    st.markdown("### Select Drill-Down Workflow")
    workflow = st.selectbox(
        "Choose Multi-Dimensional Drill-Down Workflow",
        [
            "Workflow 1: Loan Grade → Loan Status → Loan Details",
            "Workflow 2: Income Band → Loan Purpose → Loan Details",
            "Workflow 3: Risk Category → Credit Score Range → Loan Details"
        ]
    )
    
    if workflow == "Workflow 1: Loan Grade → Loan Status → Loan Details":
        st.info("Step 1: Select a Loan Grade to examine loan status composition, then inspect individual loan contracts.")
        sel_drill_grade = st.selectbox("Select Loan Grade", all_grades, index=0)
        grade_filtered = [r for r in filtered if r['loan_grade'] == sel_drill_grade]
        
        st.write(f"**Found {len(grade_filtered)} loans for Grade {sel_drill_grade}**")
        status_counts = {}
        for r in grade_filtered:
            status_counts[r['loan_status']] = status_counts.get(r['loan_status'], 0) + 1
            
        fig_drill1 = px.bar(
            x=list(status_counts.keys()), y=list(status_counts.values()),
            title=f"Loan Status Breakdown for Grade {sel_drill_grade}",
            labels={'x': 'Loan Status', 'y': 'Count'},
            color_discrete_sequence=['#00B4D8']
        )
        fig_drill1.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=320)
        st.plotly_chart(fig_drill1, use_container_width=True)
        
        sel_drill_status = st.selectbox("Step 2: Select Status for Detailed Loan Inspection", list(status_counts.keys()))
        final_drill = [r for r in grade_filtered if r['loan_status'] == sel_drill_status]
        
        st.write(f"**Drill-Down Result: {len(final_drill)} Detailed Loan Records**")
        disp_cols = ['loan_id', 'customer_id', 'loan_amount', 'interest_rate', 'debt_to_income_ratio', 'credit_score', 'loan_status', 'default_flag']
        st.dataframe([{c: r[c] for c in disp_cols} for r in final_drill[:50]], use_container_width=True)

    elif workflow == "Workflow 2: Income Band → Loan Purpose → Loan Details":
        st.info("Step 1: Select an Income Band to examine Purpose distribution, then inspect individual loan contracts.")
        sel_drill_inc = st.selectbox("Select Income Band", all_income_bands, index=1)
        inc_filtered = [r for r in filtered if r['income_band'] == sel_drill_inc]
        
        purp_counts = {}
        for r in inc_filtered:
            purp_counts[r['loan_purpose']] = purp_counts.get(r['loan_purpose'], 0) + 1
            
        fig_drill2 = px.bar(
            x=list(purp_counts.keys()), y=list(purp_counts.values()),
            title=f"Loan Purposes in Income Tier: {sel_drill_inc}",
            labels={'x': 'Purpose', 'y': 'Count'},
            color_discrete_sequence=['#3A86FF']
        )
        fig_drill2.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=320)
        st.plotly_chart(fig_drill2, use_container_width=True)
        
        sel_drill_purp = st.selectbox("Step 2: Select Purpose for Detailed Loan Inspection", list(purp_counts.keys()))
        final_drill = [r for r in inc_filtered if r['loan_purpose'] == sel_drill_purp]
        
        st.write(f"**Drill-Down Result: {len(final_drill)} Detailed Loan Records**")
        disp_cols = ['loan_id', 'customer_id', 'annual_income', 'loan_amount', 'loan_purpose', 'loan_grade', 'loan_status', 'default_flag']
        st.dataframe([{c: r[c] for c in disp_cols} for r in final_drill[:50]], use_container_width=True)

    elif workflow == "Workflow 3: Risk Category → Credit Score Range → Loan Details":
        st.info("Step 1: Select a Risk Category to inspect Credit Score tiers, then review loan contracts.")
        sel_drill_rc = st.selectbox("Select Risk Category", all_risk, index=3)
        rc_filtered = [r for r in filtered if r['risk_category'] == sel_drill_rc]
        
        sr_counts = {}
        for r in rc_filtered:
            sr_counts[r['credit_score_range']] = sr_counts.get(r['credit_score_range'], 0) + 1
            
        fig_drill3 = px.bar(
            x=list(sr_counts.keys()), y=list(sr_counts.values()),
            title=f"Credit Score Distribution in {sel_drill_rc} Cohort",
            labels={'x': 'FICO Range', 'y': 'Count'},
            color_discrete_sequence=['#EF476F']
        )
        fig_drill3.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=320)
        st.plotly_chart(fig_drill3, use_container_width=True)
        
        sel_drill_sr = st.selectbox("Step 2: Select Credit Range for Detailed Loan Inspection", list(sr_counts.keys()))
        final_drill = [r for r in rc_filtered if r['credit_score_range'] == sel_drill_sr]
        
        st.write(f"**Drill-Down Result: {len(final_drill)} Detailed Loan Records**")
        disp_cols = ['loan_id', 'customer_id', 'credit_score', 'debt_to_income_ratio', 'risk_category', 'loan_amount', 'loan_status']
        st.dataframe([{c: r[c] for c in disp_cols} for r in final_drill[:50]], use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 8: DATA QUALITY MONITOR
# -----------------------------------------------------------------------------
elif page == "8. Data Quality Monitor":
    st.markdown('<div class="main-header">Data Quality & Pipeline Hygiene Audit</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Traceability log of detected raw anomalies, applied cleaning rules, and quarantined records.</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Raw Ingested Records", "10,050")
    with col2:
        st.metric("Clean Verified Records", f"{len(records_all):,}")
    with col3:
        st.metric("Quarantined Corrupted Records", "149", delta="-1.48% Anomaly Rate")
        
    st.markdown("### Automated Transformation & Remediation Log")
    if os.path.exists(QUALITY_LOG_PATH):
        with open(QUALITY_LOG_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            log_entries = list(reader)
        st.table(log_entries)
    else:
        st.warning("Data quality log file not found. Run src/data_cleaning.py first.")

# -----------------------------------------------------------------------------
# PAGE 9: SQL ANALYTICS
# -----------------------------------------------------------------------------
elif page == "9. SQL Analytics":
    st.markdown('<div class="main-header">Interactive SQL Analytics Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Query the SQLite Star Schema warehouse directly from the dashboard.</div>', unsafe_allow_html=True)
    
    sample_queries = {
        "Default Rate by Loan Grade (Query 1)": "SELECT g.grade_id, g.grade_name, COUNT(f.loan_id) AS total_loans, ROUND(100.0 * SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END), 0), 2) AS default_rate_pct FROM FACT_LOANS f JOIN DIM_LOAN_GRADE g ON f.grade_id = g.grade_id GROUP BY g.grade_id, g.grade_name ORDER BY g.grade_id;",
        "Default Rate by Income Band (Query 2)": "SELECT CASE WHEN c.annual_income < 35000 THEN '< $35,000' WHEN c.annual_income < 60000 THEN '$35,000 - $60,000' WHEN c.annual_income < 100000 THEN '$60,000 - $100,000' ELSE '> $100,000' END AS income_band, COUNT(f.loan_id) AS loans, ROUND(100.0 * SUM(CASE WHEN f.loan_status IN ('Charged Off', 'Default') THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN f.loan_status IN ('Fully Paid', 'Charged Off', 'Default') THEN 1 ELSE 0 END), 0), 2) AS default_rate_pct FROM FACT_LOANS f JOIN DIM_CUSTOMER c ON f.customer_id = c.customer_id GROUP BY income_band;",
        "Portfolio Summary View (V_PORTFOLIO_OVERVIEW)": "SELECT * FROM V_PORTFOLIO_OVERVIEW;"
    }
    
    sel_preset = st.selectbox("Select Pre-Configured Business Query", list(sample_queries.keys()))
    user_sql = st.text_area("SQL Statement", sample_queries[sel_preset], height=120)
    
    if st.button("Execute SQL Query"):
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            try:
                cur.execute(user_sql)
                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()
                st.success(f"Query executed successfully ({len(rows)} rows returned).")
                st.dataframe([dict(zip(cols, r)) for r in rows], use_container_width=True)
            except Exception as e:
                st.error(f"SQL Execution Error: {e}")
            finally:
                conn.close()
        else:
            st.error("Database data/loans.db not found. Execute src/database.py first.")

# -----------------------------------------------------------------------------
# PAGE 10: DATASET EXPLORER
# -----------------------------------------------------------------------------
elif page == "10. Dataset Explorer":
    st.markdown('<div class="main-header">Dataset Explorer & Export Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Search, inspect, and export clean banking records.</div>', unsafe_allow_html=True)
    
    search_term = st.text_input("🔍 Search by Loan ID or Customer ID", "")
    if search_term:
        disp_data = [r for r in filtered if search_term.upper() in r['loan_id'] or search_term.upper() in r['customer_id']]
    else:
        disp_data = filtered
        
    st.write(f"Displaying **{len(disp_data):,}** records (showing first 100 below):")
    st.dataframe([{k: r[k] for k in ['loan_id', 'customer_id', 'age', 'employment_type', 'annual_income', 'credit_score', 'loan_amount', 'interest_rate', 'loan_purpose', 'loan_grade', 'risk_category', 'loan_status']} for r in disp_data[:100]], use_container_width=True)
    
    st.markdown("### Download Data Deliverables")
    with open(CLEAN_DATA_PATH, mode='r', encoding='utf-8') as f:
        clean_csv_bytes = f.read()
    st.download_button(
        label="📥 Download Cleaned Dataset (CSV)",
        data=clean_csv_bytes,
        file_name="loans_clean.csv",
        mime="text/csv"
    )

# -----------------------------------------------------------------------------
# PAGE 11: PROJECT INFORMATION
# -----------------------------------------------------------------------------
elif page == "11. Project Information":
    st.markdown('<div class="main-header">Project Information & Technical Architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">B.Tech 2nd Year CSE Practical Evaluation Specifications.</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Project Metadata
    - **Project No.:** 6
    - **Official Title:** Loan Default Analysis and Risk Dashboard
    - **Domain:** Banking & Financial Services
    - **Developer:** B.Tech 2nd-Year CSE Student
    - **Technology Stack:** Python 3.x, Streamlit, Plotly, SQLite, Microsoft Power BI Desktop, Microsoft Excel
    
    ### Dimensional Architecture
    - **FACT_LOANS:** Fact table holding transaction metrics (`loan_amount`, `default_flag`, `outstanding_balance`, etc.)
    - **DIM_CUSTOMER:** Borrower demographics, income, and FICO credit scores.
    - **DIM_DATE:** Calendar dates with year, quarter, month, and month-name.
    - **DIM_LOAN_PURPOSE:** Categorical classification of loan proceeds.
    - **DIM_LOAN_GRADE:** Standardized risk rating master (Grades A to G).
    
    ### Acceptance Criteria Status
    1. **Default rate by grade:** Verified and dynamically updating across all pages.
    2. **Default rate by income band:** Verified across 4 income segments.
    3. **Default rate by purpose:** Verified across 7 purpose categories.
    4. **Documented Risk Bands:** 4-tier hybrid model (Low, Moderate, High, Critical Risk) documented and implemented.
    5. **Functional Drill-Downs:** 3 multi-dimensional drill-downs operating on Page 7.
    """)

# -----------------------------------------------------------------------------
# Global Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748B; font-size: 0.85rem;'>"
    "<b>Dataset Source Disclosure:</b> Standardized Synthetic Banking Dataset (N=9,901 clean records, random seed 42) "
    "calibrated against LendingClub credit rating benchmark standards. For academic, college evaluation, and portfolio demonstration purposes only."
    "</div>",
    unsafe_allow_html=True
)
