from flask import Flask, request, send_file
import pdfkit
import re
import os
import zipfile
import shutil

app = Flask(__name__)
app.debug = True  # Enable debug mode for more informative error messages

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    print("Request received for /generate_pdf")  # Debug: Check if the route is reached

    # Get the uploaded WhatsApp chat ZIP file
    zip_file = request.files.get('WhatsApp Chat') 
    print("Zip file received:", zip_file)  # Debug: Check if the file is received

    if not zip_file:
        return "No file uploaded.", 400

    # Create a temporary directory for extracting files
    temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Extract the contents of the ZIP file to the temporary directory
    try:
        zip_ref = zipfile.ZipFile(zip_file, 'r')
        zip_ref.extractall(temp_dir)
        zip_ref.close()
    except zipfile.BadZipFile:
        return "Invalid ZIP file.", 400
    except Exception as e:
        return "Error extracting ZIP file: {}".format(e), 500

    # Find the text file and media files in the temporary directory
    text_file_path = None
    media_file_paths = []
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file.endswith('.txt'):
                text_file_path = os.path.join(root, file)
                print("Text file found:", text_file_path) # Debug: Check if the text file is found
            elif file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mp4', '.avi', '.mov')):
                media_file_paths.append(os.path.join(root, file))
                print("Media file found:", file) # Debug: Check if media files are found

    # Check if both text file and media files were found
    if not text_file_path:
        return "Text file not found in the ZIP file.", 400
    if not media_file_paths:
        return "Media files not found in the ZIP file.", 400

    # Parse the text file to identify the context for each media file
    with open(text_file_path, 'r') as f:
        text_data = f.read()
    media_file_contexts = []
    for line in text_data.splitlines():
        match = re.search(r'\[(image|video)\](.*)', line)
        if match:
            media_type = match.group(1)
            media_file_name = match.group(2)
            media_file_path = next((path for path in media_file_paths if os.path.basename(path) == media_file_name), None)
            if media_file_path:
                media_file_contexts.append((media_type, media_file_path))

    # Create a PDF file from the text data and media files
    html = '<html><body>'
    for line in text_data.splitlines():
        html += '<p>{}</p>'.format(line)
        for media_type, media_file_path in media_file_contexts:
            if media_file_path and os.path.basename(media_file_path) in line:
                if media_type == 'image':
                    html += '<img src="file://{}" />'.format(media_file_path)
                elif media_type == 'video':
                    html += '<video width="100%" height="100%" controls><source src="file://{}" type="video/mp4"></video>'.format(media_file_path)
    html += '</body></html>'

    # Generate PDF using pdfkit
    try:
        pdf = pdfkit.from_string(html, False, options={'enable-local-file-access': None})
    except Exception as e:
        return "Error converting HTML to PDF: {}".format(e), 500

    # Create a PDF file with the chat title as the filename
    chat_name = os.path.splitext(os.path.basename(text_file_path))[0]
    filename = f"{chat_name}.pdf"
    with open(filename, 'wb') as f:
        f.write(pdf)

    # Remove the temporary directory and files
    shutil.rmtree(temp_dir)

    # Return the PDF file as a response
    return send_file(filename, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000) # Add a port number if you are not using the default port