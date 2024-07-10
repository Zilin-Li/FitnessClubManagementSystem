from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from db_mamager import getCursor
from datetime import datetime
from utility.auth_utility import is_logged_in
from utility.member_utility import get_session_info
from utility.trainer_utility import get_trainer_info

member_trainer = Blueprint(
    'member_trainer',
    __name__,
    static_folder='static',
    template_folder='templates'
)
@member_trainer.route('/')
def view_trainer():
    is_login, userid, username, roleid = get_session_info()
    trainer_list = []
    trainer_list = get_trainer_info()
    return render_template('/member_view_trainer/member_trainer_display.html',trainer_list=trainer_list)

@member_trainer.route('/detail/<int:trainer_user_id>', methods=['GET'])
   
def trainer_detail(trainer_user_id):
    is_login, userid, username, roleid = get_session_info()
    trainer_info_list=[]
    trainer_session_list=[]
    trainer_id = ''
   
    trainer_info_list = get_trainer_info(trainer_user_id)
    trainer_id = trainer_info_list[10]
    
    get_session_info_qurey ="""
        SELECT    
            fc.name,
            fc.description,
            fc.schedule_time,
            fc.price,
            l.name AS location_name,
            fc.id AS session_id,
            b.status AS booking_status
        FROM 
            trainers t
        JOIN 
            fitness_classes fc ON t.id = fc.trainer_id
        LEFT JOIN 
            location l ON fc.location_id = l.id
        JOIN 
            course_types ct ON fc.course_type_id = ct.id
        LEFT JOIN
            bookings b ON fc.id = b.fitness_class_id
        WHERE 
            t.id = %s  
            AND ct.id = 2
            AND fc.schedule_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 14 DAY);
    """
    dbconn = getCursor()
    dbconn.execute(get_session_info_qurey, (trainer_id,))
    trainer_session_list = dbconn.fetchall()
    return render_template('/member_view_trainer/member_trainer_detail.html', trainer_session_list =trainer_session_list ,trainer_info_list =trainer_info_list)
