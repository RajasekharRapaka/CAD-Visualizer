document.addEventListener('DOMContentLoaded', () => {
    const howToUseBtn = document.getElementById('how-to-use-btn');
    const instructionsBox = document.getElementById('instructions-box');

    // Toggle instructions box
    howToUseBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent the click from reaching the document
        instructionsBox.style.display = instructionsBox.style.display === 'block' ? 'none' : 'block';
    });

    // Hide instructions box when clicking outside
    document.addEventListener('click', () => {
        instructionsBox.style.display = 'none';
    });

    // Prevent the box from closing when clicking inside it
    instructionsBox.addEventListener('click', (e) => {
        e.stopPropagation();
    });
});