from .base import *  # noqa: F403

MIDDLEWARE.append("api.middleware.RangesMiddleware")  # noqa: F405
CORS_ORIGIN_WHITELIST = (
    "http://127.0.0.1:3000", "http://0.0.0.0:3000", "http://localhost:3000", "http://localhost:8000",
    "http://localhost:9004", "http://localhost:9003", "http://47.103.76.95:9003", "http://47.103.76.95:9004")
CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST
