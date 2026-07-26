import cv2
import os
import numpy as np


def train():

    path = "images"

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    detector = cv2.CascadeClassifier(
        "haarcascade_frontalface_default.xml"
    )


    faces = []
    ids = []

    names = []

    current_id = 0


    for student in os.listdir(path):

        student_path = os.path.join(
            path,
            student
        )


        if not os.path.isdir(student_path):
            continue


        names.append(student)


        for image_name in os.listdir(student_path):

            img_path = os.path.join(
                student_path,
                image_name
            )


            img = cv2.imread(
                img_path,
                cv2.IMREAD_GRAYSCALE
            )


            detected_faces = detector.detectMultiScale(
                img
            )


            for (x,y,w,h) in detected_faces:

                faces.append(
                    img[y:y+h,x:x+w]
                )

                ids.append(
                    current_id
                )


        current_id += 1



    recognizer.train(
        faces,
        np.array(ids)
    )


    recognizer.save(
        "trainer.yml"
    )


    with open(
        "names.txt",
        "w"
    ) as f:

        for name in names:

            f.write(
                name + "\n"
            )


    print("Training completed")
    print("Students:", names)



train()