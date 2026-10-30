
/**
 * Color palette interactions.
 *
 * Handles saved color swatches and dynamically adding color inputs
 * to the palette creation form.
 */

document.addEventListener("DOMContentLoaded", () => {
    // Apply saved hexadecimal colors to their corresponding swatches.
    document.querySelectorAll("[data-color]").forEach((element) => {
        const color = element.dataset.color;

        // Accept only six-digit hexadecimal colors.
        if (/^#[0-9a-fA-F]{6}$/.test(color)) {
            element.style.backgroundColor = color;
        }
    });

    // Set up the palette creation form, if it exists on this page.
    const container = document.querySelector("#palette-colors");
    const addButton = document.querySelector("#add-palette-color");

    if (!container || !addButton) {
        return;
    }

    const maxColors = 12;

    addButton.addEventListener("click", () => {
        const existingInputs = container.querySelectorAll(
            'input[name="colors"]'
        );

        // Do not allow more than 12 colors in a palette.
        if (existingInputs.length >= maxColors) {
            addButton.disabled = true;
            addButton.textContent = "Maximum of 12 colors reached";
            return;
        }

        const colorNumber = existingInputs.length + 1;

        // Create a label for the new color picker.
        const label = document.createElement("label");
        label.textContent = `Color ${colorNumber} `;

        // Create the color picker.
        const input = document.createElement("input");
        input.type = "color";
        input.name = "colors";
        input.value = "#77747D";
        input.required = true;

        label.appendChild(input);
        container.appendChild(label);

        // Update the button when the maximum is reached.
        if (colorNumber >= maxColors) {
            addButton.disabled = true;
            addButton.textContent = "Maximum of 12 colors reached";
        }
    });
});
