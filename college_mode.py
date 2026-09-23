import pandas as pd


# ==============================
# STUDY PLAN GENERATION
# ==============================
def get_personalized_timetable(hours, prep_level, subject):
    h = float(hours)
    
    # 1. Define Focus and Time Ratios
    if prep_level == "scratch":
        focus = "Intensive Learning Mode"
        ratios = [0.1, 0.6, 0.3] # 10% Rev, 60% Reading, 30% Practice
    elif prep_level == "intermediate":
        focus = "Balanced Reinforcement"
        ratios = [0.2, 0.4, 0.4] # 20% Rev, 40% Reading, 40% Practice
    else: # advanced
        focus = "Mastery & Speed Practice"
        ratios = [0.3, 0.1, 0.6] # 30% Rev, 10% Reading, 60% Practice

    # 2. Generate Sessions with Breaks
    # We create a 4-step cycle: Revision -> Break -> Deep Study -> Break -> Practice
    break_time = 0.25 # 15 minutes break fixed
    
    timetable = [
        {"activity": "Quick Concept Recap", "time": f"{h*ratios[0]:.1f} hrs"},
        {"activity": "☕ Short Break", "time": f"{break_time} hrs"},
        {"activity": f"Reading {subject} Notes", "time": f"{(h*ratios[1]) - (break_time/2):.1f} hrs"},
        {"activity": "🚶 Stretching/Water Break", "time": f"{break_time} hrs"},
        {"activity": "Solving Question Bank", "time": f"{(h*ratios[2]) - (break_time/2):.1f} hrs"}
    ]
    
    return focus, timetable
# ==============================
# INTERNSHIP RECOMMENDATION
# ==============================
def get_internships(domain):
    df = pd.read_csv("datasets/internship_suggestions.csv")
    return df[df["Domain"] == domain].head(10).to_dict(orient="records")


