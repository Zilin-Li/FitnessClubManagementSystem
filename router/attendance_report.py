from flask import Blueprint, render_template
from db_mamager import getCursor

attendance_report = Blueprint(
    'attendance_report',
    __name__,
    static_folder='static',
    template_folder='templates'
)


@attendance_report.route('/', methods=['GET'])
def attendance_report_summary():
    individual_data = get_individual_attendance_data()
    class_data = get_class_attendance_data()
    return render_template('/attendance_report/attendance_report.html', individual_data=individual_data, class_data=class_data)


def get_individual_attendance_data():
    with getCursor() as cursor:
        cursor.execute("""
            SELECT members.id, members.first_name, members.last_name,
                   SUM(bookings.is_attend) AS total_attendance, COUNT(bookings.id) AS total_bookings
            FROM members
            LEFT JOIN bookings ON members.id = bookings.member_id
            GROUP BY members.id, members.first_name, members.last_name
        """)

        columns = [column[0] for column in cursor.description]

        data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    for row in data:
        if row["total_bookings"] != 0:
            row["percentage"] = round(
                row["total_attendance"] / row["total_bookings"] * 100, 2)
        else:
            row["percentage"] = 0

    return data


def get_class_attendance_data():
    attendance_rate = calculate_attendance_rate()
    result = {}

    for fitness_class_id, rate in attendance_rate.items():
        class_name = get_class_name(fitness_class_id)
        result[class_name] = rate

    return result


def calculate_attendance_rate():
    query_total_bookings = """
        SELECT fitness_class_id, 
               COUNT(*) AS total_bookings
        FROM bookings
        GROUP BY fitness_class_id
    """

    query_total_attendance = """
        SELECT fitness_class_id, 
               SUM(CASE WHEN is_attend = 1 THEN 1 ELSE 0 END) AS total_attendance
        FROM bookings
        GROUP BY fitness_class_id
    """

    cursor = getCursor()

    cursor.execute(query_total_bookings)
    total_bookings = cursor.fetchall()

    cursor.execute(query_total_attendance)
    total_attendance = cursor.fetchall()

    attendance_rate = {}

    for (fitness_class_id, total_bookings_count), (id, attendance_count) in zip(total_bookings, total_attendance):
        if total_bookings_count != 0:
            rate = round(attendance_count / total_bookings_count * 100, 2)
        else:
            rate = 0

        attendance_rate[fitness_class_id] = rate

    return attendance_rate


def get_class_name(fitness_class_id):
    query_class_name = "SELECT name FROM fitness_classes WHERE id = {}".format(
        fitness_class_id)
    cursor = getCursor()
    cursor.execute(query_class_name)
    result = cursor.fetchone()
    return result[0] if result else None
