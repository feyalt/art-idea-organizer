
"""Tests for database models and their relationships."""

from app.extensions import db
from app.models import (
    Collection,
    ColorPalette,
    Medium,
    PaletteColor,
    ProjectIdea,
    ReferenceImage,
)


def test_create_idea(app):
    """An idea can be saved and retrieved."""
    idea = ProjectIdea(
        title="Moonlit Garden",
        description="A study of flowers under moonlight.",
    )

    db.session.add(idea)
    db.session.commit()

    saved_idea = db.session.get(ProjectIdea, idea.id)

    assert saved_idea is not None
    assert saved_idea.title == "Moonlit Garden"
    assert saved_idea.description == "A study of flowers under moonlight."


def test_idea_can_have_multiple_mediums(app):
    """An idea can be associated with multiple art mediums."""
    idea = ProjectIdea(title="Botanical Study")
    watercolor = Medium(name="Watercolor")
    pencil = Medium(name="Colored Pencil")

    idea.mediums.extend([watercolor, pencil])
    db.session.add(idea)
    db.session.commit()

    saved_idea = db.session.get(ProjectIdea, idea.id)

    assert {medium.name for medium in saved_idea.mediums} == {
        "Watercolor",
        "Colored Pencil",
    }


def test_idea_can_belong_to_multiple_collections(app):
    """An idea can appear in more than one collection."""
    idea = ProjectIdea(title="Landscape Concept")
    nature = Collection(name="Nature")
    favorites = Collection(name="Favorites")

    idea.collections.extend([nature, favorites])
    db.session.add(idea)
    db.session.commit()

    saved_idea = db.session.get(ProjectIdea, idea.id)

    assert {collection.name for collection in saved_idea.collections} == {
        "Nature",
        "Favorites",
    }


def test_idea_can_have_palette_and_reference(app):
    """An idea can store colors and external image references."""
    idea = ProjectIdea(title="Autumn Illustration")

    palette = ColorPalette(name="Autumn", colors=[
        PaletteColor(hex_code="#C65D3A", position=0),
        PaletteColor(hex_code="#E4B363", position=1),
    ])

    reference = ReferenceImage(
        url="https://example.com/autumn.jpg",
        caption="Autumn leaves",
    )

    idea.palettes.append(palette)
    idea.reference_images.append(reference)

    db.session.add(idea)
    db.session.commit()

    saved_idea = db.session.get(ProjectIdea, idea.id)

    assert len(saved_idea.palettes) == 1
    assert len(saved_idea.palettes[0].colors) == 2
    assert saved_idea.palettes[0].colors[0].hex_code == "#C65D3A"
    assert saved_idea.reference_images[0].caption == "Autumn leaves"
