from flask import Flask

from app.api import register_blueprints


def create_app() -> Flask:
    """
    Create and configure the Flask application.

    This function initializes the Flask app, registers all blueprints,
    and returns the app instance for use by a WSGI/ASGI server or main entrypoint.

    Returns:
        Flask: A configured Flask application instance.
    """
    app: Flask = Flask(__name__)
    register_blueprints(app)
    return app
