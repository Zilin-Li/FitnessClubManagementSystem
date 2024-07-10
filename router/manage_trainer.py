from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from db_mamager import getCursor
from utility.auth_utility import is_logged_in,check_password
from utility.manager_utility import manager_get_trainer_info
from utility.member_utility import get_session_info, allowed_file
import re
import os
import uuid

manage_trainer = Blueprint(
    'manage_trainer',
    __name__,
    static_folder='static',
    template_folder='templates'
)
#SCRUM 10 manager manage trainers function by Danfeng
@manage_trainer.route('/')
@is_logged_in
def display_trainer():
    is_login, userid, username, roleid = get_session_info()
    trainer_list = []
    if roleid != 3:
        return redirect(url_for('login'))
    else:
        trainer_list = manager_get_trainer_info()
        return render_template('/manager_manage_trainer/manage_trainer_display.html',trainer_list = trainer_list, is_login=is_login, userid=userid, username=username, roleid=roleid)        

@manage_trainer.route('/detail/<int:current_user_id>', methods=['GET'])
@is_logged_in    
def trainer_detail(current_user_id):
    is_login, userid, username, roleid = get_session_info()
    trainer_detail = []
    if roleid != 3:
        return redirect(url_for('login'))
    else:
        trainer_detail = manager_get_trainer_info(current_user_id)      
        return render_template('/manager_manage_trainer/manage_trainer_detail.html',trainer_detail = trainer_detail,  is_login=is_login, userid=userid, username=username, roleid=roleid)

@manage_trainer.route('/update/<int:current_user_id>', methods=['GET'])
@is_logged_in
def update_trainer(current_user_id):
    is_login, userid, username, roleid = get_session_info()
    trainer_detail = []
    if roleid != 3:
        return redirect(url_for('login'))
    else:
        trainer_detail = manager_get_trainer_info(current_user_id)
        
        return render_template('/manager_manage_trainer/manage_trainer_edit.html',trainer_detail = trainer_detail,  is_login=is_login, userid=userid, username=username, roleid=roleid)

@manage_trainer.route('/update/submit/<int:current_user_id>', methods=['POST'])
@is_logged_in
def update_trainer_submit(current_user_id):
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('login'))
    else:
        first_name= request.form.get('first_name', '')
        last_name= request.form.get('last_name', '')
        title=request.form.get('title', '')
        phone_number= request.form.get('phone_number', '')
        email=request.form.get('email', '')
        # new_password=request.form.get('new_password')
        # confirm_password= request.form.get('confirm_password')
        status_value=request.form.get('status')
        status = 1 if status_value == 'Active' else 0
        profile_image = request.files.get('profile_image', None) 
        description=request.form.get('description', '')   
        # PASSWORD VALIDATION
        # if new_password and confirm_password:
        #     if new_password != confirm_password:
        #         flash('Password does not match', 'error')
        #         return redirect(url_for('manage_trainer.update_trainer', current_user_id=current_user_id))
        #     elif not check_password(new_password):
        #         return redirect(url_for('manage_trainer.update_trainer', current_user_id=current_user_id))
        # elif new_password or confirm_password:
        #     flash('Please fill in both password fields to update your password.', 'danger')
        #     return redirect(url_for('manage_trainer.update_trainer', current_user_id=current_user_id))

        if email :
            if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                flash('Invalid email address!','error')
                return redirect(url_for('manage_trainer.update_trainer', current_user_id=current_user_id))
        
        # PROFILE IMAGE VALIDATION
        if profile_image and not allowed_file(profile_image.filename):
            flash('Invalid file type', 'error')
            return redirect(url_for('manage_trainer.update_trainer', current_user_id=current_user_id))
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
                # save the image to the static/images/trainer folder
                new_profile_image.save(os.path.join('static/images/trainer', filename))
                # update the profile_image in the database
                update_image_query = "UPDATE trainers SET profile_image = %s WHERE user_id = %s"
                dbconn.execute(update_image_query, (filename, current_user_id))

        # PROFILE UPDATE
            update_status_query = "UPDATE users SET status = %s,email = %s WHERE id = %s"
            update_trainer_query = "UPDATE trainers SET first_name = %s, last_name = %s, title = %s, phone_number = %s, description =%s WHERE user_id = %s"
       
            dbconn.execute(update_status_query, (status, email, current_user_id))
            dbconn.execute(update_trainer_query, (first_name,last_name,title,phone_number, description,current_user_id))
            flash('Update trainer successfully', 'success')
        except Exception as e:
            print('An error occurred: ' + str(e))
            flash('An error occurred. Please try again later.', 'danger')
        return redirect(url_for('manage_trainer.update_trainer',current_user_id =current_user_id))

@manage_trainer.route('/add',methods=['GET'])
@is_logged_in
def add_trainer():
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('login'))
    else:
        return render_template('/manager_manage_trainer/manage_trainer_add.html',is_login=is_login, userid=userid, username=username, roleid=roleid)
        
@manage_trainer.route('/add/submit',  methods=['POST'])
@is_logged_in
def add_trainer_submit():
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('login'))
    else:
        new_username= request.form.get('new_username')
        first_name= request.form.get('first_name','')
        last_name= request.form.get('last_name','')
        title=request.form.get('title','')
        phone_number= request.form.get('phone_number','')
        email=request.form.get('email','')
        password=request.form.get('new_password')
        confirm_password= request.form.get('confirm_password')
        status_value=request.form.get('status')
        status = 1 if status_value == 'Active' else 0
        profile_image = request.files.get('profile_image','')
        description = request.form.get('description','')          
        #if new_username,password,confirm_password in request.form:
        if request.method == 'POST' and new_username and password and confirm_password:
            # print (new_username, password, confirm_password,request.method)
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
                return redirect(url_for('manage_trainer.add_trainer',is_login=is_login, userid=userid, username=username, roleid=roleid))
            # EMAIL VALIDATION
            if email and not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    flash('Invalid email address!','error')
                    return redirect(url_for('manage_trainer.add_trainer',is_login=is_login, userid=userid, username=username, roleid=roleid))       
        # PASSWORD VALIDATION
            if password != confirm_password:
                flash('Password does not match', 'error')
                return redirect(url_for('manage_trainer.add_trainer',is_login=is_login, userid=userid, username=username, roleid=roleid))
            elif not check_password(password):
                return redirect(url_for('manage_trainer.add_trainer',is_login=is_login, userid=userid, username=username, roleid=roleid))
            else:
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)           
            # PROFILE IMAGE VALIDATION
            if profile_image:
                if not allowed_file(profile_image.filename):
                    flash('Invalid file type', 'error')
                    return redirect(url_for('manage_trainer.add_trainer',is_login=is_login, userid=userid, username=username, roleid=roleid))
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
                    new_profile_image.save(os.path.join('static/images/trainer', filename))
            else:
                filename = None
            
            try:
                dbconn = getCursor()
                insert_user_query = """INSERT INTO users(username, password_hash, email, role_id, status) VALUES (%s, %s, %s, %s, %s)"""
                dbconn.execute(insert_user_query, (new_username, hashed_password, email, 2, status))
                new_user_id = dbconn.lastrowid
                insert_trainer_query = """INSERT INTO trainers(user_id, first_name, last_name, title, phone_number, description,profile_image) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
                try:     
                    dbconn.execute(insert_trainer_query, (new_user_id, first_name, last_name, title, phone_number, description,filename))
                    flash('Add trainer successfully', 'success')
                except Exception as e_inner:
                    # if the trainer insert fails, delete the user which was inserted before
                    delete_user_query = """DELETE FROM users WHERE id = %s"""
                    dbconn.execute(delete_user_query, (new_user_id,))
                    raise e_inner       
            except Exception as e:
                print('An error occurred: ' + str(e))
                flash('An error occurred. Please try again later.', 'danger')
        else:
            flash('Something wrong.', 'danger')
    return redirect(url_for('manage_trainer.add_trainer',is_login=is_login, userid=userid, username=username, roleid=roleid))

@manage_trainer.route('/delete/<int:current_user_id>', methods=['GET'])
@is_logged_in
def delete_trainer(current_user_id):
    is_login, userid, username, roleid = get_session_info()
    if roleid != 3:
        return redirect(url_for('login'))
    else:
        try:
            dbconn = getCursor()
            select_course_query = "SELECT * FROM fitness_classes f JOIN trainers t ON f.trainer_id=t.id WHERE t.user_id = %s"
            dbconn.execute(select_course_query , (current_user_id,))
            course=dbconn.fetchone()
            if course is not None:
                flash('This trainer can not be deleted as this trainer has courses', 'danger')
            else:
                try:
                    delete_trainer_query = "DELETE FROM trainers WHERE user_id = %s"
                    delete_user_query = "DELETE FROM users WHERE id = %s"
                    dbconn.execute(delete_trainer_query, (current_user_id,))
                    dbconn.execute(delete_user_query, (current_user_id,))
                    flash('Delete trainer successfully', 'success')
                except Exception as e:
                    print('An error occurred: ' + str(e))
                    flash('An error occurred. Please try again later.', 'danger')
        except Exception as e:
                    print('An error occurred: ' + str(e))
                    flash('An error occurred. Please try again later.', 'danger')              
        return redirect(url_for('manage_trainer.display_trainer',is_login=is_login, userid=userid, username=username, roleid=roleid))