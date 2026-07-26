import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime


# ==============================
# LOAD ATTENDANCE DATA
# ==============================

def load_attendance():

    conn = sqlite3.connect(
        "data/attendance.db"
    )

    df = pd.read_sql_query(
        "SELECT * FROM attendance",
        conn
    )

    conn.close()

    return df



# ==============================
# REPORT PAGE
# ==============================

def show():

    st.title(
        "📄 GuardianAttend AI Reports"
    )

    st.subheader(
        "🛡️ AI AVENGERS | Attendance Intelligence Report"
    )

    st.divider()



    df = load_attendance()



    if df.empty:

        st.warning(
            "No attendance data available"
        )

        return



    # ==============================
    # STUDENT FILTER
    # ==============================


    students = sorted(
        df["name"].unique()
    )


    selected_student = st.selectbox(
        "🎓 Select Student",
        students
    )



    student_data = df[
        df["name"] == selected_student
    ]



    # ==============================
    # CALCULATION
    # ==============================


    total_attendance = len(
        student_data
    )


    total_days = df["date"].nunique()



    percentage = round(
        (total_attendance / total_days) * 100,
        2
    ) if total_days else 0



    # ==============================
    # REPORT CARDS
    # ==============================


    col1,col2,col3 = st.columns(3)


    with col1:

        st.metric(
            "📅 Total Days",
            total_days
        )


    with col2:

        st.metric(
            "✅ Present",
            total_attendance
        )


    with col3:

        st.metric(
            "📊 Attendance %",
            f"{percentage}%"
        )



    st.divider()



    # ==============================
    # TABLE
    # ==============================


    st.subheader(
        "📝 Attendance History"
    )


    st.dataframe(
        student_data,
        width="stretch"
    )



    st.divider()



    # ==============================
    # DOWNLOAD CSV
    # ==============================


    csv = student_data.to_csv(
        index=False
    )


    st.download_button(

        label="⬇️ Download CSV Report",

        data=csv,

        file_name=
        f"{selected_student}_attendance.csv",

        mime="text/csv"

    )



    st.divider()



    # ==============================
    # DAILY ANALYTICS
    # ==============================


    st.subheader(
        "📈 Attendance Trend"
    )


    chart = (

        student_data
        .groupby("date")
        ["name"]
        .count()

    )


    st.line_chart(
        chart
    )



    st.caption(
        f"Generated on {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    )