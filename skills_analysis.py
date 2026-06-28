import pandas as pd

# Pehle wali CSV file ko load karte hain
df = pd.read_csv("jobs_data_full.csv")

# Jo skills check karni hain, unki list
skills_list = [
    "python", "sql", "excel", "power bi", "tableau",
    "machine learning", "r programming", "aws", "azure",
    "statistics", "spark", "hadoop", "deep learning",
    "data visualization", "etl", "java"
]

# Description ko lowercase mein convert karte hain (case-insensitive matching ke liye)
df["description_lower"] = df["description"].str.lower()

# Har skill ke liye ek naya column banate hain
for skill in skills_list:
    column_name = "skill_" + skill.replace(" ", "_")
    df[column_name] = df["description_lower"].str.contains(skill, na=False)

# Check karte hain kitni jobs mein kaunsi skill mention hai
print("Skill demand (kitni jobs mein mention hai):\n")
for skill in skills_list:
    column_name = "skill_" + skill.replace(" ", "_")
    count = df[column_name].sum()
    print(f"{skill}: {count} jobs")

# Final result CSV mein save karte hain (skills columns ke saath)
df.to_csv("jobs_with_skills.csv", index=False)
print("\nSaved to jobs_with_skills.csv")