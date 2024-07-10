from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from db_mamager import getCursor
from utility.auth_utility import is_logged_in
from utility.member_utility import get_session_info

member_subscribe = Blueprint('member_subscribe', __name__,  static_folder='static', template_folder='templates')

@member_subscribe.route('/member_subscribe', methods=['GET'])
@is_logged_in
def view_subscribe():
    is_login, userid, username, roleid = get_session_info()
    subscriptions = []
    dbconn = getCursor()
    query="""
        SELECT 
            ss.id as SubscriptionId,
            sp.id as PlanId,
            sp.type AS SubscriptionType,
            sp.price AS SubscriptionPrice,
            ss.start_date AS StartDate,
            ss.end_date AS EndDate,
            CASE
                WHEN ss.end_date >= CURDATE() THEN 'Active'
                ELSE 'Expired'
            END AS SubscriptionStatus
        FROM 
            specific_subscriptions ss
        JOIN 
            subscription_plans sp ON ss.subscription_plan_id = sp.id
        WHERE 
            ss.user_id = %s
        ORDER BY 
            ss.end_date DESC;;
    """
    try:
        dbconn.execute(query, (userid,))
        subscriptions = dbconn.fetchall()
    except Exception as e:
        print(e)
        flash('Error in fetching data from database', 'danger')

    return render_template('/member_view_subscrib/member_subscribe.html',subscriptions=subscriptions )
