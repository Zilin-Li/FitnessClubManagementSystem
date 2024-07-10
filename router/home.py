from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from db_mamager import getCursor
from datetime import datetime
from utility.auth_utility import is_logged_in
from utility.member_utility import get_session_info
from utility.trainer_utility import get_trainer_info

home = Blueprint(
    'home',
    __name__,
    static_folder='static',
    template_folder='templates'
)


@home.route('/')
def view_trainer():
    # Check if the user is logged in
    is_login = False
    userid = None
    username = None
    roleid = None

    trainer_list = get_trainer_info()  # Get trainer information 

    return render_template('/home/member_trainer_display.html', trainer_list=trainer_list, is_login=is_login, userid=userid, username=username, roleid=roleid)

@home.route('/detail/<int:trainer_user_id>', methods=['GET'])
def trainer_detail(trainer_user_id):
    trainer_info_list = get_trainer_info(trainer_user_id)
    trainer_id = trainer_info_list[10]
    
    get_session_info_query = """
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
    dbconn.execute(get_session_info_query, (trainer_id,))
    trainer_session_list = dbconn.fetchall()
    
    return render_template('/home/member_trainer_detail.html', trainer_session_list=trainer_session_list, trainer_info_list=trainer_info_list)
