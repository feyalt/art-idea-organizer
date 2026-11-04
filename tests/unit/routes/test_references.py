"""Tests for reference image routes."""

import pytest
from sqlalchemy import select

from app.extensions import db
from app.models import ProjectIdea, ReferenceImage
from app.routes.references import is_valid_image_url


@pytest.mark.parametrize("url", [
    "https://example.com/image.jpg",
    "http://example.com/image.png",
])
def test_valid_image_url(url):
    """HTTP and HTTPS image URLs are accepted."""
    assert is_valid_image_url(url)


@pytest.mark.parametrize("url", [
    "",
    "example.com/image.jpg",
    "ftp://example.com/image.jpg",
    "javascript:alert(1)",
    "https:///image.jpg",
    "https://example.com/my image.jpg",
])
def test_invalid_image_url(url):
    """URLs without a valid HTTP or HTTPS address are rejected."""
    assert not is_valid_image_url(url)


def test_create_reference(client, app):
    """A valid reference image can be added to an idea."""
    with app.app_context():
        idea = ProjectIdea(title="Autumn Illustration")
        db.session.add(idea)
        db.session.commit()
        idea_id = idea.id

    response = client.post(
        f"/ideas/{idea_id}/references",
        data={"url": "https://example.com/autumn.jpg", "caption": "Autumn leaves"},
    )

    assert response.status_code == 302

    with app.app_context():
        reference = db.session.scalar(
            select(ReferenceImage).where(ReferenceImage.idea_id == idea_id)
        )
        assert reference is not None
        assert reference.url == "https://example.com/autumn.jpg"
        assert reference.caption == "Autumn leaves"
        assert reference.position == 0


def test_create_reference_without_caption(client, app):
    """A reference image can be added without a caption."""
    with app.app_context():
        idea = ProjectIdea(title="Landscape Study")
        db.session.add(idea)
        db.session.commit()
        idea_id = idea.id

    response = client.post(
        f"/ideas/{idea_id}/references",
        data={"url": "https://example.com/landscape.jpg"},
    )

    assert response.status_code == 302

    with app.app_context():
        reference = db.session.scalar(
            select(ReferenceImage).where(ReferenceImage.idea_id == idea_id)
        )
        assert reference is not None
        assert reference.caption == ""


def test_create_reference_with_invalid_url(client, app):
    """A reference with an invalid URL is rejected."""
    with app.app_context():
        idea = ProjectIdea(title="Landscape Study")
        db.session.add(idea)
        db.session.commit()
        idea_id = idea.id

    response = client.post(
        f"/ideas/{idea_id}/references",
        data={"url": "ftp://example.com/image.jpg"},
    )

    assert response.status_code == 302

    with app.app_context():
        assert db.session.scalar(select(ReferenceImage)) is None


def test_create_reference_with_url_over_2048_characters(client, app):
    """A reference URL cannot exceed 2048 characters."""
    with app.app_context():
        idea = ProjectIdea(title="Landscape Study")
        db.session.add(idea)
        db.session.commit()
        idea_id = idea.id

    url = "https://example.com/" + "a" * 2048
    response = client.post(
        f"/ideas/{idea_id}/references",
        data={"url": url},
    )

    assert response.status_code == 302

    with app.app_context():
        assert db.session.scalar(select(ReferenceImage)) is None


def test_create_reference_with_caption_over_255_characters(client, app):
    """A reference caption cannot exceed 255 characters."""
    with app.app_context():
        idea = ProjectIdea(title="Landscape Study")
        db.session.add(idea)
        db.session.commit()
        idea_id = idea.id

    response = client.post(
        f"/ideas/{idea_id}/references",
        data={
            "url": "https://example.com/image.jpg",
            "caption": "A" * 256,
        },
    )

    assert response.status_code == 302

    with app.app_context():
        assert db.session.scalar(select(ReferenceImage)) is None


def test_create_reference_for_nonexistent_idea(client):
    """A reference cannot be added to an idea that does not exist."""
    response = client.post(
        "/ideas/9999/references",
        data={"url": "https://example.com/image.jpg"},
    )

    assert response.status_code == 404


def test_create_reference_uses_next_position(client, app):
    """New references are assigned the next available position."""
    with app.app_context():
        idea = ProjectIdea(title="Landscape Study")
        idea.reference_images.append(ReferenceImage(
            url="https://example.com/first.jpg",
            caption="First image",
            position=0,
        ))
        db.session.add(idea)
        db.session.commit()
        idea_id = idea.id

    response = client.post(
        f"/ideas/{idea_id}/references",
        data={"url": "https://example.com/second.jpg"},
    )

    assert response.status_code == 302

    with app.app_context():
        references = db.session.scalars(
            select(ReferenceImage)
            .where(ReferenceImage.idea_id == idea_id)
            .order_by(ReferenceImage.position)
        ).all()
        assert len(references) == 2
        assert [reference.position for reference in references] == [0, 1]


def test_delete_reference(client, app):
    """An existing reference image can be removed."""
    with app.app_context():
        idea = ProjectIdea(title="Autumn Illustration")
        idea.reference_images.append(ReferenceImage(
            url="https://example.com/autumn.jpg",
            caption="Autumn leaves",
        ))
        db.session.add(idea)
        db.session.commit()
        idea_id = idea.id
        reference_id = idea.reference_images[0].id

    response = client.post(f"/references/{reference_id}/delete")

    assert response.status_code == 302
    assert str(idea_id) in response.location

    with app.app_context():
        assert db.session.get(ReferenceImage, reference_id) is None
        assert db.session.get(ProjectIdea, idea_id) is not None


def test_delete_nonexistent_reference(client):
    """Deleting a reference that does not exist returns a 404."""
    response = client.post("/references/9999/delete")

    assert response.status_code == 404