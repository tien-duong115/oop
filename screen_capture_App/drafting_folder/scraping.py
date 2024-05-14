#!/Users/tienduong/Desktop/DEVELOPMENT/SCRAPT_PROJ/screen_capture_App/venv/bin/python3
import cv2
def select_camera():
    ind=0
    arr=[]
    while True:
        cap=cv2.VideoCapture(ind)
        if not cap.read()[0]:
            break
        else:
            arr.append(ind)
        cap.release()
        ind+= 1
    return arr





cameras=select_camera()
print("All Available Cameras: ", cameras)
camera_index = int(input("Enter the index of the camera to use: "))

# Create a video capture object with the selected camera
capture = cv2.VideoCapture(camera_index)

while True:
    ret, frame = capture.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow('Video Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()