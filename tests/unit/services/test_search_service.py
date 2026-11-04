
"""Tests for SearchService."""

from app.extensions import db
from app.models import (
    Collection,
    ColorPalette,
    Medium,
    PaletteColor,
    ProjectIdea,
)
from app.services.search_service import SearchService


def create_sample_idea(title, description=""):
    """Create and persist a basic idea for testing."""
    idea = ProjectIdea(title=title, description=description)
    db.session.add(idea)
    db.session.flush()
    return idea


def test_search_matches_title_and_description(app):
    create_sample_idea("Moonlit Garden")
    create_sample_idea("Landscape", "A garden full of flowers.")

    results = SearchService.search("garden")

    assert {idea.title for idea in results} == {
        "Moonlit Garden",
        "Landscape",
    }


def test_search_matches_medium(app):
    idea = create_sample_idea("Botanical Study")
    watercolor = Medium(name="Watercolor")
    idea.mediums.append(watercolor)
    db.session.commit()

    results = SearchService.search("watercolor")

    assert [result.title for result in results] == ["Botanical Study"]



def test_filter_by_collection(app):
    idea = create_sample_idea("Forest Sketch")
    collection = Collection(name="Nature")

    db.session.add(collection)
    db.session.flush()

    collection.ideas.append(idea)
    db.session.commit()

    results = SearchService.search(collection_id=collection.id)

    assert [result.title for result in results] == ["Forest Sketch"]


def test_filter_by_color(app):
    idea = create_sample_idea("Autumn Leaves")
    palette = ColorPalette(
        name="Autumn",
        colors=[PaletteColor(hex_code="#C65D3A", position=0)],
    )
    idea.palettes.append(palette)
    db.session.commit()

    results = SearchService.search(color="#C65D3A")

    assert [result.title for result in results] == ["Autumn Leaves"]


def test_search_combines_filters(app):
    watercolor = Medium(name="Watercolor")
    collection = Collection(name="Botanical Studies")

    matching = create_sample_idea("Flowers in Spring")
    matching.mediums.append(watercolor)
    matching.collections.append(collection)

    other = create_sample_idea("Flowers in Ink")
    other.mediums.append(Medium(name="Ink"))

    db.session.commit()

    results = SearchService.search(
        query="flowers",
        medium_id=watercolor.id,
        collection_id=collection.id,
    )

    assert [idea.title for idea in results] == ["Flowers in Spring"]


def test_search_without_criteria_returns_all_ideas(app):
    create_sample_idea("First Idea")
    create_sample_idea("Second Idea")

    results = SearchService.search()

    assert {idea.title for idea in results} == {
        "First Idea",
        "Second Idea",
    }


def test_search_with_no_matches_returns_empty_list(app):
    create_sample_idea("Landscape")

    assert SearchService.search("nonexistent") == []
