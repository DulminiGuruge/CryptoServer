# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Copy application files to the container
ADD . /app

# Set the working directory to /app
WORKDIR /app

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the Flask application port
EXPOSE 7655

# Run the application with Gunicorn for better concurrency
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7655", "app:app"]
