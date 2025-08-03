# Use Python Alpine image
FROM python:3.11-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    sqlite \
    sqlite-dev

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create directory for SQLite database
RUN mkdir -p /app/db

# Expose port
EXPOSE 8000