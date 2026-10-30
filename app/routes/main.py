
"""Routes for the main idea archive."""

from flask import Blueprint, render_template, request

from app.models import Collection, Medium
from app.services.search_service import SearchService


main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    """Display ideas with combined search and filters."""
    query = request.args.get("q", "").strip()
    medium_id = request.args.get("medium_id", type=int)
    collection_id = request.args.get("collection_id", type=int)
    color = request.args.get("color", "").strip()

    ideas = SearchService.search(
        query=query,
        medium_id=medium_id,
        collection_id=collection_id,
        color=color,
    )

    return render_template(
        "index.html",
        ideas=ideas,
        query=query,
        selected_medium=medium_id,
        selected_collection=collection_id,
        color=color,
        mediums=Medium.query.order_by(Medium.name).all(),
        collections=Collection.query.order_by(Collection.name).all(),
    )
