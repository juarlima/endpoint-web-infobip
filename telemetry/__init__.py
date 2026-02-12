"""Telemetry module for OpenTelemetry metrics."""

from telemetry.metrics import (
    increment_http_request_handled,
    record_latency_operation_a,
    register_asynchronous_gauge,
)

__all__ = [
    "increment_http_request_handled",
    "record_latency_operation_a",
    "register_asynchronous_gauge",
]
