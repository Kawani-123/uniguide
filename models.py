import csv
import os
from datetime import datetime
from config import Config

# ==============================
# DATABASE FILE PATH
# ==============================
USERS_FILE = os.path.join("database", "users.csv")

# Ensure database folder exists
os.makedirs("database", exist_ok=True)


# ==============================
# READ ALL USERS
# ==============================
def get_all_users():
    if not os.path.exists(USERS_FILE):
        return []

    with open(USERS_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


# ==============================
# CHECK USER LOGIN
# ==============================
def check_user(email, password):

    if not os.path.exists(USERS_FILE):
        return None

    with open(USERS_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if (
                row["email"].strip() == email.strip()
                and row["password"].strip() == password.strip()
            ):
                return row

    return None


# ==============================
# ADD USER (REGISTER)
# ==============================
def add_user(name, email, password, mode):

    file_exists = os.path.isfile(USERS_FILE)

    with open(USERS_FILE, mode="a", newline="", encoding="utf-8") as file:
        fieldnames = ["name", "email", "password", "mode", "created_at"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "name": name,
            "email": email,
            "password": password,
            "mode": mode,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return True, "User registered successfully"


# ==============================
# DELETE USER (ADMIN)
# ==============================
def delete_user(email):

    users = get_all_users()
    users = [user for user in users if user["email"] != email]

    with open(USERS_FILE, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["name", "email", "password", "mode", "created_at"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)

    return True


# ==============================
# UPDATE USER (ADMIN)
# ==============================
def update_user(email, new_name=None, new_mode=None):

    users = get_all_users()

    for user in users:
        if user["email"] == email:
            if new_name:
                user["name"] = new_name
            if new_mode:
                user["mode"] = new_mode

    with open(USERS_FILE, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["name", "email", "password", "mode", "created_at"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)

    return True


# ==============================
# ADMIN CHECK
# ==============================
def check_admin(email, password):

    # Simple hardcoded admin
    if email == "admin@uniguide.com" and password == "admin123":
        return True

    return False