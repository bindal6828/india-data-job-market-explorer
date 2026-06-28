import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression, RidgeCV


df = pd.read_csv("jobs_final_cleaned.csv")
skill_columns = [col for col in df.columns if col.startswith("skill_")]

# ---------- Sirf wahi rows lo jisme salary_max present hai ----------
model_df = df[df["salary_max"].notna()].copy()
print(f"Training data: {len(model_df)} jobs with salary info")

# ---------- Features (X) aur Target (y) define karte hain ----------
X = model_df[skill_columns]          # Input: kaunsi skills hain (0/1)
y = model_df["salary_max"]           # Output: salary_max predict karni hai

# ---------- Train-test split ----------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------- Model train karna ----------
# RidgeCV khud best alpha (penalty strength) dhundta hai, multiple values try karke
model = RidgeCV(alphas=[0.1, 1, 10, 50, 100, 500, 1000])
model.fit(X_train, y_train)
print(f"\nBest alpha (penalty strength) chosen: {model.alpha_}")

# ---------- Model ko test karna ----------
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f"\nModel Performance:")
print(f"Mean Absolute Error: Rs.{mae:,.0f}")
print(f"R² Score: {r2:.2f}")

# ---------- Har skill ka salary pe impact dekhte hain ----------
coefficients = pd.Series(model.coef_, index=skill_columns).sort_values(ascending=False)
coefficients.index = [s.replace("skill_", "").replace("_", " ").title() for s in coefficients.index]

print("\nSkill Impact on Salary (Rs. added/subtracted):")
print(coefficients)

# ---------- Model ko save karte hain (dashboard mein use karne ke liye) ----------
import joblib
joblib.dump(model, "salary_model.pkl")
print("\nModel saved as salary_model.pkl")