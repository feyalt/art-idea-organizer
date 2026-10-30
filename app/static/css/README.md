# CSS Documentation

The `static/css/` directory contains the stylesheets responsible for the application's visual design, page layouts, reusable interface components, and responsive behavior.

The stylesheets are separated by responsibility to keep the styling organized and make the interface easier to maintain.

## File Structure

| File | Purpose |
|---|---|
| `tokens.css` | Defines shared design tokens, including colors, typography, spacing, layout dimensions, borders, and transitions. |
| `components.css` | Contains reusable styles for interface elements such as buttons, links, forms, tags, flash messages, color palettes, reference images, and idea cards. |
| `layout.css` | Defines the overall page structure, including the site header, navigation, main content area, footer, and shared layout behavior. |
| `main.css` | Contains page-specific styling for the archive, idea forms, idea detail pages, collections, mediums, and other application views. |

## Stylesheet Overview

### `tokens.css`

Defines the application's central design system through CSS custom properties.

These variables provide a consistent source of values across the stylesheets.

The tokens are organized into the following categories:

- **Colors:** Core colors, including charcoal, cool grays, dusty pink, and semantic interface colors.
- **Typography:** Font families, including Nanum Myeongjo and Mea Culpa, along with a shared type scale.
- **Layout:** Content width, page gutters, section spacing, and reusable spacing values.
- **Borders and motion:** Border styles, corner radii, and standard transition timing.

Other stylesheets reference these variables rather than repeatedly defining the same values.

### `components.css`

Contains reusable styles for common interface elements and more specialized components.

Its main sections include:

- **Buttons and links:** Primary, secondary, and danger buttons, text links, hover states, and keyboard focus indicators.
- **Tags:** Tag lists and individual tags used to display associated information.
- **Forms:** Form fields, labels, input controls, selection options, and helper text.
- **Flash messages:** Visual styling for success and error notifications.
- **Idea details:** Headings, descriptions, metadata, and detail-page sections.
- **Color palettes:** Palette creation forms, saved palettes, and color swatches.
- **Reference images:** Image forms, reference cards, image grids, and error placeholders.
- **Collections and mediums:** Creation forms, collection cards, medium lists, and management controls.
- **Archive components:** Search fields, filters, archive toolbars, idea cards, metadata, and empty states.
- **Responsive behavior:** Adjustments to component layouts at smaller screen widths.
- **Reduced motion:** Overrides for users who prefer reduced animation.

### `layout.css`

Defines the shared structure of the application.

It establishes the overall page layout and ensures that common elements remain consistent across different views.

Key elements include:

- **Global defaults:** Box sizing, minimum page height, default typography, and base element styling.
- **Site header:** Logo placement, navigation alignment, spacing, and responsive behavior.
- **Page content:** Main content width, centered positioning, and page gutters.
- **Site footer:** Footer spacing, borders, and text alignment.

The stylesheet also includes shared layout rules for page headings and other recurring page structures.

### `main.css`

Contains styling for the application's individual pages and their primary content areas.

Its sections cover:

- **Typography and page headings:** Heading sizes, introductory text, eyebrow labels, and script accents.
- **Archive page:** Archive headers, search controls, toolbars, idea grids, and idea cards.
- **Empty states:** Layout and typography for pages or sections without saved content.
- **Collections:** Collection creation forms, saved collection cards, and collection grids.
- **Medium management:** Medium creation, listing, inline editing, and management controls.
- **Forms:** Idea creation and editing page layouts.
- **Idea detail pages:** Idea headings, descriptions, metadata, and detail sections.
- **Color palettes:** Palette layouts and individual color swatches.
- **Reference images:** Reference lists and image links.
- **Responsive layouts:** Adjustments to page structures and grids for smaller screens.
- **Medium and collection selection:** Layout for selecting associated mediums and collections when creating or editing an idea.

## Responsive Design

The stylesheets use CSS media queries to adapt the interface to different screen sizes.

Depending on the component, responsive adjustments include:

- Reducing multi-column grids to two columns or a single column.
- Stacking navigation and form controls vertically.
- Adjusting page gutters, padding, and heading sizes.
- Making image grids and card layouts fit smaller screens.
- Changing medium and collection selection layouts.

The stylesheets also include `prefers-reduced-motion` rules to reduce transitions and hover animations when requested by the user's system preferences.

## Design Consistency

The application uses shared CSS variables from `tokens.css` to maintain a consistent visual language.

The overall design combines:

- Charcoal and cool gray as the primary neutral colors.
- Dusty pink as the accent color.
- Nanum Myeongjo for body typography.
- Mea Culpa for decorative script accents.
- Consistent spacing, borders, and subtle transitions.

Centralizing these values makes it easier to adjust the visual appearance of the application without having to modify individual components.

## Maintenance

When updating the stylesheets:

- Add shared design values to `tokens.css` rather than duplicating them.
- Keep reusable interface styles in `components.css`.
- Place global page structure and shared layout rules in `layout.css`.
- Keep page-specific styling in `main.css`.
- Use existing CSS variables whenever possible to maintain consistency.
- Preserve responsive and reduced-motion behavior when modifying existing components.