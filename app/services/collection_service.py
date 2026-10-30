
"""Business operations for collections."""

from sqlalchemy import select

from app.extensions import db
from app.models import Collection, ProjectIdea


class CollectionService:
    """Create collections and manage their ideas."""

    @staticmethod
    def create(name, description=""):
        """Create a collection with a unique, nonempty name."""
        name = name.strip() if name else ""

        if not name:
            raise ValueError("A collection must have a name.")

        existing = db.session.scalar(
            select(Collection).where(Collection.name == name)
        )

        if existing is not None:
            raise ValueError("A collection with this name already exists.")

        collection = Collection(
            name=name,
            description=description.strip() if description else "",
        )

        db.session.add(collection)
        db.session.commit()

        return collection

    @staticmethod
    def get_by_id(collection_id):
        """Return a collection by ID, or None if it does not exist."""
        return db.session.get(Collection, collection_id)

    @staticmethod
    def list_all():
        """Return collections in alphabetical order."""
        statement = select(Collection).order_by(Collection.name.asc())
        return db.session.scalars(statement).all()

    @staticmethod
    def add_idea(collection_id, idea_id):
        """Add an existing idea to a collection."""
        collection = db.session.get(Collection, collection_id)
        idea = db.session.get(ProjectIdea, idea_id)

        if collection is None or idea is None:
            return False

        if idea not in collection.ideas:
            collection.ideas.append(idea)
            db.session.commit()

        return True

    @staticmethod
    def remove_idea(collection_id, idea_id):
        """Remove an idea from a collection without deleting the idea."""
        collection = db.session.get(Collection, collection_id)
        idea = db.session.get(ProjectIdea, idea_id)

        if collection is None or idea is None:
            return False

        if idea in collection.ideas:
            collection.ideas.remove(idea)
            db.session.commit()

        return True

    @staticmethod
    def delete(collection_id):
        """Delete a collection without deleting its ideas."""
        collection = db.session.get(Collection, collection_id)

        if collection is None:
            return False

        db.session.delete(collection)
        db.session.commit()

        return True
