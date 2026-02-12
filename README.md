# Python endpoint-web-infobip App

![technology Python](https://img.shields.io/badge/technology-python-blue.svg)

This is a basic python application created by Fury to be used as a starting point for your project.

## Setup endpoint_web_infobip

To install it just run:

```bash
# Install dependencies
poetry install
```

## Usage

You can run the Flask web app with:

```bash
# Activate the virtual environment and open a shell inside it
poetry shell

# Optional: Set Flask in debug mode
export FLASK_DEBUG=1

# Execute the Flask app
flask run
```

Finally you can check your app is running:

```bash
curl http://127.0.0.1:5000/dummy 
"Hello World."
```

### pre-commit

We encourage you to activate the [pre-commit hooks](https://github.com/pre-commit/pre-commit)
```bash
poetry run pre-commit install
```

## Testing endpoint_web_infobip

You can choose to test this module with **pytest** or **fury**.

### Pytest

```bash
# Install dependencies
poetry install

# Run the tests
poetry run pytest

# Another way to do the same
poetry shell
pytest
```

### Fury

```bash
fury test
```

## Setting Python version

By default, your app will run with Python 3.8 inside Fury. To change it, modify the tag in `Dockerfile` and `Dockerfile.runtime` to match the needed version.

**E.g.:**

`FROM hub.furycloud.io/mercadolibre/python:3.10-mini`

`FROM hub.furycloud.io/mercadolibre/python:3.10-mini-runtime`

### Available tags

You can find all available tags for your Dockerfile [here](https://github.com/mercadolibre/fury_python-mini-runtime#suported-tags)

## What's in this boilerplate

- *Requirement Management*: Install only what's needed where it's needed.
    - See [PEP-508](https://www.python.org/dev/peps/pep-0508).
    - Productive requirements will be located in `pyproject.toml` at tool.poetry.dependencies section.
        - Containing what's needed for your app during runtime.
    - Test requirements will be located in `pyproject.toml` at tool.poetry.dev-dependencies section.
        - Containing what's needed for running tests (during `fury test`, CI and app-version creation).
    - Development requirements will be located in `pyproject.toml` at tool.poetry.dev-dependencies section.
        - Here you can include development-only dependencies (such as linters, jupyter, etc).
- *Modularization*: Make your app scale easily.
    - `app` module contains a submodule that defines a [Flask Blueprint](https://flask.palletsprojects.com/en/1.1.x/blueprints/) object.
    - Each submodule defines a part of your app.
    - They must expose a `Blueprint` object in the `__init__.py`.
    - Define the views in the `views.py`.
    - The blueprint object must be added to `ACTIVE_ENDPOINTS` in `app/__init__.py` alongisde its url prefix in order to be accessible.
    - Removing a blueprint object disables that blueprint and all of its subroutes.
    - As examples, `ping` and `dummy` modules follow this rules and are registered by default.
- *Pre-commit hooks*: Automatic code analysis on your repository.
    - Tools to identify and fix coding-style issues with your code before submitting it to the repository.
    - Refer to [pre-commit repository](https://github.com/pre-commit/pre-commit).
    - By default, [flake8](http://flake8.pycqa.org/en/latest/) and [black](https://black.readthedocs.io/en/stable/) are added to enable consistent formatting and avoiding erroneous code to reach the repo (`black` requires python 3.6.0+ to run but it can reformat python2 code. Make sure you have Python3 in your system.).
    - See [this curated list](https://github.com/pre-commit/pre-commit-hooks) to add more hooks.
    - Although optional, these tools are highly recommended.
- *Tests*: Easily test your Flask app.
    - [pytest](https://docs.pytest.org/en/latest/) chosen as default testing tool.
    - Locate your tests on the `tests` repository.
    - Locate your pytest configuration on `tests/conftest.py`
    - Includes the [pytest-flask](https://pytest-flask.readthedocs.io/en/latest/) fixture to easily test flask functions.
    - Contains a basic test as an example
- *`Flask-RESTX`*: Extension to develop REST APIs.
    - Refer to the [documentation](https://flask-restx.readthedocs.io/en/latest/) to see all its features
    - As an example, the `dummy` module contains an example REST resource.
- *Python MELI Toolkit*: Python Tools for MercadoLibre's develop environment
    - See the full list [here](https://github.com/mercadolibre/fury_python-toolkit#python-official-toolkits)
    - Located in MercadoLibre's [PyPI](http://pypi.artifacts.furycloud.io/simple/)
    - Requirements already support them as a source, just add them to your `pyproject.toml`

## Newrelic integration

By default your app integrates with [newrelic](https://docs.newrelic.com/docs/apm/new-relic-apm/getting-started). This means that your scopes will have their own newrelic dashboards.

## Contact Us

- juarlima - author@mercadolibre.com
