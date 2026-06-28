import requests
import pandas as pd
import time

# Apni Adzuna credentials
from config import APP_ID, APP_KEY

# Jo job titles search karne hain
job_titles = ["data analyst", "data scientist"]

# Jo cities search karni hain
cities = [
    "bangalore", "delhi", "mumbai", "pune", "hyderabad",
    "chennai", "kolkata", "jaipur", "ahmedabad", "noida",
    "gurgaon", "indore", "chandigarh", "kochi", "coimbatore",
    "bhubaneswar", "nagpur", "lucknow", "surat", "vadodara"
]

# Kitne pages chahiye har combination ke liye (1 page = 10 results)
pages_per_search = 2

# Final list - sab jobs yahan jama hongi
all_jobs = []

# Nested loop - pehle job title pe loop, uske andar city pe loop, uske andar page pe loop
for title in job_titles:
    for city in cities:
        for page in range(1, pages_per_search + 1):

            url = f"https://api.adzuna.com/v1/api/jobs/in/search/{page}"

            params = {
                "app_id": APP_ID,
                "app_key": APP_KEY,
                "what": title,
                "where": city,
                "content-type": "application/json"
            }

            response = requests.get(url, params=params)

            # Agar request fail ho gayi, skip karo aur aage badho
            if response.status_code != 200:
                print(f"Failed: {title} in {city}, page {page}")
                continue

            data = response.json()
            results = data.get("results", [])

            print(f"Fetched {len(results)} jobs for '{title}' in '{city}' (page {page})")

            for job in results:
                job_info = {
                    "search_title": title,
                    "search_city": city,
                    "title": job.get("title", "N/A"),
                    "company": job.get("company", {}).get("display_name", "Not Specified"),
                    "location": job.get("location", {}).get("display_name", "N/A"),
                    "description": job.get("description", ""),
                    "salary_min": job.get("salary_min", None),
                    "salary_max": job.get("salary_max", None),
                    "created": job.get("created", "")
                }
                all_jobs.append(job_info)

            # Adzuna ko thoda time dete hain (politeness/rate-limit ke liye)
            time.sleep(1)

# Sab jobs ko ek DataFrame mein convert karte hain
df = pd.DataFrame(all_jobs)

# Duplicate jobs hata dete hain (agar same job 2 baar aa gayi ho)
df = df.drop_duplicates(subset=["title", "company", "location", "description"])

# Final CSV save karte hain
df.to_csv("jobs_data_full.csv", index=False)

print("\nTotal unique jobs saved:", len(df))
print(df["search_city"].value_counts())