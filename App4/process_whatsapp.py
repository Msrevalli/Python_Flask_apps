import os
import zipfile
import re
from fpdf import FPDF
from PIL import Image

# Function to extract ZIP file
def extract_zip(zip_path, extract_to='.'):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

# Function to read chat file and process text and media
def process_chat_file(chat_file, media_folder, pdf_output):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    with open(chat_file, 'r', encoding='utf-8') as file:
        for line in file:
            # Check for media file references in the line
            media_match = re.search(r'<Media omitted>|(IMG-\d{8}-WA\d{4}.jpg|VID-\d{8}-WA\d{4}.mp4)', line)
            if media_match:
                media_file = media_match.group(0)
                media_path = os.path.join(media_folder, media_file)
                if os.path.isfile(media_path):
                    # If it's an image, add it to the PDF
                    if media_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        pdf.image(media_path, x=10, w=pdf.w - 20)
                        pdf.ln(10)
                    else:
                        # For non-image media files, add a placeholder text
                        pdf.cell(0, 10, f"[Media file: {media_file}]", ln=True)
            else:
                # Add the text line to the PDF
                pdf.multi_cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'))
    
    pdf.output(pdf_output)

# Main function
def whatsapp_chat_to_pdf(zip_path, output_pdf):
    # Extract ZIP file
    extract_folder = os.path.splitext(zip_path)[0]
    extract_zip(zip_path, extract_folder)
    
    # Locate the chat file and media folder
    chat_file = None
    media_folder = None

    for root, dirs, files in os.walk(extract_folder):
        for file in files:
            if file.endswith('.txt'):
                chat_file = os.path.join(root, file)
            elif any(file.lower().endswith(ext) for ext in ('.png', '.jpg', '.jpeg', '.mp4')):
                media_folder = root
    
    if chat_file and media_folder:
        process_chat_file(chat_file, media_folder, output_pdf)
    else:
        print("Chat file or media folder not found in the extracted content.")
