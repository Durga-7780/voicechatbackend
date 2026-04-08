FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# 👇 CRITICAL: force binary install (no gcc build)
RUN pip install --upgrade pip && \
    pip install --only-binary=:all: --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]