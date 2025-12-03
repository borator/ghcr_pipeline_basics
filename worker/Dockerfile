FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y iputils-ping

COPY . .

# Use CMD, so it can be overridden in docker-compose.yml
CMD ["python", "worker.py"]

