import email
from flask import Flask, flash, render_template, request, redirect, url_for, session
import pandas as pd
import csv
import os
import random
from config import Config
from modules.chatbot import get_fresher_chatbot_response,get_chatbot_response
from database.models import (
    check_user, add_user, 
    check_admin
)


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
DATASETS_DIR = os.path.join(BASE_DIR, 'datasets')

# Path assignments based on your folder image
# 1. users.csv is inside the 'database' folder
USERS_CSV = os.path.join(DATABASE_DIR, 'users.csv') 
FEEDBACK_CSV = os.path.join(DATABASE_DIR, 'feedback.csv') 
# 2. These are inside the 'datasets' folder
JOBS_CSV = os.path.join(DATASETS_DIR, 'jobs.csv')
PROJECTS_CSV = os.path.join(DATASETS_DIR, 'fresher_projects.csv')
CHATBOT_COLLEGE_CSV = os.path.join(DATASETS_DIR, 'chatbot_college.csv')
CHATBOT_FRESHER_CSV = os.path.join(DATASETS_DIR, 'chatbot_fresher.csv')
NOTES_CSV = os.path.join(DATASETS_DIR, 'notes.csv')  # Assuming your notes are here
IMP_QA_CSV = os.path.join(DATASETS_DIR, 'imp_qa.csv')

# =====================================
# APP INITIALIZATION
# =====================================

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "uniguide_secret"

# =====================================
# PUBLIC PAGES
# =====================================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/approach")
def approach():
    return render_template("approach.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():

    import os, csv

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_DIR = os.path.join(BASE_DIR, "database")
    FEEDBACK_CSV = os.path.join(DATABASE_DIR, "feedback.csv")

    os.makedirs(DATABASE_DIR, exist_ok=True)

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        rating = request.form.get("rating")

        new_entry = [name, email, message, rating]

        # ✅ CHECK DUPLICATE
        exists = False
        if os.path.exists(FEEDBACK_CSV):
            with open(FEEDBACK_CSV, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row == new_entry:
                        exists = True
                        break

        # ✅ SAVE ONLY IF NEW
        if not exists:
            with open(FEEDBACK_CSV, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)

                if os.path.getsize(FEEDBACK_CSV) == 0:
                    writer.writerow(["user", "email", "message", "rating"])

                writer.writerow(new_entry)

        flash("Thank you for your feedback!")

        return redirect(url_for("contact"))

    return render_template("contact.html")
# =====================================
# AUTH
# =====================================

@app.route("/login", methods=["POST"])
def login():

    email = request.form.get("email")
    password = request.form.get("password")
    print(email, password,)

    user = check_user(email, password)

    if user:
        session["email"] = user["email"]
        session["name"] = user["name"]
        session["mode"] = user["mode"]

        flash("Login successful!", "success")

        if user["mode"] == "college":
            return redirect(url_for("college"))
        else:
            return redirect(url_for("fresher"))

    else:
        flash("Invalid email or password.", "danger")
        return redirect(url_for("index"))

@app.route("/register", methods=["POST"])
def register():
    print("REGISTER ROUTE HIT")
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    mode = request.form.get("mode")
    
    success, msg = add_user(name, email, password, mode)

    if success:
        session["name"] = name
        session["email"] = email
        session["mode"] = mode

        flash("Account created successfully!", "success")
    else:
        flash(msg, "danger")

    return redirect(url_for("index"))

from flask import session, request, render_template, redirect, url_for, flash
import csv

def get_all_users():
    with open(USERS_CSV, newline='', encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save_all_users(users, fieldnames):
    with open(USERS_CSV, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)
@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    user_email = session.get("email")
    if not user_email:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))

    users = get_all_users()
    
    # Check if bio column exists; if not, add it to fieldnames
    fieldnames = users[0].keys() if users else ["email", "password", "name", "mode"]
    if "bio" not in fieldnames:
        fieldnames = list(fieldnames) + ["bio"]

    # Find the current user
    user = next((u for u in users if u["email"] == user_email), None)
     # Find the current user
    user = next((u for u in users if u["email"] == user_email), None)
    if not user:
        flash("User not found!", "danger")
        return redirect(url_for("index"))
    if request.method == "POST":
        
        # Update name, bio, mode
        name = request.form.get("name", user.get("name"))
        bio = request.form.get("bio", user.get("bio", ""))
        mode = request.form.get("mode", user.get("mode", "college"))  # default college
        user["name"] = name
        user["bio"] = bio
        user["mode"] = mode
        # Update session
        session["name"] = name
        session["bio"] = bio
        session["mode"] = mode
        # Save all users back to CSV
        save_all_users(users, fieldnames)

        flash("Profile updated successfully!", "success")
        return redirect(url_for("index"))

    return render_template("edit_profile.html", user=user, bio=user.get("bio", ""))
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
    

# =====================================
# DASHBOARDS
# =====================================

@app.route("/college")
def college():
    if "email" not in session:
        flash("Please login first", "error")
        return redirect(url_for("index"))

    if session.get("mode") != "college":
        flash("Switch to College Mode to access StudyPro", "error")
        return redirect(url_for("index"))

    return render_template("college.html")

@app.route("/fresher")
def fresher():
    if "email" not in session:
        flash("Please login first", "error")
        return redirect(url_for("index"))

    if session.get("mode") != "fresher":
        flash("Switch to Career Mode to access CareerStart", "error")
        return redirect(url_for("index"))

    return render_template("fresher.html")


# =====================================
# COLLEGE FEATURES
# =====================================
import os
import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for
# --- UNIVERSAL HELPER FUNCTION ---
# This version handles paths safely and prevents duplicate rows automatically
def get_csv_data(file_name, filters=None):
    base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'datasets')
    path = os.path.join(base_path, file_name)
    
    if not os.path.exists(path):
        print(f"CRITICAL ERROR: {file_name} not found at {path}")
        return []
    
    # Load and immediately drop identical rows to prevent repetition
    df = pd.read_csv(path).drop_duplicates()
    
    if filters:
        for col, val in filters.items():
            if col in df.columns and val:
                # Case-insensitive, whitespace-trimmed filtering
                df = df[df[col].astype(str).str.strip().str.lower() == str(val).strip().lower()]
    
    return df.to_dict(orient='records')

# --- 1. ACADEMIC SUCCESS PLANNER ---
@app.route('/study', methods=['GET', 'POST'])
def study_plan():
    timetable, notes, questions = None, [], []
    if request.method == 'POST':
        branch = request.form.get('branch', '').strip()
        subject = request.form.get('subject', '').strip()
        try:
            hours = float(request.form.get('hours', 0))
        except: hours = 0
        
        timetable = [
            {"activity": f"Core Concept Learning: {subject}", "time": f"{round(hours*0.5, 1)} Hrs"},
            {"activity": "Solving Important Q&A", "time": f"{round(hours*0.3, 1)} Hrs"},
            {"activity": "Self-Assessment & Revision", "time": f"{round(hours*0.2, 1)} Hrs"}
        ]
        
        # Filtering by exact Branch and Subject
        notes = get_csv_data('notes.csv', {'Branch': branch, 'Subject': subject})
        questions = get_csv_data('imp_qa.csv', {'Branch': branch, 'Subject': subject})

    return render_template('college/study.html', timetable=timetable, notes=notes, questions=questions)

# --- 2. QUIZ ENGINE ---
import random
CSV_FILE = os.path.join(DATASETS_DIR, 'quiz_questions.csv')   # change filename here

def load_questions(selected_branch=None):
    questions = []
    branches = set()

    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            branch = row["Branch"].strip()
            branches.add(branch)

            if selected_branch and branch != selected_branch:
                continue

            questions.append({
                "question": row["Question"],
                "options": {
                    "A": row["Option A"],
                    "B": row["Option B"],
                    "C": row["Option C"],
                    "D": row["Option D"]
                },
                "correct": row["Correct_Answer"].strip()
            })

    return questions, sorted(list(branches))


@app.route("/quiz",methods=['GET', 'POST'])
def quiz():
    selected_branch = request.args.get("branch")
    questions, branches = load_questions(selected_branch)
    return render_template(
        "college/quiz.html",
        questions=questions,
        branches=branches,
        selected_branch=selected_branch
    )

#Project Suggestions

# Helper function to read and filter project data
def get_projects(selected_branch):
    projects = []
    # Ensure the path to your CSV is correct
    csv_path = os.path.join(os.path.dirname(__file__), 'project_suggestions.csv')
    
    if not os.path.exists(csv_path):
        return []

    with open(csv_path, mode='r', encoding='utf-8') as f:
        # DictReader uses the first row of the CSV as keys for each row dictionary
        reader = csv.DictReader(f)
        # Clean headers to remove any leading/trailing spaces
        reader.fieldnames = [name.strip() for name in reader.fieldnames]
        
        for row in reader:
            # Match the branch (case-insensitive and whitespace-safe)
            if row.get('Branch', '').strip().lower() == selected_branch.strip().lower():
                projects.append(row)
    return projects
@app.route('/project', methods=['GET', 'POST'])
def project():  
    projects = []
    if request.method == 'POST':
        branch = request.form.get('branch')
        projects = get_csv_data('project_suggestions.csv', {'Branch': branch})
    return render_template('college/project.html', projects=projects)

#INTERSHIP SUGGESTIONS
INT_QS= os.path.join(DATASETS_DIR, 'internship_suggestions.csv')
def load_internship_data():
    internships = []
    

    with open(INT_QS, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            internships.append(row)


    return internships

@app.route("/internship", methods=["GET", "POST"])
def internship():
    selected_domain = None
    internships = []

    # Always load data first
    all_data = load_internship_data()

    print(all_data[0])  # safe now

    if request.method == "POST":
        selected_domain = request.form.get("domain")

        if selected_domain:
            internships = [
                i for i in all_data
                if i.get("Branch") and
                i["Branch"].strip().lower() == selected_domain.strip().lower()
            ]

    return render_template(
        "college/internship.html",
        internships=internships,
        selected_domain=selected_domain
    )
# --- 5. PLACEMENT PREDICTION ---
@app.route('/placement', methods=['GET', 'POST'])
def placement():
    prediction = None
    if request.method == 'POST':
        try:
            cgpa = float(request.form.get('cgpa', 0))
            internships = int(request.form.get('internships', 0))
            projects = int(request.form.get('projects', 0))
        except: cgpa, internships, projects = 0, 0, 0

        if cgpa >= 8.0 and internships >= 1 and projects >= 2:
            prediction = "Placed (Ready)"
        elif cgpa >= 7.0 and (internships >= 1 or projects >= 1):
            prediction = "Placement Likely (Better)"
        else:
            prediction = "Needs Improvement (Average)"
    return render_template('college/placement.html', prediction=prediction)

# --- 6. COLLEGE CHATBOT ---
@app.route("/chatbot_college", methods=["GET", "POST"])
def chatbot_college():

    response = None

    if request.method == "POST":
        user_message = request.form["message"]
        response = get_chatbot_response(user_message)

    return render_template("college/chatbot_college.html", response=response)

from flask import jsonify

@app.route("/api/chatbot_college", methods=["POST"])
def api_chatbot_college():
    data = request.get_json()
    user_message = data.get("message")

    response = get_chatbot_response(user_message)

    return jsonify({
        "response": response
    })

# ====================================
# FRESHER FEATURES
# =====================================

#Interview Preparation
@app.route("/interviewprep")
def interviewprep():

    category = request.args.get("category")
    questions = []
    categories = set()

    with open("datasets/interview_preparation.csv", newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:

            categories.add(row["Category"])

            if category and row["Category"] != category:
                continue

            questions.append({
                "category": row["Category"],
                "sub": row["Sub_Category"],
                "question": row["Question"],
                "answer": row["Suggested_Answer_Tip"],
                "difficulty": row["Difficulty_Level"]
            })

    return render_template(
        "fresher/interviewprep.html",
        questions=questions,
        categories=sorted(categories),
        selected_category=category
    )

# CAREER RECOMMENDATION
@app.route("/careerpath", methods=["GET", "POST"])
def careerpath():

    careers = []
    branches = set()
    selected_branch = None

    with open("datasets/career_suggestions.csv", newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            branches.add(row["Branch"])

            if request.method == "POST":
                selected_branch = request.form.get("branch")

                if row["Branch"] == selected_branch:
                    careers.append({
                        "career": row["Career_Suggestion"],
                        "description": row["Brief_Description"]
                    })

    return render_template(
        "fresher/careerpath.html",
        careers=careers,
        branches=sorted(branches),
        selected_branch=selected_branch
    )

# SKILL RECOMMENDATION

import pandas as pd
from flask import jsonify

df = pd.read_csv("datasets/skill_recommendations.csv")

@app.route("/get_roles/<branch>")
def get_roles(branch):

    roles = df[df["Branch"] == branch]["Job_Role"].unique().tolist()
    return jsonify({"roles": roles})

@app.route("/skillgap", methods=["GET","POST"])
def skillgap():

    branches = sorted(df["Branch"].unique())

    skills = []

    if request.method == "POST":

        branch = request.form.get("branch")
        role = request.form.get("role")

        skills = df[
      (df["Branch"] == branch) &
      (df["Job_Role"] == role)
      ]["Required_Skills"].tolist()
    return render_template(
        "fresher/skillgap.html",
        branches=branches,
        skills=skills
    )
#RESUME BUILDER
@app.route("/resumecheck")
def resume_builder():
    return render_template("fresher/resumecheck.html")

# JOB RECOMMENDATION
@app.route("/job_recommendation", methods=["GET","POST"])
def job_recommendation():

    csv_file = "datasets/jobs.csv"

    jobs = []
    branches = set()
    selected_branch = None

    with open(csv_file, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)

        data = list(reader)

        for row in data:
            branches.add(row["Branch"])

    if request.method == "POST":

        selected_branch = request.form.get("branch")

        for row in data:
            if row["Branch"] == selected_branch:
                jobs.append(row)

    return render_template(
        "fresher/job_recommendation.html",
        branches=sorted(branches),
        jobs=jobs,
        selected_branch=selected_branch
    )

#CHATBOT
@app.route("/chatbot_fresher", methods=["GET","POST"])
def chatbot_fresher():

    response = ""

    if request.method == "POST":

        question = request.form.get("question", "")   # prevents None

        if question.strip() != "":
            response = get_fresher_chatbot_response(question)
        else:
            response = "Please enter a question."

    return render_template(
        "fresher/chatbot_fresher.html",
        response=response
    )
from flask import jsonify

@app.route("/api/chatbot_fresher", methods=["POST"])
def api_chatbot_fresher():
    data = request.get_json()
    user_message = data.get("message")

    response = get_fresher_chatbot_response(user_message)

    return jsonify({
        "response": response
    })



# =====================================
# ADMIN
# =====================================

 # Defining Base Directories



@app.route("/admin/admin_login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check admin credentials
        if check_admin(email, password):
            session["admin"] = True
            session["admin_email"] = email

            flash("Admin logged in successfully!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid admin credentials!", "danger")

    return render_template("admin/admin_login.html")
    

@app.route("/admin/admin_dashboard")
def admin_dashboard():

    if not session.get("admin"):
        flash("Please login as admin first", "danger")
        return redirect(url_for("admin_login"))

    return render_template("admin/admin_dashboard.html")

# --- MANAGE USERS (Delete Only) ---
@app.route('/admin/users')
def manage_users():
    # Now USERS_CSV is recognized because it was defined above
    df = pd.read_csv(USERS_CSV)
    users_list = df.to_dict(orient='records')
    return render_template('admin/manage_users.html', users=users_list)

@app.route('/admin/delete_user/<email>')
def admin_delete_user(email):
    df = pd.read_csv(USERS_CSV)
    # Filter out the user with the matching email
    df = df[df['email'] != email]
    df.to_csv(USERS_CSV, index=False)
    flash(f"User {email} deleted successfully.")
    return redirect(url_for('manage_users'))

# --- MANAGE JOBS (Add & Update) ---
@app.route('/admin/jobs', methods=['GET', 'POST'])
def manage_jobs():
    if request.method == 'POST':
        df = pd.read_csv(JOBS_CSV)
        # Generate a simple JobID based on current row count + 1
        new_id = len(df) + 1
        
        new_job = {
            'JobID': new_id,
            'Company': request.form.get('company'),
            'Role': request.form.get('role'),
            'Location': request.form.get('location'),
            'Salary': request.form.get('salary'),
            'ExperienceRequired': request.form.get('experience')
        }
        
        df = pd.concat([df, pd.DataFrame([new_job])], ignore_index=True)
        df.to_csv(JOBS_CSV, index=False)
        flash("Job added to jobs.csv successfully!")
        return redirect(url_for('manage_jobs'))
    return render_template('admin/manage_jobs.html')

# --- MANAGE PROJECTS (Add & Update) ---
@app.route('/admin/projects', methods=['GET', 'POST'])
def manage_projects():
    if request.method == 'POST':
        new_project = {
            'Branch': request.form.get('branch'),
            'Subject': request.form.get('subject'),
            'Project_Idea': request.form.get('project_idea')
        }
        
        df = pd.read_csv(PROJECTS_CSV)
        df = pd.concat([df, pd.DataFrame([new_project])], ignore_index=True)
        df.to_csv(PROJECTS_CSV, index=False)
        flash("Project idea added to fresher_projects.csv")
        return redirect(url_for('manage_projects'))
    return render_template('admin/manage_projects.html')

# --- MANAGE CHATBOT ---
@app.route('/admin/chatbot/<type>', methods=['GET', 'POST'])
def manage_chatbot(type):
    # Select path based on the type passed from the URL
    target_path = CHATBOT_COLLEGE_CSV if type == 'college' else CHATBOT_FRESHER_CSV
    
    if request.method == 'POST':
        new_entry = {
            'question': request.form.get('question'),
            'answer': request.form.get('answer')
        }
        df = pd.read_csv(target_path)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(target_path, index=False)
        flash(f"Entry added to {os.path.basename(target_path)}")
        return redirect(url_for('manage_chatbot', type=type))
    return render_template('admin/manage_chatbot.html', type=type)

# CSV file paths
QUIZ_CSV = "datasets/quiz.csv"
INTERVIEW_CSV = "datasets/interview_qs.csv"
CAREER_CSV = "datasets/career_suggestions.csv"

# =========================
# QUIZ MANAGEMENT
# =========================
@app.route('/admin/quiz', methods=['GET', 'POST'])
def manage_quiz():

    if request.method == 'POST':

        new_question = {
            'Branch': request.form.get('branch'),
            'Subject': request.form.get('subject'),
            'Question': request.form.get('question'),
            'Option A': request.form.get('option_a'),
            'Option B': request.form.get('option_b'),
            'Option C': request.form.get('option_c'),
            'Option D': request.form.get('option_d'),
            'Correct_Answer': request.form.get('correct_answer')
        }

        df = pd.read_csv(QUIZ_CSV)

        df = pd.concat([df, pd.DataFrame([new_question])], ignore_index=True)

        df.to_csv(QUIZ_CSV, index=False)

        flash("Quiz question added successfully!")

        return redirect(url_for('manage_quiz'))

    return render_template('admin/manage_quiz.html')


# =========================
# INTERVIEW QUESTIONS
# =========================
@app.route('/admin/interview_qs', methods=['GET', 'POST'])
def manage_interview_qs():

    if request.method == 'POST':

        new_question = {
            'Category': request.form.get('category'),
            'Sub_Category': request.form.get('sub_category'),
            'Question': request.form.get('question'),
            'Suggested_Answer_Tip': request.form.get('answer_tip'),
            'Difficulty_Level': request.form.get('difficulty')
        }

        df = pd.read_csv(INTERVIEW_CSV)

        df = pd.concat([df, pd.DataFrame([new_question])], ignore_index=True)

        df.to_csv(INTERVIEW_CSV, index=False)

        flash("Interview question added successfully!")

        return redirect(url_for('manage_interview_qs'))

    return render_template('admin/manage_interview_qs.html')

# =========================
# CAREER SUGGESTIONS
# =========================
@app.route('/admin/career_qs', methods=['GET', 'POST'])
def manage_career_qs():

    if request.method == 'POST':

        new_career = {
            'Branch': request.form.get('branch'),
            'Career_Suggestion': request.form.get('career'),
            'Brief_Description': request.form.get('description')
        }

        df = pd.read_csv(CAREER_CSV)

        df = pd.concat([df, pd.DataFrame([new_career])], ignore_index=True)

        df.to_csv(CAREER_CSV, index=False)

        flash("Career suggestion added successfully!")

        return redirect(url_for('manage_career_qs'))

    return render_template('admin/manage_career_qs.html')

# =====================================
# RUN
# =====================================

if __name__ == "__main__":
    app.run(debug=True)