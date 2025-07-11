from fastapi import FastAPI

from app.app_factory import create_app


def test_create_app_returns_fastapi_instance():
    """
    Ensure the application factory returns a FastAPI app instance.
    """
    app = create_app(config_path="tests/test_config.yml")
    assert isinstance(app, FastAPI)


def test_app_metadata_matches_config():
    """
    Ensure FastAPI app metadata matches the test config file.
    """
    app = create_app(config_path="tests/test_config.yml")

    assert app.title == "Test API"
    assert app.description == "API for testing"
    assert app.version == "0.1.0"
    assert app.docs_url == "/docs"
    assert app.redoc_url == "/redoc"
    assert app.openapi_url == "/openapi.json"
    assert app.debug is True


def test_app_has_routes():
    """
    Ensure the app has at least one registered route from the router.
    """
    app = create_app(config_path="tests/test_config.yml")

    route_paths = [route.path for route in app.routes]
    assert any(route_paths)
