# DOCX to PDF Converter Web Application

## Overview

This project is a Flask-based web application that allows users to upload Microsoft Word documents (`.docx`), view file metadata, and download the file as a converted PDF. The application supports optional password protection for the generated PDFs. 

The project is containerized using Docker and is designed to run on a Kubernetes cluster, utilizing microservices architecture. It includes Kubernetes manifests for deployment, service configuration.

---

## Features

1. **Upload DOCX Files**: Users can upload `.docx` files via a simple web interface.
2. **View File Metadata**: Displays core properties of the uploaded Word document (e.g., title, author, creation date).
3. **Download as PDF**: Converts the uploaded document to a PDF and offers it for download.
4. **Password-Protected PDFs**: Optionally encrypts the PDF with a user-provided password.
5. **Dockerized and Kubernetes-Ready**: Easily deployable in containerized and distributed environments.

---

## Technologies Used

### Backend
- **Flask**: Python-based lightweight web framework.
- **docx2pdf**: Library to convert `.docx` to PDF.
- **PyPDF2**: For PDF encryption.
- **python-docx**: To extract metadata from `.docx` files.

### Deployment Tools
- **Docker**: For containerizing the application.
- **Kubernetes**: For managing containerized deployments.
- **Persistent Volumes**: For storing uploaded files across pod restarts.

---

## Getting Started

### Prerequisites
- Docker
- Kubernetes (minikube for local testing or a cloud-based Kubernetes service)
- Python 3.9 or later (for local development)

### Installation and Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/nimishmedatwal/RapidFort-Task
   ```

2. **Install Dependencies**
   If you want to run the application locally without Docker:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application Locally**
   ```bash
   python app.py
   ```
   Visit `http://localhost:5000` in your browser.

---

## Docker Deployment

1. **Build the Docker Image**
   ```bash
   docker build -t docx-to-pdf .
   ```

2. **Run the Container**
   ```bash
   docker run -d -p 5000:5000 --name docx_to_pdf_app docx-to-pdf
   ```

3. **Access the Application**
   Visit `http://localhost:5000`.

---

## Kubernetes Deployment

1. **Build and Push Docker Image**
   ```bash
   docker tag docx-to-pdf <your-dockerhub-username>/docx-to-pdf
   docker push <your-dockerhub-username>/docx-to-pdf
   ```

2. **Deploy Kubernetes Manifests**
   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```

3. **Access the Service**
   Retrieve the NodePort:
   ```bash
   kubectl get services
   ```
   Access the application at `http://<node-ip>:<node-port>`.

---

## Project Structure

```plaintext
project/
├── app.py                    
├── requirements.txt          
├── templates/                
│   ├── index.html            
│   ├── metadata.html         
├── static/                   
│   ├── style.css             
├── uploads/                  
├── Dockerfile                
├── deployment.yaml           
├── service.yaml              
├── run.sh                    
```

---


## Kubernetes Components

1. **Deployment**:
   - Manages replicas of the Flask app container for scalability and high availability.

2. **Service**:
   - Exposes the application using a NodePort to enable external access.

3. **Persistent Volumes**:
   - Stores uploaded files persistently across pod restarts.

---

## Key Functions

- **File Upload**: Handles `.docx` file uploads and saves them to the server.
- **Metadata Extraction**: Uses `python-docx` to extract core document properties.
- **DOCX to PDF Conversion**: Utilizes `docx2pdf` for high-quality conversion.
- **PDF Encryption**: Uses `PyPDF2` to add password protection to PDFs.

--- 
