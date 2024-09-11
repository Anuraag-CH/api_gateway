from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi_limiter import Limiter
from fastapi_limiter.depends import RateLimiter
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time

app = FastAPI()

limiter = Limiter(
    key_func=lambda: "user_id",
    default_limits=["5 per minute"]
)

@app.middleware("http")
async def add_rate_limiter(request: Request, call_next):
    return await limiter(request=request, call_next=call_next)

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 10, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        if client_ip not in self.requests:
            self.requests[client_ip] = []

        self.requests[client_ip] = [t for t in self.requests[client_ip] if current_time - t < self.window_seconds]

        if len(self.requests[client_ip]) >= self.max_requests:
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

        self.requests[client_ip].append(current_time)
        return await call_next(request)

@app.get("/items/", dependencies=[Depends(RateLimiter(times=5, seconds=1))])
async def read_items():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]
