function toggleAdventures() {
    const showButton = document.getElementById('showAdventures');
    const hideButton = document.getElementById('hideAdventures');
    const adventuresContainer = document.getElementById('adventuresContainer');

    if (showButton && hideButton && adventuresContainer) {
        showButton.addEventListener('click', function() {
            adventuresContainer.style.display = 'block';
            showButton.style.display = 'none';
            hideButton.style.display = 'inline';
        });

        hideButton.addEventListener('click', function() {
            adventuresContainer.style.display = 'none';
            showButton.style.display = 'inline';
            hideButton.style.display = 'none';
        });
    }
}

document.addEventListener("DOMContentLoaded", function() {
    toggleAdventures();
});
