# Use official Python runtime as a parent image
FROM python:3.12-slim as builder

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final production stage
FROM python:3.12-slim

WORKDIR /app

# Set production environment variables
ENV ENVIRONMENT="production"
ENV PORT=8080

# Copy wheels from builder and install
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy the rest of the application code into the backend namespace
COPY . /app/backend

# Create a non-root user and switch to it
RUN chown -R 1000:1000 /app
RUN addgroup --system app && adduser --system --group app
USER app

# Command to run the application using uvicorn with workers for production
# Cloud Run injects the PORT environment variable dynamically
ENV PYTHONPATH=/app
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT} --workers 4 --proxy-headers --forwarded-allow-ips='*'"]
