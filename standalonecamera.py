import datetime

import cv2
import threading
import time
import numpy as np
# Initialize the camera (default camera is 0)
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
counter = 0
latest_frame = None
video_writer = None

def avrgdif(imageA, imageB):

    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err


# returns image
def take_picture():
    ret, frame = camera.read()
    return frame

def save_picture(picture):
    fileName = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
    print(f"Saving picture as: {fileName}")
    success = cv2.imwrite(fileName, picture)
    if success:
        print("Image saved successfully.")
    else:
        print("Failed to save the image.")


def initialize_video_writer(frame):
    global video_writer
    height, width, _ = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    file_name = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.avi"
    video_writer = cv2.VideoWriter(file_name, fourcc, 20.0, (width, height))
    print(f"Video recording started: {file_name}")


def stop_video_writer():
    global video_writer
    if video_writer is not None:
        video_writer.release()
        video_writer = None
        print("Video recording stopped.")


def detection():
    global counter, latest_frame
    previous_frame = take_picture()
    time.sleep(3)
    while True:
        frame = take_picture()


        if previous_frame is not None:

            sensitvity = 500
            avrgdifresult = avrgdif(frame,previous_frame)

            if avrgdifresult > sensitvity:
                save_picture(frame)
                if video_writer is None:
                    initialize_video_writer(frame)

                video_writer.write(frame)

                same_frame_count = 0
            else:
                if video_writer is not None:
                    same_frame_count += 1

                    video_writer.write(frame)

                    if same_frame_count >= 5:
                        stop_video_writer()

            previous_frame = frame






def full():
    detection()




thread = threading.Thread(target=full, daemon=True)
thread.start()

while True:
   time.sleep(4)


camera.release()
cv2.destroyAllWindows()
