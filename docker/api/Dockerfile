# Use official Python image as base
FROM python:3.10-slim

# Set who created this image
LABEL maintainer="Souleymane SOUMAHORO"

# Set working directory inside container
WORKDIR /app

# Copy API requirements (without dashboard dependencies)
COPY requirements-api.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Copy ML models
COPY *.pkl ./

# Set Python path
ENV PYTHONPATH=/app

# Expose port for API
EXPOSE 8000

# Command to run the API
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]