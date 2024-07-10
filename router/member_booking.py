from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from datetime import datetime
from werkzeug.utils import secure_filename
from db_mamager import getCursor
from utility.auth_utility import is_logged_in
from utility.member_utility import get_session_info

member_booking = Blueprint('member_booking', __name__,  static_folder='static', template_folder='templates')

# create a route to display the member booking
@member_booking.route('/', methods=['GET', 'POST'])
@is_logged_in
def view_booking():
    # Get session info
    is_login, userid, username, roleid = get_session_info()

    # Check if the user is a member
    if roleid != 1:
        return redirect(url_for('home'))

    # Get the class type and payment status from request arguments
    class_type = request.args.get('class_type', '0')
    payment_status = request.args.get('payment_status', 'all')

    # Base query
    query_base = """
        SELECT 
            b.id AS booking_id,
            b.status AS booking_status,
            b.is_attend,
            b.is_paid,
            fc.name AS class_name,
            fc.course_type_id,
            DATE(fc.schedule_time) AS class_date,
            DATE_FORMAT(fc.schedule_time, '%H:%i') AS class_time,

            loc.name AS location_name,
            tr.first_name AS trainer_first_name,
            tr.last_name AS trainer_last_name,
            CASE 
                WHEN b.is_attend = 1 THEN 'Attended'
                WHEN b.is_attend = 0 AND fc.schedule_time > NOW() THEN 'Not yet'
                WHEN b.is_attend = 0 AND fc.schedule_time <= NOW() THEN 'Missed'
            END AS attendance_status
        FROM 
            bookings b
        JOIN 
            fitness_classes fc ON b.fitness_class_id = fc.id
        JOIN 
            location loc ON fc.location_id = loc.id
        JOIN 
            trainers tr ON fc.trainer_id = tr.id
        JOIN 
            members m ON b.member_id = m.id
        WHERE 
            m.user_id = %s
    """

    # Conditions based on class type and payment status
    query_conditions = []
    filter_values = [userid]

    if class_type in ['1', '2']:
        query_conditions.append(" AND fc.course_type_id = %s ")
        filter_values.append(class_type)

    if payment_status == 'paid':
        query_conditions.append(" AND b.is_paid = 1 ")
    elif payment_status == 'unpaid':
        query_conditions.append(" AND b.is_paid = 0 ")

    # Combine all parts of the query
    query_condition = "".join(query_conditions)
    # query_suffix = "ORDER BY CASE WHEN attendance_status = 'Not yet' THEN 1 WHEN attendance_status = 'Attended' THEN 2 WHEN attendance_status = 'Missed' THEN 3 END, fc.schedule_time;"
    query_suffix = "ORDER BY CASE WHEN attendance_status = 'Not yet' THEN 1 ELSE 2 END, fc.schedule_time;"
    query = query_base + query_condition + query_suffix

    dbconn = getCursor()
    try:
        dbconn.execute(query, tuple(filter_values))
        bookings = dbconn.fetchall()
    except Exception as e:
        print(e)
        flash('Error getting booking info', 'danger')
        return redirect(url_for('home'))
   

    return render_template('/member_view_booking/member_booking.html', bookings=bookings, class_type=class_type, payment_status=payment_status)

# create a route to pay for the booking
@member_booking.route('/pay_for_class', methods=['POST'])
@is_logged_in
def pay_for_class():
    # get the session info
    is_login, userid, username, roleid = get_session_info()
    booking_id = request.form.get('booking_id')
    # check if the user is a member
    if roleid != 1:
        return redirect(url_for('home'))
    try:
        # get the member booking
        pay_booking_query = """
            UPDATE 
                bookings
            SET 
                is_paid = 1
            WHERE 
                id = %s;"""
        # get the member booking
        dbconn = getCursor()
        dbconn.execute(pay_booking_query, (booking_id,))
        flash('Payment successful', 'success')
        
        return redirect(url_for('member_booking.view_booking'))
    except Exception as e:  
        print(e)
        flash('Error paying for class', 'danger')
        return redirect(url_for('home'))




# create a route to cancel the booking
@member_booking.route('/cancel_booking/<int:booking_id>', methods=['POST'])
@is_logged_in
def cancel_booking(booking_id):
    # get the session info
    is_login, userid, username, roleid = get_session_info()
    # check if the user is a member
    if roleid != 1:
        return redirect(url_for('home'))
    
    # get the member booking
    cancel_booking_query = """
        DELETE FROM 
            bookings
        WHERE 
            id = %s;"""
    # get the member booking
    dbconn = getCursor()
    try:
        dbconn.execute(cancel_booking_query, (booking_id,))
       
        flash('Booking cancelled', 'success')
        return redirect(url_for('member_booking.view_booking'))
    except Exception as e:
        print(e)
        flash('Error cancelling booking', 'danger')
        return redirect(url_for('home'))
    