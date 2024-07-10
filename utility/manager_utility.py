from flask import session, request, redirect, url_for, flash
from db_mamager import getCursor

#created by Danfeng
def manager_get_trainer_info(user_id=None):
    # get trainer info from the database, if user_id is None, return all the users, otherwise, return the user with the user_id
    query = """
        SELECT
            u.id,
            u.username,
            u.email,
            t.first_name,
            t.last_name,
            t.title,
            t.phone_number,
            t.profile_image,
            t.description,
            u.status,
            t.id
        FROM users u
        JOIN trainers t ON u.id = t.user_id
    """
    if user_id is not None:
        query += " WHERE u.id = %s;"

    dbconn = getCursor()
    try:
        if user_id is not None:
            dbconn.execute(query, (user_id,))
        else:
            dbconn.execute(query)
        if user_id is not None:
            return dbconn.fetchone()  # if it is a single user, return a single record
        else:
            return dbconn.fetchall()  # if it is all users, return all the records
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_finance_report():
    finance_report_sql = """
        SELECT
            YEAR(payment_date) as year,
            MONTH(payment_date) as month,
            payment_type,
            SUM(payment_amount) as total_payment_amount
        FROM
            (
            SELECT
                ss.start_date AS payment_date,
                sp.price AS payment_amount,
                'subscription' AS payment_type
            FROM
                specific_subscriptions ss
            join subscription_plans sp on
                ss.subscription_plan_id = sp.id
        UNION
            SELECT
                b.booking_date AS payment_date,
                fc.price AS payment_amount,
                'session' AS payment_type
            FROM
                bookings b
            join fitness_classes fc on
                b.fitness_class_id = fc.id
            join course_types ct on
                fc.course_type_id = ct.id
            WHERE
                b.is_paid = 1
                and ct.id = 2
                ) payment
        WHERE
            payment_date > DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 12 MONTH), '%Y-%m-01')
        GROUP BY
            YEAR(payment_date),
            MONTH(payment_date),
            payment_type
        ORDER BY
            YEAR(payment_date),
            MONTH(payment_date)
    """
    dbconn = getCursor()
    dbconn.execute(finance_report_sql) 
    return dbconn.fetchall()


#created by Danfeng
def manager_get_session(session_id=None,trainer_name=None):
# get session info from the database, if session_id is None, return all the sessions, otherwise, return the sessions with the session_id 
    query = """
        SELECT
            c.id,
            c.name,
            c.description,
            t.name,
            c.schedule_time,
            l.name,
            c.price,
            c.capacity,  
            t.id,
            l.id,
            tr.first_name,
            tr.last_name,
            tr.id,
            DATEDIFF(CURRENT_DATE(),c.schedule_time) 
        FROM fitness_classes c  
        JOIN location l ON c.location_id = l.id
        JOIN course_types t ON c.course_type_id = t.id
        JOIN trainers tr ON c.trainer_id = tr.id
        WHERE c.course_type_id=2
    """
    dbconn = getCursor()
    try:
        if session_id is not None:
            query += " AND c.id = %s"
            dbconn.execute(query, (session_id,))
            return dbconn.fetchone()  # if it is a single session, return a single record
        elif trainer_name is not None:
            trainer_name_updated=f"%{trainer_name}%"
            query += " AND (tr.first_name LIKE %s OR tr.last_name LIKE %s) ORDER BY c.schedule_time"
            dbconn.execute(query,(trainer_name_updated, trainer_name_updated))
            return dbconn.fetchall()  # if it is for a trainer, return all the records for the trainer 
        else:
            query += "ORDER BY tr.last_name, tr.first_name, c.schedule_time"
            dbconn.execute(query)
            return dbconn.fetchall()  # if it is all sessions, return all the records            
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#created by Danfeng
def manager_get_class(class_id=None,trainer_name=None):
# get class info from the database, if class_id is None, return all the classes, otherwise, return the classes with the class_id 
    query = """
        SELECT
            c.id,
            c.name,
            c.description,
            t.name,
            c.schedule_time,
            l.name,
            c.price,
            c.capacity,  
            t.id,
            l.id,
            tr.first_name,
            tr.last_name,
            tr.id,
            DATEDIFF(CURRENT_DATE(),c.schedule_time) 
        FROM fitness_classes c  
        JOIN location l ON c.location_id = l.id
        JOIN course_types t ON c.course_type_id = t.id
        JOIN trainers tr ON c.trainer_id = tr.id
        WHERE c.course_type_id=1
    """
    dbconn = getCursor()
    try:
        if class_id is not None:
            query += " AND c.id = %s"
            dbconn.execute(query, (class_id,))
            return dbconn.fetchone()  # if it is a single class, return a single record
        elif trainer_name is not None:
            trainer_name_updated=f"%{trainer_name}%"
            query += " AND (tr.first_name LIKE %s OR tr.last_name LIKE %s) ORDER BY c.schedule_time"
            dbconn.execute(query,(trainer_name_updated, trainer_name_updated))
            return dbconn.fetchall()  # if it is for a trainer, return all the records for the trainer 
        else:
            query += "ORDER BY tr.last_name, tr.first_name, c.schedule_time"
            dbconn.execute(query)
            return dbconn.fetchall()  # for all the classes, return all the records            
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#created by Danfeng
def manager_get_course(course_id=None,trainer_name=None):
# get course info from the database, if course_id is None, return all the courses, otherwise, return the courses with the course_id 
    query = """
        SELECT
            c.id,
            c.name,
            c.description,
            t.name,
            c.schedule_time,
            l.name,
            c.price,
            c.capacity,  
            tr.id,
            l.id,
            DATEDIFF(CURRENT_DATE(),c.schedule_time),
            tr.last_name, 
            tr.first_name
        FROM fitness_classes c  
        JOIN location l ON c.location_id = l.id
        JOIN course_types t ON c.course_type_id = t.id
        JOIN trainers tr ON c.trainer_id = tr.id
    
    """
    dbconn = getCursor()
    try:
        if course_id is not None:
            query += " WHERE c.id = %s"
            dbconn.execute(query, (course_id,))
            return dbconn.fetchone()  # if it is a single course, return a single record
        else:
            query += "ORDER BY t.name, tr.last_name, tr.first_name, c.schedule_time"
            dbconn.execute(query, )
            return dbconn.fetchall()  # if it is all courses, return all the records            
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#created by Danfeng
def manager_get_member_info(course_id):
# get participant info from the database
    query = """
        SELECT
            m.profile_image,
            u.username,
            m.first_name,
            m.last_name,            
            b.is_attend,
            b.id
            

        FROM members m  
        JOIN bookings b ON m.id = b.member_id
        JOIN fitness_classes f ON f.id = b.fitness_class_id
        JOIN trainers tr ON f.trainer_id = tr.id
        JOIN users u ON m.user_id = u.id
        WHERE f.id = %s
        ORDER BY m.last_name, m.first_name
    """
    dbconn = getCursor()
    try:
        dbconn.execute(query, (course_id,))
        return dbconn.fetchall()          
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
# get location
def get_location():
    # get location info from the database
    query = """
        SELECT
            id,
            name,
            description
        FROM location
    """
    dbconn = getCursor()
    try:
        dbconn.execute(query)
        return dbconn.fetchall()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def manager_get_class_timetable(class_id=None):
    query = """
        SELECT
            c.id,
            c.name,
            c.description,
            t.name,
            c.schedule_time,
            l.name,
            0.00 as price,
            15 as capacity,
            t.id as trainer_id,
            l.id as location_id,
            tr.first_name,
            tr.last_name,
            tr.id as trainer_id,
            15 - IFNULL(b.booking_count, 0) as remaining_capacity
        FROM fitness_classes c  
        JOIN location l ON c.location_id = l.id
        JOIN course_types t ON c.course_type_id = t.id
        JOIN trainers tr ON c.trainer_id = tr.id
        LEFT JOIN (
            SELECT fitness_class_id, COUNT(*) as booking_count
            FROM bookings
            GROUP BY fitness_class_id
        ) b ON c.id = b.fitness_class_id
        WHERE c.course_type_id = 1
    """

    # If class_id is specified, filter by class_id
    if class_id is not None:
        query += " AND c.id = %s"
    else:
        query += " ORDER BY tr.last_name, tr.first_name, c.schedule_time"  # Order by trainer's name and schedule time

    dbconn = getCursor()
    try:
        if class_id is not None:
            dbconn.execute(query, (class_id,))
            return dbconn.fetchone()  # If it's a single class, return a single record
        else:
            dbconn.execute(query)
            return dbconn.fetchall()  # If it's all classes, return all the records
    except Exception as e:
        print(f"An error occurred: {e}")
        return None    