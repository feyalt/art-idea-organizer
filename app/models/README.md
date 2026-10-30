
# Database Models

For a high-level overview of the database structure and entity relationships, see the [Database Schema README](../../docs/database/README.md).

## Overview

The `app/models/` package contains the SQLAlchemy models that define the application's database structure. Each model represents a database entity and specifies its columns, constraints, and relationships.

The application uses SQLite for persistent storage and SQLAlchemy ORM to interact with database records through Python objects.

The models are organized into separate modules based on their responsibilities:

| File | Model(s) | Description |
|---|---|---|
| `project_idea.py` | ProjectIdea | Central model representing an individual art idea. |
| `collection.py` | Collection | Represents a user-created collection of ideas. |
| `medium.py` | Medium | Represents a reusable art medium. |
| `color_palette.py` | ColorPalette, PaletteColor | Represents color palettes and their individual colors. |
| `reference_image.py` | ReferenceImage | Represents external visual references attached to ideas. |
| `associations.py` | `idea_collections`, `idea_mediums` | Defines many-to-many association tables. |
| `__init__.py` | Model exports | Exposes the models through the package. |

## Model Definitions

### 1. ProjectIdea

**File:** `project_idea.py`  
**Table:** `project_ideas`

ProjectIdea is the central model of the application. Each record represents an art idea that the user wants to develop into an artwork.

| Attribute | Data Type | Constraints / Default | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique identifier for the idea. |
| `title` | String(120) | NOT NULL | Title of the idea. |
| `description` | Text | NOT NULL, default `""` | Description of the idea. |
| `created_at` | DateTime | NOT NULL, default `utc_now` | Timestamp indicating when the idea was created. |
| `updated_at` | DateTime | NOT NULL, default `utc_now` | Timestamp of the most recent update. |

**Relationships:**

- Collections: Many-to-many relationship with Collection, using the `idea_collections` association table.
- Mediums: Many-to-many relationship with Medium, using the `idea_mediums` association table.
- Palettes: One-to-many relationship with ColorPalette.
- Reference images: One-to-many relationship with ReferenceImage.

The `updated_at` field uses SQLAlchemy's `onupdate` parameter to refresh the timestamp whenever the record is updated. Both timestamps are generated using the timezone-aware UTC helper function `utc_now()`.

The palettes and reference images relationships use `all, delete-orphan` cascading behavior.

### 2. Collection

**File:** `collection.py`  
**Table:** `collections`

Collection represents a user-created group used to organize related art ideas.

| Attribute | Data Type | Constraints / Default | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique identifier for the collection. |
| `name` | String(100) | NOT NULL, UNIQUE | Name of the collection. |
| `description` | Text | NOT NULL, default `""` | Optional description of the collection. |

**Relationships:**

- Ideas: Many-to-many relationship with ProjectIdea, using the `idea_collections` association table.

The unique constraint on `name` prevents multiple collections from having the same name.

### 3. Medium

**File:** `medium.py`  
**Table:** `mediums`

Medium represents a reusable art medium that can be assigned to one or more ideas.

Examples include watercolor, charcoal, acrylic, and digital illustration.

| Attribute | Data Type | Constraints / Default | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique identifier for the medium. |
| `name` | String(80) | NOT NULL, UNIQUE | Name of the art medium. |

**Relationships:**

- Ideas: Many-to-many relationship with ProjectIdea, using the `idea_mediums` association table.

The unique constraint on `name` prevents duplicate medium entries.

### 4. ColorPalette

**File:** `color_palette.py`  
**Table:** `color_palettes`

ColorPalette represents a named collection of colors associated with an individual art idea.

| Attribute | Data Type | Constraints / Default | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique identifier for the palette. |
| `name` | String(100) | NOT NULL | Name of the palette. |
| `idea_id` | Integer | Foreign Key, NOT NULL | References `project_ideas.id`. |

**Relationships:**

- Idea: Many-to-one relationship with ProjectIdea.
- Colors: One-to-many relationship with PaletteColor.

Each palette belongs to one idea and can contain multiple individual colors.

The colors relationship uses `all, delete-orphan` cascading behavior and orders colors by their `position` attribute.

### 5. PaletteColor

**File:** `color_palette.py`  
**Table:** `palette_colors`

PaletteColor represents an individual color within a ColorPalette.

| Attribute | Data Type | Constraints / Default | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique identifier for the color. |
| `hex_code` | String(7) | NOT NULL | Hexadecimal color value. |
| `position` | Integer | NOT NULL, default `0` | Position of the color within its palette. |
| `palette_id` | Integer | Foreign Key, NOT NULL | References `color_palettes.id`. |

**Relationships:**

- Palette: Many-to-one relationship with ColorPalette.

The `position` attribute determines the ordering of colors within a palette.

### 6. ReferenceImage

**File:** `reference_image.py`  
**Table:** `reference_images`

ReferenceImage represents an external visual reference associated with an art idea. Images are stored as URLs rather than as files within the database.

| Attribute | Data Type | Constraints / Default | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique identifier for the reference image. |
| `url` | String(2048) | NOT NULL | URL pointing to the external image. |
| `caption` | String(255) | NOT NULL, default `""` | Optional image caption. |
| `position` | Integer | NOT NULL, default `0` | Position of the image within an idea's references. |
| `created_at` | DateTime | NOT NULL, default UTC timestamp | Timestamp indicating when the reference was added. |
| `idea_id` | Integer | Foreign Key, NOT NULL | References `project_ideas.id`. |

**Relationships:**

- Idea: Many-to-one relationship with ProjectIdea.

The `position` attribute allows reference images to be displayed in a specific order.

### 7. Association Tables

**File:** `associations.py`

The application uses two association tables to implement many-to-many relationships between ideas and their organizational attributes.

#### idea_collections

Connects ProjectIdea records with Collection records.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `idea_id` | Integer | Primary Key, Foreign Key | References `project_ideas.id`. |
| `collection_id` | Integer | Primary Key, Foreign Key | References `collections.id`. |

#### idea_mediums

Connects ProjectIdea records with Medium records.

| Column | Data Type | Constraints | Description |
|---|---|---|---|
| `idea_id` | Integer | Primary Key, Foreign Key | References `project_ideas.id`. |
| `medium_id` | Integer | Primary Key, Foreign Key | References `mediums.id`. |

Both association tables use composite primary keys consisting of their two foreign key columns. This prevents duplicate associations between the same records.

Their foreign keys also specify `ON DELETE CASCADE`, configuring associated rows to be deleted when a referenced record is deleted.

## Relationships and Cascading Behavior

The models define the following relationships:

| Relationship | Type | Implementation |
|---|---|---|
| ProjectIdea ↔ Collection | Many-to-Many | `idea_collections` |
| ProjectIdea ↔ Medium | Many-to-Many | `idea_mediums` |
| ProjectIdea → ColorPalette | One-to-Many | Foreign key: `color_palettes.idea_id` |
| ColorPalette → PaletteColor | One-to-Many | Foreign key: `palette_colors.palette_id` |
| ProjectIdea → ReferenceImage | One-to-Many | Foreign key: `reference_images.idea_id` |

Several relationships also define cascading deletion behavior:

- Deleting a ProjectIdea through the ORM removes its associated color palettes and reference images through `all, delete-orphan` cascades.
- Deleting a ColorPalette through the ORM removes its associated palette colors.
- The association tables define `ON DELETE CASCADE` on their foreign keys to handle dependent association records.

## Model Package Organization

The `__init__.py` file exposes the database models through the `app.models` package.

It imports and makes the following models available:

- Collection
- ColorPalette
- Medium
- PaletteColor
- ProjectIdea
- ReferenceImage

This organization allows other parts of the application to import models directly from the package rather than importing each model from its individual module.

For example:

```python
from app.models import ProjectIdea, Collection, Medium
```