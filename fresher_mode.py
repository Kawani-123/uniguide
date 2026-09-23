import pandas as pd


# ==============================
# SKILL RECOMMENDATION
# ==============================
def recommend_skills(domain):
    skills_map = {
        "AI": ["Python", "TensorFlow", "Machine Learning", "Deep Learning"],
        "Web Development": ["HTML", "CSS", "JavaScript", "React"],
        "Data Science": ["Python", "Pandas", "NumPy", "SQL"]
    }
    return skills_map.get(domain, ["Communication", "Problem Solving"])


# ==============================
# JOB RECOMMENDATION
# ==============================
def recommend_jobs(role):
    df = pd.read_csv("datasets/jobs.csv")
    return df[df["Role"] == role].head(10).to_dict(orient="records")


# ==============================
# PROJECT SUGGESTIONS
# ==============================
def recommend_projects(domain):
    try:
        # Load the provided CSV file 
        df = pd.read_csv("C:/Users/ASUS/Desktop/Practice project/datasets/fresher_projects.csv")
        # Filter rows where the 'Branch' column matches the user selection 
        return df[df["Branch"] == domain].head(10).to_dict(orient="records")
    except Exception as e:
        print(f"Error: {e}")
        return []