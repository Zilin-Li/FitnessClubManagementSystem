from db_mamager import getCursor
from flask import session, request, flash
import os
from datetime import datetime

def get_session_info():
   # get the session information, if the user is not logged in, return False, None, '', None
   # otherwise, return True, user_id, username, role_id
    is_login = session.get('logged_in', False)
    userid = session.get('user_id', None)
    username = session.get('username', '')
    roleid = session.get('role_id', None)
    return is_login, userid, username, roleid


def get_member_form_data():
    # get the form data for the member
    form_data = {
        'first_name': request.form.get('first_name', ''),
        'last_name': request.form.get('last_name', ''),
        'position': request.form.get('position', ''),
        'phone_number': request.form.get('phone_number', ''),
        'address': request.form.get('address', ''),
        'birth_date': request.form.get('birth_date', ''),
        'profile_image': request.files['profile_image'] if 'profile_image' in request.files else None,
        'health_info': request.form.get('health_info', '')
    }
    return form_data


def get_member_info(user_id=None):
    # get member info from the database, if user_id is None, return all the users, otherwise, return the user with the user_id
    query = """
        SELECT
            u.id,
            u.username,
            u.email,
            m.first_name,
            m.last_name,
            m.position,
            m.phone_number,
            m.address,
            m.birth_date,
            m.profile_image,
            u.status,
            m.health_info
        FROM users u
        LEFT JOIN members m ON u.id = m.user_id
        WHERE u.role_id = 1
    """
    if user_id is not None:
        query += " AND u.id = %s;"

    dbconn = getCursor()
    try:
        if user_id is not None:
            dbconn.execute(query, (user_id,))
        else:
            dbconn.execute(query)
        if user_id is not None:
            return dbconn.fetchone()  # if it is a single user, return a single record
        else:
            return dbconn.fetchall()  # if it is all users, return all the records
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# validate image file


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


# save image file
PROFILE_IMAGE_FOLDER = 'static/images/member'

# add member ptofile


def add_member(user_id, form_data):
    # Check if birth_date is provided and within the allowed range
    if 'birth_date' in form_data:
        birth_date = datetime.strptime(form_data['birth_date'], '%Y-%m-%d')
        eighteen_years_ago = datetime.now().replace(year=datetime.now().year - 18)

        if birth_date > eighteen_years_ago:
            flash('You must be at least 18 years old to register.', 'danger')
            return False

    # save the profile image file to the static/images/member folder
    image_path = None
    if 'profile_image' in form_data and form_data['profile_image'] is not None:
        profile_image = form_data['profile_image']
        image_path = os.path.join(PROFILE_IMAGE_FOLDER, profile_image.filename)
        print(image_path)
        try:
            profile_image.save(image_path)
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    else:
        image_path = None

    dbconn = getCursor()

    try:
        # delete existing member
        delete_query = """
            DELETE FROM members WHERE user_id = %s;
        """
        dbconn.execute(delete_query, (user_id,))
    except Exception as e:
        print(f"An error occurred while deleting existing member: {e}")
        dbconn.rollback()
        return False

    try:
        # add a new member to the database
        insert_query = """
            INSERT INTO members (user_id, first_name, last_name, position, phone_number, address, birth_date, profile_image, health_info)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        dbconn.execute(insert_query, (user_id, form_data['first_name'], form_data['last_name'], form_data['position'], form_data['phone_number'],
                                      form_data['address'], form_data['birth_date'], image_path, form_data['health_info']))

        return True
    except Exception as e:
        print(f"An error occurred while adding new member: {e}")
        dbconn.rollback()
        return False
