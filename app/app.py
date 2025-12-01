from flask import Flask, render_template, request, redirect, url_for
import redis
import os
from prometheus_client import Counter, Histogram, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

app = Flask(__name__)

# Prometheus metrics
REQ_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint"])
REQ_LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["endpoint"])

@app.before_request
def before_req():
    import time
    from flask import g
    g._start_time = time.time()

@app.after_request
def after_res(response):
    from flask import request, g
    try:
        elapsed = __import__("time").time() - getattr(g, "_start_time", 0)
        REQ_LATENCY.labels(request.path).observe(elapsed)
        REQ_COUNT.labels(request.method, request.path).inc()
    except Exception:
        pass
    return response

@app.route("/", methods=["GET"])
def index():
    words = r.lrange("words", 0, -1)
    return render_template("index.html", words=words)

#@app.route("/add", methods=["POST"])
#def add_word():
#    word = request.form.get("word","").strip()
#    if word:
#        r.rpush("words", word)
#    return redirect(url_for("index"))

@app.route("/add", methods=["POST"])
def add_word():
    word = request.form.get("word", "").strip()
    if word:
        r.rpush("words", word)   # store for web UI
        r.lpush("tasks", word)   # send task to worker
    return redirect(url_for("index"))


# Mount prometheus /metrics
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    "/metrics": make_wsgi_app()
})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

