from flask import Flask, request, send_file
import os
from fpdf import FPDF
from PIL import Image

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Assuming you have extracted the text and media files
        text_file_path = "WhatsApp Chat with AWS Summit slides.txt"
        media_folder_path = "WhatsApp Chat with AWS Summit slides"

        # Create a PDF object
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Read text messages from the text file and add them to the PDF
        with open(text_file_path, "r", encoding="utf-8") as text_file:
            for line in text_file:
                pdf.cell(200, 10, txt=line, ln=True)

        # Embed media files (images) into the PDF
        for filename in os.listdir(media_folder_path):
            if filename.endswith((".jpg", ".jpeg")):  # Assuming images are JPEG format
                image_path = os.path.join(media_folder_path, filename)
                img = Image.open(image_path)
                # Resize image if needed to fit the PDF layout
                # Add image to PDF
                pdf.image(image_path, x=10, y=pdf.get_y() + 10, w=100)

        # Output PDF to a file
        output_filename = "whatsapp_chat.pdf"
        pdf.output(output_filename)

        # Serve the PDF file for download
        return send_file(output_filename, as_attachment=True)

    return "Hello, please upload your WhatsApp chat files."

if __name__ == "__main__":
    app.run(host="0.0.0.0")
