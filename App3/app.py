from flask import Flask, render_template, Response
import cv2
import time
import numpy as np
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Initialize video capture
video_capture = cv2.VideoCapture(0)

# Load the Indian flag image
flag_image = Image.open("indian_flag.png")

def generate_frames():
    """
    Generates frames for the video stream.
    """
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

        # Resize the flag image to match the frame width
        flag_width = frame.shape[1]
        flag_image_resized = flag_image.resize((flag_width, int(flag_width * flag_image.height / flag_image.width)), Image.LANCZOS)

        # Paste the flag image onto the bottom of the frame
        pil_image.paste(flag_image_resized, (0, frame.shape[0] - flag_image_resized.height), flag_image_resized)

        # Convert the PIL Image back to a numpy array
        frame = np.array(pil_image)

        # Convert the frame back to BGR for OpenCV
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

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

if __name__ == '__main__':
    app.run(debug=True)