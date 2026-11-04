# Tests

This directory contains the automated test suite for the application. Tests are written using `pytest` and organized into unit and integration tests.

Current code coverage is 92%

## Structure

- **`unit/`** — Tests individual application components, including services and database models.
- **`integration/`** — Tests interactions between application components, including application routes and HTTP requests.
- **`conftest.py`** — Defines shared pytest fixtures, including an isolated Flask application and test client.

## Running Tests

From the project root directory, activate your virtual environment and install the project dependencies.

Run the entire test suite:

```bash
pytest