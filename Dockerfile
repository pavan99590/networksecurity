# Use Bullseye (Debian 11) instead of Buster (Debian 10)
FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install awscli

COPY . /app

EXPOSE 8080

CMD ["python3", "app.py"]