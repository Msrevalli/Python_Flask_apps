from flask import Flask, render_template, request, send_from_directory
import cv2
import os

app = Flask(__name__)

# Initialize video capture
video_capture = cv2.VideoCapture(0)

# Ensure the static directory exists
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    success, frame = video_capture.read()
    if success:
        save_path = 'static/captured_image.jpg'
        cv2.imwrite(save_path, frame)
        return render_template('index.html', captured=True, image_path=save_path)
    else:
        return render_template('index.html', captured=False)

@app.route('/display_captured_image')
def display_captured_image():
    return send_from_directory('static', 'captured_image.jpg')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
