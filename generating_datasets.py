import pandas as pd
import random
import uuid
from faker import Faker
import os

fake = Faker()

BASE_PATH = "datasets"
DB_PATH = "database"

os.makedirs(BASE_PATH, exist_ok=True)
os.makedirs(DB_PATH, exist_ok=True)

# =====================================================
# EMPTY DATABASE FILES (CORRECT APPROACH)
# =====================================================

pd.DataFrame(columns=["id", "name", "email", "password", "mode"]).to_csv(f"{DB_PATH}/users.csv", index=False)

pd.DataFrame(columns=["id", "email", "password"]).to_csv(f"{DB_PATH}/admin.csv", index=False)

pd.DataFrame(columns=["user_id", "result_type", "details"]).to_csv(f"{DB_PATH}/results.csv", index=False)

pd.DataFrame(columns=["user_id", "message", "response", "rating"]).to_csv(f"{DB_PATH}/feedback.csv", index=False)

pd.DataFrame(columns=["timestamp", "activity"]).to_csv(f"{DB_PATH}/logs.csv", index=False)

print("✅ Empty database CSV files created")


# =====================================================
# INTERNSHIPS (600 RECORDS)
# =====================================================
internships = []
for _ in range(600):
    internships.append({
        "InternshipID": random.randint(1000, 9999),
        "Company": fake.company(),
        "Domain": random.choice(["AI", "Web Dev", "Data Science", "Cyber Security"]),
        "Location": fake.city(),
        "Stipend": random.randint(5000, 20000),
        "Duration": random.choice(["2 Months", "3 Months", "6 Months"])
    })

pd.DataFrame(internships).to_csv(f"{BASE_PATH}/internships.csv", index=False)


# =====================================================
# JOBS (700 RECORDS)
# =====================================================
jobs = []
for _ in range(700):
    jobs.append({
        "JobID": random.randint(10000, 99999),
        "Company": fake.company(),
        "Role": random.choice(["Software Engineer", "Data Analyst", "ML Engineer"]),
        "Location": fake.city(),
        "Salary": random.randint(300000, 1200000),
        "ExperienceRequired": random.choice(["0-1", "1-2", "2-3"])
    })

pd.DataFrame(jobs).to_csv(f"{BASE_PATH}/jobs.csv", index=False)


# =====================================================
# FRESHER PROJECTS (800 RECORDS)
# =====================================================
projects = []
for i in range(800):
    projects.append({
        "ProjectID": i,
        "Title": f"{random.choice(['AI', 'ML', 'Web', 'Data'])} Project {i}",
        "Domain": random.choice(["AI", "ML", "Web Development", "Data Science"]),
        "Difficulty": random.choice(["Beginner", "Intermediate", "Advanced"]),
        "TechnologiesUsed": random.choice(["Python", "Flask", "React", "TensorFlow"]),
        "EstimatedTime": random.choice(["1 Month", "2 Months", "3 Months"])
    })

pd.DataFrame(projects).to_csv(f"{BASE_PATH}/fresher_projects.csv", index=False)


# =====================================================
# PLACEMENT DATASET (600 RECORDS)
# =====================================================
placement = []
for _ in range(600):
    cgpa = round(random.uniform(5.0, 9.5), 2)
    internships_count = random.randint(0, 3)
    projects_count = random.randint(1, 5)
    placed = 1 if cgpa > 7 and internships_count > 0 else 0

    placement.append({
        "CGPA": cgpa,
        "Internships": internships_count,
        "Projects": projects_count,
        "Placed": placed
    })

pd.DataFrame(placement).to_csv(f"{BASE_PATH}/placement_dataset.csv", index=False)


# =====================================================
# CERTIFICATIONS (500 RECORDS)
# =====================================================
certifications = []
for _ in range(500):
    certifications.append({
        "CertificationID": random.randint(1000, 9999),
        "Title": random.choice(["AI Certification", "Python Mastery", "Cloud Basics"]),
        "Platform": random.choice(["Coursera", "Udemy", "NPTEL"]),
        "Duration": random.choice(["4 Weeks", "6 Weeks", "8 Weeks"])
    })

pd.DataFrame(certifications).to_csv(f"{BASE_PATH}/certifications.csv", index=False)


# =====================================================
# CHATBOT DATA (500 EACH)
# =====================================================
chatbot_college = []
for i in range(500):
    chatbot_college.append({
        "question": f"College Question {i}",
        "answer": "Focus on CGPA, internships and skill development."
    })

pd.DataFrame(chatbot_college).to_csv(f"{BASE_PATH}/chatbot_college.csv", index=False)


chatbot_fresher = []
for i in range(500):
    chatbot_fresher.append({
        "question": f"Fresher Question {i}",
        "answer": "Build projects, improve communication and apply consistently."
    })

pd.DataFrame(chatbot_fresher).to_csv(f"{BASE_PATH}/chatbot_fresher.csv", index=False)


print("✅ All dataset CSV files created successfully!")