
/**
 * Handle reference images that fail to load.
 */

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".reference-card img").forEach((image) => {
        image.addEventListener("error", () => {
            const card = image.closest(".reference-card");

            if (!card) {
                return;
            }

            image.hidden = true;

            let message = card.querySelector(".reference-card__error");

            if (!message) {
                message = document.createElement("p");
                message.className = "reference-card__error";
                message.textContent = "Image unavailable";
                message.setAttribute("role", "status");

                image.parentElement.appendChild(message);
            }
        });
    });
});
