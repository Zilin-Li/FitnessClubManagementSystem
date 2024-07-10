from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from db_mamager import getCursor
from utility.auth_utility import is_logged_in
from utility.member_utility import get_session_info
from utility.trainer_utility import trainer_get_session, get_type_info, get_location_info, trainer_get_session_info
from datetime import datetime

# SCRUM-26 Trainer view sessions by gavin
trainer_view_session = Blueprint(
    'trainer_view_session',
    __name__,
    static_folder='static',
    template_folder='templates'
)

# trainer displays sessions
@trainer_view_session.route('/')
@is_logged_in
def display_session():
    is_login, userid, username, roleid = get_session_info()
    class_list = []
    if roleid != 2:
        return redirect(url_for('auth.login'))
    else:
        class_list = trainer_get_session_info(userid,)
        return render_template('/trainer_view_session/trainer_view_session_display.html',class_list = class_list, is_login=is_login, userid=userid, username=username, roleid=roleid)        

# trainer view the details of a sessions
@trainer_view_session.route('/detail/<int:current_class_id>', methods=['GET'])
@is_logged_in    
def session_detail(current_class_id):
    is_login, userid, username, roleid = get_session_info()
    session_detail = []
    if roleid != 2:
        return redirect(url_for('auth.login'))
    else:
        session_detail = trainer_get_session_info(userid,current_class_id)      
        return render_template('/trainer_view_session/trainer_view_session_detail.html',class_detail = session_detail,  is_login=is_login, userid=userid, username=username, roleid=roleid)

