FROM python:3-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["fastapi", "dev", "--host", "0.0.0.0", "app/main.py"]

