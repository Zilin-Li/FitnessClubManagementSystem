from datetime import date
from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from db_mamager import getCursor
from utility.profile_utility import get_form_data, show_profiles, edit_profile
from utility.member_utility import get_member_form_data, add_member,allowed_file
from utility.member_utility import get_session_info
from werkzeug.utils import secure_filename
import uuid
import os

# create a blueprint
member = Blueprint(
    'member',
    __name__,
    static_folder='static',
    template_folder='templates'
)

# create a route to display the member profiles
@member.route('/', methods=['GET'])
def member_profile():
    is_login = get_session_info()
    if is_login == False:
        flash('Please check your membership authorization', 'info')
        return redirect(url_for('home'))
    else:
    # get user_id and role_id from the session
        user_id = session['user_id']
        role_id = session['role_id']
        profile = show_profiles(user_id, role_id)

    return render_template('/user_profile/profile.html', profile=profile)

# create a route to edit the member profile
@member.route('/edit', methods=['GET', 'POST'])
def edit_member_profile():
    # get user_id and role_id from the session
    user_id = session['user_id']
    role_id = session['role_id']

    # check if the user is already have a profile
    if show_profiles(user_id, role_id) is None:
        flash('You are not have a profile yet, please create a profile first', 'info')
        return redirect(url_for('member.member_profile'))

    # check if the request method is POST
    elif request.method == 'POST':
        # get the form data
        form_data = get_form_data(role_id)  
        # check if all of the form data is not empty
        if form_data is not None:
            profile_image = request.files.get('profile_image', None) 
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
                new_profile_image.save(os.path.join('static/images/member', filename))
                # update the profile_image in the database
                update_image_query = "UPDATE members SET profile_image = %s WHERE user_id = %s"
                dbconn = getCursor()
                dbconn.execute(update_image_query, (filename, user_id))
            # update the member profile
            edit_profile(user_id, role_id, form_data)
            # redirect to the member profile page
            return redirect(url_for('member.member_profile'))
        else:
            # flash a message
            flash('Please fill all the form', 'danger')

    # get the member profile to display in the form
    profile = show_profiles(user_id, role_id)

    return render_template('/user_profile/edit_profile.html', profile=profile)


@member.route('/class/<int:class_id>', methods=['GET'])
def class_detail(class_id):
    # connect to the database and get the cursor
    dbconn = getCursor()
    # create query
    query = """
        select 
            fc.id, 
            fc.name, 
            fc.description, 
            concat(t.first_name, ' ', t.last_name) as trainer_name, 
            t.title as trainer_title, 
            t.phone_number,
            t.profile_image,
            t.description as trainer_description,
            fc.schedule_time, 
            l.name as location, 
            fc.price,
            fc.description,
            fc.course_type_id,
            t.user_id
        from fitness_classes fc
        join trainers t on fc.trainer_id = t.id
        join location l on fc.location_id = l.id
        where fc.id = %s;
    """
    # execute the query
    dbconn.execute(query, (class_id,))
    class_result = dbconn.fetchall()
    if len(class_result) == 0:
        flash('Class not found', 'error')
        return render_template('home.html')

    query_book_history = """
        select fb.id, fc.course_type_id, m.user_id from bookings fb
        join members m on m.id = fb.member_id 
        join fitness_classes fc on fb.fitness_class_id = fc.id
        where fb.status=1 and fb.fitness_class_id = %s;
    """
    user_id = session.get('user_id')
    # execute the query
    dbconn.execute(query_book_history, (class_id,))
    book_history_result = dbconn.fetchall()
    class_unavailable = False
    current_user_booked = False
    book_history_id = 0
    if len(book_history_result) > 0:
        if book_history_result[0][1] == 2:
            class_unavailable = True
            if book_history_result[0][2] == user_id:
                current_user_booked = True
                book_history_id = book_history_result[0][0]
        else:
            if len(book_history_result) >= 15:
                class_unavailable = True
            for booking in book_history_result:
               if booking[2] == user_id:
                    current_user_booked = True       
                    book_history_id = booking[0] 
    return render_template('book_class.html', fitness_class=class_result[0], class_unavailable=class_unavailable, current_user_booked=current_user_booked, book_history_id=book_history_id)


@member.route('/class/book', methods=['POST'])
def book_class():
    user_id = session.get('user_id')
    class_id = request.form.get('class_id')
    try:
        # connect to the database and get the cursor
        dbconn = getCursor()
        # create query
        query_member = """
            select 
                u.id,
                m.id 
            from users u
            join members m on m.user_id = u.id
                where u.id = %s;
        """
        # execute the query
        dbconn.execute(query_member, (user_id,))
        member_result = dbconn.fetchall()
        if len(member_result) == 0:
            return {'code': 401, 'msg': 'Member not found'}

        member_id = member_result[0][1]

        query_book_history = """
            select id from bookings where status = 1 and member_id = %s and fitness_class_id = %s;
        """
        # execute the query
        dbconn.execute(query_book_history, (member_id, class_id,))
        book_history_result = dbconn.fetchall()
        if len(book_history_result) > 0:
            return {'code': 502, 'msg': 'You have already booked this class'}

        # create query
        insert_booking = """
            INSERT INTO bookings (member_id, fitness_class_id, booking_date, status, is_attend, is_paid) VALUES (%s, %s, %s, '1', 0, 1);
        """
        # execute the query
        class_result = dbconn.execute(
            insert_booking, (member_id, class_id, date.today(),))
        return {'code': 200, 'msg': 'You have booked the class successfully'}
    except Exception as e:
        # log error
        print(e)
        return {'code': 500, 'msg': 'Booking failed'}


@member.route('/class/cancel', methods=['POST'])
def cancel_class():
    try:
        book_id = request.form.get('book_id')
        # connect to the database and get the cursor
        dbconn = getCursor()
        query_book_history = """
            select fb.id from bookings fb where fb.status=1 and fb.id = %s;
        """
        # execute the query
        dbconn.execute(query_book_history, (book_id,))
        book_history_result = dbconn.fetchall()
        if len(book_history_result) == 0:
            return {'code': 502, 'msg': 'No booking found, Or you have already cancelled this booking'}

        # create query
        query_cancel_class = """ Update bookings set status=0, is_paid=0 where id=%s """
        # execute the query
        dbconn.execute(query_cancel_class, (book_id,))
        return {'code': 200, 'msg': 'Your booking has been cancelled'}
    except Exception as e:
        # log error
        print(e)
        return {'code': 500, 'msg': 'Cancel booking failed'}
