# Database Migrations

This directory contains the Alembic configuration and migration scripts used by Flask-Migrate to track changes to the application's database schema.

## Files

- **`alembic.ini`** — Provides Alembic configuration and logging settings.
- **`env.py`** — Configures the migration environment, connects Alembic to the Flask application and SQLAlchemy database, and supports offline and online migrations.
- **`script.py.mako`** — Template used to generate new migration scripts.
- **`versions/`** — Contains individual migration scripts that define database schema changes.

## Initial Migration

The initial migration creates the application's database tables, including projects, collections, mediums, color palettes, reference images, and their associated relationships.

Each migration includes an `upgrade()` function to apply changes and a `downgrade()` function to reverse them.