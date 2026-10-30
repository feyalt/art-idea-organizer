
# Application Routes

## Overview

The application's routes are responsible for handling incoming HTTP requests, processing form submissions, and returning the appropriate responses.

The application uses Flask Blueprints to organize routes by functionality. Each Blueprint groups related endpoints and keeps the application's routing logic separated into manageable modules.

The routes interact with SQLAlchemy models and service classes to retrieve, create, update, and delete database records. HTML templates are used to render pages, while Flask's flash messaging system provides feedback after user actions.

## Route Organization

The application's routes are organized into the following modules:

| Route Module | Blueprint | Responsibility |
|---|---|---|
| Main routes | `main` | Displays the idea archive and handles searching and filtering. |
| Idea routes | `ideas` | Creates, displays, edits, and deletes art ideas. |
| Collection routes | `collections` | Creates, displays, and deletes collections. |
| Medium routes | `mediums` | Creates, displays, renames, and deletes art mediums. |
| Palette routes | `palettes` | Creates and deletes color palettes associated with ideas. |
| Reference routes | `references` | Adds and removes external reference images. |

## Route Definitions

### 1. Main Routes

**Responsibility:** Display the main art idea archive and provide search and filtering functionality.

The main Blueprint handles requests to the application's homepage.

| Method | Endpoint | Function | Description |
|---|---|---|---|
| GET | `/` | `index()` | Displays the idea archive with optional search and filters. |

**Functionality:**

The index route retrieves search and filter parameters from the URL query string:

- `q`: Searches ideas by text.
- `medium_id`: Filters ideas by an associated medium.
- `collection_id`: Filters ideas by collection.
- `color`: Filters ideas by color.

These parameters are passed to `SearchService.search()`, which retrieves the matching ideas.

The route also retrieves the available mediums and collections to populate the filtering controls in the template.

**Template:** `index.html`

### 2. Idea Routes

**Responsibility:** Manage the creation, viewing, editing, and deletion of art ideas.

The ideas Blueprint uses `IdeaService` to handle idea-related operations.

| Method | Endpoint | Function | Description |
|---|---|---|---|
| GET, POST | `/ideas/new` | `create_idea()` | Displays the creation form and processes new ideas. |
| GET | `/ideas/<idea_id>` | `idea_detail()` | Displays an individual idea. |
| GET, POST | `/ideas/<idea_id>/edit` | `edit_idea()` | Displays the editing form and saves changes. |
| POST | `/ideas/<idea_id>/delete` | `delete_idea()` | Deletes an existing idea. |

**Functionality:**

- Creating an idea: Accepts a title, description, selected mediums, and selected collections. The submitted information is passed to `IdeaService.create()`.
- Viewing an idea: Retrieves an idea using `IdeaService.get_by_id()` and displays its details.
- Editing an idea: Loads the existing idea and allows its title, description, mediums, and collections to be updated through `IdeaService.update()`.
- Deleting an idea: Uses `IdeaService.delete()` to remove the selected idea.

The creation and editing forms retrieve available mediums and collections from the database so users can associate them with an idea.

If an idea cannot be found, the detail and editing routes return a 404 response.

**Templates:**

- `idea_form.html` — Used for creating and editing ideas.
- `idea_detail.html` — Displays an individual idea.

### 3. Collection Routes

**Responsibility:** Manage collections used to organize art ideas.

The collections Blueprint uses `CollectionService` to perform collection-related operations.

| Method | Endpoint | Function | Description |
|---|---|---|---|
| GET | `/collections/` | `index()` | Displays all collections. |
| POST | `/collections/new` | `create()` | Creates a new collection. |
| POST | `/collections/<collection_id>/delete` | `delete()` | Deletes a collection. |

**Functionality:**

- Listing collections: Retrieves all collections using `CollectionService.list_all()`.
- Creating collections: Accepts a collection name and optional description, then passes them to `CollectionService.create()`.
- Deleting collections: Uses `CollectionService.delete()` to remove a collection.

If collection creation fails validation, an error message is displayed. Successful operations also display confirmation messages.

Deleting a collection does not delete the art ideas associated with it.

**Template:** `collections.html`

### 4. Medium Routes

**Responsibility:** Manage the reusable art mediums available throughout the application.

The mediums Blueprint interacts directly with the Medium model and uses SQLAlchemy queries to retrieve and modify records.

| Method | Endpoint | Function | Description |
|---|---|---|---|
| GET | `/mediums/` | `index()` | Displays all available mediums. |
| POST | `/mediums/new` | `create()` | Creates a new medium. |
| POST | `/mediums/<medium_id>/edit` | `edit()` | Renames an existing medium. |
| POST | `/mediums/<medium_id>/delete` | `delete()` | Deletes a medium. |

**Functionality:**

- Listing mediums: Retrieves all mediums alphabetically, using a case-insensitive sort.
- Creating mediums: Validates the submitted name and checks for existing mediums before saving a new record.
- Editing mediums: Retrieves the selected medium, validates the new name, and checks for duplicates before updating it.
- Deleting mediums: Removes the selected medium from the database.

Medium names are required, must not exceed 80 characters, and must be unique regardless of capitalization.

Deleting a medium does not delete its associated ideas.

**Template:** `mediums.html`

### 5. Palette Routes

**Responsibility:** Manage color palettes associated with individual art ideas.

The palettes Blueprint allows users to add and remove color palettes from existing ideas.

| Method | Endpoint | Function | Description |
|---|---|---|---|
| POST | `/ideas/<idea_id>/palettes` | `create_palette()` | Creates a color palette for an idea. |
| POST | `/palettes/<palette_id>/delete` | `delete_palette()` | Deletes an existing color palette. |

**Functionality:**

- Creating palettes: Verifies that the requested idea exists, retrieves the palette name and submitted colors, and passes them to `IdeaService.add_palette()`.
- Deleting palettes: Retrieves the selected palette, deletes it from the database, and redirects back to its associated idea.

Palette creation uses the idea service to handle validation and database operations.

If the associated idea or palette cannot be found, the route returns a 404 response.

### 6. Reference Image Routes

**Responsibility:** Manage external image references attached to art ideas.

The references Blueprint allows users to attach image URLs to ideas and remove existing references.

| Method | Endpoint | Function | Description |
|---|---|---|---|
| POST | `/ideas/<idea_id>/references` | `create_reference()` | Adds a reference image to an idea. |
| POST | `/references/<reference_id>/delete` | `delete_reference()` | Removes a reference image. |

**Functionality:**

- Adding references: Verifies that the associated idea exists, validates the submitted image URL, and creates a ReferenceImage record.
- Removing references: Retrieves the selected reference image, deletes it, and redirects back to its associated idea.

Reference URLs must:

- Use either HTTP or HTTPS.
- Include a valid network location.
- Contain no whitespace.
- Be no longer than 2,048 characters.

Captions are optional and limited to 255 characters.

Each reference image is assigned a position based on the number of existing references associated with the idea.

### 7. Route Responses and Error Handling

The application uses several Flask features to manage responses and communicate the results of user actions.

| Flask Feature | Purpose |
|---|---|
| `render_template()` | Renders an HTML template and passes data to it. |
| `redirect()` | Redirects the user to another route after an operation. |
| `url_for()` | Generates URLs using registered endpoint names. |
| `request.form` | Retrieves submitted form values. |
| `request.args` | Retrieves URL query parameters. |
| `flash()` | Displays success and error messages to the user. |
| `abort(404)` | Returns a 404 response when a requested record cannot be found. |

Most routes that modify database records use the POST method and redirect the user after processing the request.

This follows the Post/Redirect/Get pattern, helping prevent accidental form resubmissions when users refresh a page.

Validation errors are communicated through Flask flash messages, while missing database records generally result in a 404 response.

## Service Layer Integration

Some route modules delegate their business logic to service classes rather than performing database operations directly.

| Service | Used By | Responsibility |
|---|---|---|
| `IdeaService` | Idea and palette routes | Handles idea creation, retrieval, updates, deletion, and palette creation. |
| `CollectionService` | Collection routes | Handles collection retrieval, creation, and deletion. |
| `SearchService` | Main routes | Handles searching and filtering art ideas. |

Other route modules, including the medium and reference routes, interact directly with SQLAlchemy models and the database session.

This provides a separation between route handling and business logic where service classes are used, while keeping simpler database operations within their respective route modules.
