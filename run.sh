docker network create docx-to-pdf-network
docker build -t docx-to-pdf:latest .

docker run -d -p 5000:5000 --network docx-to-pdf-network --name docx_to_pdf_app docx-to-pdf:latest
