FROM python:3.11-slim

# Install ALL required system dependencies for aiortc + av
RUN apt-get update && apt-get install -y \
    ffmpeg \
    pkg-config \
    gcc \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libavfilter-dev \
    libswscale-dev \
    libswresample-dev \
    libssl-dev \
    libffi-dev \
    libopus-dev \
    libvpx-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port $PORT"]