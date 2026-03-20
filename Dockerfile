FROM python:3.10-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install awscli

COPY . /app

CMD ["python3", "app.py"]
