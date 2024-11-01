import cv2
import threading
import time
import numpy as np
# Initialize the camera (default camera is 0)
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
counter = 0
latest_frame = None


def avrgdif(imageA, imageB):

    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err


# returns image
def take_picture():
    ret, frame = camera.read()
    return frame

def to_video():
    cap = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))


    frame = cv2.flip(latest_frame, 0)

    # write the flipped frame
    out.write(frame)

    cv2.imshow('frame', frame)


def detection():
    global counter, latest_frame
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






def full():
    detection()




thread = threading.Thread(target=full, daemon=True)
thread.start()

while True:
   time.sleep(4)


camera.release()
cv2.destroyAllWindows()
