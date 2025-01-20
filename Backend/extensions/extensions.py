from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize Flask-Limiter with Redis storage.
# Flask-Limiter allows you to use a decorator in routes so that calls to that route are limited.
limiter = Limiter(
    get_remote_address,
    storage_uri="redis://redis:6379/0"  # This automatically uses Redis for rate-limiting
)