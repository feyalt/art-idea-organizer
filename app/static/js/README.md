# JavaScript Documentation

The `static/js/` directory contains JavaScript files that provide client-side interactivity for the application.

Each script handles a specific feature of the interface, keeping functionality separated and making the code easier to maintain.

## File Structure

| File | Purpose |
|---|---|
| `medium.js` | Handles inline editing of existing art mediums. |
| `palette.js` | Applies saved palette colors to their swatches and dynamically adds color inputs to the palette creation form. |
| `references.js` | Handles reference images that fail to load by displaying an alternative message. |

## Script Overview

### `medium.js`

Handles inline editing for art mediums on the medium management page.

When the document has loaded, the script finds each medium item and attaches event listeners to its editing controls.

**Functionality:**

- Hides the displayed medium name and edit button when editing begins.
- Reveals the corresponding edit form.
- Automatically focuses and selects the current name in the input field.
- Allows users to cancel editing.
- Restores the original medium name and returns the item to its display state when editing is cancelled.

The script uses `data-*` attributes and CSS classes to identify the relevant elements within each medium item.

### `palette.js`

Handles client-side interactions related to color palettes.

The script has two primary responsibilities.

**Displaying saved colors:**

- Finds elements containing a `data-color` attribute.
- Reads the associated hexadecimal color value.
- Validates that the value follows the expected six-digit hexadecimal format.
- Applies valid colors as the background of the corresponding element.

**Adding colors to a new palette:**

- Locates the palette creation form and its color input container.
- Adds a new color picker when the user selects the add-color button.
- Creates a corresponding label for each new color input.
- Assigns a default color value of `#77747D`.
- Limits palettes to a maximum of 12 colors.
- Disables the add-color button and updates its text when the limit is reached.

The script checks whether the palette form exists before initializing its functionality, allowing it to be included without requiring that form on every page.

### `references.js`

Handles reference images that fail to load.

When a reference image triggers an image-loading error, the script:

- Locates the corresponding reference card.
- Hides the image that failed to load.
- Creates an alternative message displaying "Image unavailable."
- Assigns the message a `role="status"` attribute so that the status can be communicated to assistive technology.
- Avoids creating duplicate error messages within the same card.

This provides a consistent fallback instead of leaving broken images visible in the interface.

## Initialization

All three scripts use the `DOMContentLoaded` event.

This ensures that the HTML document has been fully parsed before the scripts attempt to locate elements or attach event listeners.

Each script uses DOM methods such as `querySelector()`, `querySelectorAll()`, `createElement()`, and `addEventListener()` to interact with the page.

## Design and Maintenance

The JavaScript files are organized by feature rather than combining all client-side functionality into one script.

When adding or modifying functionality:

- Keep scripts focused on their respective features.
- Use descriptive CSS classes and `data-*` attributes to identify interactive elements.
- Check that required elements exist before initializing page-specific functionality.
- Use event listeners to respond to user interactions.
- Preserve existing validation and interface limits when modifying functionality.
- Provide appropriate fallback behavior when external resources, such as reference images, fail to load.