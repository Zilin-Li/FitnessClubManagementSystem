from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from db_mamager import getCursor
from utility.auth_utility import is_logged_in,check_password
from utility.manager_utility import manager_get_session, manager_get_trainer_info
from utility.trainer_utility import get_type_info, get_location_info
from utility.member_utility import get_session_info
import re
import os
import uuid
from datetime import datetime

# SCRUM-31 manager manage session by Danfeng
manager_manage_session = Blueprint(
    'manager_manage_session',
    __name__,
    static_folder='static',
    template_folder='templates'
)

# manager displays sessions
@manager_manage_session.route('/')
@is_logged_in
def display_session():
    is_login, userid, username, roleid = get_session_info()
    session_list = []
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        trainer_name = request.args.get('trainer_name')
        if trainer_name is not None:
            session_list = manager_get_session(None, trainer_name)
        else:
            session_list = manager_get_session()
        session_list_to_do=[]
        session_list_done=[]
        for session in session_list:
            if session[13]<=0:
                session_list_to_do.append(session)
            else:
                session_list_done.append(session)
        return render_template('/manager_manage_session/manager_manage_session_display.html', session_list_to_do = session_list_to_do, session_list_done=session_list_done, is_login=is_login, userid=userid, username=username, roleid=roleid)        

# manager view the details of a session
@manager_manage_session.route('/detail/<int:current_session_id>', methods=['GET'])
@is_logged_in    
def session_detail(current_session_id):
    is_login, userid, username, roleid = get_session_info()
    session_detail = []
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        session_detail = manager_get_session(current_session_id)      
        return render_template('/manager_manage_session/manager_manage_session_detail.html',session_detail = session_detail,  is_login=is_login, userid=userid, username=username, roleid=roleid)

# manager update a session    
@manager_manage_session.route('/update/<int:current_session_id>', methods=['GET'])
@is_logged_in
def update_session(current_session_id):
    is_login, userid, username, roleid = get_session_info()
    session_detail = []
    type_list=[]
    location_list=[]
    trainer_list=[]
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        session_detail = manager_get_session(current_session_id)
        initial_price = "{:.2f}".format(session_detail[6] if session_detail[6] is not None else 0.00)   #Format the initial price
        type_list=get_type_info()
        location_list=get_location_info()
        trainer_list=manager_get_trainer_info()
        return render_template('/manager_manage_session/manager_manage_session_edit.html', trainer_list=trainer_list, session_detail = session_detail, initial_price=initial_price, type_list=type_list, location_list=location_list, is_login=is_login, userid=userid, username=username, roleid=roleid)
    
@manager_manage_session.route('/update/submit/<int:current_session_id>', methods=['POST'])
@is_logged_in
def update_session_submit(current_session_id):
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        trainer_id= request.form.get('trainer_id', '')
        sessionname= request.form.get('sessionname', '')
        course_type_id= request.form.get('course_type_id', '')
        schedule_time=request.form.get('schedule_time', '')
        location_id= request.form.get('location_id', '')
        price= request.form.get('price', '')
        capacity= request.form.get('capacity', '')
        description=request.form.get('description', '') 

        # Ensure schedule_time is within the specified range
        schedule_time_datetime = datetime.strptime(schedule_time, '%Y-%m-%dT%H:%M')
        if schedule_time_datetime.hour < 6 or schedule_time_datetime.hour >= 20:
            flash('Schedule time must be between 6 am and 8 pm, 7 days a week.', 'danger')
            return redirect(url_for('manager_manage_session.update_session', current_session_id=current_session_id))
        # Exclude Christmas Day and Boxing Day
        if schedule_time_datetime.month == 12 and schedule_time_datetime.day in [25, 26]:
            flash('Sessions cannot be scheduled on Christmas Day or Boxing Day.', 'danger')
            return redirect(url_for('manager_manage_session.update_session', current_session_id=current_session_id))
        
        try:    
            dbconn = getCursor() 
            # session UPDATE
            update_session_query = "UPDATE fitness_classes SET trainer_id= %s, name = %s,course_type_id= %s, schedule_time = %s,location_id= %s, price=%s,capacity=%s, description = %s WHERE id = %s"       
            dbconn.execute(update_session_query, (trainer_id, sessionname, course_type_id, schedule_time, location_id, price, capacity, description, current_session_id))
            flash('Update session successfully', 'success')
        except Exception as e:
            print('An error occurred: ' + str(e))
            flash('An error occurred. Please try again later.', 'danger')
        return redirect(url_for('manager_manage_session.update_session',current_session_id =current_session_id))

# manager add a session    
@manager_manage_session.route('/add',methods=['GET'])
@is_logged_in
def add_session():
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        type_list=get_type_info()
        location_list=get_location_info()
        formatted_now = datetime.now().strftime('%Y-%m-%d %H:%M')
        trainer_list=manager_get_trainer_info()
        return render_template('/manager_manage_session/manager_manage_session_add.html',trainer_list=trainer_list, formatted_now=formatted_now, type_list=type_list, location_list=location_list, is_login=is_login, userid=userid, username=username, roleid=roleid)
        
@manager_manage_session.route('/add/submit', methods=['POST'])
@is_logged_in
def add_session_submit():
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        trainer_id= request.form.get('trainer_id', '')
        sessionname = request.form.get('sessionname')
        course_type_id = request.form.get('course_type_id')
        schedule_time = request.form.get('schedule_time')
        location_id = request.form.get('location_id')
        price = request.form.get('price')
        capacity = request.form.get('capacity')
        description = request.form.get('description', '')  

        # Ensure schedule_time is within the specified range
        schedule_time_datetime = datetime.strptime(schedule_time, '%Y-%m-%dT%H:%M')
        if schedule_time_datetime.hour < 6 or schedule_time_datetime.hour >= 20:
            flash('Schedule time must be between 6 am and 8 pm, 7 days a week.', 'danger')
            return redirect(url_for('manager_manage_session.add_session'))
        # Exclude Christmas Day and Boxing Day
        if schedule_time_datetime.month == 12 and schedule_time_datetime.day in [25, 26]:
            flash('Sessions cannot be scheduled on Christmas Day or Boxing Day.', 'danger')
            return redirect(url_for('manager_manage_session.add_session'))
        
        if request.method == 'POST' and trainer_id and sessionname and course_type_id and schedule_time and location_id and price and capacity:
            try:
                dbconn = getCursor()
                insert_session_query = """INSERT INTO fitness_classes VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)"""
                dbconn.execute(insert_session_query, (sessionname, description, course_type_id, trainer_id, schedule_time, location_id, price, capacity))  
                flash('Add session successfully', 'success')   
            except Exception as e:
                print('An error occurred: ' + str(e))
                flash('An error occurred. Please try again later.', 'danger')
        else:
            flash('Something wrong.', 'danger')
    return redirect(url_for('manager_manage_session.add_session'))

# manager delete sessions
@manager_manage_session.route('/delete/<int:current_session_id>', methods=['GET'])
@is_logged_in
def delete_session(current_session_id):
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        try:
            dbconn = getCursor()
            select_booking_query = "SELECT * FROM bookings WHERE fitness_class_id = %s"
            dbconn.execute(select_booking_query , (current_session_id,))
            booking=dbconn.fetchone()
            if booking is not None:
                flash('This session can not be deleted as it has bookings', 'danger')
            else:
                try:
                    delete_session_query = "DELETE FROM fitness_classes WHERE id = %s"
                    dbconn.execute(delete_session_query, (current_session_id,))
                    flash('Delete session successfully', 'success')
                except Exception as e:
                    print('An error occurred: ' + str(e))
                    flash('An error occurred. Please try again later.', 'danger')
        except Exception as e:
                    print('An error occurred: ' + str(e))
                    flash('An error occurred. Please try again later.', 'danger')        
        return redirect(url_for('manager_manage_session.display_session',is_login=is_login, userid=userid, username=username, roleid=roleid))   
    
