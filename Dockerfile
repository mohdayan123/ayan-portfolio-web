# Multi-stage lightweight Python Dockerfile for Mohd Ayan Portfolio
FROM python:3.10-slim AS base

# Set working directory
WORKDIR /app

# Prevent Python from writing .pyc files & enable unbuffered stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app.py .
COPY templates/ ./templates/

# Expose standard container port
EXPOSE 5000

ENV PORT=5000
ENV FLASK_ENV=production

# Healthcheck for container orchestration
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/health')" || exit 1

# Production WSGI server via Gunicorn
CMD ["gunicorn", "--workers=2", "--threads=4", "--bind=0.0.0.0:5000", "app:app"]
