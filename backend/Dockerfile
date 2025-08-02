# Use a more production-ready base image
FROM python:3.10-slim

# Install necessary system dependencies for Uvicorn/Gunicorn
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./tests ./tests
COPY ./migration ./migration

EXPOSE 8000

# Use Gunicorn to run Uvicorn workers
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
