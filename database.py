import sqlite3


DATABASE = "guardianattend.db"



# ==========================
# CREATE DATABASE
# ==========================

def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()



    # STUDENTS TABLE

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS students (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        roll_no TEXT,

        department TEXT,

        image_path TEXT

    )

    """)




    # ATTENDANCE TABLE

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS attendance (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        student_id INTEGER,

        name TEXT,

        date TEXT,

        time TEXT,

        status TEXT,

        confidence REAL,


        FOREIGN KEY(student_id)

        REFERENCES students(id)

    )

    """)



    conn.commit()

    conn.close()





# ==========================
# INSERT STUDENT
# ==========================

def add_student(
        name,
        roll_no,
        department,
        image_path
):


    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()



    cursor.execute(

    """

    INSERT INTO students

    (name,roll_no,department,image_path)

    VALUES (?,?,?,?)

    """,

    (
        name,
        roll_no,
        department,
        image_path
    )


    )


    conn.commit()

    conn.close()






# ==========================
# ADD ATTENDANCE
# ==========================

def add_attendance(

        student_id,

        name,

        date,

        time,

        status,

        confidence

):


    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()



    cursor.execute(

    """

    INSERT INTO attendance

    (

    student_id,

    name,

    date,

    time,

    status,

    confidence

    )

    VALUES (?,?,?,?,?,?)

    """,

    (

        student_id,

        name,

        date,

        time,

        status,

        confidence

    )


    )


    conn.commit()

    conn.close()





# ==========================
# GET DATA
# ==========================

def get_students():


    conn = sqlite3.connect(DATABASE)


    data = conn.execute(

        "SELECT * FROM students"

    ).fetchall()


    conn.close()


    return data





def get_attendance():


    conn = sqlite3.connect(DATABASE)


    data = conn.execute(

        "SELECT * FROM attendance"

    ).fetchall()


    conn.close()


    return data