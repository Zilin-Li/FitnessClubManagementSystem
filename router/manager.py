from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from utility.profile_utility import get_form_data, show_profiles, edit_profile
from utility.manager_utility import get_location
from db_mamager import getCursor


# create a blueprint
manager = Blueprint(
    'manager',
    __name__,
    static_folder='static',
    template_folder='templates'
)

# create a route to display the member profiles
@manager.route('/', methods=['GET'])
def manager_profile():
    # get user_id and role_id from the session
    user_id = session['user_id']
    role_id = session['role_id']

    # get the member profile
    profile = show_profiles(user_id, role_id)

    return render_template('/user_profile/profile.html', profile=profile)


# create a route to edit the member profile
@manager.route('/edit', methods=['GET', 'POST'])
def edit_manager_profile():
    # get user_id and role_id from the session
    user_id = session['user_id']
    role_id = session['role_id']

    # check if the user is already have a profile
    if show_profiles(user_id, role_id) is None:
        flash('You are not have a profile yet, please create a profile first', 'info')
        return redirect(url_for('manager.manager_profile'))

    # check if the request method is POST
    elif request.method == 'POST':
        # get the form data
        form_data = get_form_data(role_id)

        # check if all of the form data is not empty
        if form_data is not None:
            # update the member profile
            edit_profile(user_id, role_id, form_data)
            # redirect to the member profile page
            return redirect(url_for('manager.manager_profile'))
        else:
            # flash a message
            flash('Please fill all the form', 'danger')

    # get the member profile to display in the form
    profile = show_profiles(user_id, role_id)

    return render_template('/user_profile/edit_profile.html', profile=profile)


# create a route to manage the location for fitness class
@manager.route('/list_location', methods=['GET', 'POST'])
def manage_location():
    # check if there is a location
    if get_location() is None:
        flash('There is no location yet, please add a location first', 'info')
        return redirect(url_for('manager.add_location'))

    else:
        locations = get_location()

    return render_template('/manager_view_location/list_location.html', locations=locations)


# create a route to show class list in this location
@manager.route('/show_class_list/<int:location_id>', methods=['GET', 'POST'])
def show_class_list(location_id):
    dbconn = getCursor()
    try:
        dbconn.execute("""
            SELECT
                fc.id,
                fc.name,
                fc.description,
                fc.course_type_id,
                fc.trainer_id,
                fc.schedule_time,
                fc.location_id,
                fc.price,
                fc.capacity       
            FROM fitness_classes fc
            WHERE fc.location_id = %s
        """, (location_id,))
        class_list = dbconn.fetchall()
    except Exception as e:
        print(f"An error occurred: {e}")
        class_list = None

    return render_template('/manager_view_location/show_class_list_by_location.html', class_list=class_list)


# create a route to add a location
@manager.route('/add_location', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        name = request.form['location_name']
        print(name)
        description = request.form['location_description']
        print(description)

        if name is not None and description is not None:
            try:
                cursor = getCursor()
                cursor.execute("""
                    INSERT INTO location (name, description)
                    VALUES (%s, %s)
                """, (name, description))
                flash('Location added successfully', 'success')
                return redirect(url_for('manager.manage_location'))

            except Exception as e:
                print(f"An error occurred: {e}")
                flash('An error occurred, please try again', 'danger')
        else:
            flash('Please fill all the form', 'danger')

    return render_template('/manager_view_location/add_location.html')


# create a route to delate a location
@manager.route('/delete_location/<int:location_id>', methods=['GET'])
def delete_location(location_id):
    try:
        cursor = getCursor()
        select_course_query = "SELECT * FROM fitness_classes WHERE location_id = %s"
        cursor.execute(select_course_query , (location_id,))
        course=cursor.fetchone()
        if course is not None:
            flash('This location can not be deleted as there are courses arranged on it', 'danger')
        else:
            try:
                cursor.execute("""DELETE FROM location WHERE id = %s""", (location_id,))
                flash('Delete location successfully', 'success')
            except Exception as e:
                print('An error occurred: ' + str(e))
                flash('An error occurred. Please try again later.', 'danger')
    except Exception as e:
                print('An error occurred: ' + str(e))
                flash('An error occurred. Please try again later.', 'danger')   
    return redirect(url_for('manager.manage_location'))


# create a route to edit a location
@manager.route('/edit_location/<int:location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    if request.method == 'POST':
        name = request.form['location_name']
        description = request.form['location_description']

        if name is not None and description is not None:
            try:
                cursor = getCursor()
                cursor.execute("""
                    UPDATE location
                    SET name = %s, description = %s
                    WHERE id = %s
                """, (name, description, location_id))
                flash('Location updated successfully', 'success')
                return redirect(url_for('manager.manage_location'))

            except Exception as e:
                print(f"An error occurred: {e}")
                flash('An error occurred, please try again', 'danger')
        else:
            flash('Please fill all the form', 'danger')

    # show location in input box
    locations = location_list(location_id)

    return render_template('/manager_view_location/edit_location.html', locations=locations)


def location_list(location_id):
    # get location info from the database
    query = """
        SELECT
            id,
            name,
            description
        FROM location
        WHERE id = %s
    """
    dbconn = getCursor()
    try:
        dbconn.execute(query, (location_id,))
        return dbconn.fetchall()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

