# Use official Python image as base
FROM python:3.10-slim

# Set who created this image
LABEL maintainer="Souleymane SOUMAHORO"

# Set working directory inside container
WORKDIR /app

# Copy dashboard requirements (lightweight)
COPY requirements-dashboard.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy dashboard code only
COPY src/dashboard/ ./src/dashboard/

# Expose port for Streamlit
EXPOSE 8501

# Command to run the dashboard
CMD ["streamlit", "run", "src/dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]