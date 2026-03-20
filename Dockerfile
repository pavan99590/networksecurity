FROM python:3.10-bookworm

# Set the working directory
WORKDIR /app

# Copy requirements first (cache optimization)
COPY requirements.txt .

# Install pip deps + AWS CLI (no apt)
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install awscli

# Copy app
COPY . /app

# Run app
CMD ["python3", "app.py"]
