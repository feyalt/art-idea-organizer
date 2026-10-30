
"""Integration tests for the Flask application."""


def test_health_endpoint(client):
    """The health endpoint responds successfully."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}
