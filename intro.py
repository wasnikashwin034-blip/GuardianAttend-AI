import streamlit as st
import time


def show_intro():


    placeholder = st.empty()


    with placeholder.container():

        st.markdown(
        """
        <style>

        body{

            background:black;

        }


        .intro{

            height:100vh;

            display:flex;

            flex-direction:column;

            justify-content:center;

            align-items:center;

            color:white;

            animation:fade 3s;

        }


        .logo{

            width:180px;

            animation:
            zoom 2s ease-in-out;

        }


        .title{

            font-size:55px;

            font-weight:900;

            color:#ff1f1f;

            letter-spacing:4px;

            animation:
            glow 2s infinite alternate;

        }


        .tag{

            font-size:20px;

            color:#bbbbbb;

        }



        @keyframes zoom{

            from{

                transform:scale(0);

                opacity:0;

            }

            to{

                transform:scale(1);

                opacity:1;

            }

        }



        @keyframes glow{

            from{

                text-shadow:
                0 0 10px red;

            }


            to{

                text-shadow:
                0 0 40px red;

            }

        }



        @keyframes fade{

            from{

                opacity:0;

            }

            to{

                opacity:1;

            }

        }


        </style>



        <div class="intro">


        <img class="logo"
        src="data:image/png;base64,{{logo}}">


        <div class="title">

        GuardianAttend AI

        </div>


        <div class="tag">

        AI Powered Smart Attendance System

        </div>


        <br>


        <div>

        Powered by AI AVENGERS

        </div>


        </div>

        """,

        unsafe_allow_html=True

        )


    time.sleep(4)

    placeholder.empty()