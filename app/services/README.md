
# Application Services

## Overview

The application's service layer contains the business logic used to manage art ideas, collections, and search functionality.

Services act as an intermediary between the application's routes and database models. They handle operations such as creating records, updating relationships, validating input, retrieving data, and deleting records.

The application uses SQLAlchemy to interact with the database. Service methods perform database queries and modifications through the shared database session.

## Service Organization

The services are organized into separate modules based on their responsibilities:

| File | Service | Description |
|---|---|---|
| `idea_service.py` | IdeaService | Handles the creation, retrieval, updating, and deletion of art ideas, as well as color palette creation. |
| `collection_service.py` | CollectionService | Manages collections and their relationships with art ideas. |
| `search_service.py` | SearchService | Searches and filters ideas using text queries, mediums, collections, and colors. |

## Service Definitions

### 1. IdeaService

**File:** `idea_service.py`

IdeaService handles the primary operations involving art ideas. It also manages the assignment of mediums and collections and provides functionality for creating color palettes.

| Method | Description |
|---|---|
| `create()` | Creates an idea with a title, description, and optional mediums and collections. |
| `get_by_id()` | Retrieves an idea using its ID. |
| `list_all()` | Returns all ideas, ordered from newest to oldest. |
| `update()` | Updates an idea's details and assigned mediums and collections. |
| `delete()` | Deletes an idea and its dependent records. |
| `add_palette()` | Creates a named color palette containing individual colors for an idea. |

**Key responsibilities:**

- Validates that each idea has a nonempty title.
- Removes leading and trailing whitespace from submitted titles and descriptions.
- Associates ideas with existing mediums and collections using their database IDs.
- Updates existing idea information and its many-to-many relationships.
- Deletes ideas through the ORM, allowing configured cascading behavior to handle dependent records.
- Creates color palettes and their associated color records.

**Color palette validation:**

The `add_palette()` method performs additional validation when creating palettes:

- The associated idea must exist.
- Each palette must have a nonempty name.
- Colors must use the six-digit hexadecimal format (for example, `#AABBCC`).
- Valid color values are converted to uppercase before being stored.
- Each color receives a position based on its order in the submitted list.

The palette and its colors are saved together through a database commit.

### 2. CollectionService

**File:** `collection_service.py`

CollectionService manages collections and the relationships between collections and art ideas.

| Method | Description |
|---|---|
| `create()` | Creates a collection with a unique, nonempty name. |
| `get_by_id()` | Retrieves a collection using its ID. |
| `list_all()` | Returns all collections in alphabetical order. |
| `add_idea()` | Adds an existing idea to a collection. |
| `remove_idea()` | Removes an idea from a collection without deleting the idea. |
| `delete()` | Deletes a collection without deleting its associated ideas. |

**Key responsibilities:**

- Validates that collection names are not empty.
- Removes leading and trailing whitespace from names and descriptions.
- Prevents duplicate collection names.
- Retrieves collections in alphabetical order.
- Manages the many-to-many relationship between ideas and collections.
- Prevents duplicate associations when adding ideas to collections.
- Allows ideas to be removed from collections without deleting the underlying idea.

The `add_idea()` and `remove_idea()` methods verify that both records exist before modifying their relationship.

If either record cannot be found, these methods return `False`. Otherwise, they return `True`, including when the requested relationship already exists or has already been removed.

Deleting a collection only removes the collection itself. Its associated ideas remain in the database.

### 3. SearchService

**File:** `search_service.py`

SearchService handles searching and filtering art ideas using SQLAlchemy queries.

| Method | Description |
|---|---|
| `search()` | Retrieves ideas matching any combination of supported search criteria. |

The search method accepts four optional parameters:

| Parameter | Description |
|---|---|
| `query` | Searches idea titles, descriptions, medium names, collection names, and palette color values. |
| `medium_id` | Filters ideas associated with a specific medium. |
| `collection_id` | Filters ideas belonging to a specific collection. |
| `color` | Filters ideas containing a matching hexadecimal color value. |

**Search functionality:**

The service supports combining multiple search criteria within a single query.

For example, users can search for a keyword while also filtering by a specific medium and collection.

Text searches use SQLAlchemy's `ilike()` operator, allowing case-insensitive partial matching.

The search query checks the following fields:

- Idea titles
- Idea descriptions
- Associated medium names
- Associated collection names
- Color values within associated palettes

Medium and collection filters use relationship-based queries to find ideas associated with the selected records.

Color filtering checks the hexadecimal values stored in palette colors.

Results are ordered by creation date, with the newest ideas appearing first. The idea ID is used as a secondary sorting field to provide consistent ordering when timestamps are identical.

## Database Interaction

All three services use the shared SQLAlchemy database session provided by `app.extensions`.

The services use several SQLAlchemy operations to interact with database records:

| Operation | Purpose |
|---|---|
| `db.session.get()` | Retrieves a record using its primary key. |
| `db.session.scalar()` | Executes a query and returns a single result. |
| `db.session.scalars()` | Executes a query and returns scalar results. |
| `db.session.add()` | Adds a new record to the session. |
| `db.session.delete()` | Marks a record for deletion. |
| `db.session.commit()` | Saves pending database changes. |

Database changes are committed after successful create, update, and delete operations.

The services also use SQLAlchemy relationship attributes to manage associations between ideas, collections, mediums, palettes, and colors.

## Validation and Error Handling

The service layer performs validation before committing changes to the database.

Validation behavior varies depending on the operation:

| Operation | Validation / Error Handling |
|---|---|
| Idea creation | Raises `ValueError` if the title is empty. |
| Idea update | Raises `ValueError` if the title is empty. |
| Collection creation | Raises `ValueError` if the name is empty or already exists. |
| Palette creation | Raises `ValueError` if the name is empty or a color has an invalid hexadecimal format. |
| Record retrieval | Returns `None` if the requested record does not exist. |
| Collection relationship updates | Returns `False` if either associated record does not exist. |
| Record deletion | Returns `False` if the requested record does not exist. |

Validation errors are raised as Python `ValueError` exceptions. The route layer catches these exceptions and displays the corresponding messages to users through Flask flash notifications.

## Service Layer Integration

The service classes are called by the route modules to perform application operations.

| Service | Route Module | Main Responsibilities |
|---|---|---|
| IdeaService | `ideas` | Manages art ideas and creates color palettes. |
| IdeaService | `palettes` | Creates color palettes for existing ideas. |
| CollectionService | `collections` | Manages collections and their associated ideas. |
| SearchService | `main` | Handles searching and filtering in the idea archive. |

The services help keep business logic separate from request handling and HTML rendering.

This allows the route functions to focus on processing requests, passing data to the appropriate service, and returning responses.

