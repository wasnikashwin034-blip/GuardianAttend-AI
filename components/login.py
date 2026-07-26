import streamlit as st
import sqlite3
import hashlib
from datetime import datetime


DATABASE = "data/attendance.db"



# ==============================
# CREATE USER TABLE
# ==============================

def create_user_table():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password TEXT,

        role TEXT,

        created_date TEXT

        )
        """
    )


    conn.commit()

    conn.close()



# ==============================
# PASSWORD HASH
# ==============================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()



# ==============================
# CREATE DEFAULT ADMIN
# ==============================

def create_admin():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    password = hash_password(
        "admin123"
    )


    try:

        cursor.execute(
            """
            INSERT INTO users
            (username,password,role,created_date)

            VALUES(?,?,?,?)

            """,

            (
                "admin",
                password,
                "Admin",
                datetime.now().strftime("%Y-%m-%d")
            )
        )


        conn.commit()


    except sqlite3.IntegrityError:

        pass



    conn.close()



# ==============================
# LOGIN CHECK
# ==============================

def verify_login(username,password):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()


    cursor.execute(

        """
        SELECT username,role
        FROM users
        WHERE username=? AND password=?

        """,

        (
            username,
            hash_password(password)
        )

    )


    user = cursor.fetchone()


    conn.close()


    return user




# ==============================
# LOGIN PAGE
# ==============================


def show_login():


    create_user_table()

    create_admin()



    st.title(
        "🔐 GuardianAttend AI Login"
    )


    st.subheader(
        "🛡️ AI AVENGERS Security System"
    )



    st.divider()



    username = st.text_input(
        "Username"
    )


    password = st.text_input(
        "Password",
        type="password"
    )



    if st.button(
        "Login"
    ):


        user = verify_login(

            username,

            password

        )



        if user:


            st.session_state.logged_in=True

            st.session_state.username=user[0]

            st.session_state.role=user[1]


            st.success(
                "Login Successful"
            )


            st.rerun()



        else:


            st.error(
                "Invalid Username or Password"
            )