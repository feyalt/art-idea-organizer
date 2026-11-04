"""Tests for medium management routes."""

from app.extensions import db
from app.models import Medium
from bs4 import BeautifulSoup


def test_mediums_index(client, app):
    """The mediums page displays mediums in alphabetical order."""
    with app.app_context():
        db.session.add_all([
            Medium(name="Watercolor"),
            Medium(name="Acrylic"),
            Medium(name="Charcoal"),
        ])
        db.session.commit()

    response = client.get("/mediums/")

    assert response.status_code == 200

    soup = BeautifulSoup(response.data, "html.parser")
    names = [
        element.get_text(strip=True)
        for element in soup.select("[data-medium-name]")
    ]

    assert names == ["Acrylic", "Charcoal", "Watercolor"]


def test_create_medium(client, app):
    """A valid medium can be created."""
    response = client.post("/mediums/new", data={"name": "Watercolor"})

    assert response.status_code == 302
    assert response.location.endswith("/mediums/")

    with app.app_context():
        medium = db.session.scalar(
            db.select(Medium).where(Medium.name == "Watercolor")
        )
        assert medium is not None


def test_create_medium_with_empty_name(client, app):
    """A medium cannot be created without a name."""
    response = client.post("/mediums/new", data={"name": "   "})

    assert response.status_code == 302

    with app.app_context():
        assert db.session.scalar(db.select(Medium)) is None


def test_create_medium_with_name_over_80_characters(client, app):
    """A medium name cannot exceed 80 characters."""
    response = client.post("/mediums/new", data={"name": "A" * 81})

    assert response.status_code == 302

    with app.app_context():
        assert db.session.scalar(db.select(Medium)) is None


def test_create_duplicate_medium(client, app):
    """Medium names must be unique, regardless of capitalization."""
    with app.app_context():
        db.session.add(Medium(name="Watercolor"))
        db.session.commit()

    response = client.post("/mediums/new", data={"name": "watercolor"})

    assert response.status_code == 302

    with app.app_context():
        mediums = db.session.scalars(db.select(Medium)).all()
        assert len(mediums) == 1


def test_edit_medium(client, app):
    """An existing medium can be renamed."""
    with app.app_context():
        medium = Medium(name="Pencil")
        db.session.add(medium)
        db.session.commit()
        medium_id = medium.id

    response = client.post(
        f"/mediums/{medium_id}/edit",
        data={"name": "Colored Pencil"},
    )

    assert response.status_code == 302

    with app.app_context():
        medium = db.session.get(Medium, medium_id)
        assert medium.name == "Colored Pencil"


def test_edit_medium_with_empty_name(client, app):
    """A medium cannot be renamed to an empty name."""
    with app.app_context():
        medium = Medium(name="Pencil")
        db.session.add(medium)
        db.session.commit()
        medium_id = medium.id

    response = client.post(
        f"/mediums/{medium_id}/edit",
        data={"name": ""},
    )

    assert response.status_code == 302

    with app.app_context():
        medium = db.session.get(Medium, medium_id)
        assert medium.name == "Pencil"


def test_edit_medium_with_name_over_80_characters(client, app):
    """A medium cannot be renamed to a name longer than 80 characters."""
    with app.app_context():
        medium = Medium(name="Pencil")
        db.session.add(medium)
        db.session.commit()
        medium_id = medium.id

    response = client.post(
        f"/mediums/{medium_id}/edit",
        data={"name": "A" * 81},
    )

    assert response.status_code == 302

    with app.app_context():
        medium = db.session.get(Medium, medium_id)
        assert medium.name == "Pencil"


def test_edit_medium_to_duplicate_name(client, app):
    """A medium cannot be renamed to another medium's name."""
    with app.app_context():
        db.session.add_all([
            Medium(name="Pencil"),
            Medium(name="Watercolor"),
        ])
        db.session.commit()
        medium = db.session.scalar(
            db.select(Medium).where(Medium.name == "Pencil")
        )
        medium_id = medium.id

    response = client.post(
        f"/mediums/{medium_id}/edit",
        data={"name": "watercolor"},
    )

    assert response.status_code == 302

    with app.app_context():
        medium = db.session.get(Medium, medium_id)
        assert medium.name == "Pencil"


def test_edit_nonexistent_medium(client):
    """Editing a medium that does not exist returns a 404."""
    response = client.post(
        "/mediums/9999/edit",
        data={"name": "Watercolor"},
    )

    assert response.status_code == 404


def test_delete_medium(client, app):
    """An existing medium can be deleted."""
    with app.app_context():
        medium = Medium(name="Charcoal")
        db.session.add(medium)
        db.session.commit()
        medium_id = medium.id

    response = client.post(f"/mediums/{medium_id}/delete")

    assert response.status_code == 302

    with app.app_context():
        assert db.session.get(Medium, medium_id) is None


def test_delete_nonexistent_medium(client):
    """Deleting a medium that does not exist returns a 404."""
    response = client.post("/mediums/9999/delete")

    assert response.status_code == 404