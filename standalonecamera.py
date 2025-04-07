import datetime
import cv2
import threading
import time
import numpy as np
import asyncio

# Initialize the camera (default camera is 0)
camera = None
counter = 0
latest_frame = None
video_writer = None
same_frame_count = 0
global reset
global video_filename
reset = True
def avrgdif(imageA, imageB):

    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def write_to_file(txtfile, message, datapath):
    with open(txtfile, "w") as log_file:
        log_file.write(f"{message}:{datapath}")
    print("Motion detection logged.")

def initialize_camera():
    global camera
    if camera is None or not camera.isOpened():
        print("Initializing camera inside standalonecamera...")
        camera = cv2.VideoCapture(0)
    return camera

# returns image
def take_picture():
    cam = initialize_camera()
    ret, frame = cam.read()
    return frame

def save_picture(picture):
    fileName = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
    print(f"Saving picture as: {fileName}")
    success = cv2.imwrite(fileName, picture)
    if success:
        print("Image saved successfully.")
        return fileName
    else:
        print("Failed to save the image.")
        return None


def initialize_video_writer(frame):
    global video_writer
    global video_filename
    height, width, _ = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    video_filename = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp4"
    video_writer = cv2.VideoWriter(video_filename, fourcc, 20.0, (width, height))
    print(f"Video recording started: {video_filename}")


def stop_video_writer():
    global video_writer
    if video_writer is not None:
        video_writer.release()
        video_writer = None
        print("Video recording stopped.")

def stop_camera():
    global camera
    if camera is not None:
        print("releasing camera")
        camera.release()

def detection():
    print("starting detection")
    global counter, latest_frame, same_frame_count, reset
    previous_frame = take_picture()
    time.sleep(3)
    while True:
        frame = take_picture()
        if previous_frame is None:
            print("camera is not working")
        if previous_frame is not None:
            sensitvity = 500
            avrgdifresult = avrgdif(frame, previous_frame)

            if avrgdifresult > sensitvity:
                image_path = save_picture(frame)
                if video_writer is None:
                    initialize_video_writer(frame)


                video_writer.write(frame)
                if reset and image_path:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    write_to_file("motion_log.txt", f"detected: at {timestamp}",image_path)  # Log motion only on first detection after reset

                same_frame_count = 0
                reset = False

            else:
                if video_writer is not None:
                    same_frame_count += 1

                    video_writer.write(frame)

                    if same_frame_count >= 30:
                        global video_filename
                        stop_video_writer()
                        write_to_file(message="recording: done, no motion detected",txtfile="motion_log.txt", datapath=video_filename)
                        reset = True

            previous_frame = frame


async def full():
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, detection)


if __name__ == "__main__":
    import threading
    thread = threading.Thread(target=detection, daemon=True)
    thread.start()

    while True:
        time.sleep(4)



cam = initialize_camera()
cam.release()
cv2.destroyAllWindows()