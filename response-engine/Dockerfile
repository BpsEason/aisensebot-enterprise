# Base image for the response engine
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY response-engine/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY response-engine/main.py .

# Expose port
EXPOSE 5055

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5055"]