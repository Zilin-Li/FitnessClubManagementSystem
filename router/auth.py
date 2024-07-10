from datetime import datetime, timedelta,date, time
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from db_mamager import getCursor
from utility.auth_utility import is_logged_in,prevent_logged_access, check_username, check_password
from utility.member_utility import get_session_info
import re

# create a blueprint
auth = Blueprint(
    'auth',
    __name__,
    static_folder='static',
    template_folder='templates'
)


# create a route to display login page
@auth.route('/login', methods=['GET', 'POST'])
@prevent_logged_access
def login():
    # check if the request method is POST
    if request.method == 'POST':
        if 'username' not in request.form or 'password' not in request.form:
            # flash a message to the user
            flash('Please fill in all the fields', 'error')
            return redirect(url_for('auth.login'))
        else:# get the form data
            username = request.form['username']
            password = request.form['password']
            # check if the username exists
            user_info = check_username(username)
            if not user_info:
                # flash a message to the user
                flash('Invalid username', 'error')
                return redirect(url_for('auth.login'))
            else:
                # check if the password is correct
                if not check_password_hash(user_info[2], password):
                    # flash a message to the user
                    flash('Invalid password', 'error')
                    return redirect(url_for('auth.login'))
                else:
                    # user_info[4] = role_id, user_info[5] = status
                    # if user is a manager or trainer, login; if user is a member, check subscription status
                    if user_info[4] == 1:
                        # Check if the user has a subscription, if not redirect to the subscribe page
                        if user_info[5] == 1:
                            # Check user subscription status, if expired redirect to the subscribe page
                            dbconn = getCursor()
                            dbconn.execute(
                            "SELECT * FROM specific_subscriptions WHERE user_id = %s AND end_date > %s", (user_info[0], datetime.now()))
                            subscription = dbconn.fetchone()
                            if not subscription:
                                # create a session for the user
                                session['user_id'] = user_info[0]
                                # flash a message to the user
                                flash('Your subscription is valid. Please subscribe to a plan to activate your account', 'error')
                                # change user status to inactive
                                try:
                                    dbconn.execute( "UPDATE users SET status = 0 WHERE id = %s", (user_info[0],))
                                    flash('Your account is now inactive', 'error')
                                except Exception as e:
                                    print('An error occurred: ' + str(e))
                                    flash('An error occurred. Please try again later.', 'danger')

                                # redirect the user to the subscribe page
                                return redirect(url_for('auth.subscribe'))
                        else:
                            # create a session for the user
                            session['user_id'] = user_info[0]
                            # flash a message to the user
                            flash('Please subscribe to a plan to activate your account', 'error')
                            # redirect the user to the subscribe page
                            return redirect(url_for('auth.subscribe'))

                    session['logged_in'] = True
                    session['user_id'] = user_info[0]
                    session['username'] = user_info[1]
                    session['role_id'] = user_info[4]
                    # flash a message to the user
                    flash('You are now logged in', 'success')
                    # redirect the user to the home page
                    return redirect(url_for('home'))
    else:
        # render the login page
        return render_template('/auth/login.html')

# create a route to display register page
@auth.route('/register', methods=['GET', 'POST'])
@prevent_logged_access
def register():
    # check if the request method is POST and the form is filled
    if request.method == 'POST':
        if 'username' not in request.form or 'password' not in request.form or 'confirm_password' not in request.form or 'email' not in request.form:
            # flash a message to the user
            flash('Please fill in all the fields', 'error')
            return redirect(url_for('auth.register'))
        else:
            # get the form data
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            email = request.form['email']
            # check if the username is already taken
            if check_username(username):
                flash('Username is already taken', 'error')
                return redirect(url_for('auth.register'))
            else:
                # check if the password and confirm password are the same
                if password != confirm_password:
                    flash('Password does not match', 'error')
                    return redirect(url_for('auth.register'))
                else:
                    # check if the password is secure
                    if not check_password(password):
                        return redirect(url_for('auth.register'))
                        #check if the email is available
                    else:
                        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                            flash('Invalid email address', 'error')
                            return redirect(url_for('auth.register'))
                        else:
                            # hash the password
                            hashed_password = generate_password_hash(
                                password, method='pbkdf2:sha256', salt_length=8)
                            # Insert the user into the database
                            try:
                                user_status=0
                                # connect to the database and get the cursor
                                dbconn = getCursor()
                                # execute the query
                                dbconn.execute(
                                    "INSERT INTO users (username, password_hash, email, role_id,status) VALUES (%s, %s, %s, %s,%s)", (username, hashed_password, email, 1,user_status))

                                # Get the user_id that was just created
                                user_id = dbconn.lastrowid
                                # flash a message to the user
                                flash(
                                    'You are now registered, please subscribe to a plan to activate your account', 'success')
                                # create a session for the user
                                session['user_id'] = user_id
                                session['role_id'] = 1
                                # redirect the user to the suscription page
                                return redirect(url_for('auth.subscribe'))

                            except Exception as e:
                                print('An error occurred: ' + str(e))
                                # flash a message to the user
                                flash('An error occurred. Please try again later.', 'danger')
                                return redirect(url_for('auth.register'))
    return render_template('/auth/register.html')


# create a route to subscribe to a member plan
@auth.route('/subscribe', methods=['GET', 'POST'])
def subscribe():   
    user_id = session.get('user_id')
    role_id = session.get('role_id')
    # Check the method of the request
    if request.method == 'POST' and  'plan_id' in request.form :
        if user_id is None:
            flash('Please register before subscribing.', 'danger')
            return redirect(url_for('auth.register'))
        elif role_id == 2:
            flash('You are a trainer, you don''t need to subscribe', 'danger')
            return redirect(url_for('home'))
        elif role_id == 3:
            flash('You are a manager, you don''t need to subscribe', 'danger')
            return redirect(url_for('home'))
        else:
            # Get the form data
            subscription_plan_id = request.form['plan_id']
            #start_date is the current date
            start_date = datetime.now()  

            dbconn = getCursor()
            #Check if the user was an old member
            try:
                old_member = None
                dbconn.execute( "SELECT * FROM members WHERE user_id = %s;", (user_id,))
                old_member = dbconn.fetchone()
            except Exception as e:
                print('An error occurred: ' + str(e))
                return redirect(url_for('auth.subscribe'))
            # if the user is an old member, check if the user has a valid subscription
            subscription_status = None 
            if old_member:
                try:                   
                    dbconn.execute(
                        "SELECT * FROM specific_subscriptions WHERE user_id = %s AND end_date > %s", (user_id, datetime.now()))
                    subscription_status = dbconn.fetchall()
                except Exception as e:
                    print('An error occurred: ' + str(e))
                    return redirect(url_for('auth.subscribe'))
                # if the user has a valid subscription, get the end date.
                if subscription_status:
                    dbconn.execute("select end_date from specific_subscriptions where user_id = %s ORDER BY end_date DESC", (user_id,))
                    result = dbconn.fetchall()
                    print('result: ', result)
                    if result:
                        start_date = result[0][0]
                        print('start_date: ', start_date)
                        if isinstance(start_date, str):
                            start_date = datetime.strptime(start_date, '%Y-%m-%d')          
            try:
                # Calculate the end date
                if subscription_plan_id == '1':
                    end_date = start_date + timedelta(days=30)
                elif subscription_plan_id == '2':
                    end_date = start_date + timedelta(days=90)
                elif subscription_plan_id == '3':
                    end_date = start_date + timedelta(days=180)
                elif subscription_plan_id == '4':
                    end_date = start_date + timedelta(days=365)    
                print('end_date: ', end_date)          
                dbconn.execute(
                    "INSERT INTO specific_subscriptions (user_id, subscription_plan_id, start_date, end_date) VALUES (%s, %s, %s, %s)", (user_id, subscription_plan_id, start_date, end_date)) 

                print('end_date: ', end_date)                
                # activate user status as active
                dbconn.execute(
                    "UPDATE users SET status = 1 WHERE id = %s", (user_id,))
                # if user is an old member and has a valid subscription,when the user subscribes to a new plan,redirect to the home page
                if subscription_status:
                    flash('You have successfully renewed your subscription', 'success')
                    return redirect(url_for('home'))
                
                # flash a message to the user    
                flash('You have successfully subscribed to a plan, please login to continue', 'success')       
                # if the user is a new member, add the user to the members table
                if old_member is None:
                    first_name =''
                    last_name = ''
                    position = ''
                    phone_number = ''
                    address = ''
                    birth_date = None
                    health_info = ''
                    profile_image = None
                    try:
                        dbconn.execute(
                            "INSERT INTO members (user_id, first_name, last_name, position,phone_number,address,birth_date,health_info,profile_image) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s)", (user_id, first_name, last_name, position,phone_number,address,birth_date,health_info,profile_image))
                         
                    except Exception as e:
                        flash('Can not add a new member', 'danger')
                        print('An error occurred: ' + str(e))
                        return redirect(url_for('auth.subscribe'))          
                # redirect the user to the home page
                return redirect(url_for('auth.login'))
            except Exception as e:
                print('An error occurred: ' + str(e))
                # flash a message to the user
                flash('An error occurred. Please try again later.', 'danger')
                # clean session           
    return render_template('/auth/subscribe.html')





# create a route to logout the user
@auth.route('/logout')
def logout():
    is_login, userid, username, roleid = get_session_info()
    if is_login:
    # clear the session
        session.pop('logged_in', False)
        session.pop('user_id', None)
        session.pop('username', None)
        session.pop('role_id', None)
    # flash a message to the user
        flash('You have been logged out', 'success')
        # redirect the user to the login page
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    

@auth.route('/change_password', methods=['GET', 'POST'])
# @is_logged_in
def change_password():
    is_login, user_id, username, role_id = get_session_info()
    # check if the request method is POST
    if not is_login:
        flash('You need to login to change password', 'danger')
        return redirect(url_for('auth.login'))
    if request.method == 'POST' and is_login:
        if 'old_password' not in request.form or 'new_password' not in request.form or 'confirm_password' not in request.form:
            # flash a message to the user
            flash('Please fill in all the fields', 'error')
            return redirect(url_for('auth.change_password'))
        else:
            # get the form data
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            # check if the new password and confirm password are the same
            if new_password != confirm_password:
                flash('Password does not match', 'error')
                return redirect(url_for('auth.change_password'))
            else:
                # check if the old password is correct
                dbconn = getCursor()
                dbconn.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                user_info = dbconn.fetchone()
                if not check_password_hash(user_info[2], old_password):
                    flash('Invalid password', 'error')
                    return redirect(url_for('auth.change_password'))
                else:
                    if not check_password(new_password):
                        return redirect(url_for('auth.change_password'))
                    else:
                        # hash the new password
                        hashed_password = generate_password_hash(
                            new_password, method='pbkdf2:sha256', salt_length=8)
                        # update the password in the database
                        try:
                            dbconn.execute(
                                "UPDATE users SET password_hash = %s WHERE id = %s", (hashed_password, user_id))
                            # flash a message to the user
                            flash('Password changed successfully', 'success')
                            # clean session
                            session.pop('logged_in', False)
                            session.pop('user_id', None)
                            session.pop('username', None)
                            session.pop('role_id', None)
                            # redirect the user to the login page

                            return redirect(url_for('auth.login'))
                        except Exception as e:
                            print('An error occurred: ' + str(e))
                            # flash a message to the user
                            flash('An error occurred. Please try again later.', 'danger')
                            return redirect(url_for('auth.change_password'))
    return render_template('/auth/change_password.html')