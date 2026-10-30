
"""Routes for managing art mediums."""

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from sqlalchemy import func, select

from app.extensions import db
from app.models import Medium


mediums_bp = Blueprint("mediums", __name__, url_prefix="/mediums")


@mediums_bp.get("/")
def index():
    """Display all mediums."""
    mediums = db.session.scalars(
        select(Medium).order_by(func.lower(Medium.name))
    ).all()

    return render_template("mediums.html", mediums=mediums)


@mediums_bp.post("/new")
def create():
    """Create a new medium."""
    name = request.form.get("name", "").strip()

    if not name:
        flash("Please enter a medium name.", "error")
        return redirect(url_for("mediums.index"))

    if len(name) > 80:
        flash("Medium names must be 80 characters or fewer.", "error")
        return redirect(url_for("mediums.index"))

    existing = db.session.scalar(
        select(Medium).where(func.lower(Medium.name) == name.lower())
    )

    if existing:
        flash("That medium already exists.", "error")
        return redirect(url_for("mediums.index"))

    medium = Medium(name=name)
    db.session.add(medium)
    db.session.commit()

    flash("Medium added successfully.", "success")
    return redirect(url_for("mediums.index"))



@mediums_bp.post("/<int:medium_id>/edit")
def edit(medium_id):
    """Rename an existing medium."""
    medium = db.session.get(Medium, medium_id)

    if medium is None:
        abort(404)

    name = request.form.get("name", "").strip()

    if not name:
        flash("Please enter a medium name.", "error")
        return redirect(url_for("mediums.index"))

    if len(name) > 80:
        flash("Medium names must be 80 characters or fewer.", "error")
        return redirect(url_for("mediums.index"))

    existing = db.session.scalar(
        select(Medium).where(
            func.lower(Medium.name) == name.lower(),
            Medium.id != medium.id,
        )
    )

    if existing:
        flash("A medium with that name already exists.", "error")
        return redirect(url_for("mediums.index"))

    medium.name = name
    db.session.commit()

    flash("Medium updated successfully.", "success")
    return redirect(url_for("mediums.index"))


@mediums_bp.post("/<int:medium_id>/delete")
def delete(medium_id):
    """Delete a medium without deleting its associated ideas."""
    medium = db.session.get(Medium, medium_id)

    if medium is None:
        abort(404)

    db.session.delete(medium)
    db.session.commit()

    flash("Medium deleted.", "success")
    return redirect(url_for("mediums.index"))
