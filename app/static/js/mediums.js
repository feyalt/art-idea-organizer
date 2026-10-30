
/**
 * Inline editing for art mediums.
 */

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".medium-item").forEach((item) => {
        const name = item.querySelector("[data-medium-name]");
        const editForm = item.querySelector(".medium-item__edit-form");
        const editButton = item.querySelector("[data-edit-medium]");
        const cancelButton = item.querySelector("[data-cancel-edit]");
        const input = editForm.querySelector('input[name="name"]');

        const originalName = input.value;

        editButton.addEventListener("click", () => {
            name.hidden = true;
            editButton.hidden = true;
            editForm.hidden = false;

            input.focus();
            input.select();
        });

        cancelButton.addEventListener("click", () => {
            input.value = originalName;
            editForm.hidden = true;
            name.hidden = false;
            editButton.hidden = false;
        });
    });
});
