import time
import redis
import random
import string
import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

print(f"Sending load to Redis on {REDIS_HOST}:{REDIS_PORT}")

while True:
    word = "".join(random.choices(string.ascii_lowercase, k=5))
    r.rpush("tasks", word)
    print("Queued:", word)
    time.sleep(0.01)

