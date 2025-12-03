FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install "redis>=4.5"
RUN apt-get update && apt-get install -y iputils-ping

COPY . .

# Use CMD, so it can be overridden in docker-compose.yml
CMD ["python", "loadgen.py"]

