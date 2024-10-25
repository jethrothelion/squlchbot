import cv2
import threading
import time

# Initialize the camera (default camera is 0)
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
counter = 0
ret, frame = camera.read()
previous_frame = frame

# returns image
def take_picture():
    ret, frame = camera.read()
    return frame

def save_pictures():
    global counter, previous_frame


    while True:
        frame = take_picture()
        if frame is None:
            continue

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if previous_frame is not None:
            # Convert previous frame to grayscale
            gray_previous_frame = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
            # Compute absolute difference between the two frames
            frame_diff = cv2.absdiff(gray_frame, gray_previous_frame)
            # Count non-zero pixels (indicating a difference)
            non_zero_count = cv2.countNonZero(frame_diff)

            difference_threshold = 30000
            if non_zero_count < difference_threshold:
                print("Frames are the same")
            else:
                print("Frames are different")

        counter += 1
        image_filename = f"{counter}.jpg"
        cv2.imwrite(image_filename, frame)
        print(f"Image saved as {image_filename}")

        previous_frame = frame

        time.sleep(0.5)



if not camera.isOpened():
    print("Error: Unable to access the camera.")
else:
    # Start the thread to save pictures
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