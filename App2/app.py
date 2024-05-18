from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configuration for file uploads
app.config['TEMPLATE_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')  # Directory where uploaded files will be stored
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # Allowed file extensions
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'supersecretkey'  # Secret key for session management and flash messages

# Create the uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """
    Check if the file has an allowed extension.
    :param filename: Name of the file to check.
    :return: True if the file has an allowed extension, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """
    Handle file upload via POST and display the upload form via GET.
    :return: Rendered HTML template for GET requests or redirect after handling POST requests.
    """
    if request.method == 'POST':
        print("POST request received")  # Debug information

        # Check if a file was uploaded in the request
        if 'file' not in request.files:
            print("No file part")  # Debug information
            flash('No file part')  # Display flash message to the user
            return redirect(request.url)  # Redirect back to the form

        file = request.files['file']

        # Check if the user selected a file
        if file.filename == '':
            print("No selected file")  # Debug information
            flash('No selected file')  # Display flash message to the user
            return redirect(request.url)  # Redirect back to the form

        # Validate the file and save it to the upload folder
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Sanitize the filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)  # Save the file
            print(f"File saved to {file_path}")  # Debug information
            # Redirect to display the uploaded image
            return redirect(url_for('uploaded_file', filename=filename))
        else:
            print("Invalid file type")  # Debug information
            flash('Invalid file type')  # Display flash message to the user
            return redirect(request.url)  # Redirect back to the form

    print("GET request received, rendering template")  # Debug information
    return render_template('index.html')  # Render the upload form

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serve the uploaded file.
    :param filename: Name of the file to serve.
    :return: The requested file or a 404 error if the file is not found.
    """
    print(f"Requesting file: {filename}")  # Debug information
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"File path: {file_path}")  # Debug information

    if os.path.exists(file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        print("File not found")  # Debug information
        return "File not found", 404

if __name__ == "__main__":
    # Run the Flask application
    app.run(host="0.0.0.0", debug=True)  # Use debug mode for development