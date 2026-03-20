FROM python:3.10-bookworm

# Set the working directory
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install AWS CLI and clean up to keep the image small
RUN apt-get update -y && \
    apt-get install -y awscli && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Start the FastAPI application
CMD ["python3", "app.py"]