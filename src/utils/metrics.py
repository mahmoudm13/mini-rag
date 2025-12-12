from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from typing import Callable, Awaitable
import time

# Define metrics
REQUEST_COUNT = Counter(
    name="http_requests_total", 
    documentation="Total HTTP Requests", 
    labelnames=["method", "endpoint", "status"],
)
REQUEST_LATENCY = Histogram(
    name="https_request_duration_seconds",
    documentation="HTTP Request Latency",
    labelnames=["method", "endpoint"],
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        
        start_time = time.time()
        
        response = await call_next(request)
        
        duration = time.time() - start_time
        endpoint = request.url.path
        
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status=response.status_code).inc()
        REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(duration)
        
        return response

def setup_metrics(app: FastAPI):
    """
    Setup Prometheus metrics middleware and endpoint
    """
    app.add_middleware(PrometheusMiddleware)
    
    @app.get("/Tssldjkf_sd39fj_dlsklkj", include_in_schema=False)
    def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
