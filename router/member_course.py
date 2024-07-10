from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from db_mamager import getCursor
from datetime import datetime
from utility.auth_utility import is_logged_in
from utility.course_utility import get_course_info

member_course = Blueprint(
    'member_course',
    __name__,
    static_folder='static',
    template_folder='templates'
)
@member_course.route('/classes_timetable', methods=['GET'])
# Display all the classes timetable for all visitors
def view_class():
    courses_by_date = get_course_info(1)
    return render_template('/member_view_course/member_classes_timetable.html',courses_by_date=courses_by_date)

@member_course.route('sessions_timetable', methods=['GET'])
# Display all the sessions timetable for all visitors
def view_session():
    courses_by_date = get_course_info(2)
    return render_template('/member_view_course/member_sessions_timetable.html',courses_by_date=courses_by_date)