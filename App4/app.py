from flask import Flask, request, render_template, send_file, redirect, url_for
import os
from werkzeug.utils import secure_filename
from process_whatsapp import whatsapp_chat_to_pdf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['GENERATED_FOLDER'] = 'generated'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(zip_path)

        output_pdf = os.path.join(app.config['GENERATED_FOLDER'], f'{os.path.splitext(filename)[0]}.pdf')
        whatsapp_chat_to_pdf(zip_path, output_pdf)

        return redirect(url_for('download_file', filename=os.path.basename(output_pdf)))
    
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['GENERATED_FOLDER'], filename)
    return render_template('download.html', filename=filename, file_path=file_path)

@app.route('/download_pdf/<filename>')
def download_pdf(filename):
    file_path = os.path.join(app.config['GENERATED_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
