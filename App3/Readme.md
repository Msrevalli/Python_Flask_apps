# Indian Flag Video Stream

This Flask application streams live video from your webcam, with the Indian flag dynamically superimposed at the bottom.

## Features

* **Live Webcam Feed:**  Streams video from your default webcam.
* **Dynamic Flag Placement:**  The Indian flag is resized to fit the width of the video frame and placed at the bottom.
* **Mirror Effect:** The video feed is flipped horizontally for a mirror view.

## Getting Started

1. **Install Python:** Make sure you have Python installed on your system.
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Install additional libraries:**
   - For Debian-based Linux distributions:
     ```bash
     sudo apt-get update 
     sudo apt-get install libgl1-mesa-dev libglu1-mesa-dev libx11-dev libxext-dev libxrandr-dev 
     ```
   - For Windows, these libraries are typically included with the graphics drivers. Make sure your drivers are up to date.
   - For MacOS, these libraries are typically included with the system. Make sure your system is up to date.