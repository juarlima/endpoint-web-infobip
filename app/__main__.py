"""Run flask app."""

# pylint: disable=import-outside-toplevel

import os
import sys

try:
    import newrelic.agent

    newrelic.agent.initialize(f"{os.getcwd()}/newrelic.ini")
except Exception as exc:  # pylint: disable=broad-except
    print(f"Warning: newrelic initialization failed: {exc}", file=sys.stderr)


from . import create_app  # noqa: E402

app = create_app()


if __name__ == "__main__":  # Only in dev
    app.run(host="0.0.0.0", port=8080, debug=True)  # nosec
