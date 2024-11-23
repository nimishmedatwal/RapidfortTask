import os
import pytest
from app import app

UPLOAD_FOLDER = 'uploads'

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Upload" in response.data  

def test_upload_invalid_file(client):
    data = {
        'file': (open(__file__, 'rb'), 'test.py')  # Non-DOCX file
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert b"Invalid file type" in response.data

def test_upload_valid_file(client):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    docx_file_path = os.path.join(UPLOAD_FOLDER, 'test.docx')
    
    from docx import Document
    doc = Document()
    doc.add_paragraph("This is a test document.")
    doc.save(docx_file_path)

    data = {
        'file': (open(docx_file_path, 'rb'), 'test.docx'),
        'password': 'test123'
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert b"Metadata" in response.data 

def test_convert_to_pdf(client):
    docx_file_path = os.path.join(UPLOAD_FOLDER, 'test.docx')
    pdf_file_path = os.path.join(UPLOAD_FOLDER, 'test.pdf')
    assert os.path.exists(docx_file_path)

    response = client.get(f'/convert/{os.path.basename(docx_file_path)}')
    assert response.status_code == 200
    assert os.path.exists(pdf_file_path)
    os.remove(docx_file_path)
    os.remove(pdf_file_path)
