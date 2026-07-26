import streamlit as st
import pandas as pd
import os


def show():

    st.title("📊 AI Attendance Analytics")

    st.write(
        "GuardianAttend AI - Attendance Analysis Dashboard"
    )


    file_path = "attendance.csv"


    # Check file exists

    if not os.path.exists(file_path):

        st.warning(
            "Attendance file not found"
        )

        return



    try:

        # Your CSV has no header
        df = pd.read_csv(
            file_path,
            header=None,
            names=[
                "Name",
                "Time",
                "Date"
            ]
        )


    except Exception as e:

        st.error(
            f"Unable to read attendance file: {e}"
        )

        return



    if df.empty:

        st.warning(
            "No attendance records available"
        )

        return



    # Remove empty rows

    df.dropna(
        inplace=True
    )


    # -------------------------
    # Statistics Cards
    # -------------------------

    total_records = len(df)

    total_students = df["Name"].nunique()



    col1, col2, col3 = st.columns(3)



    with col1:

        st.metric(
            "Total Attendance",
            total_records
        )



    with col2:

        st.metric(
            "Total Students",
            total_students
        )



    with col3:

        today = df["Date"].iloc[-1]

        st.metric(
            "Latest Date",
            today
        )



    st.divider()



    # -------------------------
    # Attendance Table
    # -------------------------

    st.subheader(
        "📋 Attendance Records"
    )


    st.dataframe(
        df,
        use_container_width=True
    )



    st.divider()



    # -------------------------
    # Student Attendance Count
    # -------------------------

    st.subheader(
        "👨‍🎓 Student Attendance Count"
    )


    attendance_count = (
        df["Name"]
        .value_counts()
    )


    st.bar_chart(
        attendance_count
    )



    st.divider()



    # -------------------------
    # Recent Attendance
    # -------------------------

    st.subheader(
        "🕒 Recent Attendance"
    )


    st.dataframe(
        df.tail(10),
        use_container_width=True
    )