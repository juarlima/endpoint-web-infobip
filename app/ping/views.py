"""Module with ping endpoint."""

from flask import Blueprint

try:
    import newrelic.agent
    _has_newrelic = True
except ImportError:
    _has_newrelic = False


ping = Blueprint("ping", __name__)


@ping.route("/ping")
def main():
    """Ping endpoint, used to know if the app is up."""
    if _has_newrelic:
        newrelic.agent.ignore_transaction(flag=True)
    return "pong"
