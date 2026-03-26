# Use a specific version for stability
FROM python:3.10-slim-buster

# Install essential system dependencies (needed for some pandas/numpy operations)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install awscli

# Copy everything else (including your final_model folder)
COPY . /app

# Expose the port (good practice for documentation)
EXPOSE 8080

# Run app
CMD ["python3", "app.py"]