import streamlit as st
import streamlit.components.v1 as components
import base64
import time

from streamlit_option_menu import option_menu



# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="GuardianAttend AI",
    page_icon="🛡️",
    layout="wide"
)



# ==============================
# INTRO ANIMATION
# ==============================

def show_intro():

    with open("assets/logo.png","rb") as f:

        logo = base64.b64encode(
            f.read()
        ).decode()



    components.html(

f"""

<html>

<head>

<style>


html,body{{

margin:0;

padding:0;

background:black;

width:100%;

height:100%;

overflow:hidden;

}}



.intro{{

height:100vh;

width:100vw;

background:black;

display:flex;

justify-content:center;

align-items:center;

flex-direction:column;

}}



.logo{{

width:180px;

animation:

zoom 2s ease,

glow 1.5s infinite alternate;

}}



.company{{

margin-top:25px;

font-size:32px;

font-weight:800;

font-family:Arial;

letter-spacing:10px;

color:#ff3030;

opacity:0;

animation:

fade 2s ease forwards;

}}



.product{{

margin-top:20px;

font-size:55px;

font-weight:900;

font-family:Arial;

letter-spacing:5px;

color:white;

opacity:0;

animation:

product 2s ease 1s forwards;

}}



.tagline{{

margin-top:20px;

font-size:22px;

font-family:Arial;

color:#cccccc;

opacity:0;

animation:

fade 2s ease 2s forwards;

}}




@keyframes zoom{{


0%{{

transform:scale(0);

opacity:0;

}}


100%{{

transform:scale(1);

opacity:1;

}}


}}



@keyframes glow{{


from{{

filter:drop-shadow(0 0 5px red);

}}


to{{

filter:drop-shadow(0 0 45px red);

}}


}}



@keyframes fade{{


from{{

opacity:0;

transform:translateY(-30px);

}}


to{{

opacity:1;

transform:translateY(0);

}}


}}



@keyframes product{{


from{{

opacity:0;

letter-spacing:30px;

}}


to{{

opacity:1;

letter-spacing:5px;

}}


}}



</style>


</head>


<body>


<div class="intro">


<img

class="logo"

src="data:image/png;base64,{logo}">



<div class="company">

AI AVENGERS

</div>



<div class="product">

GuardianAttend AI

</div>



<div class="tagline">

Smart Attendance Powered by Artificial Intelligence

</div>



</div>


</body>


</html>

""",

height=900,

width=1600

)





# ==============================
# PLAY INTRO ONCE
# ==============================


if "intro_done" not in st.session_state:

    st.session_state.intro_done=False



if not st.session_state.intro_done:


    show_intro()

    time.sleep(5)


    st.session_state.intro_done=True


    st.rerun()




# ==============================
# SIDEBAR
# ==============================


with st.sidebar:


    st.image(
        "assets/logo.png",
        width=120
    )


    st.markdown(
        """
        # AI AVENGERS
        
        ### GuardianAttend AI
        
        Smart Attendance System
        """
    )



    selected = option_menu(

        menu_title=None,

        options=[

            "Dashboard",

            "Register Student",

            "Student List",

            "AI Attendance",

            "Analytics",

            "Reports"

        ],


        icons=[

            "speedometer",

            "person-plus",

            "people",

            "camera",

            "graph-up",

            "file-text"

        ],


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




show()