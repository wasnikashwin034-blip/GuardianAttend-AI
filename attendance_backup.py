import cv2
import csv
from datetime import datetime


recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read(
    "trainer.yml"
)


face_cascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)


names = {}

with open("names.txt") as f:

    for line in f:

        id, name = line.strip().split(",")

        names[int(id)] = name



cap = cv2.VideoCapture(
    2,
    cv2.CAP_DSHOW
)


marked = False


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
        1.3,
        5
    )


    for (x,y,w,h) in faces:


        face = gray[y:y+h, x:x+w]


        id, confidence = recognizer.predict(
            face
        )


        if confidence < 70:

            student_name = names[id]


            cv2.putText(
                frame,
                student_name,
                (x,y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )


            if not marked:

                with open(
                    "attendance.csv",
                    "a",
                    newline=""
                ) as f:


                    writer = csv.writer(f)

                    writer.writerow(
                        [
                            student_name,
                            datetime.now().strftime("%H:%M:%S"),
                            datetime.now().strftime("%d-%m-%Y")
                        ]
                    )


                marked = True


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


    if cv2.waitKey(1)==27:
        break



cap.release()

cv2.destroyAllWindows()