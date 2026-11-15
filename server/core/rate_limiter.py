from fastapi import Request
from slowapi import Limiter

from config import settings


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"

limiter = Limiter(
    key_func=get_client_ip,
    storage_uri=settings.redis_url,
    default_limits=["15/minute", "200/hour", "1000/day"],
)
