
"""Application configuration."""

import os


class Config:
    """Default configuration for local development."""

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "development-only-key-change-before-deployment",
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///art_idea_organizer.db",
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"