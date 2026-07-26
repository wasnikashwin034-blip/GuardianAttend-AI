import cv2
import os
import numpy as np
from PIL import Image


data_path = "images"

recognizer = cv2.face.LBPHFaceRecognizer_create()

detector = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)

faces = []
ids = []

student_id = 0

names = {}


for folder in os.listdir(data_path):

    folder_path = os.path.join(
        data_path,
        folder
    )

    if os.path.isdir(folder_path):

        print("Training:", folder)

        names[student_id] = folder


        for image_name in os.listdir(folder_path):

            image_path = os.path.join(
                folder_path,
                image_name
            )

            img = Image.open(
                image_path
            ).convert("L")


            img_numpy = np.array(
                img,
                "uint8"
            )


            detected_faces = detector.detectMultiScale(
                img_numpy
            )


            for (x, y, w, h) in detected_faces:

                faces.append(
                    img_numpy[y:y+h, x:x+w]
                )

                ids.append(
                    student_id
                )


        student_id += 1


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

    for key,value in names.items():

        f.write(
            f"{key},{value}\n"
        )


print("---------------------------")
print("Training Completed Successfully")
print("Model saved as trainer.yml")
print("---------------------------")