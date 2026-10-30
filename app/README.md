# Application Package

This directory contains the core Flask application, including application initialization, configuration, and shared extensions.

## Files

### `__init__.py`

Defines the Flask application factory through `create_app()`. It creates and configures the application instance, initializes the SQLAlchemy and Flask-Migrate extensions, imports the database models, and registers the route blueprints. It also defines a `/health` endpoint to confirm that the application is running.

### `config.py`

Defines the application's default configuration through the `Config` class. It manages the Flask secret key, database connection, and debug mode using environment variables, with local development defaults where applicable.

### `extensions.py`

Defines the shared Flask extensions used throughout the application. SQLAlchemy (`db`) provides database access and ORM functionality, while Flask-Migrate (`migrate`) handles database migrations. These extensions are initialized separately so they can be connected to the application through the application factory.

## Directories

- **`routes/`** — Contains the Flask blueprints responsible for application routes and request handling.
- **`models/`** — Contains the SQLAlchemy models that define the application's database structure.
- **`services/`** — Contains reusable application-level operations and business logic.
- **`templates/`** — Contains the Jinja templates used to render the application's HTML pages.
- **`static/`** — Contains the application's static assets, including CSS stylesheets, JavaScript files, and images.