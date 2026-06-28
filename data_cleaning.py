import pandas as pd

df = pd.read_csv("jobs_with_skills.csv")

# Remote detection (already pata chala 0 hai, but column rakhte hain documentation ke liye)
df["is_remote"] = df["description"].str.lower().str.contains(
    "remote|work from home|wfh", na=False
)

# Salary cleaning: agar salary_max 1000 se kam hai, toh use invalid maan ke NaN bana dete hain
df.loc[df["salary_max"] < 1000, "salary_max"] = None
df.loc[df["salary_min"] < 1000, "salary_min"] = None

# Ab dekhte hain kitni valid salary entries bachi
valid_salary_count = df["salary_max"].notna().sum()
print(f"Valid salary entries: {valid_salary_count} out of {len(df)}")

print("\nCleaned salary_max distribution:")
print(df["salary_max"].describe())

# Final cleaned file save karte hain
df.to_csv("jobs_final_cleaned.csv", index=False)
print("\nSaved to jobs_final_cleaned.csv")