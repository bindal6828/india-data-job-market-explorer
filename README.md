# 📊 India Data Job Market Explorer

A real-world data analytics project that collects, cleans, and analyzes live Data Analyst & Data Scientist job postings across 20 major Indian cities — surfacing in-demand skills, city-wise market differences, and a salary-prediction model, all wrapped in an interactive dashboard.

**[🔗 Live Dashboard](#)** *(add your deployed Streamlit Cloud link here)*

---

## 🎯 Why This Project

Most "job market analysis" projects rely on static, pre-cleaned Kaggle datasets. This project instead pulls **live data directly from a public job API**, handles the real-world messiness that comes with it (missing fields, inconsistent salary scales, irrelevant titles, API rate limits), and turns it into actionable insight — the same workflow a working data analyst would follow.

---

## ✨ Features

- **Live data collection** from the Adzuna Jobs API (India) across 20 cities and 2 role types
- **Automated skill extraction** from raw job descriptions using keyword-based NLP matching
- **Data cleaning pipeline** — handles missing values, salary outliers, and unreliable small-sample data
- **Interactive Streamlit dashboard** with city/skill filters, dynamic metrics, and auto-generated insight text
- **City × Skill heatmap** for spotting regional demand patterns
- **Salary prediction model** (Ridge Regression) estimating how individual skills affect expected salary
- Fully reproducible pipeline — re-run anytime to refresh the data

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.13 |
| Data Collection | Requests, Adzuna Jobs API |
| Data Processing | Pandas |
| Visualization | Plotly, Matplotlib |
| Dashboard | Streamlit |
| Machine Learning | scikit-learn (RidgeCV) |

---

## 📂 Project Structure

```
Job-Market_analysis/
├── scraper.py                  # Pulls job data from Adzuna API
├── skills_analysis.py          # Extracts skill mentions from descriptions
├── data_cleaning.py            # Cleans salary outliers, flags remote jobs
├── make_charts.py              # Generates static charts (PNG)
├── location_comparison.py      # City-wise skill demand breakdown
├── salary_model.py             # Trains the salary prediction model
├── dashboard.py                # Interactive Streamlit dashboard
├── config.py                   # API credentials (NOT included — see setup)
├── .streamlit/config.toml      # Dashboard theme settings
└── jobs_final_cleaned.csv      # Final processed dataset
```

---

## ⚙️ Setup & How to Run

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/india-data-job-market-explorer.git
   cd india-data-job-market-explorer
   ```

2. **Install dependencies**
   ```bash
   pip install requests pandas matplotlib streamlit plotly scikit-learn joblib
   ```

3. **Add your API credentials**
   Get a free key at [developer.adzuna.com](https://developer.adzuna.com), then create a `config.py` file:
   ```python
   APP_ID = "your_app_id"
   APP_KEY = "your_app_key"
   ```

4. **Run the pipeline** (in order)
   ```bash
   python scraper.py
   python skills_analysis.py
   python data_cleaning.py
   python make_charts.py
   python location_comparison.py
   python salary_model.py
   ```

5. **Launch the dashboard**
   ```bash
   python -m streamlit run dashboard.py
   ```

---

## 📈 Key Insights

Based on **579 unique job postings** across 20 cities:

- **Machine Learning (90 jobs)** and **Python (79 jobs)** are the most frequently requested skills overall — ahead of traditional BI tools like Excel (46) and Power BI (20).
- **Tableau and R programming** appear in fewer than 3% of postings in this sample, suggesting most current demand in these search categories skews toward Python/ML-based roles over classic BI tooling.
- City-level patterns differ meaningfully: smaller cities like **Ahmedabad** show a surprisingly high concentration of ML-related postings relative to their job count, while metro hubs show more balanced skill distribution.
- Only **~17% of job postings (98 of 579)** disclosed salary information — a reminder that salary transparency is still limited in the Indian job market.
- A **Ridge Regression salary model** found that Machine Learning, Statistics, and ETL skills correlate with higher predicted salaries, while Excel and Data Visualization correlate with lower ones — directionally consistent with industry expectations, though the model's R² remains low due to limited sample size (see Limitations).

---

## 🔍 Methodology Notes

- **Skill extraction** is keyword-based (case-insensitive substring match on job descriptions) — not full NLP entity recognition. This is fast and transparent but can occasionally over/under-count skills phrased unusually.
- **Remote job detection** was attempted via description-text keyword search; no postings in this sample explicitly mentioned "remote" — a real finding about this dataset, not a pipeline error.
- **Salary outliers** (e.g., values too small to be annual CTC) were identified by inspecting the distribution and excluded from salary-based analysis, while keeping the job listing itself in the dataset.
- **The city × skill heatmap** only includes cities with 15+ postings, to avoid misleading percentages from very small samples (e.g., a city with 4 postings where 2 mention a skill would show "50% demand," which isn't statistically meaningful).

---

## ⚠️ Limitations & Future Work

- **Snapshot, not time-series:** This data represents a single point in time. Genuine trend/growth forecasting would require repeated scraping over weeks/months — noted here as a deliberate scope decision, not an oversight.
- **Salary model sample size:** Only 98 postings had disclosed salaries, which is small for a 16-feature regression model. Results are directionally useful but not precise predictions. Regularization (RidgeCV) was used specifically to reduce overfitting risk from this small sample.
- **Planned next steps:**
  - Schedule the scraper to run weekly to build a time-series dataset
  - Use that time-series data for genuine trend forecasting (e.g., "is ML demand growing month-over-month?")
  - Expand skill extraction to a proper NLP/NER-based approach for better accuracy

---

## 📊 Dashboard Preview

*(Add 2–3 screenshots of your dashboard here once uploaded to GitHub)*

---

## 📄 Data Source

Job listing data sourced from the [Adzuna Jobs API](https://developer.adzuna.com/) (India region). This project is for educational/portfolio purposes only.

---

## 👤 Author

**Tushar** — Data Analytics & Data Science enthusiast
*Built as a hands-on, end-to-end project: API integration → data cleaning → analysis → ML → interactive dashboard.*
