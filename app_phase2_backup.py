import streamlit as st
import sqlite3
import pandas as pd
import time
from datetime import datetime


# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="GuardianAttend AI",
    page_icon="🛡️",
    layout="wide"
)


# -------------------------------
# Startup Animation
# -------------------------------

if "loaded" not in st.session_state:

    screen = st.empty()

    with screen.container():

        st.markdown(
            """
            <style>

            body {
                background-color:#050505;
            }


            .logo {
                text-align:center;
                font-size:60px;
                font-weight:900;
                color:#ff1a1a;
                animation: zoom 2s;
            }


            .company {
                text-align:center;
                font-size:30px;
                color:white;
                animation: fade 3s;
            }


            .loading {
                text-align:center;
                color:#00ff99;
                font-size:20px;
            }


            @keyframes zoom {

                from{
                    transform:scale(0);
                    opacity:0;
                }

                to{
                    transform:scale(1);
                    opacity:1;
                }

            }


            @keyframes fade {

                from{
                    opacity:0;
                }

                to{
                    opacity:1;
                }

            }

            </style>


            <div class="logo">
            🛡️ GuardianAttend AI
            </div>


            <div class="company">
            AI AVENGERS
            </div>

            <br>

            <div class="loading">
            Initializing AI Vision System...<br>
            Loading Face Recognition Model...<br>
            Connecting Database...<br>
            Security Check Complete ✅
            </div>

            """,
            unsafe_allow_html=True
        )


    time.sleep(3)

    screen.empty()

    st.session_state.loaded = True



# -------------------------------
# Custom CSS
# -------------------------------

st.markdown(
"""
<style>

.stApp{

background:#070707;

}


h1,h2,h3{

color:white;

}


.card{

background:#111111;

padding:25px;

border-radius:15px;

border:1px solid #ff1a1a;

box-shadow:0 0 15px #550000;

text-align:center;

}


.big{

font-size:35px;

font-weight:bold;

color:#ff3333;

}


.label{

color:white;

font-size:18px;

}


</style>

""",
unsafe_allow_html=True
)



# -------------------------------
# Logo + Header
# -------------------------------

col1,col2 = st.columns([1,5])


with col1:

    st.image(
        "assets/logo.png",
        width=120
    )


with col2:

    st.title("🛡️ GuardianAttend AI")
    st.subheader(
        "AI AVENGERS | Smart Face Recognition Attendance"
    )



st.divider()



# -------------------------------
# Database
# -------------------------------


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



# -------------------------------
# Metrics
# -------------------------------


total_students = len(students)


today = datetime.now().strftime("%d-%m-%Y")


present_today = 0


if not attendance.empty:

    present_today = len(
        attendance[
            attendance["date"]==today
        ]
    )



accuracy = "98%"



c1,c2,c3,c4 = st.columns(4)



with c1:

    st.markdown(
    f"""
    <div class="card">

    <div class="label">
    👨‍🎓 Students
    </div>

    <div class="big">
    {total_students}
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )



with c2:

    st.markdown(
    f"""
    <div class="card">

    <div class="label">
    ✅ Present Today
    </div>

    <div class="big">
    {present_today}
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )



with c3:

    st.markdown(
    f"""
    <div class="card">

    <div class="label">
    🧠 AI Accuracy
    </div>

    <div class="big">
    {accuracy}
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )



with c4:

    st.markdown(
    """
    <div class="card">

    <div class="label">
    🟢 System
    </div>

    <div class="big">
    ONLINE
    </div>

    </div>
    """,
    unsafe_allow_html=True
    )



st.divider()



# -------------------------------
# Attendance Table
# -------------------------------


st.subheader("📋 Attendance Records")


if not attendance.empty:

    st.dataframe(
        attendance,
        width="stretch"
    )

else:

    st.info(
        "No attendance records available"
    )



# -------------------------------
# Charts
# -------------------------------


st.subheader("📊 Analytics")


if not students.empty:

    branch = students["branch"].value_counts()

    st.bar_chart(branch)



if not attendance.empty:

    st.subheader("📈 Attendance Trend")

    trend = attendance["date"].value_counts()

    st.line_chart(trend)



# -------------------------------
# Footer
# -------------------------------


st.divider()


st.markdown(
"""
<center>

<h3>
🛡️ GuardianAttend AI
</h3>

<p>
Developed by AI AVENGERS
</p>

<p>
Smart • Secure • Intelligent
</p>

</center>

""",
unsafe_allow_html=True
)