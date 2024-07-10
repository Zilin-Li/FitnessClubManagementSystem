from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from db_mamager import getCursor
from utility.auth_utility import is_logged_in,check_password
from utility.manager_utility import manager_get_course, manager_get_member_info
from utility.member_utility import get_session_info
import re
import os
import uuid


# SCRUM-32 manager record attendance by Danfeng
manager_record_attendance = Blueprint(
    'manager_record_attendance',
    __name__,
    static_folder='static',
    template_folder='templates'
)

# manager displays courses
@manager_record_attendance.route('/')
@is_logged_in
def display_course():
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        course_list = manager_get_course()
        return render_template('/manager_record_attendance/manager_record_attendance_display.html',course_list = course_list, is_login=is_login, userid=userid, username=username, roleid=roleid)        

# manager updates attendance for a course    
@manager_record_attendance.route('/update/<int:current_course_id>', methods=['GET'])
@is_logged_in
def update_attendance(current_course_id):
    is_login, userid, username, roleid = get_session_info()
    member_list = []
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        member_list = manager_get_member_info(current_course_id)
        return render_template('/manager_record_attendance/manager_record_attendance_member.html', current_course_id=current_course_id, member_list = member_list, is_login=is_login, userid=userid, username=username, roleid=roleid)
    
@manager_record_attendance.route('/update/submit/<int:current_course_id>', methods=['POST'])
@is_logged_in
def update_attendance_submit(current_course_id):
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:        
        bookingid=request.form.get('bookingid', '')
        is_attend= request.form.get('is_attend', '')
        try:    
            dbconn = getCursor() 
            update_attendance_query = "UPDATE bookings SET is_attend = %s WHERE id = %s"       
            dbconn.execute(update_attendance_query, (is_attend, bookingid))
            flash('Update attendance successfully', 'success')
        except Exception as e:
            print('An error occurred: ' + str(e))
            flash('An error occurred. Please try again later.', 'danger')
        return redirect(url_for('manager_record_attendance.update_attendance',current_course_id =current_course_id))
