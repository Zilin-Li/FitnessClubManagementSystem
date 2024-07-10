from flask import session, redirect, url_for, flash
from functools import wraps
from db_mamager import getCursor


# create a decorator to check if the user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # check if the user is logged in
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('auth.login'))
    return wrap


# create a decorator to prevent logged in user from accessing the page
def prevent_logged_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            flash('You are already logged in', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function


# check if the username is already taken
def check_username(username):
    # connect to the database and get the cursor
    dbconn = getCursor()
    # query the database
    try:
        dbconn.execute(
            "SELECT * FROM users Where username = %s", (username,))
        # fetch the result
        result = dbconn.fetchone()

        return result
    except Exception as e:
        print('An error occurred: ' + str(e))
        return False


# check if the password is secure
def check_password(password):
    # check if the password is at least 8 characters long
    if len(password) < 8:
        flash('Password must be at least 8 characters long', 'danger')
    # check if password does not contain any numbers
    elif not any(char.isdigit() for char in password):
        flash('Password must contain at least one number', 'danger')
    # check if password does not contain any uppercase characters
    elif not any(char.isupper() for char in password):
        flash('Password must contain at least one uppercase character', 'danger')
    # check if password does not contain any lowercase characters
    elif not any(char.islower() for char in password):
        flash('Password must contain at least one lowercase character', 'danger')
    # check if password does not contain any special characters
    elif not any(char in '!@#$%^&*()-_=+[]{}|;:,.<>?`~' for char in password):
        flash('Password must contain at least one special character', 'danger')
        return False
    else:
        return True

