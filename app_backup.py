import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime


st.set_page_config(
    page_title="VisionAttend AI",
    page_icon="🎓",
    layout="wide"
)


st.title("🎓 VisionAttend AI")
st.subheader("Smart AI Face Recognition Attendance System")


# Database connection

conn = sqlite3.connect(
    "data/attendance.db"
)


students = pd.read_sql_query(
    "SELECT * FROM students",
    conn
)


attendance = pd.read_sql_query(
    "SELECT * FROM attendance",
    conn
)


conn.close()



# Calculations

total_students = len(students)

total_records = len(attendance)


today = datetime.now().strftime(
    "%d-%m-%Y"
)


if not attendance.empty:

    present_today = len(
        attendance[
            attendance["date"] == today
        ]
    )

else:

    present_today = 0



if total_students > 0:

    attendance_rate = round(
        (present_today / total_students) * 100,
        2
    )

else:

    attendance_rate = 0



# Metrics

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "👨‍🎓 Total Students",
        total_students
    )


with col2:
    st.metric(
        "✅ Present Today",
        present_today
    )


with col3:
    st.metric(
        "📊 Attendance %",
        f"{attendance_rate}%"
    )


with col4:
    st.metric(
        "💾 Database",
        "Online"
    )


st.divider()



# Attendance Table

st.subheader(
    "📋 Attendance Records"
)


if not attendance.empty:

    st.dataframe(
        attendance,
        width="stretch"
    )

else:

    st.info(
        "No attendance records found"
    )



st.divider()



# Student Table

st.subheader(
    "👨‍🎓 Registered Students"
)


st.dataframe(
    students,
    width="stretch"
)



st.divider()



# Charts

col1, col2 = st.columns(2)



with col1:

    st.subheader(
        "🏢 Students by Branch"
    )

    if not students.empty:

        branch = students["branch"].value_counts()

        st.bar_chart(
            branch
        )



with col2:

    st.subheader(
        "📈 Attendance Trend"
    )

    if not attendance.empty:

        trend = attendance["date"].value_counts()

        st.line_chart(
            trend
        )



st.divider()



# Download

st.subheader(
    "📥 Download Attendance Report"
)


if not attendance.empty:

    csv = attendance.to_csv(
        index=False
    )


    st.download_button(
        "Download CSV",
        csv,
        "attendance_report.csv",
        "text/csv"
    )

else:

    st.warning(
        "No attendance data available"
    )