import cv2
import csv
from datetime import datetime


# Load trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read(
    "trainer.yml"
)


# Load face detector
face_cascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)


# Load names
names = {}

with open("names.txt") as file:

    for line in file:

        student_id, student_name = line.strip().split(",")

        names[int(student_id)] = student_name



# Iriun camera
cap = cv2.VideoCapture(
    2,
    cv2.CAP_DSHOW
)


marked_students = set()


while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera not detected")
        break


    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )


    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )


    for (x, y, w, h) in faces:


        face = gray[y:y+h, x:x+w]


        student_id, confidence = recognizer.predict(
            face
        )


        if confidence < 70:


            student_name = names[student_id]


            cv2.putText(
                frame,
                student_name,
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )


            if student_id not in marked_students:


                with open(
                    "attendance.csv",
                    "a",
                    newline=""
                ) as file:


                    writer = csv.writer(file)


                    writer.writerow(
                        [
                            student_name,
                            datetime.now().strftime("%H:%M:%S"),
                            datetime.now().strftime("%d-%m-%Y")
                        ]
                    )


                marked_students.add(student_id)

                print(
                    "Attendance marked:",
                    student_name
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


    cv2.imshow(
        "VisionAttend AI",
        frame
    )


    if cv2.waitKey(1) == 27:
        break



cap.release()

cv2.destroyAllWindows()