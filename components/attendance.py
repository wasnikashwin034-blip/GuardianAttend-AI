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



    cursor.execute(
        """
        SELECT id FROM attendance
        WHERE name=? AND date=?
        """,
        (name,date)
    )


    exists = cursor.fetchone()



    if exists:

        conn.close()

        return False



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

    conn.close()


    return True




# ==========================
# ATTENDANCE PAGE
# ==========================

def show():


    st.title(
        "🤖 AI Face Recognition Attendance"
    )


    st.subheader(
        "🛡️ AI AVENGERS | GuardianAttend AI"
    )


    st.divider()



    start = st.button(
        "📷 Start AI Camera"
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
            "names.txt"
        ) as f:

            names = f.read().splitlines()



        cap = cv2.VideoCapture(1)



        frame_box = st.image([])



        status_box = st.empty()



        confidence_box = st.empty()



        marked_people = set()



        while True:


            ret,frame = cap.read()



            if not ret:

                st.error(
                    "Camera not detected"
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



                face = gray[y:y+h,x:x+w]



                id,confidence = recognizer.predict(

                    face

                )



                accuracy = round(
                    100-confidence,
                    2
                )



                if accuracy > 50 and id < len(names):


                    name = names[id]



                    color = (0,255,0)



                    status_box.success(

                        f"✅ Recognized: {name}"

                    )


                    confidence_box.info(

                        f"AI Confidence: {accuracy}%"

                    )



                    if name not in marked_people:


                        saved = save_attendance(

                            name,

                            accuracy

                        )



                        if saved:


                            st.toast(

                                f"Attendance marked: {name}"

                            )


                        else:


                            st.toast(

                                f"{name} already present"

                            )



                        marked_people.add(name)




                else:


                    name="Unknown"

                    color=(0,0,255)



                    status_box.error(

                        "⚠️ Unknown Person Detected"

                    )



                    confidence_box.warning(

                        f"Confidence: {accuracy}%"

                    )




                cv2.rectangle(

                    frame,

                    (x,y),

                    (x+w,y+h),

                    color,

                    2

                )



                cv2.putText(

                    frame,

                    f"{name} {accuracy}%",

                    (x,y-10),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.8,

                    color,

                    2

                )



            rgb=cv2.cvtColor(

                frame,

                cv2.COLOR_BGR2RGB

            )



            frame_box.image(

                rgb,

                width="stretch"

            )



        cap.release()