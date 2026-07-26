import streamlit as st
import cv2
import os
import subprocess

from database import add_student



# ==========================
# TRAIN MODEL FUNCTION
# ==========================

def train_model():

    try:

        result = subprocess.run(
            ["python", "train_new.py"],
            capture_output=True,
            text=True
        )


        if result.returncode == 0:

            return True, result.stdout


        else:

            return False, result.stderr


    except Exception as e:

        return False, str(e)




# ==========================
# REGISTER PAGE
# ==========================

def show():

    st.title("👤 Register New Student")


    st.write(
        "Capture face images and save student data"
    )



    # Student Details

    name = st.text_input(
        "Enter Student Name"
    )


    roll_no = st.text_input(
        "Enter Roll Number"
    )


    department = st.text_input(
        "Enter Department"
    )



    start = st.button(
        "📷 Start Face Capture"
    )



    if start:


        if name == "":

            st.error(
                "Please enter student name"
            )

            return



        folder = f"images/{name}"

        os.makedirs(
            folder,
            exist_ok=True
        )



        camera = cv2.VideoCapture(1)



        detector = cv2.CascadeClassifier(
            "haarcascade_frontalface_default.xml"
        )



        count = 0



        frame_window = st.image([])


        progress = st.progress(0)



        st.info(
            "Look at camera. Capturing 50 images..."
        )



        while True:


            ret, frame = camera.read()



            if not ret:

                st.error(
                    "Camera not working"
                )

                break




            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )



            faces = detector.detectMultiScale(
                gray,
                1.3,
                5
            )



            for x,y,w,h in faces:


                count += 1



                face = gray[
                    y:y+h,
                    x:x+w
                ]



                cv2.imwrite(

                    f"{folder}/{count}.jpg",

                    face

                )



                cv2.rectangle(

                    frame,

                    (x,y),

                    (x+w,y+h),

                    (0,255,0),

                    2

                )




            rgb = cv2.cvtColor(

                frame,

                cv2.COLOR_BGR2RGB

            )



            frame_window.image(
                rgb
            )



            progress.progress(
                min(count/50,1.0)
            )



            if count >= 50:

                break




        camera.release()

        cv2.destroyAllWindows()



        st.success(
            "✅ 50 Face Images Captured Successfully"
        )



        # ==========================
        # SAVE TO DATABASE
        # ==========================


        add_student(

            name,

            roll_no,

            department,

            folder

        )



        st.success(
            "✅ Student Saved in Database"
        )



        st.divider()



        # ==========================
        # TRAIN MODEL
        # ==========================


        if st.button(
            "🤖 Train AI Model"
        ):


            with st.spinner(
                "Training Face Recognition Model..."
            ):


                success, message = train_model()



            if success:


                st.success(
                    "🎉 AI Model Trained Successfully!"
                )


                st.info(
                    "trainer.yml and names.txt updated"
                )



            else:


                st.error(
                    "Training Failed"
                )


                st.code(
                    message
                )