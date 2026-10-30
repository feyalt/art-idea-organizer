# Unit Tests

This directory contains tests for individual application components, focusing on service functionality, database models, and search operations.

## Test Files

- **`test_collection_service.py`** — Tests collection creation, validation, duplicate handling, idea associations, and deletion.
- **`test_idea_service.py`** — Tests idea creation, updating, deletion, retrieval, and input validation.
- **`test_models.py`** — Tests database model creation, persistence, and relationships between ideas, collections, mediums, palettes, and reference images.
- **`test_search_service.py`** — Tests searching and filtering ideas by title, description, medium, collection, and color, including combinations of filters.

## Running Unit Tests

From the project root directory, run:

```bash
pytest tests/unit/
```

To run a specific test file:

```bash
pytest tests/unit/test_idea_service.py
```

To run tests with more detailed output:

```bash
pytest tests/unit/ -v
```