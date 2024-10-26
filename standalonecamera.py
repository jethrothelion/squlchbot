import cv2
import threading
import time
import numpy as np
# Initialize the camera (default camera is 0)
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
counter = 0


def avrgdif(imageA, imageB):

    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

# returns image
def take_picture():
    ret, frame = camera.read()
    return frame

def save_pictures():
    global counter
    previous_frame = take_picture()
    time.sleep(3)
    while True:
        frame = take_picture()


        if previous_frame is not None:
            sensitvity = 500
            if avrgdif(frame,previous_frame) > sensitvity:
                print("this dif")
                counter += 1
                image_filename = f"{counter}.jpg"
                cv2.imwrite(image_filename, frame)
                print(f"Image saved as {image_filename}")

                previous_frame = frame






thread = threading.Thread(target=save_pictures, daemon=True)
thread.start()

# Run the main thread for a specified amount of time
try:
    while True:
       time.sleep(4)  # Main thread sleeps; adjust as necessary
except KeyboardInterrupt:
    print("Program interrupted. Exiting...")

# Release the camera and close any OpenCV windows
camera.release()
cv2.destroyAllWindows()