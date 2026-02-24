"""Flask app creation."""

import os

from flask import Flask

try:
    from opentelemetry.instrumentation.flask import FlaskInstrumentor
except ImportError:
    FlaskInstrumentor = None

from app.api import api_bp
from app.dummy import dummy
from app.ping import ping

# Active endpoints noted as following:
# (url_prefix, blueprint_object)
ACTIVE_ENDPOINTS = (("/", ping), ("/dummy", dummy), ("/api", api_bp))


def instrument_app(app: Flask) -> None:
    """Instrument app with OpenTelemetry."""
    enabled = os.getenv("OTEL_AGENT_ENABLED", "false")

    if enabled == "true" and FlaskInstrumentor is not None:
        FlaskInstrumentor().instrument_app(app)


def create_app() -> Flask:
    """Create Flask app."""
    app = Flask(__name__)

    # accepts both /endpoint and /endpoint/ as valid URLs
    app.url_map.strict_slashes = False

    # register each active blueprint
    for url, blueprint in ACTIVE_ENDPOINTS:
        app.register_blueprint(blueprint, url_prefix=url)

    instrument_app(app)

    return app
