FROM python:3.10-bookworm

# Set the working directory
WORKDIR /app

# Copy requirements first for better caching 
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install awscli

# Copy all files to the container
COPY . /app

# Start the FastAPI application
CMD ["python3", "app.py"]