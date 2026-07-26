import streamlit as st
import sqlite3
import pandas as pd



DATABASE = "data/attendance.db"



# ==============================
# LOAD STUDENT DATA
# ==============================

def get_student_data(username):

    conn = sqlite3.connect(
        DATABASE
    )


    student = pd.read_sql_query(

        """
        SELECT *
        FROM students
        WHERE name=?

        """,

        conn,

        params=(username,)

    )


    conn.close()


    return student




# ==============================
# ATTENDANCE DATA
# ==============================

def get_attendance(name):

    conn = sqlite3.connect(
        DATABASE
    )


    attendance = pd.read_sql_query(

        """
        SELECT *
        FROM attendance
        WHERE name=?

        ORDER BY date DESC

        """,

        conn,

        params=(name,)

    )


    conn.close()


    return attendance




# ==============================
# STUDENT PORTAL
# ==============================


def show():


    st.title(
        "🎓 Student Portal"
    )


    st.subheader(
        "🛡️ GuardianAttend AI | Personal Dashboard"
    )


    st.divider()



    username = st.session_state.username



    student = get_student_data(
        username
    )



    if student.empty:


        st.warning(
            "Student profile not found"
        )

        return



    name = student.iloc[0]["name"]



    attendance = get_attendance(
        name
    )



    # ==============================
    # CALCULATIONS
    # ==============================


    total_days = len(attendance)


    present = len(

        attendance[
            attendance["status"]=="Present"
        ]

    )


    absent = total_days - present



    percentage = 0


    if total_days > 0:

        percentage = round(

            (present / total_days) * 100,

            2

        )



    # ==============================
    # PROFILE
    # ==============================


    st.markdown(
    f"""

## 👤 {name}


**Role:** Student


**Branch:** {student.iloc[0]['branch']}


**Roll No:** {student.iloc[0]['roll']}


"""
    )



    st.divider()



    # ==============================
    # CARDS
    # ==============================


    col1,col2,col3,col4 = st.columns(4)



    with col1:

        st.metric(
            "📅 Total Classes",
            total_days
        )


    with col2:

        st.metric(
            "✅ Present",
            present
        )


    with col3:

        st.metric(
            "❌ Absent",
            absent
        )


    with col4:

        st.metric(
            "📊 Attendance %",
            f"{percentage}%"
        )



    st.divider()



    # ==============================
    # ATTENDANCE HISTORY
    # ==============================


    st.subheader(
        "📋 My Attendance History"
    )



    if not attendance.empty:


        st.dataframe(

            attendance,

            width="stretch"

        )


        st.subheader(
            "📈 Attendance Trend"
        )


        chart = (

            attendance
            .groupby("date")
            ["name"]
            .count()

        )


        st.line_chart(
            chart
        )


    else:


        st.info(
            "No attendance records available"
        )