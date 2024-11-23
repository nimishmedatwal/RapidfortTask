from flask import Flask, request, send_file, render_template, redirect, url_for
from docx import Document
import PyPDF2
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    password = request.form.get('password')
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith('.docx'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        metadata = get_doc_metadata(filepath)
        return render_template('metadata.html', metadata=metadata, filename=file.filename, password=password)
    else:
        return 'Invalid file type. Please upload a .docx file.'

def get_doc_metadata(filepath):
    doc = Document(filepath)
    properties = doc.core_properties
    metadata = {
        'Title': properties.title,
        'Author': properties.author,
        'Subject': properties.subject,
        'Keywords': properties.keywords,
        'Comments': properties.comments,
        'Last Modified By': properties.last_modified_by,
        'Last Printed': properties.last_printed,
        'Created': properties.created,
        'Modified': properties.modified
    }
    return metadata

def encrypt_pdf(pdf_path, password):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    pdf_writer = PyPDF2.PdfWriter()

    for page_num in range(len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    pdf_writer.encrypt(password)

    encrypted_pdf_path = pdf_path.replace('.pdf', '_encrypted.pdf')
    with open(encrypted_pdf_path, 'wb') as encrypted_pdf_file:
        pdf_writer.write(encrypted_pdf_file)

    return encrypted_pdf_path

def convert_docx_to_pdf(docx_path):
    # Use LibreOffice's CLI to convert DOCX to PDF
    pdf_path = docx_path.replace('.docx', '.pdf')
    try:
        subprocess.run(
            ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', UPLOAD_FOLDER, docx_path],
            check=True
        )
        return pdf_path
    except subprocess.CalledProcessError as e:
        print(f"Error converting DOCX to PDF: {e}")
        return None

@app.route('/convert/<filename>')
def convert_to_pdf(filename):
    password = request.args.get('password')
    docx_path = os.path.join(UPLOAD_FOLDER, filename)
    pdf_path = convert_docx_to_pdf(docx_path)

    if not pdf_path or not os.path.exists(pdf_path):
        return "Error during conversion. Please try again.", 500

    if password:
        encrypted_pdf_path = encrypt_pdf(pdf_path, password)
        return send_file(encrypted_pdf_path, as_attachment=True)
    else:
        return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
