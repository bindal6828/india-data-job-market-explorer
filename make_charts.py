import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("jobs_final_cleaned.csv")

skill_columns = [col for col in df.columns if col.startswith("skill_")]

# ---------- CHART 1: Overall skill demand (bar chart) ----------

skill_totals = df[skill_columns].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
skill_totals.plot(kind="bar", color="steelblue")
plt.title("Overall Skill Demand Across All Jobs")
plt.xlabel("Skill")
plt.ylabel("Number of Jobs Mentioning Skill")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("chart_overall_skills.png")
print("Saved: chart_overall_skills.png")
plt.close()

# ---------- CHART 2: City-wise comparison (grouped bar chart) ----------

comparison = df.groupby("search_city")[skill_columns].mean() * 100

# Sirf top 6 skills lete hain (taaki chart clean rahe, sab 16 nahi)
top_skills = skill_totals.head(6).index
comparison_top = comparison[top_skills]

comparison_top.T.plot(kind="bar", figsize=(10, 6))
plt.title("Top Skills Demand by City (%)")
plt.xlabel("Skill")
plt.ylabel("% of Jobs Mentioning Skill")
plt.xticks(rotation=45, ha="right")
plt.legend(title="City")
plt.tight_layout()
plt.savefig("chart_city_comparison.png")
print("Saved: chart_city_comparison.png")
plt.close()