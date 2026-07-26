import streamlit as st
import cv2
import sqlite3
from datetime import datetime


st.title("📷 AI Face Recognition Attendance")


# Load model

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read(
    "trainer.yml"
)


face_cascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)


# Load names

names = {}

with open("names.txt") as file:

    for line in file:

        student_id, name = line.strip().split(",")

        names[int(student_id)] = name



st.success("AI Model Loaded Successfully")


start = st.button(
    "▶ Start Camera"
)


camera_placeholder = st.empty()


if start:


    cap = cv2.VideoCapture(
        2,
        cv2.CAP_DSHOW
    )


    marked = set()


    while True:


        ret, frame = cap.read()


        if not ret:

            st.error(
                "Camera not detected"
            )

            break



        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )



        faces = face_cascade.detectMultiScale(
            gray,
            1.3,
            5
        )



        for (x,y,w,h) in faces:


            face = gray[y:y+h,x:x+w]


            student_id, confidence = recognizer.predict(
                face
            )



            if confidence < 70:


                student_name = names[student_id]


                cv2.putText(
                    frame,
                    student_name,
                    (x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2
                )


                if student_id not in marked:

conn = sqlite3.connect(
    "data/attendance.db"
)

cursor = conn.cursor()


cursor.execute(
    """
    INSERT INTO attendance
    (student_id, name, date, time)
    VALUES (?, ?, ?, ?)
    """,
    (
        student_id,
        student_name,
        datetime.now().strftime("%d-%m-%Y"),
        datetime.now().strftime("%H:%M:%S")
    )
)


conn.commit()

conn.close()


                    marked.add(student_id)


                    st.success(
                        f"Attendance marked: {student_name}"
                    )



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



        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        camera_placeholder.image(
            frame
        )



    cap.release()