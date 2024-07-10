from flask import session, request, redirect, url_for, flash
from db_mamager import getCursor
from datetime import datetime
def get_course_info(course_type_id=1): 
    query = """
            SELECT 
                fc.id AS class_id,
                fc.name AS class_name,    
                DATE(fc.schedule_time) AS class_date, 
                TIME(fc.schedule_time) AS class_time, 
                fc.capacity,
                tr.first_name AS trainer_first_name, 
                tr.last_name AS trainer_last_name, 
                loc.name AS location_name,
                COUNT(b.id) AS booking_count,
                fc.price AS class_price
            FROM 
                fitness_classes AS fc
            JOIN 
                trainers AS tr ON fc.trainer_id = tr.id
            JOIN 
                location AS loc ON fc.location_id = loc.id
            LEFT JOIN 
                bookings AS b ON fc.id = b.fitness_class_id AND b.status = 1
            WHERE 
                fc.course_type_id = %s
            AND 
                fc.schedule_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 7 DAY)
            GROUP BY 
                fc.id
            ORDER BY 
                DATE(fc.schedule_time), 
                TIME(fc.schedule_time);
            """
    dbconn = getCursor()
    class_list = []
    courses_by_date = {}
    try:
        dbconn.execute(query, (course_type_id,))
        class_list = dbconn.fetchall() 
        for daily_class in class_list:
            class_date = daily_class[2]
            if class_date not in courses_by_date:
                courses_by_date[class_date] = []
            courses_by_date[class_date].append({
                'class_id': daily_class[0],
                'class_name': daily_class[1],
                'class_time': daily_class[3],
                'capacity': daily_class[4],
                'trainer_first_name': daily_class[5],
                'trainer_last_name': daily_class[6],
                'location_name': daily_class[7],
                'booking_count': daily_class[4] -daily_class[8],
                'class_price': daily_class[9]
            })
        print(courses_by_date)
    except Exception as e:
        print(e)
        flash('Error in fetching data from database', 'danger')
    return courses_by_date