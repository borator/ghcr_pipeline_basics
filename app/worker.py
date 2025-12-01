import os
import time
import redis

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", "6379"))

print(f"Connecting to Redis at {redis_host}:{redis_port}")
r = redis.Redis(host=redis_host, port=redis_port)

print("Worker started. Waiting for tasks...")

while True:
    #start = time.time()
    task = r.lpop("tasks")
    vals = r.lrange("tasks", 0, -1)
    #r.incr("tasks_processed_total")
    if task:
        #duration = time.time() - start
        #print(f"Processing task: {task.decode()} type: {r.type('tasks')} all words so far {len(vals)} time {duration}")
        print(f"Processing task: {task.decode()} type: {r.type('tasks')} all words so far {len(vals)}")
        #r.incrbyfloat("task_processing_seconds_total", duration)
    time.sleep(1)

