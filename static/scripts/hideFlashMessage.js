function hideFlashMessage() {
    const flashMessage = document.getElementById("flash-message");

    if (flashMessage) {
        setTimeout(function() {
            flashMessage.style.display = "none";
        }, 3000);
    }
}

document.addEventListener("DOMContentLoaded", function() {
    hideFlashMessage();
});
