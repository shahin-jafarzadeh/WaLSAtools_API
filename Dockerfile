# Use a minimal Python 3.10 base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your FastAPI code into the container
COPY . .

# Expose port 8080 (Google Cloud Run expects this)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
