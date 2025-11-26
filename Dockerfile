FROM python:3.10-alpine
#PYTHONUNBUFFERED=1 ensures logs appear immediately in docker compose logs.
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"] 
