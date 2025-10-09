# Multi-stage Dockerfile for AURA Backend Services
FROM python:3.11-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash aura
RUN chown -R aura:aura /app
USER aura

# Expose common ports
EXPOSE 8000 8001 8002 8003 8004 8005

# Default command (can be overridden in docker-compose)
CMD ["uvicorn", "api_gateway.main:api_gateway", "--host", "0.0.0.0", "--port", "8000"]
