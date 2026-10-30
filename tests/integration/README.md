# Integration Tests

This directory contains tests that verify interactions between application components, particularly Flask routes and HTTP requests.

## Test Files

- **`test_app.py`** — Tests the application's health endpoint and verifies that it returns the expected HTTP status code and JSON response.
- **`test_web_routes.py`** — Tests the application's web routes, including page loading, idea creation, editing, deletion, and handling requests for missing ideas.

## Running Integration Tests

From the project root directory, run:

```bash
pytest tests/integration/
```

To run a specific test file:

```bash
pytest tests/integration/test_web_routes.py
```

To run tests with more detailed output:

```bash
pytest tests/integration/ -v
```