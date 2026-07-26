import streamlit as st
import sqlite3
import pandas as pd
import os


# ==============================
# DATABASE
# ==============================

def load_students():

    conn = sqlite3.connect(
        "data/attendance.db"
    )

    students = pd.read_sql_query(
        "SELECT * FROM students",
        conn
    )

    conn.close()

    return students



# ==============================
# ATTENDANCE COUNT
# ==============================

def get_attendance(name):

    try:

        conn = sqlite3.connect(
            "data/attendance.db"
        )


        result = pd.read_sql_query(
            """
            SELECT COUNT(*) as total
            FROM attendance
            WHERE name=?
            """,
            conn,
            params=(name,)
        )


        conn.close()


        return result["total"][0]


    except:

        return 0




# ==============================
# STUDENT DIRECTORY
# ==============================


def show():


    st.title(
        "👨‍🎓 Student Management"
    )


    st.subheader(
        "🛡️ AI AVENGERS | GuardianAttend AI"
    )


    st.divider()



    students = load_students()



    # ==============================
    # TOP CARDS
    # ==============================


    col1,col2,col3 = st.columns(3)



    with col1:

        st.metric(
            "🎓 Total Students",
            len(students)
        )



    with col2:

        st.metric(
            "🤖 AI Models",
            len(students)
        )



    with col3:

        st.metric(
            "🗄️ Database",
            "Connected"
        )



    st.divider()



    if students.empty:


        st.warning(
            "No students registered"
        )

        return




    # ==============================
    # SEARCH
    # ==============================


    search = st.text_input(
        "🔍 Search Student"
    )



    if search:


        students = students[
            students["name"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]



    st.subheader(
        "📋 Student Profiles"
    )



    # ==============================
    # PROFILE CARDS
    # ==============================


    for _,row in students.iterrows():



        name = row["name"]



        attendance = get_attendance(
            name
        )



        with st.container():


            col1,col2,col3 = st.columns(
                [1,2,1]
            )



            # PHOTO

            with col1:


                folder = name.replace(
                    " ",
                    "_"
                )


                image = (
                    f"images/{folder}/1.jpg"
                )


                if os.path.exists(image):

                    st.image(
                        image,
                        width=120
                    )

                else:

                    st.info(
                        "No Photo"
                    )



            # DETAILS

            with col2:


                st.markdown(
                    f"""

### 🎓 {name}


**Roll Number:** {row['roll']}


**Branch:** {row['branch']}


**Face Recognition:** ✅ Active


**Attendance Count:** {attendance}


"""
                )



            # STATUS

            with col3:


                if attendance > 0:

                    st.success(
                        "ACTIVE"
                    )

                else:

                    st.warning(
                        "NEW"
                    )



            st.divider()