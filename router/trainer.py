from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from utility.profile_utility import get_form_data, show_profiles, edit_profile
from utility.member_utility import allowed_file
from db_mamager import getCursor
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import uuid
import os

# SCRUM-24 trainer view classes by Xing
trainer = Blueprint(
    'trainer',
    __name__,
    static_folder='static',
    template_folder='templates'
)

# create a route to display the trainer profiles
@trainer.route('/', methods=['GET'])
def trainer_profile():
    # get user_id and role_id from the session
    user_id = session['user_id']
    role_id = session['role_id']

    # get the trainer profile
    profile = show_profiles(user_id, role_id)

    return render_template('/user_profile/profile.html', profile=profile)


# create a route to edit the trainer profile
@trainer.route('/edit', methods=['GET', 'POST'])
def edit_trainer_profile():
    # get user_id and role_id from the session
    user_id = session['user_id']
    role_id = session['role_id']

    # check if the user is already have a profile
    if show_profiles(user_id, role_id) is None:
        flash('You are not have a profile yet, please create a profile first', 'info')
        return redirect(url_for('trainer.trainer_profile'))

    # check if the request method is POST
    elif request.method == 'POST':
        # get the form data
        form_data = get_form_data(role_id)
        # check if all of the form data is not empty
        if form_data is not None:
            profile_image = request.files.get('profile_image', None) 
            print(profile_image)
            if profile_image and not allowed_file(profile_image.filename):
                flash('Invalid file type', 'error')
                return redirect(url_for('member.edit_member_profile'))
            # update the profile image
            if profile_image:            
                # get the image data from the form 
                new_profile_image = profile_image
                # generate a random filename by uuid
                random_filename = str(uuid.uuid4())
                # get the file extension
                _, ext = os.path.splitext(new_profile_image.filename)
                # create a new filename 
                filename = random_filename + ext
                # save the image to the static/images/member folder
                new_profile_image.save(os.path.join('static/images/trainer', filename))
                # update the profile_image in the database
                update_image_query = "UPDATE trainers SET profile_image = %s WHERE user_id = %s"
                dbconn = getCursor()
                dbconn.execute(update_image_query, (filename, user_id))
            # update the trainer profile
            edit_profile(user_id, role_id, form_data)
            # redirect to the trainer profile page
            return redirect(url_for('trainer.trainer_profile'))
        else:
            # flash a message
            flash('Please fill all the form', 'danger')

    # get the trainer profile to display in the form
    profile = show_profiles(user_id, role_id)

    return render_template('/user_profile/edit_profile.html', profile=profile)

# Fetch trainer ID based on user ID
def fetch_trainer_id(user_id):
    try:
        dbconn = getCursor()
        dbconn.execute("SELECT id FROM trainers WHERE user_id = %s", (user_id,))
        result = dbconn.fetchone()
        if result:
            trainer_id = result[0]  # Accessing the first element of the tuple
            return trainer_id
        else:
            return None
    except Exception as e:
        print(f"Error fetching trainer ID: {e}")
        return None

# Fetch locations based on trainer ID
def fetch_locations(trainer_id):
    try:
        dbconn = getCursor()
        dbconn.execute("""
            SELECT DISTINCT l.name
            FROM location l
            INNER JOIN fitness_classes fc ON l.id = fc.location_id
            WHERE fc.trainer_id = %s AND fc.course_type_id = 1
        """, (trainer_id,))
        location_rows = dbconn.fetchall()
        locations = [row[0] for row in location_rows]
        return locations
    except Exception as e:
        print(f"Error fetching locations: {e}")
        return []

# Fetch schedule times based on trainer ID
def fetch_schedule_times(trainer_id):
    try:
        dbconn = getCursor()
        dbconn.execute("""
            SELECT DISTINCT fc.schedule_time
            FROM fitness_classes fc
            WHERE fc.trainer_id = %s AND fc.course_type_id = 1
        """, (trainer_id,))
        schedule_time_rows = dbconn.fetchall()
        schedule_times = [row[0].strftime('%Y-%m-%d %H:%M:%S') for row in schedule_time_rows]
        return schedule_times
    except Exception as e:
        print(f"Error fetching schedule times: {e}")
        return []

    # Fetch exercise class timetable data for the logged-in trainer
def fetch_exercise_class_timetable(trainer_id):
    try:
        # connect to the database and get the cursor
        dbconn = getCursor()
        # execute the query with a join to get location name
        dbconn.execute("""
            SELECT fc.*, l.name AS location_name, CONCAT(t.first_name, ' ', t.last_name) AS trainer_name
            FROM fitness_classes fc
            INNER JOIN location l ON fc.location_id = l.id
            INNER JOIN trainers t ON fc.trainer_id = t.id
            WHERE fc.trainer_id = %s""", (trainer_id,))
        exercise_classes = dbconn.fetchall()
        # Convert each result tuple to a dictionary
        exercise_classes_dicts = []
        for cls in exercise_classes:
            cls_dict = {
                'id': cls[0],
                'name': cls[1],
                'description': cls[2],
                'course_type_id': cls[3],
                'trainer_id': cls[4],
                'schedule_time': cls[5].strftime('%Y-%m-%d %H:%M:%S'),
                'location_id': cls[6],
                'price': cls[7],
                'location_name': cls[9]
            }
            exercise_classes_dicts.append(cls_dict)

        return exercise_classes_dicts
    except Exception as e:
        print(f"Error fetching exercise class timetable: {e}")
        return []

# Filter exercise class timetable data by location name and schedule time
def filter_exercise_class_timetable(exercise_classes, location_name, schedule_time):
    filtered_classes = exercise_classes

    if location_name:
        filtered_classes = [cls for cls in filtered_classes if cls['location_name'] == location_name]

    if schedule_time:
        # Convert schedule times to datetime objects for comparison
        schedule_time_datetime = datetime.strptime(schedule_time, '%Y-%m-%d %H:%M:%S')
        time_range = timedelta(minutes=60)
        filtered_classes = [cls for cls in filtered_classes if 
                            schedule_time_datetime - time_range <= datetime.strptime(cls['schedule_time'], '%Y-%m-%d %H:%M:%S') <= schedule_time_datetime + time_range]

    return filtered_classes


# Create a route to view exercise class timetable
@trainer.route('/exercise_class_timetable', methods=['GET', 'POST'])
def view_exercise_class_timetable():
    user_id = session['user_id']
    if user_id is None:
        # Handle case when user is not logged in
        return render_template('register_login.html')  
    # Fetch trainer ID
    trainer_id = fetch_trainer_id(user_id)

    # Fetch exercise class timetable
    exercise_classes = fetch_exercise_class_timetable(trainer_id)

    # Fetch locations and schedule times
    locations = fetch_locations(trainer_id)
    schedule_times = fetch_schedule_times(trainer_id)
    
    # Initialize filter options
    filter_options = {
        'location_name': None,
        'schedule_time': None
    }

    if request.method == 'POST':
        # Get filter options from form data
        location_name = request.form.get('location_name', None)
        schedule_time = request.form.get('schedule_time', None)

        # Implement filter options
        filter_options['location_name'] = location_name
        filter_options['schedule_time'] = schedule_time

        # Apply filters
        filtered_classes = exercise_classes
        if location_name or schedule_time:
            filtered_classes = filter_exercise_class_timetable(exercise_classes, location_name, schedule_time)
    else:
        filtered_classes = exercise_classes

    return render_template('/trainer_view_class/trainer_class_timetable_view.html', filtered_classes=filtered_classes, filter_options=filter_options, locations=locations, schedule_times=schedule_times)

