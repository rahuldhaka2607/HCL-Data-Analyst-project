# Academic Project Synopsis

## 1. Title of the Project
**Loan Default Analysis and Risk Dashboard**  
*Project No.: 6 | Academic Level: B.Tech 2nd Year CSE*  

---

## 2. Problem
Commercial and retail lending institutions incur heavy financial losses when borrowers fail to meet their debt obligations (loan default). In real-world banking environments, credit analysts face raw transactional data plagued by missing records, extreme loan values, duplicate entries, and inconsistent status labels. Without a systematic data cleaning pipeline, rigorous dimensional modeling, and intuitive multi-level dashboards, credit risk officers cannot promptly detect subprime concentration risks or understand how borrower income, credit scores, and loan purposes influence default rates.

---

## 3. Objectives
1. **Data Pipeline Engineering:** Develop an end-to-end Python pipeline to ingest, clean, and validate 10,000 synthetic banking records with controlled real-world data quality anomalies.
2. **Relational & Dimensional Modeling:** Design and implement an industry-standard Star Schema (1 Fact, 4 Dimensions) with SQLite and Oracle SQL DDL, ensuring referential integrity and optimized analytical queries.
3. **Cross-Tool Financial Reconciliation:** Compute 11 essential banking KPIs and guarantee 100% numerical alignment across Python, SQL, Excel, and Power BI.
4. **Interactive BI Visualizations:** Construct a modern 11-page Streamlit web application and an enterprise Power BI report with dynamic slicers and three functional drill-down workflows to assist credit decision-making.

---

## 4. Scope
- **In Scope:**
  - Synthetic dataset generation (10,000 rows, 20 attributes) with fixed seed `42`.
  - Automated data cleaning, quarantine logging, and before/after quality reporting.
  - Multi-tier risk categorization (Low, Moderate, High, Critical Risk).
  - Seven comprehensive SQL analytical queries and view definitions.
  - Interactive Streamlit dashboard with Navy/Teal UI, KPI cards, and Plotly charts.
  - Power BI data model specification, DAX measure library, and setup guide.
  - Excel analysis with Power Query instructions, PivotTables, and dashboard sheets.
  - Automated pipeline testing suite and academic viva voce documentation.
- **Out of Scope:**
  - Machine learning real-time model deployment in cloud production.
  - Direct connection to proprietary live banking mainframe APIs.

---

## 5. Data Source
A realistic synthetic retail banking dataset generated using Python (Pandas/NumPy) with fixed seed `42` simulating 10,000 loan applications across credit grades A through G, credit scores (300–850), debt-to-income ratios (5%–60%), annual incomes, and loan terms (36 and 60 months). Injected anomalies include missing incomes, extreme loan amounts, duplicate IDs, invalid credit scores, and irregular dates.

---

## 6. Tools and Technologies
- **Programming & Analysis:** Python 3.x (Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit, OpenPyXL).
- **Database & Querying:** SQLite (local embedded engine) and Oracle SQL-compatible DDL/queries.
- **Business Intelligence:** Microsoft Power BI Desktop (Power Query, Star Schema, DAX).
- **Spreadsheet:** Microsoft Excel (Formulas, PivotTables, Power Query).
- **Development Environment:** VS Code, Git, Google Colab / Jupyter Notebook.

---

## 7. Deliverables
1. Python source code (`src/` for generation, cleaning, risk scoring, KPIs, reconciliation, and database management).
2. Cleaned datasets and quarantined anomaly records (`data/clean/`, `data/reports/`).
3. SQL scripts (`sql/schema.sql`, `sql/queries.sql`, `sql/oracle/`, `sql/views/`).
4. 11-page Streamlit dashboard (`app/streamlit_app.py`).
5. Jupyter Notebook (`notebooks/loan_default_analysis.ipynb`).
6. Power BI documentation (`powerbi/dax_measures.dax`, `powerbi/setup_guide.md`).
7. Excel analytical workbook (`excel/loan_analysis_dashboard.xlsx`).
8. Automated test suite (`tests/test_pipeline.py`) and reports (`reports/`).
9. Academic project report, documentation, and Viva Voce guide (`docs/`).

---

## 8. Six-Week Project Plan

| Week | Phase Focus | Key Activities & Milestones | Deliverables |
|:---:|:---|:---|:---|
| **Week 1** | P1 – P3 | Requirements analysis, project synopsis, risk band formulation, and complete SRS creation. | `problem_statement.md`, `synopsis.md`, `srs.md` |
| **Week 2** | P4 – P6 | Synthetic dataset generation (10k rows), data dictionary generation, cleaning pipeline, and quality logging. | `data_generator.py`, `data_cleaning.py`, `data_dictionary.md`, `data_quality_report.md` |
| **Week 3** | P7 – P10 | Star schema design, SQLite/Oracle DDL, 7 SQL analytical queries, Python KPI engine, and Jupyter Notebook. | `schema.sql`, `queries.sql`, `kpis.json`, `loan_default_analysis.ipynb` |
| **Week 4** | P11 – P13 | Interactive 11-page Streamlit web app, Power BI data model, DAX measures library, and setup guide. | `streamlit_app.py`, `dax_measures.dax`, `data_model.md`, `setup_guide.md` |
| **Week 5** | P14 – P15 | Microsoft Excel workbook with PivotTables/Power Query, test suite creation, and automated pipeline validation. | `loan_analysis_dashboard.xlsx`, `test_pipeline.py`, `test_results.csv` |
| **Week 6** | P16 – P20 | Final academic report, README, viva voce preparation guide, cross-tool reconciliation, and evaluation checklist. | `README.md`, `final_report.md`, `viva_questions.md`, `reconciliation_report.csv` |

---

## 9. Expected Outcome
The student will deliver a fully functioning, industry-aligned Data Analytics system demonstrating data hygiene, relational modeling, advanced SQL querying, interactive BI visualization, and cross-platform verification. The project equips the student with practical experience and complete confidence for college semester evaluations, viva defense, and professional portfolio presentation.
