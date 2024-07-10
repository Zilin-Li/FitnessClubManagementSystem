# Crafted with passion and determination by NING LI(https://ningli.me)
from flask import request, redirect, url_for, flash
from db_mamager import getCursor
from datetime import datetime
import re

# get form data for different roles
def get_form_data(role_id):
    if role_id == 1:
        profile_image = request.files.get('profile_image', None) 
        form_data = {
            'first_name': request.form.get('first_name', ''),
            'last_name': request.form.get('last_name', ''),
            'position': request.form.get('position', ''),
            'phone_number': request.form.get('phone_number', ''),
            'address': request.form.get('address', ''),
            'birth_date': request.form.get('birth_date', None),
            'health_info': request.form.get('health_info', ''),
            'user_email': request.form.get('user_email', '')
        }
         
        return form_data

    elif role_id == 2:
        form_data = {
            'first_name': request.form.get('first_name', ''),
            'last_name': request.form.get('last_name', ''),
            'title': request.form.get('title', ''),
            'phone_number': request.form.get('phone_number', ''),
            'description': request.form.get('description', ''),
            'user_email': request.form.get('user_email', '')
        }

        return form_data

    elif role_id == 3:
        form_data = {
            'first_name': request.form.get('first_name', ''),
            'last_name': request.form.get('last_name', ''),
            'title': request.form.get('title', ''),
            'phone_number': request.form.get('phone_number', ''),
            'user_email': request.form.get('user_email', '')
        }

        return form_data


# show profiles for different roles by user_id and role_id
def show_profiles(user_id, role_id):
    # get user_email from the database
    dbconn = getCursor()
    get_email_query = "SELECT email FROM users WHERE id = %s"
    try:
        dbconn.execute(get_email_query, (user_id,))
        user_email = dbconn.fetchone()[0]
    except Exception as e:
        print(e)
        flash('Error: ' + str(e))
    # if the role_id is 1, then it is a member
    if role_id == 1:
        try:
            dbconn.execute(
                "SELECT * FROM members Where user_id = %s", (user_id,))
        except Exception as e:
            print(e)
            flash('Error: ' + str(e))
        # fetch all the results
        results = dbconn.fetchall()
        # insert the user_email into the results
        results[0] = results[0] + (user_email,)
       
        # return the results
        return results

    # if the role_id is 2, then it is a trainer
    elif role_id == 2:
        try:
            dbconn.execute(
                "SELECT * FROM trainers Where user_id = %s", (user_id, ))
        except Exception as e:
            print(e)
            flash('Error: ' + str(e))
        # fetch all the results
        results = dbconn.fetchall()
        # insert the user_email into the results
        results[0] = results[0] + (user_email,)
        # return the results
        return results

    # if the role_id is 3, then it is a manager
    elif role_id == 3:
        try:
            dbconn.execute(
                "SELECT * FROM managers Where user_id = %s", (user_id, ))
        except Exception as e:
            print(e)
            flash('Error: ' + str(e))
        # fetch all the results
        results = dbconn.fetchall()
        # insert the user_email into the results
        results[0] = results[0] + (user_email,)
        # return the results
        return results

    # if the role_id is not 1, 2, or 3, then it is an invalid role_id
    else:
        # print the error message
        flash('You are forbidden to access this page', 'danger')
        # return None and redirect to the home page
        return None, redirect(url_for('home'))


# update profiles for different roles by user_id and role_id
def edit_profile(user_id, role_id, form_data):

    # Check if birth_date is provided and within the allowed range
    if 'birth_date' in form_data:
        if form_data['birth_date'] == '':
           birth_date = None 
        else:
            birth_date = datetime.strptime(form_data['birth_date'], '%Y-%m-%d')
            eighteen_years_ago = datetime.now().replace(year=datetime.now().year - 18)

            if birth_date > eighteen_years_ago:
                flash('You must be at least 18 years old to register.', 'danger')
                return False

    if 'user_email' in form_data:
        if not re.match(r'[^@]+@[^@]+\.[^@]+', form_data['user_email']):
            flash('Invalid email address!','error')
            return False
        
    # define the specific columns to update based on role_id
    if role_id == 1:
        specific_columns = 'first_name = %s, last_name = %s, position = %s, address = %s, birth_date = %s, phone_number = %s, health_info = %s'
        specific_table = 'members'
    elif role_id == 2:
        specific_columns = 'first_name = %s, last_name = %s, title = %s, description = %s, phone_number = %s'
        specific_table = 'trainers'
    elif role_id == 3:
        specific_columns = 'first_name = %s, last_name = %s, title = %s, phone_number = %s'
        specific_table = 'managers'
    else:
        # invalid role
        flash('Illegal behavior to edit profile', 'danger')
        return False

    # connect to the database and get the cursor
    dbconn = getCursor()
    try:
        # update the specific profile based on role_id
        if role_id == 1:     
            dbconn.execute(f'''
                UPDATE {specific_table}
                SET {specific_columns}
                WHERE user_id = %s
            ''', (form_data['first_name'], form_data['last_name'], form_data.get('position'), form_data.get('address'), birth_date, form_data.get('phone_number'), form_data.get('health_info'), user_id))
        elif role_id == 2:
            # dbconn.execute("UPDATE users SET email = %s WHERE id = %s", (form_data.get('user_email'), user_id))
            dbconn.execute(f'''
                UPDATE {specific_table}
                SET {specific_columns}
                WHERE user_id = %s
            ''', (form_data['first_name'], form_data['last_name'], form_data.get('title'), form_data.get('description'), form_data.get('phone_number'),  user_id))
        elif role_id == 3:
            dbconn.execute(f'''
                UPDATE {specific_table}
                SET {specific_columns}
                WHERE user_id = %s
            ''', (form_data['first_name'], form_data['last_name'], form_data.get('title'), form_data.get('phone_number'), user_id))
        dbconn.execute("UPDATE users SET email = %s WHERE id = %s", (form_data.get('user_email'), user_id))
        # return success message
        flash('Profile updated successfully', 'success')
        return True
    except Exception as e:
        # print the error message
        print('An error occurred while updating the profile:', e)
        flash('Failed to update profile', 'danger')
        return False
