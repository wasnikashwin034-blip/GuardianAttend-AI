import streamlit as st
import pandas as pd
import os
from datetime import datetime


def show():

    st.title("🛡️ GuardianAttend AI Dashboard")

    st.subheader(
        "AI Powered Smart Attendance Management System"
    )

    st.divider()


    # ==========================
    # LOAD ATTENDANCE DATA
    # ==========================

    file = "attendance.csv"


    if os.path.exists(file) and os.path.getsize(file) > 0:

        df = pd.read_csv(
            file,
            header=None,
            names=[
                "Name",
                "Time",
                "Date"
            ]
        )


    else:

        df = pd.DataFrame(
            columns=[
                "Name",
                "Time",
                "Date"
            ]
        )



    # ==========================
    # CALCULATIONS
    # ==========================


    total_students = df["Name"].nunique()



    today = datetime.now().strftime(
        "%d-%m-%Y"
    )


    today_data = df[
        df["Date"] == today
    ]



    present_today = today_data["Name"].nunique()



    absent_today = max(
        total_students - present_today,
        0
    )



    if total_students > 0:

        attendance_percentage = round(
            (present_today / total_students) * 100,
            2
        )

    else:

        attendance_percentage = 0



    # ==========================
    # CARDS
    # ==========================


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
            "❌ Absent Today",
            absent_today
        )


    with col4:

        st.metric(
            "📊 Attendance %",
            f"{attendance_percentage}%"
        )



    st.divider()



    # ==========================
    # ATTENDANCE GRAPH
    # ==========================


    st.subheader(
        "📈 Attendance Trend"
    )


    if not df.empty:


        graph = (
            df.groupby("Date")
            ["Name"]
            .count()
        )


        st.line_chart(graph)


    else:

        st.info(
            "No attendance data available"
        )



    st.divider()



    # ==========================
    # RECENT RECORDS
    # ==========================


    st.subheader(
        "📝 Recent Attendance"
    )


    if not df.empty:


        st.dataframe(
            df.tail(10),
            use_container_width=True
        )


    else:

        st.warning(
            "No attendance records found"
        )