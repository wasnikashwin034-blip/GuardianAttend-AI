import streamlit as st
import cv2
import sqlite3
from datetime import datetime



DATABASE = "data/attendance.db"



# ==========================
# SAVE ATTENDANCE
# ==========================

def save_attendance(name, confidence):


    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()



    now = datetime.now()

    date = now.strftime("%Y-%m-%d")

    time = now.strftime("%H:%M:%S")



    # Prevent duplicate attendance

    cursor.execute(
        """
        SELECT * FROM attendance
        WHERE name=? AND date=?
        """,
        (
            name,
            date
        )
    )


    result = cursor.fetchone()



    if result is None:


        cursor.execute(

            """
            INSERT INTO attendance
            (name,date,time,status,confidence)

            VALUES(?,?,?,?,?)

            """,

            (
                name,
                date,
                time,
                "Present",
                confidence
            )

        )


        conn.commit()

        saved=True


    else:

        saved=False



    conn.close()


    return saved





# ==========================
# ATTENDANCE PAGE
# ==========================


def show():


    st.title(
        "📷 AI Face Recognition Attendance"
    )


    st.write(
        "GuardianAttend AI | AI AVENGERS"
    )



    start = st.button(
        "Start Camera"
    )



    if start:


        recognizer = cv2.face.LBPHFaceRecognizer_create()



        recognizer.read(
            "trainer.yml"
        )



        detector = cv2.CascadeClassifier(
            "haarcascade_frontalface_default.xml"
        )



        with open(
            "names.txt",
            "r"
        ) as f:

            names = f.read().splitlines()



        cap = cv2.VideoCapture(1)



        frame_window = st.image([])



        marked=False



        while True:


            ret, frame = cap.read()



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


                id, confidence = recognizer.predict(

                    gray[y:y+h, x:x+w]

                )



                accuracy = round(
                    100-confidence
                )



                if accuracy > 50 and id < len(names):


                    name = names[id]



                    cv2.putText(

                        frame,

                        f"{name} {accuracy}%",

                        (x,y-10),

                        cv2.FONT_HERSHEY_SIMPLEX,

                        1,

                        (0,255,0),

                        2

                    )



                    if not marked:


                        saved = save_attendance(

                            name,

                            accuracy

                        )



                        if saved:

                            st.success(

                                f"✅ Attendance marked: {name}"

                            )


                        else:

                            st.info(

                                f"Already marked today: {name}"

                            )


                        marked=True



                else:


                    cv2.putText(

                        frame,

                        "Unknown",

                        (x,y-10),

                        cv2.FONT_HERSHEY_SIMPLEX,

                        1,

                        (0,0,255),

                        2

                    )




                cv2.rectangle(

                    frame,

                    (x,y),

                    (x+w,y+h),

                    (255,0,0),

                    2

                )




            rgb = cv2.cvtColor(

                frame,

                cv2.COLOR_BGR2RGB

            )


            frame_window.image(rgb)



            if marked:

                break




        cap.release()