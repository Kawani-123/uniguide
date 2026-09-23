from database.models import add_user, check_user, check_admin


# ==============================
# USER REGISTER
# ==============================
def user_register(name, email, password, mode):
    return add_user(name, email, password, mode)


# ==============================
# USER LOGIN
# ==============================
def user_login(email, password):
    return check_user(email, password)


# ==============================
# ADMIN LOGIN
# ==============================
def admin_login_user(email, password):
    return check_admin(email, password)