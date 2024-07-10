from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from db_mamager import getCursor
from utility.auth_utility import is_logged_in,check_password
from utility.manager_utility import manager_get_class, manager_get_trainer_info
from utility.trainer_utility import get_type_info, get_location_info
from utility.member_utility import get_session_info
import re
import os
import uuid
from datetime import datetime, timedelta

# SCRUM-30 manager manage class and weekly timetable by Xing
manager_manage_class = Blueprint(
    'manager_manage_class',
    __name__,
    static_folder='static',
    template_folder='templates'
)

# manager displays class
@manager_manage_class.route('/')
@is_logged_in
def display_class():
    is_login, userid, username, roleid = get_session_info()
    class_list = []
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        class_list = manager_get_class()
        class_list_to_do=[]
        class_list_done=[]
        for aclass in class_list:
            if aclass[13]<=0:
                class_list_to_do.append(aclass)
            else:
                class_list_done.append(aclass)
        return render_template('/manager_manage_class/manager_manage_class_display.html', class_list_to_do = class_list_to_do, class_list_done=class_list_done, is_login=is_login, userid=userid, username=username, roleid=roleid)         

@manager_manage_class.route('/display_weekly/<selected_week>')
@is_logged_in
def display_class_weekly(selected_week):
    is_login, userid, username, roleid = get_session_info()
    class_list = []
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        try:
            # Split the selected week into year and week number
            year, week_str = selected_week.split('-W')
            week_number = int(week_str)
            # Ensure the week number is within a valid range (1 to 52)
            if not (1 <= week_number <= 52):
                raise ValueError("Week number is not within a valid range (1 to 52)")

            # Calculate the start and end dates of the selected week
            start_date = datetime.strptime(f"{year}-W{week_number}-1", '%G-W%V-%u')
            end_date = start_date + timedelta(days=6)

            # Call the function to get all classes
            all_classes = manager_get_class()

            # Filter classes for the selected week
            class_list = [cls for cls in all_classes if start_date <= cls[4] <= end_date]
            class_list_to_do=[]
            class_list_done=[]
            for aclass in class_list:
                if aclass[13]<=0:
                    class_list_to_do.append(aclass)
                else:
                    class_list_done.append(aclass)
            return render_template('/manager_manage_class/manager_manage_class_display.html', class_list_to_do = class_list_to_do, class_list_done=class_list_done, is_login=is_login, userid=userid, username=username, roleid=roleid) 
        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('manager_manage_class.display_class'))

# manager view the details of a class
@manager_manage_class.route('/detail/<int:current_class_id>', methods=['GET'])
@is_logged_in    
def class_detail(current_class_id):
    is_login, userid, username, roleid = get_session_info()
    class_detail = []
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        class_detail = manager_get_class(current_class_id)      
        return render_template('/manager_manage_class/manager_manage_class_detail.html',class_detail = class_detail,  is_login=is_login, userid=userid, username=username, roleid=roleid)

# manager update a class    
@manager_manage_class.route('/update/<int:current_class_id>', methods=['GET'])
@is_logged_in
def update_class(current_class_id):
    is_login, userid, username, roleid = get_session_info()
    class_detail = []
    type_list=[]
    location_list=[]
    trainer_list=[]
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        class_detail = manager_get_class(current_class_id)
        initial_price = "{:.2f}".format(class_detail[6] if class_detail[6] is not None else 0.00)   #Format the initial price
        type_list=get_type_info()
        location_list=get_location_info()
        trainer_list=manager_get_trainer_info()
        return render_template('/manager_manage_class/manager_manage_class_edit.html', trainer_list=trainer_list, class_detail = class_detail, initial_price=initial_price, type_list=type_list, location_list=location_list, is_login=is_login, userid=userid, username=username, roleid=roleid)
    
@manager_manage_class.route('/update/submit/<int:current_class_id>', methods=['POST'])
@is_logged_in
def update_class_submit(current_class_id):
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        trainer_id= request.form.get('trainer_id', '')
        classname= request.form.get('classname', '')
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
            return redirect(url_for('manager_manage_class.update_class', current_class_id=current_class_id))
        # Exclude Christmas Day and Boxing Day
        if schedule_time_datetime.month == 12 and schedule_time_datetime.day in [25, 26]:
            flash('Classes cannot be scheduled on Christmas Day or Boxing Day.', 'danger')
            return redirect(url_for('manager_manage_class.update_class', current_class_id=current_class_id))
        
        try:    
            dbconn = getCursor() 
            # class UPDATE
            update_class_query = "UPDATE fitness_classes SET trainer_id= %s, name = %s,course_type_id= %s, schedule_time = %s,location_id= %s, price=%s,capacity=%s, description = %s WHERE id = %s"       
            dbconn.execute(update_class_query, (trainer_id, classname, course_type_id, schedule_time, location_id, price, capacity, description, current_class_id))
            flash('Update class successfully', 'success')
        except Exception as e:
            print('An error occurred: ' + str(e))
            flash('An error occurred. Please try again later.', 'danger')
        return redirect(url_for('manager_manage_class.update_class',current_class_id =current_class_id))

# manager add a class    
@manager_manage_class.route('/add',methods=['GET'])
@is_logged_in
def add_class():
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        type_list=get_type_info()
        location_list=get_location_info()
        formatted_now = datetime.now().strftime('%Y-%m-%d %H:%M')
        trainer_list=manager_get_trainer_info()
        return render_template('/manager_manage_class/manager_manage_class_add.html',trainer_list=trainer_list, formatted_now=formatted_now, type_list=type_list, location_list=location_list, is_login=is_login, userid=userid, username=username, roleid=roleid)
        
@manager_manage_class.route('/add/submit', methods=['POST'])
@is_logged_in
def add_class_submit():
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        trainer_id= request.form.get('trainer_id', '')
        classname = request.form.get('classname')
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
            return redirect(url_for('manager_manage_class.add_class'))
        # Exclude Christmas Day and Boxing Day
        if schedule_time_datetime.month == 12 and schedule_time_datetime.day in [25, 26]:
            flash('Classes cannot be scheduled on Christmas Day or Boxing Day.', 'danger')
            return redirect(url_for('manager_manage_class.add_class'))
        
        if request.method == 'POST' and trainer_id and classname and course_type_id and schedule_time and location_id and price and capacity:
            try:
                dbconn = getCursor()
                insert_class_query = """INSERT INTO fitness_classes VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)"""
                dbconn.execute(insert_class_query, (classname, description, course_type_id, trainer_id, schedule_time, location_id, price, capacity))  
                flash('Add class successfully', 'success')   
            except Exception as e:
                print('An error occurred: ' + str(e))
                flash('An error occurred. Please try again later.', 'danger')
        else:
            flash('Something wrong.', 'danger')
    return redirect(url_for('manager_manage_class.add_class'))

# manager delete class
@manager_manage_class.route('/delete/<int:current_class_id>', methods=['GET'])
@is_logged_in
def delete_class(current_class_id):
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        try:
            dbconn = getCursor()
            select_booking_query = "SELECT * FROM bookings WHERE fitness_class_id = %s"
            dbconn.execute(select_booking_query , (current_class_id,))
            booking=dbconn.fetchone()
            if booking is not None:
                flash('This class can not be deleted as it has bookings', 'danger')
            else:
                try:
                    delete_class_query = "DELETE FROM fitness_classes WHERE id = %s"
                    dbconn.execute(delete_class_query, (current_class_id,))
                    flash('Delete class successfully', 'success')
                except Exception as e:
                    print('An error occurred: ' + str(e))
                    flash('An error occurred. Please try again later.', 'danger')
        except Exception as e:
                    print('An error occurred: ' + str(e))
                    flash('An error occurred. Please try again later.', 'danger') 
        return redirect(url_for('manager_manage_class.display_class',is_login=is_login, userid=userid, username=username, roleid=roleid))   
    
