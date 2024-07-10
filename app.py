from flask import Flask, render_template
from router.auth import auth
from router.manager import manager
from router.member import member
from router.trainer import trainer
from router.manage_trainer import manage_trainer
from router.manager_member import manager_member
from router.manage_finance_report import manage_report
from router.member_trainer import member_trainer
from router.member_course import member_course
from router.trainer_manage_session import trainer_manage_session
from router.trainer_view_session import trainer_view_session
from router.trainer_record_attendance import trainer_record_attendance
from router.manager_record_attendance import manager_record_attendance
from router.member_subscribe import member_subscribe
from router.member_booking import member_booking
from router.manager_manage_session import manager_manage_session
from router.manager_manage_class import manager_manage_class

from router.home import home

from router.manager_news import manager_news
from router.manage_view_subscription_status import manage_view_subscription_status
from router.attendance_report import attendance_report


app = Flask(__name__)


# set the secret key.  keep this really secret:
app.secret_key = 'lkdshijh2398ih$%#8&8%$NMBVh54#%40-0_'


# register the blueprint
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(home, url_prefix='/home')
app.register_blueprint(manager, url_prefix='/manager')
app.register_blueprint(member, url_prefix='/member')
app.register_blueprint(trainer, url_prefix='/trainer')
app.register_blueprint(trainer_manage_session,
                       url_prefix='/trainer_manage_session')
app.register_blueprint(trainer_view_session,
                       url_prefix='/trainer_view_session')
app.register_blueprint(trainer_record_attendance,
                       url_prefix='/trainer_record_attendance')

app.register_blueprint(manage_trainer, url_prefix='/manage_trainer')
app.register_blueprint(manager_member, url_prefix='/manager_member')
app.register_blueprint(manage_report, url_prefix='/manage_report')
app.register_blueprint(manager_manage_class, url_prefix='/manager_manage_class')
app.register_blueprint(manager_record_attendance, url_prefix='/manager_record_attendance')
app.register_blueprint(manager_manage_session,
                       url_prefix='/manager_manage_session')

app.register_blueprint(member_trainer, url_prefix='/member_trainer')
app.register_blueprint(member_course, url_prefix='/member_course')
app.register_blueprint(member_subscribe, url_prefix='/member_subscribe')
app.register_blueprint(member_booking, url_prefix='/member_booking')
app.register_blueprint(manager_news, url_prefix='/manager_news')
app.register_blueprint(manage_view_subscription_status,
                       url_prefix='/subscription_status')
app.register_blueprint(attendance_report, url_prefix='/attendance_report')


@app.route('/')
def home():
    return render_template('home.html')


# run the app
if __name__ == '__main__':
    app.run(debug=True, port=8080)

# UPLOAD_FOLDER = 'static/images/member'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
