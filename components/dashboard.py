import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime


# ==============================
# DATABASE CONNECTION
# ==============================

def load_attendance():

    try:

        conn = sqlite3.connect(
            "data/attendance.db"
        )

        df = pd.read_sql_query(
            "SELECT * FROM attendance",
            conn
        )

        conn.close()

        return df


    except Exception:

        return pd.DataFrame()



# ==============================
# DASHBOARD
# ==============================


def show():

    st.title("🛡️ GuardianAttend AI")

    st.subheader(
        "AI AVENGERS | Smart Attendance Intelligence Dashboard"
    )


    st.divider()


    # LOAD DATA

    df = load_attendance()



    if df.empty:

        st.warning(
            "No attendance records available"
        )

        return



    # ==============================
    # DATA PROCESSING
    # ==============================


    total_students = df["name"].nunique()



    today = datetime.now().strftime(
        "%Y-%m-%d"
    )



    today_data = df[
        df["date"] == today
    ]



    present_today = today_data["name"].nunique()



    attendance_rate = round(
        (present_today / total_students) * 100,
        2
    ) if total_students else 0



    total_records = len(df)



    # ==============================
    # STAT CARDS
    # ==============================


    col1,col2,col3,col4 = st.columns(4)



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
            "📌 Total Attendance",
            total_records
        )



    with col4:

        st.metric(
            "📊 Attendance Rate",
            f"{attendance_rate}%"
        )



    st.divider()



    # ==============================
    # ANALYTICS
    # ==============================


    st.subheader(
        "📈 Attendance Analytics"
    )



    daily = (

        df.groupby("date")
        ["name"]
        .count()

    )



    st.line_chart(
        daily
    )



    st.divider()



    # ==============================
    # TOP STUDENTS
    # ==============================


    st.subheader(
        "🏆 Student Attendance Ranking"
    )



    ranking = (

        df.groupby("name")
        .size()
        .sort_values(
            ascending=False
        )
        .reset_index()

    )


    ranking.columns = [

        "Student",

        "Attendance Count"

    ]



    st.dataframe(
        ranking,
        width="stretch"
    )



    st.divider()



    # ==============================
    # RECENT ATTENDANCE
    # ==============================


    st.subheader(
        "📝 Recent Attendance Records"
    )



    recent = df.tail(10)



    st.dataframe(

        recent,

        width="stretch"

    )