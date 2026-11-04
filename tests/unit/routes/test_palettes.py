"""Tests for color palette routes."""

import pytest
from sqlalchemy import select

from app.extensions import db
from app.models import ColorPalette, PaletteColor, ProjectIdea


def test_create_palette(client, app):
    """A valid color palette can be added to an idea."""
    with app.app_context():
        idea = ProjectIdea(title="Autumn Illustration")
        db.session.add(idea)
        db.session.commit()
        idea_id = idea.id

    response = client.post(
        f"/ideas/{idea_id}/palettes",
        data={"palette_name": "Autumn", "colors": ["#c65d3a", "#e4b363"]},
    )

    assert response.status_code == 302
    assert str(idea_id) in response.location

    with app.app_context():
        palette = db.session.scalar(
            select(ColorPalette).where(ColorPalette.idea_id == idea_id)
        )
        assert palette is not None
        assert palette.name == "Autumn"
        assert [color.hex_code for color in palette.colors] == ["#C65D3A", "#E4B363"]
        assert [color.position for color in palette.colors] == [0, 1]


@pytest.mark.parametrize("data", [
    {"palette_name": "", "colors": ["#C65D3A"]},
    {"palette_name": "Autumn", "colors": []},
    {"palette_name": "Autumn", "colors": ["red"]},
    {"palette_name": "Autumn", "colors": ["#12345"]},
    {"palette_name": "Autumn", "colors": ["#GGGGGG"]},
    {"palette_name": "Autumn", "colors": ["#C65D3A"] * 13},
])
def test_create_palette_with_invalid_data(client, app, data):
    """Invalid palette names or colors are rejected."""
    with app.app_context():
        idea = ProjectIdea(title="Autumn Illustration")
        db.session.add(idea)
        db.session.commit()
        idea_id = idea.id

    response = client.post(f"/ideas/{idea_id}/palettes", data=data)

    assert response.status_code == 302

    with app.app_context():
        assert db.session.scalar(select(ColorPalette)) is None


def test_create_palette_for_nonexistent_idea(client):
    """A palette cannot be created for an idea that does not exist."""
    response = client.post(
        "/ideas/9999/palettes",
        data={"palette_name": "Autumn", "colors": ["#C65D3A"]},
    )

    assert response.status_code == 404


def test_edit_palette(client, app):
    """An existing palette can be updated with a new name and colors."""
    with app.app_context():
        idea = ProjectIdea(title="Autumn Illustration")
        palette = ColorPalette(
            name="Original",
            colors=[
                PaletteColor(hex_code="#000000", position=0),
                PaletteColor(hex_code="#FFFFFF", position=1),
            ],
        )
        idea.palettes.append(palette)
        db.session.add(idea)
        db.session.commit()
        idea_id = idea.id
        palette_id = palette.id

    response = client.post(
        f"/palettes/{palette_id}/edit",
        data={"palette_name": "Autumn", "colors": ["#c65d3a", "#e4b363"]},
    )

    assert response.status_code == 302
    assert str(idea_id) in response.location

    with app.app_context():
        palette = db.session.get(ColorPalette, palette_id)
        assert palette.name == "Autumn"
        assert [color.hex_code for color in palette.colors] == ["#C65D3A", "#E4B363"]
        assert [color.position for color in palette.colors] == [0, 1]


@pytest.mark.parametrize("data", [
    {"palette_name": "", "colors": ["#C65D3A"]},
    {"palette_name": "Autumn", "colors": []},
    {"palette_name": "Autumn", "colors": ["invalid"]},
    {"palette_name": "Autumn", "colors": ["#C65D3A"] * 13},
])
def test_edit_palette_with_invalid_data(client, app, data):
    """Invalid palette updates are rejected without changing the original palette."""
    with app.app_context():
        idea = ProjectIdea(title="Autumn Illustration")
        palette = ColorPalette(
            name="Original",
            colors=[PaletteColor(hex_code="#000000", position=0)],
        )
        idea.palettes.append(palette)
        db.session.add(idea)
        db.session.commit()
        palette_id = palette.id

    response = client.post(f"/palettes/{palette_id}/edit", data=data)

    assert response.status_code == 302

    with app.app_context():
        palette = db.session.get(ColorPalette, palette_id)
        assert palette.name == "Original"
        assert [color.hex_code for color in palette.colors] == ["#000000"]


def test_edit_nonexistent_palette(client):
    """Editing a palette that does not exist returns a 404."""
    response = client.post(
        "/palettes/9999/edit",
        data={"palette_name": "Autumn", "colors": ["#C65D3A"]},
    )

    assert response.status_code == 404


def test_delete_palette(client, app):
    """An existing palette can be deleted."""
    with app.app_context():
        idea = ProjectIdea(title="Autumn Illustration")
        idea.palettes.append(ColorPalette(
            name="Autumn",
            colors=[PaletteColor(hex_code="#C65D3A", position=0)],
        ))
        db.session.add(idea)
        db.session.commit()
        idea_id = idea.id
        palette_id = idea.palettes[0].id

    response = client.post(f"/palettes/{palette_id}/delete")

    assert response.status_code == 302
    assert str(idea_id) in response.location

    with app.app_context():
        assert db.session.get(ColorPalette, palette_id) is None
        assert db.session.get(ProjectIdea, idea_id) is not None


def test_delete_nonexistent_palette(client):
    """Deleting a palette that does not exist returns a 404."""
    response = client.post("/palettes/9999/delete")

    assert response.status_code == 404