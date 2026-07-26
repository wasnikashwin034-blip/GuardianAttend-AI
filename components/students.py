import streamlit as st
import sqlite3
import pandas as pd


def show():

    st.title("👥 Student Directory")

    st.subheader(
        "GuardianAttend AI | Registered Students"
    )

    st.divider()


    # Database connection

    conn = sqlite3.connect(
        "data/attendance.db"
    )


    students = pd.read_sql_query(
        "SELECT * FROM students",
        conn
    )


    conn.close()



    # Total students

    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "🎓 Total Students",
            len(students)
        )


    with col2:

        st.metric(
            "🛡️ Database",
            "Connected"
        )


    st.divider()



    if students.empty:

        st.warning(
            "No students registered yet"
        )


    else:


        # Search

        search = st.text_input(
            "🔍 Search Student"
        )


        if search:

            students = students[
                students["name"]
                .str.contains(
                    search,
                    case=False
                )
            ]



        st.subheader(
            "Student Profiles"
        )


        for index,row in students.iterrows():


            with st.container():

                col1,col2 = st.columns(
                    [1,3]
                )


                with col1:

                    folder_name = row["name"].replace(
                        " ",
                        "_"
                    )


                    image_path = (
                        f"images/{folder_name}/0.jpg"
                    )


                    try:

                        st.image(
                            image_path,
                            width=120
                        )

                    except:

                        st.write(
                            "No Image"
                        )


                with col2:

                    st.markdown(
                        f"""
                        ### 🎓 {row['name']}

                        **Roll No:** {row['roll']}

                        **Branch:** {row['branch']}

                        **AI Face Model:** Registered ✅

                        """
                    )


                st.divider()