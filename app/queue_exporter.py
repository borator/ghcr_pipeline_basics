import os
import redis
from flask import Flask

REDIS_SERVER = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

app = Flask(__name__)
r = redis.Redis(host=REDIS_SERVER, port=REDIS_PORT)

@app.route("/metrics")
def metrics():
    qsize = r.llen("tasks")
    print("Current queue size: {qsize}") 
    #processed = int(r.get("tasks_processed_total") or 0)
    #seconds_total = float(r.get("task_processing_seconds_total") or 0)

#    return (
#        f"queue_length {qsize}\n"
#        f"tasks_processed_total {processed}\n"
#        f"task_processing_seconds_total {seconds_total}\n"
#    )

    return f"queue_length {qsize}\n"

app.run(host="0.0.0.0", port=8000)

