import cv2

camera_index = 1

cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

print("Camera started")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Cannot read frame")
        break

    cv2.imshow("Camera Test", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()