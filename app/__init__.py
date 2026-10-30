
"""Application package and Flask application factory."""

from pathlib import Path

from flask import Flask

from app.config import Config
from app.extensions import db, migrate


def create_app(config_class=Config):
    """Create and configure a Flask application instance."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config_class)

    # Ensure the instance directory exists for local application data.
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    # Initialize extensions after loading the application configuration.
    db.init_app(app)
    from app import models  # noqa: F401
    from app.routes.ideas import ideas_bp
    from app.routes.main import main_bp
    from app.routes.palettes import palettes_bp
    from app.routes.references import references_bp
    from app.routes.collections import collections_bp
    from app.routes.mediums import mediums_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(ideas_bp)
    app.register_blueprint(palettes_bp)
    app.register_blueprint(references_bp)
    app.register_blueprint(collections_bp)
    app.register_blueprint(mediums_bp)

    migrate.init_app(app, db)

    @app.get("/health")
    def health_check():
        """Return a simple response confirming that the app is running."""
        return {"status": "ok"}

    return app
