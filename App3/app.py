from flask import Flask, render_template, Response, send_from_directory
import cv2
import time
import numpy as np
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__)

def find_camera_index():
    """
    Find an available camera index.
    """
    for i in range(10):  # Try up to 10 camera indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cap.release()
            return i
    return None

# Find an available camera index
camera_index = find_camera_index()
if camera_index is None:
    print("Error: No camera detected.")
else:
    print(f"Using camera index: {camera_index}")

# Initialize video capture
video_capture = cv2.VideoCapture(camera_index)

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Get the full path to the image file
image_path = os.path.join(script_dir, "indian_flag.png")

# Load the Indian flag image
flag_image = Image.open(image_path)

# Set flag dimensions
flag_width = 640
flag_height = 480
flag_image_resized = flag_image.resize((flag_width, flag_height), Image.LANCZOS)

# Set face detection parameters
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Variable to store the captured frame
captured_frame = None

def generate_frames():
    """
    Generates frames for the video stream.
    """
    global captured_frame  # Access the global variable
    while True:
        success, frame = video_capture.read()
        if not success:
            break

        # Flip the image horizontally for a mirror effect
        frame = cv2.flip(frame, 1)

        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create a PIL Image from the frame
        pil_image = Image.fromarray(rgb_frame)

        # Paste the resized flag image onto the frame
        pil_image.paste(flag_image_resized, (0, 0), flag_image_resized)

        # Convert the PIL Image back to a NumPy array
        frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # Detect faces using OpenCV's Haar Cascade classifier
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Capture the frame with flag background
            captured_frame = frame.copy()  # Store the current frame

        # Encode the frame as a JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    """
    Renders the HTML template for the video stream.
    """
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """
    Returns the video stream.
    """
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/captured_image')
def captured_image():
    """
    Sends the captured frame with flag background.
    """
    global captured_frame
    if captured_frame is not None:
        # Save the image to a file (optional)
        cv2.imwrite('captured_image.jpg', captured_frame)

        # Convert the captured frame to bytes for the response
        ret, buffer = cv2.imencode('.jpg', captured_frame)
        frame = buffer.tobytes()
        return Response(frame, mimetype='image/jpeg')
    else:
        return "No image captured yet."

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)