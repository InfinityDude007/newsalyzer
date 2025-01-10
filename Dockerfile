# Use official Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables/rules
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app"

# Set working directory in container
WORKDIR /app

# Update package list and install dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt file from host to container
COPY app/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy entire application from host to container
COPY . /app/

# Expose port for application to be accessed externally
EXPOSE 9000

# Start application using uvicorn
CMD ["sh", "-c", "uvicorn app.app:app --host 0.0.0.0 --port ${SERVER_PORT:-9000} --reload"]
