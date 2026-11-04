document.addEventListener("DOMContentLoaded", () => {
    const maxColors = 12;
    const defaultColor = "#77747D";

    // Update the hex label whenever a color picker changes.
    function updateColorLabel(swatch) {
        const colorInput = swatch.querySelector('input[type="color"]');
        const colorLabel = swatch.querySelector(".palette-swatch__label");
        const pickerLabel = swatch.querySelector(".palette-swatch__picker");

        if (!colorInput || !colorLabel || !pickerLabel) {
            return;
        }

        pickerLabel.style.backgroundColor = colorInput.value;
        colorLabel.textContent = colorInput.value.toUpperCase();
    }

    // Create a color swatch with an integrated color picker.
    function createColorSwatch(container, colorNumber, color, removable = false) {
        const swatch = document.createElement("div");
        swatch.className = "palette-swatch palette-swatch--editable";

        const pickerLabel = document.createElement("label");
        pickerLabel.className = "palette-swatch__picker";

        const colorInput = document.createElement("input");
        colorInput.type = "color";
        colorInput.name = "colors";
        colorInput.value = color;
        colorInput.required = true;
        colorInput.setAttribute("aria-label", `Color ${colorNumber}`);

        const colorLabel = document.createElement("span");
        colorLabel.className = "palette-swatch__label";
        colorLabel.textContent = color.toUpperCase();

        pickerLabel.appendChild(colorInput);
        swatch.appendChild(pickerLabel);
        swatch.appendChild(colorLabel);

        if (removable) {
            const removeButton = document.createElement("button");

            removeButton.type = "button";
            removeButton.className = "button button--danger";
            removeButton.dataset.removeColor = "";
            removeButton.textContent = "Remove";
            removeButton.setAttribute(
                "aria-label",
                `Remove color ${colorNumber}`
            );

            swatch.appendChild(removeButton);
        }

        container.appendChild(swatch);

        return swatch;
    }

    // Keep the add-color button disabled at the maximum.
    function updateAddButton(container, button) {
        if (!container || !button) {
            return;
        }

        const colorCount = container.querySelectorAll(
            'input[type="color"]'
        ).length;

        button.disabled = colorCount >= maxColors;
    }

    // Update color labels for the initial server-rendered swatches.
    document.querySelectorAll(".palette-swatch--editable").forEach((swatch) => {
        updateColorLabel(swatch);
    });

    // New palette form.
    const createColors = document.getElementById("palette-colors");
    const addPaletteColorButton = document.getElementById("add-palette-color");

    if (createColors && addPaletteColorButton) {
        updateAddButton(createColors, addPaletteColorButton);

        addPaletteColorButton.addEventListener("click", () => {
            const colorCount = createColors.querySelectorAll(
                'input[type="color"]'
            ).length;

            if (colorCount >= maxColors) {
                return;
            }

            createColorSwatch(
                createColors,
                colorCount + 1,
                defaultColor
            );

            updateAddButton(createColors, addPaletteColorButton);
        });
    }

    // Update a swatch's hex label when its color changes.
    document.addEventListener("input", (event) => {
        if (event.target.matches('.palette-swatch--editable input[type="color"]')) {
            const swatch = event.target.closest(".palette-swatch");
            updateColorLabel(swatch);
        }
    });

    // Open a palette's edit form.
    document.querySelectorAll("[data-edit-palette]").forEach((button) => {
        button.addEventListener("click", () => {
            const paletteId = button.dataset.editPalette;
            const display = document.getElementById(
                `palette-display-${paletteId}`
            );
            const editForm = document.getElementById(
                `palette-edit-${paletteId}`
            );

            if (!display || !editForm) {
                return;
            }

            display.hidden = true;
            editForm.hidden = false;
        });
    });

    // Cancel editing and return to the saved palette display.
    document.querySelectorAll("[data-cancel-palette]").forEach((button) => {
        button.addEventListener("click", () => {
            const paletteId = button.dataset.cancelPalette;
            const display = document.getElementById(
                `palette-display-${paletteId}`
            );
            const editForm = document.getElementById(
                `palette-edit-${paletteId}`
            );

            if (!display || !editForm) {
                return;
            }

            editForm.hidden = true;
            display.hidden = false;
        });
    });

    // Add a color to an existing palette.
    document.querySelectorAll("[data-add-color]").forEach((button) => {
        const editForm = button.closest(".palette-edit-form");
        const colorsContainer = editForm?.querySelector("[data-palette-colors]");

        if (!colorsContainer) {
            return;
        }

        updateAddButton(colorsContainer, button);

        button.addEventListener("click", () => {
            const colorCount = colorsContainer.querySelectorAll(
                'input[type="color"]'
            ).length;

            if (colorCount >= maxColors) {
                return;
            }

            createColorSwatch(
                colorsContainer,
                colorCount + 1,
                defaultColor,
                true
            );

            updateAddButton(colorsContainer, button);
        });
    });

    // Remove a color from an existing palette.
    document.addEventListener("click", (event) => {
        const removeButton = event.target.closest("[data-remove-color]");

        if (!removeButton) {
            return;
        }

        const editForm = removeButton.closest(".palette-edit-form");
        const colorsContainer = editForm?.querySelector("[data-palette-colors]");

        if (!colorsContainer) {
            return;
        }

        const swatches = colorsContainer.querySelectorAll(
            ".palette-swatch--editable"
        );

        // A palette must contain at least one color.
        if (swatches.length <= 1) {
            return;
        }

        removeButton.closest(".palette-swatch--editable").remove();

        // Update accessible color numbers after removal.
        colorsContainer
            .querySelectorAll(".palette-swatch--editable")
            .forEach((swatch, index) => {
                const colorInput = swatch.querySelector('input[type="color"]');
                const removeButton = swatch.querySelector("[data-remove-color]");

                if (colorInput) {
                    colorInput.setAttribute(
                        "aria-label",
                        `Color ${index + 1}`
                    );
                }

                if (removeButton) {
                    removeButton.setAttribute(
                        "aria-label",
                        `Remove color ${index + 1}`
                    );
                }
            });

        const addButton = editForm.querySelector("[data-add-color]");
        updateAddButton(colorsContainer, addButton);
    });
});
