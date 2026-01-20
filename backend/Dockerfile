# -------------------------------------------------
# Base image (Python 3.13)
# -------------------------------------------------
FROM python:3.13-slim

# -------------------------------------------------
# Environment configuration
# -------------------------------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -------------------------------------------------
# System dependencies (OpenCV, PIL, Torch needs)
# -------------------------------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------------------------
# Working directory
# -------------------------------------------------
WORKDIR /app

# -------------------------------------------------
# Install Python dependencies
# -------------------------------------------------
COPY backend/requirements.txt ./requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# -------------------------------------------------
# Copy application code
# -------------------------------------------------
COPY backend/ ./  

# -------------------------------------------------
# Expose FastAPI port
# -------------------------------------------------
EXPOSE 8000

# -------------------------------------------------
# Run FastAPI app
# -------------------------------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
