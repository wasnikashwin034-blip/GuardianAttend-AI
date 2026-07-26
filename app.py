import streamlit as st
import base64
import time
from streamlit_option_menu import option_menu

from components.login import show_login


# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="GuardianAttend AI",
    page_icon="🛡️",
    layout="wide"
)



# ==============================
# LOGIN SECURITY
# ==============================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False



if not st.session_state.logged_in:

    show_login()

    st.stop()



# ==============================
# CUSTOM CSS
# ==============================

st.markdown(
"""
<style>

.stApp {
    background-color:black;
    color:white;
}

section[data-testid="stSidebar"] {
    background-color:#050505;
}

</style>
""",
unsafe_allow_html=True
)



# ==============================
# INTRO ANIMATION
# ==============================

def show_intro():


    with open(
        "assets/logo.png",
        "rb"
    ) as f:

        logo = base64.b64encode(
            f.read()
        ).decode()



    html=f"""

<html>

<body style="
background:black;
height:100vh;
display:flex;
justify-content:center;
align-items:center;
flex-direction:column;
color:white;
">


<img src="data:image/png;base64,{logo}"
width="180">


<h1 style="
color:red;
letter-spacing:10px;
">

AI AVENGERS

</h1>


<h2>
GuardianAttend AI
</h2>


<p>
Smart Attendance Powered by Artificial Intelligence
</p>


</body>

</html>

"""


    st.html(html)




# ==============================
# INTRO ONLY ONCE
# ==============================


if "intro_done" not in st.session_state:

    st.session_state.intro_done=False



if not st.session_state.intro_done:


    show_intro()

    time.sleep(3)

    st.session_state.intro_done=True

    st.rerun()




# ==============================
# ROLE BASED MENU
# ==============================


role = st.session_state.role



if role == "Admin":


    menu = [

        "Dashboard",

        "Register Student",

        "Student List",

        "AI Attendance",

        "Analytics",

        "Reports",

        "User Management",

        "Fees Management"

    ]


    icons = [

        "speedometer",

        "person-plus",

        "people",

        "camera",

        "graph-up",

        "file-text",

        "person-gear",

        "cash-coin"

    ]



elif role == "Staff":


    menu = [

        "Dashboard",

        "AI Attendance",

        "Reports"

    ]


    icons = [

        "speedometer",

        "camera",

        "file-text"

    ]



else:


    menu = [

        "My Attendance",

        "My Report",

        "My Fees"

    ]


    icons = [

        "calendar-check",

        "file-text",

        "cash"

    ]





# ==============================
# SIDEBAR
# ==============================


with st.sidebar:


    st.image(
        "assets/logo.png",
        width=120
    )


    st.markdown(
    f"""

# 🛡️ AI AVENGERS

## GuardianAttend AI


👤 User:

{st.session_state.username}


🔐 Role:

{role}

"""
    )



    if st.button(
        "🚪 Logout"
    ):


        st.session_state.logged_in=False

        st.rerun()



    selected = option_menu(

        menu_title=None,

        options=menu,

        icons=icons,

        default_index=0

    )




# ==============================
# PAGE ROUTING
# ==============================


if selected=="Dashboard":

    from components.dashboard import show



elif selected=="Register Student":

    from components.register import show



elif selected=="Student List":

    from components.students import show



elif selected=="AI Attendance":

    from components.attendance import show



elif selected=="Analytics":

    from components.analytics import show



elif selected=="Reports":

    from components.reports import show



elif selected=="User Management":

    from components.users import show



elif selected=="Fees Management":

    from components.fees import show



elif selected=="My Attendance":

    from components.student_portal import show



elif selected=="My Report":

    from components.student_report import show



elif selected=="My Fees":

    from components.student_fees import show




# ==============================
# RUN PAGE
# ==============================

show()