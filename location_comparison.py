import pandas as pd

# Pehle wali skills wali file load karte hain
df = pd.read_csv("jobs_with_skills.csv")

# Saari skill wali columns ki list nikalte hain (jo "skill_" se start hoti hain)
skill_columns = [col for col in df.columns if col.startswith("skill_")]

# City ke hisaab se group karke, har skill ka average (%) nikalte hain
comparison = df.groupby("search_city")[skill_columns].mean() * 100

# Round off karte hain 1 decimal tak, readability ke liye
comparison = comparison.round(1)

print("City-wise Skill Demand (% of jobs mentioning each skill):\n")
print(comparison.T)  # .T se table ko transpose kar rahe hain (skills rows mein, cities columns mein)

# CSV mein bhi save kar lete hain
comparison.T.to_csv("location_comparison.csv")
print("\nSaved to location_comparison.csv")