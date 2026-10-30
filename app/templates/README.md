### HTML Templates

The application uses Flask's Jinja templating engine to generate dynamic HTML pages. Templates share a common base layout and extend it to provide page-specific content.

- **`base.html`** – Defines the shared page structure, including the document metadata, navigation bar, main content area, flash messages, footer, stylesheets, and JavaScript files. Other templates extend this layout.

- **`index.html`** – Displays the main idea archive. Users can browse saved ideas, search by keywords, and filter results by medium, collection, or color. Each idea is displayed with its description, associated mediums, reference images, and color palette when available.

- **`idea_detail.html`** – Displays the full details of an individual idea, including its description, assigned mediums, collections, saved color palettes, and reference images. It also provides forms for adding palettes and references, as well as options to edit or delete the idea.

- **`idea_form.html`** – Provides the form used to create new ideas and edit existing ones. Users can enter a title and description and assign mediums and collections.

- **`collections.html`** – Allows users to create, view, and delete collections. Each collection displays its name, optional description, and the number of associated ideas.

- **`mediums.html`** – Allows users to add, edit, and remove art mediums. Existing mediums are displayed with inline editing controls.

Jinja template inheritance reduces duplicated HTML by allowing individual pages to reuse the structure defined in `base.html`. Template variables, conditionals, and loops dynamically display information retrieved from the database.