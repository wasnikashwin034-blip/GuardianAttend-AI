import streamlit as st
import sqlite3
import cv2
import os


st.title("👨‍🎓 Student Registration")


# Database connection
conn = sqlite3.connect(
    "data/attendance.db"
)

cursor = conn.cursor()


name = st.text_input(
    "Student Name"
)

roll = st.text_input(
    "Roll Number"
)

branch = st.text_input(
    "Branch"
)


if st.button("📷 Capture Face"):

    if name == "":
        st.error("Enter student name first")

    else:

        folder_name = name.replace(
            " ",
            "_"
        )

        path = f"images/{folder_name}"


        os.makedirs(
            path,
            exist_ok=True
        )


        camera = cv2.VideoCapture(
            2,
            cv2.CAP_DSHOW
        )


        count = 0

        st.info(
            "Camera started. Look at camera..."
        )


        while count < 30:

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


            cv2.imwrite(
                f"{path}/{count}.jpg",
                gray
            )


            count += 1


        camera.release()


        st.success(
            "Face images captured successfully"
        )



if st.button("Register Student"):

    cursor.execute(
        """
        INSERT INTO students
        (name, roll, branch)
        VALUES (?, ?, ?)
        """,
        (
            name,
            roll,
            branch
        )
    )


    conn.commit()

    st.success(
        "Student Registered Successfully"
    )


conn.close()