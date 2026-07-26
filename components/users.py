import streamlit as st
import sqlite3
import hashlib
from datetime import datetime


DATABASE = "data/attendance.db"



# ==============================
# PASSWORD HASH
# ==============================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()



# ==============================
# ADD USER
# ==============================

def add_user(username, password, role, name, email):

    conn = sqlite3.connect(
        DATABASE
    )

    cursor = conn.cursor()


    try:

        cursor.execute(
            """
            INSERT INTO users
            (username,password,role,name,email,created_date)

            VALUES(?,?,?,?,?,?)

            """,

            (
                username,
                hash_password(password),
                role,
                name,
                email,
                datetime.now().strftime("%Y-%m-%d")
            )
        )


        conn.commit()

        result = True


    except sqlite3.IntegrityError:

        result = False



    conn.close()


    return result




# ==============================
# LOAD USERS
# ==============================

def load_users():

    conn = sqlite3.connect(
        DATABASE
    )


    users = conn.execute(
        """
        SELECT id,username,role,name,email,created_date
        FROM users
        """
    ).fetchall()


    conn.close()


    return users




# ==============================
# DELETE USER
# ==============================

def delete_user(user_id):

    conn = sqlite3.connect(
        DATABASE
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        DELETE FROM users
        WHERE id=?
        """,
        (user_id,)
    )


    conn.commit()

    conn.close()




# ==============================
# USER MANAGEMENT PAGE
# ==============================


def show():


    st.title(
        "👥 User Management"
    )


    st.subheader(
        "🛡️ AI AVENGERS | Admin Control Panel"
    )


    st.divider()



    # ==============================
    # CREATE USER
    # ==============================


    st.subheader(
        "➕ Create New User"
    )


    col1,col2 = st.columns(2)



    with col1:

        username = st.text_input(
            "Username"
        )

        name = st.text_input(
            "Full Name"
        )

        email = st.text_input(
            "Email"
        )


    with col2:

        password = st.text_input(
            "Password",
            type="password"
        )


        role = st.selectbox(
            "Role",
            [
                "Admin",
                "Staff",
                "Student"
            ]
        )



    if st.button(
        "Create User"
    ):


        if add_user(
            username,
            password,
            role,
            name,
            email
        ):

            st.success(
                "User created successfully"
            )

            st.rerun()


        else:

            st.error(
                "Username already exists"
            )



    st.divider()



    # ==============================
    # USER LIST
    # ==============================


    st.subheader(
        "📋 Registered Users"
    )


    users = load_users()



    for user in users:


        col1,col2 = st.columns(
            [4,1]
        )


        with col1:

            st.write(
                f"""
                **ID:** {user[0]}

                **Username:** {user[1]}

                **Role:** {user[2]}

                **Name:** {user[3]}

                **Email:** {user[4]}

                """
            )


        with col2:


            if st.button(
                "🗑️ Delete",
                key=user[0]
            ):

                delete_user(
                    user[0]
                )

                st.rerun()


        st.divider()