
"""Routes for managing reference images."""

from urllib.parse import urlparse

from flask import Blueprint, abort, flash, redirect, request, url_for

from app.extensions import db
from app.models import ProjectIdea, ReferenceImage


references_bp = Blueprint("references", __name__)


def is_valid_image_url(url):
    """Check that a reference URL uses HTTP or HTTPS."""
    parsed = urlparse(url)

    return (
        parsed.scheme in {"http", "https"}
        and bool(parsed.netloc)
        and not any(char.isspace() for char in url)
    )


@references_bp.post("/ideas/<int:idea_id>/references")
def create_reference(idea_id):
    """Attach a reference image URL to an idea."""
    idea = db.session.get(ProjectIdea, idea_id)

    if idea is None:
        abort(404)

    url = request.form.get("url", "").strip()
    caption = request.form.get("caption", "").strip()

    if not is_valid_image_url(url):
        flash("Enter a valid HTTP or HTTPS image URL.", "error")
        return redirect(url_for("ideas.idea_detail", idea_id=idea_id))

    if len(url) > 2048:
        flash("The image URL is too long.", "error")
        return redirect(url_for("ideas.idea_detail", idea_id=idea_id))

    if len(caption) > 255:
        flash("The caption must be 255 characters or fewer.", "error")
        return redirect(url_for("ideas.idea_detail", idea_id=idea_id))

    reference = ReferenceImage(
        url=url,
        caption=caption,
        position=len(idea.reference_images),
        idea=idea,
    )

    db.session.add(reference)
    db.session.commit()

    flash("Reference image added.", "success")
    return redirect(url_for("ideas.idea_detail", idea_id=idea_id))


@references_bp.post("/references/<int:reference_id>/delete")
def delete_reference(reference_id):
    """Remove a reference image."""
    reference = db.session.get(ReferenceImage, reference_id)

    if reference is None:
        abort(404)

    idea_id = reference.idea_id

    db.session.delete(reference)
    db.session.commit()

    flash("Reference image removed.", "success")
    return redirect(url_for("ideas.idea_detail", idea_id=idea_id))
