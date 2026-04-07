FROM python:3.11-slim

# Install ffmpeg (required for audio processing)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Upgrade pip + install deps
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Start FastAPI app
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port $PORT"]