from flask import session, request, redirect, url_for, flash
from db_mamager import getCursor

#created by Danfeng
def trainer_get_session(user_id, session_id=None):
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
            tr.id,
            l.id,
            DATEDIFF(CURRENT_DATE(),c.schedule_time)
        FROM fitness_classes c  
        JOIN location l ON c.location_id = l.id
        JOIN course_types t ON c.course_type_id = t.id
        JOIN trainers tr ON c.trainer_id = tr.id
        WHERE c.course_type_id=2 AND tr.user_id=%s
    """
    dbconn = getCursor()
    try:
        if session_id is not None:
            query += " AND c.id = %s ORDER BY t.name, c.schedule_time"
            dbconn.execute(query, (user_id,session_id))
            return dbconn.fetchone()  # if it is a single session, return a single record
        else:
            query += "ORDER BY t.name, c.schedule_time"
            dbconn.execute(query,(user_id,) )
            return dbconn.fetchall()  # if it is all sessions, return all the records            
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    
#created by Danfeng
def trainer_get_course(user_id, course_id=None):
# get course info from the database, if course_id is None, return all the courses, otherwise, return the course with the course_id 
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
            DATEDIFF(CURRENT_DATE(),c.schedule_time)
        FROM fitness_classes c  
        JOIN location l ON c.location_id = l.id
        JOIN course_types t ON c.course_type_id = t.id
        JOIN trainers tr ON c.trainer_id = tr.id
        WHERE tr.user_id=%s
    """
    dbconn = getCursor()
    try:
        if course_id is not None:
            query += " AND c.id = %s ORDER BY t.name, c.schedule_time"
            dbconn.execute(query, (user_id,course_id))
            return dbconn.fetchone()  # if it is a single course, return a single record
        else:
            query += "ORDER BY t.name, c.schedule_time"
            dbconn.execute(query,(user_id,) )
            return dbconn.fetchall()  # for all the courses, return all the records            
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#created by Danfeng
def get_type_info():
# get type info from the database
    query = """
        SELECT
            id,
            name           
        FROM course_types 
    """
    dbconn = getCursor()
    try:
        dbconn.execute(query)
        return dbconn.fetchall()  # return all the types
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#created by Danfeng
def get_location_info():
# get type info from the database
    query = """
        SELECT
            id,
            name           
        FROM location 
    """
    dbconn = getCursor()
    try:
        dbconn.execute(query)
        return dbconn.fetchall()  # return all the locations
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def get_trainer_info(user_id=None):
# get trainer info from the database, if user_id is None, return all the trainers, otherwise, return the trainer with the user_id 
    query = """
        SELECT
            u.id,
            u.username,
            u.email,
            u.status,
            t.first_name,
            t.last_name,
            t.title,
            t.phone_number,
            t.profile_image,
            t.description,
            t.id
        FROM users u
        LEFT JOIN trainers t ON u.id = t.user_id
        WHERE u.role_id = 2
    """
    if user_id is not None:
        query += " AND u.id = %s;"

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

def trainer_get_session_info(user_id, session_id=None):
# get class info from the database, if class_id is None, return all the classes, otherwise, return the classes with the class_id 
    query = """
        SELECT
            c.id,
            c.name as course_name,
            c.description,
            t.name as course_type,
            c.schedule_time,
            l.name as location,
            c.price,
            c.capacity,  
            tr.user_id,
            m.id,
            m.first_name,
            m.last_name,
            m.position,
            m.phone_number,
            m.address,
            m.birth_date,
            m.health_info
        FROM fitness_classes c  
        JOIN location l ON c.location_id = l.id
        JOIN course_types t ON c.course_type_id = t.id
        JOIN trainers tr ON c.trainer_id = tr.id
        LEFT JOIN bookings b on c.id = b.fitness_class_id
        LEFT JOIN members m on b.member_id = m.id
        WHERE tr.user_id=%s and t.name = 'session'
    """
    dbconn = getCursor()
    try:
        if session_id is not None:
            query += " AND c.id = %s"
            dbconn.execute(query, (user_id,session_id))
            return dbconn.fetchone()  # if it is a single class, return a single record
        else:
            dbconn.execute(query,(user_id,) )
            return dbconn.fetchall()  # if it is all classes, return all the records            
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#created by Danfeng
def trainer_get_member_info(user_id, class_id):
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
        WHERE tr.user_id=%s AND f.id = %s
        ORDER BY m.last_name, m.first_name
    """
    dbconn = getCursor()
    try:
        dbconn.execute(query, (user_id,class_id))
        return dbconn.fetchall()          
    except Exception as e:
        print(f"An error occurred: {e}")
        return None