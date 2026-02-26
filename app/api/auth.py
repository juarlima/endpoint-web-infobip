"""API Key authentication middleware."""

import os
from functools import wraps
from http import HTTPStatus

from flask import request


def require_api_key(f):
    """Decorator that validates the X-API-Key header against the API_KEY env var."""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Security: API key read from environment, never hardcoded
        expected_key = os.getenv("API_KEY")

        if not expected_key:
            return {"error": "API key not configured on server"}, HTTPStatus.INTERNAL_SERVER_ERROR

        provided_key = request.headers.get("X-API-Key") or request.args.get("api_key")

        if not provided_key:
            return {"error": "Missing API key (header X-API-Key or query param api_key)"}, HTTPStatus.UNAUTHORIZED

        if provided_key != expected_key:
            return {"error": "Invalid API key"}, HTTPStatus.UNAUTHORIZED

        return f(*args, **kwargs)

    return decorated
