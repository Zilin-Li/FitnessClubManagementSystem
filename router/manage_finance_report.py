from flask import Blueprint, session, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from db_mamager import getCursor
from utility.auth_utility import is_logged_in,check_password
from utility.manager_utility import get_finance_report, manager_get_trainer_info
from utility.member_utility import get_session_info, allowed_file
import re
import os
import uuid


# create a blueprint
manage_report = Blueprint(
    'manage_report',
    __name__,
    static_folder='static',
    template_folder='templates'
)

@manage_report.route('/')
@is_logged_in
def finance_report():
    is_login, userid, username, roleid = get_session_info()

    if roleid != 3:
        return redirect(url_for('auth.login'))
    else:
        finance_report = get_finance_report()
        current_year_month = str(finance_report[0][0])+"-"+str(finance_report[0][1])
        report_label = [current_year_month]
        amout_map = {}
        subscription_amout = []
        session_amout = []
        for row in finance_report:
            if str(row[0])+"-"+str(row[1]) != current_year_month:
                current_year_month = str(row[0])+"-"+str(row[1])
                report_label.append(current_year_month)
            amout_map[current_year_month+"-"+str(row[2])] = row[3]
        for label in report_label:
            if label+"-subscription" in amout_map:
                subscription_amout.append(amout_map[label+"-subscription"])
            else:
                subscription_amout.append(0)
            if label+"-session" in amout_map:
                session_amout.append(amout_map[label+"-session"])
            else:
                session_amout.append(0)

        return render_template('/manager_report/finance_report.html',report_label=report_label, subscription_amout=subscription_amout, session_amout=session_amout)        