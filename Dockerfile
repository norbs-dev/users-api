#file gnerated by chagpt
# Use official Python slim image (Linux)
FROM python:3.11-slim

# Set working directory
COPY ./app /app
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install system dependencies (optional, for building packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port (default FastAPI port)
EXPOSE 8000

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]