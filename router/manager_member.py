from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from db_mamager import getCursor
from utility.auth_utility import is_logged_in,check_password
from utility.member_utility import get_member_info, get_session_info, allowed_file
import re

import os
import uuid

manager_member = Blueprint(
    'manager_member',
    __name__,
    static_folder='static',
    template_folder='templates'
)

@manager_member.route('/')
@is_logged_in
def display_member():
    is_login, userid, username, roleid = get_session_info()
    member_list = []
    if roleid != 3:
        return redirect(url_for('login'))
    else:
        member_list = get_member_info()
        return render_template('/manage_member/manager_member_display.html',member_list = member_list, is_login=is_login, userid=userid, username=username, roleid=roleid)        

@manager_member.route('/detail/<int:current_user_id>', methods=['GET'])
@is_logged_in    
def member_detail(current_user_id):
    is_login, userid, username, roleid = get_session_info()
    member_detail = []
    if roleid != 3:
        return redirect(url_for('login'))
    else:
        member_detail = get_member_info(current_user_id)      
        return render_template('/manage_member/manager_member_detail.html',member_detail = member_detail,  is_login=is_login, userid=userid, username=username, roleid=roleid)

@manager_member.route('/update/<int:current_user_id>', methods=['GET', 'POST'])
@is_logged_in
def update_member(current_user_id):
    is_login, userid, username, roleid = get_session_info()
    member_detail = []
    if roleid != 3:
        return redirect(url_for('login'))
    else:
        member_detail = get_member_info(current_user_id)
        
        return render_template('/manage_member/manager_member_edit.html',member_detail = member_detail,  is_login=is_login, userid=userid, username=username, roleid=roleid)

@manager_member.route('/update/submit/<int:current_user_id>', methods=['POST'])
@is_logged_in
def update_member_submit(current_user_id):
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('login'))
    else:
        first_name= request.form.get('first_name', '')
        last_name= request.form.get('last_name', '')
        position=request.form.get('position', '')
        phone_number= request.form.get('phone_number', '')
        address= request.form.get('address', '')
        email=request.form.get('email', '')
        birth_date= request.form.get('birth_date', None)
        # new_password=request.form.get('new_password')
        # confirm_password= request.form.get('confirm_password')
        status_value=request.form.get('status')
        status = 1 if status_value == 'Active' else 0
        profile_image = request.files.get('profile_image', None) 
        health_info = request.form.get('health_info', '')
        if not birth_date:
            birth_date = None
        else:
            if birth_date=='':
                birth_date = None
            else:
                birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
                eighteen_years_ago = datetime.now().replace(year=datetime.now().year - 18)
                if birth_date > eighteen_years_ago:
                    flash('You must be at least 18 years old to register.', 'danger')
                    return redirect(url_for('manager_member.update_member', current_user_id=current_user_id))
        # PASSWORD VALIDATION
        # if new_password and confirm_password:
        #     if new_password != confirm_password:
        #         flash('Password does not match', 'error')
        #         return redirect(url_for('manager_member.update_member', current_user_id=current_user_id))
        #     elif not check_password(new_password):
        #         return redirect(url_for('manager_member.update_member', current_user_id=current_user_id))
        # elif new_password or confirm_password:
        #     flash('Please fill in both password fields to update your password.', 'danger')
        #     return redirect(url_for('manager_member.update_member', current_user_id=current_user_id))

        if email :
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address!','error')
                return redirect(url_for('manager_member.update_member',is_login=is_login, userid=userid, username=username, roleid=roleid))
        
        # PROFILE IMAGE VALIDATION
        if profile_image and not allowed_file(profile_image.filename):
            flash('Invalid file type', 'error')
            return redirect(url_for('manager_member.update_member', current_user_id=current_user_id))
        try:
            dbconn = getCursor() 

            # if new_password:
            #     hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
            #     update_password_query = "UPDATE users SET password_hash = %s WHERE id = %s"
            #     dbconn.execute(update_password_query, (hashed_password, current_user_id))   
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
                dbconn.execute(update_image_query, (filename, current_user_id))

        # PROFILE UPDATE
            update_status_query = "UPDATE users SET status = %s,email = %s WHERE id = %s"
            update_member_query = "UPDATE members SET first_name = %s, last_name = %s, position = %s, phone_number = %s, address = %s, birth_date = %s,health_info =%s WHERE user_id = %s"
       
            dbconn.execute(update_status_query, (status, email, current_user_id))
            dbconn.execute(update_member_query, (first_name,last_name,position,phone_number,address,birth_date, health_info,current_user_id))
            flash('Update member successfully', 'success')
        except Exception as e:
            print('An error occurred: ' + str(e))
            flash('An error occurred. Please try again later.', 'danger')
        return redirect(url_for('manager_member.update_member',current_user_id =current_user_id))

@manager_member.route('/add',methods=['GET','POST'])
@is_logged_in
def add_member():
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('login'))
    else:
        return render_template('/manage_member/manager_member_add.html',is_login=is_login, userid=userid, username=username, roleid=roleid)
        
@manager_member.route('/add/submit',  methods=['POST'])
@is_logged_in
def add_member_submit():
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('login'))
    else:
        new_username= request.form.get('new_username')
        first_name= request.form.get('first_name','')
        last_name= request.form.get('last_name','')
        position=request.form.get('position','')
        phone_number= request.form.get('phone_number','')
        address= request.form.get('address','')
        birth_date= request.form.get('birth_date','')
        email=request.form.get('email','')
        password=request.form.get('new_password')
        confirm_password= request.form.get('confirm_password')
        status_value=request.form.get('status')
        status = 1 if status_value == 'Active' else 0
        profile_image = request.files.get('profile_image','')
        health_info = request.form.get('health_info','')  
        # eighteen_years_ago = datetime.now().replace(year=datetime.now().year - 18)
        # print(eighteen_years_ago)        
        if not birth_date:
            birth_date = None
        else:
            if birth_date=='':
                birth_date = None
            else:
                birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
                eighteen_years_ago = datetime.now().replace(year=datetime.now().year - 18)
                if birth_date > eighteen_years_ago:
                    flash('You must be at least 18 years old to register.', 'danger')
                    return redirect(url_for('manager_member.add_member',is_login=is_login, userid=userid, username=username, roleid=roleid))
        #if new_username,password,confirm_password in request.form:
        if request.method == 'POST' and new_username and password and confirm_password:
        # USERNAME VALIDATION
            dbconn = getCursor()
            # query the database
            query = "SELECT COUNT(*) FROM users WHERE LOWER(username) = LOWER(%s)"
            try:
                dbconn.execute(query, (new_username,))
                result = dbconn.fetchone()
            except Exception as e:
                print('An error occurred: ' + str(e))
            # check if the username already exists  
            if result[0] > 0:
                flash('Username already exists.', 'error')
                return redirect(url_for('manager_member.add_member',is_login=is_login, userid=userid, username=username, roleid=roleid))
           
            # EMAIL VALIDATION
            if email and not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    flash('Invalid email address!','error')
                    return redirect(url_for('manager_member.add_member',is_login=is_login, userid=userid, username=username, roleid=roleid))       
        # PASSWORD VALIDATION
            if password != confirm_password:
                flash('Password does not match', 'error')
                return redirect(url_for('manager_member.add_member',is_login=is_login, userid=userid, username=username, roleid=roleid))
            elif not check_password(password):
                return redirect(url_for('manager_member.add_member',is_login=is_login, userid=userid, username=username, roleid=roleid))
            else:
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)           
            # PROFILE IMAGE VALIDATION
            if profile_image:
                if not allowed_file(profile_image.filename):
                    flash('Invalid file type', 'error')
                    return redirect(url_for('manager_member.add_member',is_login=is_login, userid=userid, username=username, roleid=roleid))
                else:
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
            else:
                filename = None
            
            try:
                dbconn = getCursor()
                insert_user_query = """INSERT INTO users(username, password_hash, email, role_id, status) VALUES (%s, %s, %s, %s, %s)"""
                dbconn.execute(insert_user_query, (new_username, hashed_password, email, 1, status))
                new_user_id = dbconn.lastrowid
                insert_member_query = """INSERT INTO members(user_id, first_name, last_name, position, phone_number, address, birth_date, health_info,profile_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s);"""
                try:     
                    dbconn.execute(insert_member_query, (new_user_id, first_name, last_name, position, phone_number, address, birth_date, health_info,filename))
                    flash('Add member successfully', 'success')
                except Exception as e_inner:
                    # if the member insert fails, delete the user which was inserted before
                    delete_user_query = """DELETE FROM users WHERE id = %s"""
                    dbconn.execute(delete_user_query, (new_user_id,))
                    raise e_inner       
            except Exception as e:
                print('An error occurred: ' + str(e))
                flash('An error occurred. Please try again later.', 'danger')
        else:
            flash('Something wrong.', 'danger')
    return redirect(url_for('manager_member.add_member',is_login=is_login, userid=userid, username=username, roleid=roleid))

@manager_member.route('/delete/<int:current_user_id>', methods=['GET'])
@is_logged_in
def delete_member(current_user_id):
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('login'))
    else:
        try:
            dbconn = getCursor()
            select_booking_query = "SELECT * FROM bookings b JOIN members m ON b.member_id=m.id WHERE m.user_id = %s"
            dbconn.execute(select_booking_query , (current_user_id,))
            booking=dbconn.fetchone()
            if booking is not None:
                flash('This member can not be deleted as this member has bookings', 'danger')
            else:
                try:
                    delete_member_query = "DELETE FROM members WHERE user_id = %s"
                    delete_user_query = "DELETE FROM users WHERE id = %s"
                    dbconn.execute(delete_member_query, (current_user_id,))
                    dbconn.execute(delete_user_query, (current_user_id,))
                    flash('Delete member successfully', 'success')
                except Exception as e:
                    print('An error occurred: ' + str(e))
                    flash('An error occurred. Please try again later.', 'danger')
        except Exception as e:
                    print('An error occurred: ' + str(e))
                    flash('An error occurred. Please try again later.', 'danger') 
        return redirect(url_for('manager_member.display_member',is_login=is_login, userid=userid, username=username, roleid=roleid))