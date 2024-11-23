# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install LibreOffice and required dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends libreoffice && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the application files
COPY . /app
COPY templates /templates
COPY static /static

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
