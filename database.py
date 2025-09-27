import sqlite3
import shutil

DB_NAME = "school.db"

def init_db():
    """This initialize the SQLite database. it creates tables for students, instructors, courses, and registrations
    if they dont already exist.

    :return: None
    :rtype: None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("create table if not exists students (id TEXT PRIMARY KEY, name TEXT, age INTEGER, email TEXT)")
    c.execute("create table if not exists instructors (id TEXT PRIMARY KEY, name TEXT, age INTEGER, email TEXT)")
    c.execute("""create table if not exists courses (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    instructor_id TEXT,
                    foreign key(instructor_id) references instructors(id)
                )""")
    c.execute("""create table if not exists registrations (
                    student_id TEXT,
                    course_id TEXT,
                    primary key(student_id, course_id),
                    foreign key(student_id) references students(id),
                    foreign key(course_id) references courses(id)
                )""")
    conn.commit()
    conn.close()


def add_student(sid, name, age, email):
    """Add or update a student.

    :param sid: Student ID (unique).
    :type sid: str
    :param name: Full name of student.
    :type name: str
    :param age: Age of student.
    :type age: int
    :param email: Email address of student.
    :type email: str
    :raises sqlite3.Error: If database operation fails.
    :return: None
    :rtype: None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("insert or replace into students values (?, ?, ?, ?)", (sid, name, age, email))
    except Exception as e:
        print("could not add student:", e)
    conn.commit()
    conn.close()

def fetch_students():
    """Retrieve all students.

    :return: List of student records as tuples (id, name, age, email).
    :rtype: list/tuple
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("select * from students")
    rows = c.fetchall()
    conn.close()
    return rows

def update_student(sid, name, age, email):
    """Update student information.

    :param sid: Student ID.
    :type sid: str
    :param name: Updated name.
    :type name: str
    :param age: Updated age.
    :type age: int
    :param email: Updated email.
    :type email: str
    :return: None
    :rtype: None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("update students set name=?, age=?, email=? where id=?", (name, age, email, sid))
    conn.commit()
    conn.close()

def remove_student(sid):
    """this removes a student and clean up registrations.

    :param sid: Student ID to delete.
    :type sid: str
    :return: None
    :rtype: None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("delete from students where id=?", (sid,))
    # also cleanup registrations
    c.execute("delete from registrations where student_id=?", (sid,))
    conn.commit(); conn.close()

def add_instructor(iid, name, age, email):
    """This one add or update an instructor.

    :param iid: Instructor ID.
    :type iid: str
    :param name: Instructor name.
    :type name: str
    :param age: Instructor age.
    :type age: int
    :param email: Instructor email.
    :type email: str
    :return: None
    :rtype: None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("insert or replace into instructors values (?, ?, ?, ?)", (iid, name, age, email))
    conn.commit(); conn.close()

def get_instructors():  
    """Retrieve all instructors.

    :return: List of instructor records as tuples (id, name, age, email).
    :rtype: list/tuplee
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("select * from instructors")
    result = c.fetchall()
    conn.close()
    return result

def update_instructor(iid, name, age, email):
    """this function update instructor details.

    :param iid: Instructor ID.
    :type iid: str
    :param name: Updated name.
    :type name: str
    :param age: Updated age.
    :type age: int
    :param email: Updated email.
    :type email: str
    :return: None
    :rtype: None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("update instructors set name=?, age=?, email=? where id=?", (name, age, email, iid))
    conn.commit()
    conn.close()

def remove_instructor(iid):
    """this delete an instructor and unassign their courses.

    :param iid: Instructor ID.
    :type iid: str
    :return: None
    :rtype: None
    """

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("delete from instructors where id=?", (iid,))
    # unassign courses too
    c.execute("update courses set instructor_id=null where instructor_id=?", (iid,))
    conn.commit(); conn.close()

def add_course(cid, name, instructor_id=None):
    """this one add or update a course.

    :param cid: Course ID.
    :type cid: str
    :param name: Course name.
    :type name: str
    :param instructor_id: Instructor assigned to the course, defaults to None.
    :type instructor_id: str, optional
    :return: None
    :rtype: None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("insert or replace into courses values (?, ?, ?)", (cid, name, instructor_id))
    conn.commit()
    conn.close()

def list_courses():  
    """this for retrieve all courses.

    :return: List of course records as tuples (id, name, instructor_id).
    :rtype: list/tuple
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("select * from courses")
    rows = c.fetchall()
    print("[debug] fetched", len(rows), "courses")  
    conn.close()
    return rows

def update_course(cid, name, instructor_id=None):
    """this update course details.

    :param cid: Course ID.
    :type cid: str
    :param name: Updated course name.
    :type name: str
    :param instructor_id: Updated instructor ID, defaults to None.
    :type instructor_id: str, optional
    :return: None
    :rtype: None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("update courses set name=?, instructor_id=? where id=?", (name, instructor_id, cid))
    conn.commit(); conn.close()

def delete_course(cid):
    """for delete course and clean up registrations.

    :param cid: Course ID.
    :type cid: str
    :return: None
    :rtype: None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("delete from courses where id=?", (cid,))
    # cleanup course regs
    c.execute("delete from registrations where course_id=?", (cid,))
    conn.commit()
    conn.close()
def register_student(sid, cid):
    """this register a student in a course.

    :param sid: Student ID.
    :type sid: str
    :param cid: Course ID.
    :type cid: str
    :return: None
    :rtype: None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("insert or replace into registrations values (?, ?)", (sid, cid))
    conn.commit(); conn.close()

def get_registrations():
    """Retrieves all registrations.

    :return: List of (student_id, course_id) tuples.
    :rtype: list/tuple
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("select * from registrations")
    rows = c.fetchall()
    conn.close()
    return rows

def delete_registration(sid, cid):
    """Deletes a student-course registration.

    :param sid: Student ID.
    :type sid: str
    :param cid: Course ID.
    :type cid: str
    :return: None
    :rtype: None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("delete from registrations where student_id=? and course_id=?", (sid, cid))
    conn.commit(); conn.close()

def backup_db():
    """this create a backup of the database.

    Copies ``school.db`` into a file named ``school_backup.db``.

    :return: Status message confirming the backup.
    :rtype: str
    """
    shutil.copy(DB_NAME, "school_backup.db")
    return "backup created in school_backup.db"
