from modules.college_mode import get_internships, get_certifications
from modules.fresher_mode import recommend_jobs, recommend_projects


# ==============================
# COLLEGE RECOMMENDATION ENGINE
# ==============================
def college_recommendation(domain):
    internships = get_internships(domain)
    
    return {
        "internships": internships
        
    }


# ==============================
# FRESHER RECOMMENDATION ENGINE
# ==============================
def fresher_recommendation(role, domain):
    jobs = recommend_jobs(role)
    projects = recommend_projects(domain)

    return {
        "jobs": jobs,
        "projects": projects
    }