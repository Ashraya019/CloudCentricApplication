from fastapi import Request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Metrics 
# You are defining Prometheus Metrics to track exactly how your application is performing in real-time.

# Metric Type: Counter. In Prometheus, a counter only goes up (it never decreases unless the app restarts).
# What it tracks: Every single time a request hits your API, you "increment" this counter.
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    # Labels ["method", "endpoint", "status"]: These are critical. They allow you to filter your data.
    ["method", "endpoint", "status"]
)

# How long (in seconds) each request takes to finish.
#  It groups requests into "buckets" (e.g., how many took < 0.1s, how many took < 0.5s, etc.).
# In 2026, we don't care about "average" speed. We care about the P99 (99th percentile)—the slowest requests that are frustrating your users. A histogram lets you calculate that.
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method","endpoint"]
)

# Middleware
# metrics_middleware is a high-efficiency implementation for tracking API performance in FastAPI. It uses a Context Manager pattern to automatically handle the timing of your requests.
async def metrics_middleware(request: Request, call_next):
    # The middleware first extracts what was done (e.g., GET) and where (e.g., /items). These are used as "Labels" so you can filter your graphs in Grafana later.
    method = request.method
    endpoint = request.url.path

    # Instead of manually recording the start_time and end_time (and doing the math yourself), the Prometheus library's .time() helper does it for you.
    # It starts a high-precision timer.
    # await call_next(request) sends the request to your actual route (like create_item).
    # When the route finishes and returns a response, the timer stops.
    # The duration is automatically saved into the REQUEST_LATENCY histogram.
    with REQUEST_LATENCY.labels(method=method, endpoint=endpoint).time():
        response = await call_next(request)

    # .inc(): Adds 1 to your total request count.
    # Unlike the timer, the Status Code (e.g., 200, 404, 500) is only known after the request finishes. By including it here, you can create a dashboard that shows your "Error Rate" (percentage of 500s vs 200s).
    REQUEST_COUNT.labels(
        method = method,
        endpoint = endpoint,
        status = response.status_code
    ).inc()

    # Crucial step: This sends the result back to the user's browser. If you forgot this line, the user would wait forever and eventually get a timeout error.
    return response

# metric endpoint
# the metrics_endpoint is the "output valve" of your monitoring system. While your middleware spends its time collecting data, this function is responsible for reporting that data to the outside world in a format that Prometheus can understand.
def metrics_endpoint():
    # This is a standard FastAPI/Starlette response object. It wraps the text data so it can be sent over the network.
    return Response(
        # This function scans all the metrics you've defined in your app (like REQUEST_COUNT and REQUEST_LATENCY).
        # It aggregates the current values and converts them into the official Prometheus Text Format (a specific plain-text structure).
        generate_latest(),
        # This sets the HTTP header Content-Type
        # In 2026, Prometheus expects a specific header (usually text/plain; version=0.0.4). CONTENT_TYPE_LATEST is a constant provided by the Prometheus library that ensures you are always using the correct, up-to-date version.
        media_type=CONTENT_TYPE_LATEST
    )