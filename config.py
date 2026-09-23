import os


class Config:
    # ==============================
    # BASE DIRECTORY
    # ==============================
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # ==============================
    # FLASK SETTINGS
    # ==============================
    SECRET_KEY = "uniguide_secret"
    DEBUG = True

    # ==============================
    # DATABASE PATHS
    # ==============================
    DATABASE_FOLDER = os.path.join(BASE_DIR, "database")

    USERS_CSV = os.path.join(DATABASE_FOLDER, "users.csv")
    RESULTS_CSV = os.path.join(DATABASE_FOLDER, "results.csv")
    LOGS_CSV = os.path.join(DATABASE_FOLDER, "logs.csv")
    FEEDBACK_CSV = os.path.join(DATABASE_FOLDER, "feedback.csv")

    # ==============================
    # DATASET PATHS
    # ==============================
    DATASET_FOLDER = os.path.join(BASE_DIR, "datasets")

    INTERNSHIPS_DATA = os.path.join(DATASET_FOLDER, "internships.csv")
    PROJECTS_DATA = os.path.join(DATASET_FOLDER, "projects.csv")
    JOBS_DATA = os.path.join(DATASET_FOLDER, "jobs.csv")
    CERTIFICATIONS_DATA = os.path.join(DATASET_FOLDER, "certifications.csv")
    PLACEMENT_DATA = os.path.join(DATASET_FOLDER, "placement_dataset.csv")