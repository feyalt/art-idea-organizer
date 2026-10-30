# How to Run

This guide explains how to set up and run Art Idea Organizer & Archive locally.

## Prerequisites

Before getting started, ensure the following are installed:

- **Python** — Required to run the Flask application.
- **Git** — Required to clone the repository.

## 1. Clone the Repository

Clone the repository and navigate into the project directory:

```bash
cd art-idea-organizer
```

## 2. Create a Virtual Environment

Create an isolated Python virtual environment:

```bash
python3 -m venv .venv
```

Activate the environment:

**macOS / Linux**
```bash
source .venv/bin/activate
```

**Windows**
```bash
.venv\Scripts\activate
```

## 3. Install Dependencies

Install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a local `.env` file using the provided example:

```bash
cp .env.example .env
```

Open `.env` and configure the application environment variables:

- **`SECRET_KEY`** — Secret key used by Flask for session security.
- **`DATABASE_URL`** — Database connection string. The application uses SQLite by default.
- **`FLASK_DEBUG`** — Controls whether Flask debug mode is enabled.

For local development, use a secure development secret key and the default SQLite database configuration unless you have a reason to change them.

The `.env` file contains local configuration and should not be committed to version control.

## 5. Initialize the Database

Apply the existing database migrations to create the required tables:

```bash
flask --app run.py db upgrade
```

This applies the migration scripts in the `migrations/` directory to the configured database.

## 6. Run the Application

Start the Flask application:

```bash
python run.py
```

Once the application is running, open the local development address in your browser:

```text
http://127.0.0.1:5000/
```

To verify that the application is running, visit the health-check endpoint:

```text
http://127.0.0.1:5000/health
```

A successful response returns:

```json
{
  "status": "ok"
}
```

## 7. Run the Tests

The project uses `pytest` for automated unit and integration testing.

To run the entire test suite from the project root directory:

```bash
pytest
```

To run only unit tests:

```bash
pytest tests/unit/
```

To run only integration tests:

```bash
pytest tests/integration/
```

For more information about the test suite, see the [Tests Documentation](../tests/README.md).

## Troubleshooting

- **Missing dependencies:** Ensure that the virtual environment is activated and that the dependencies have been installed.
- **Database errors:** Verify that the environment variables are configured correctly and that the database migrations have been applied.
- **Application startup issues:** Check the terminal output for error messages and confirm that the required packages are installed.