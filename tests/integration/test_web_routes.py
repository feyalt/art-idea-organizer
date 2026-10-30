
"""Integration tests for the idea-management pages."""


def test_archive_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Your ideas" in response.data


def test_new_idea_form_loads(client):
    response = client.get("/ideas/new")

    assert response.status_code == 200
    assert b"Capture an idea" in response.data


def test_create_idea_through_form(client):
    response = client.post(
        "/ideas/new",
        data={
            "title": "Flowers after dark",
            "description": "A study of flowers in low light.",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Flowers after dark" in response.data
    assert b"Your idea has been saved." in response.data


def test_edit_idea_through_form(client):
    from app.services.idea_service import IdeaService

    idea = IdeaService.create("Original Title")

    response = client.post(
        f"/ideas/{idea.id}/edit",
        data={
            "title": "Updated Title",
            "description": "Updated description.",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Updated Title" in response.data


def test_delete_idea_through_form(client):
    from app.services.idea_service import IdeaService

    idea = IdeaService.create("Idea to Delete")

    response = client.post(
        f"/ideas/{idea.id}/delete",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Idea to Delete" not in response.data


def test_missing_idea_returns_404(client):
    response = client.get("/ideas/999")

    assert response.status_code == 404
