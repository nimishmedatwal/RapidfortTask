
docker build -t docx-to-pdf .

docker run -d -p 5000:5000 --name docx_to_pdf_app docx-to-pdf
echo "Application is running on http://localhost:5000"
