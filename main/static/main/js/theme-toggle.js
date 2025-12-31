// Theme Toggle Logic
window.toggleTheme = function (e) {
    if (e) {
        e.preventDefault();
        console.log('Toggle clicked via inline handler');
    } else {
        console.log('Toggle called programmatically');
    }

    const htmlElement = document.documentElement;
    const currentTheme = htmlElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    htmlElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);

    updateIcon(newTheme);
};

function updateIcon(theme) {
    const toggleButton = document.getElementById('theme-toggle');
    if (!toggleButton) return;

    const icon = toggleButton.querySelector('i');
    if (!icon) return;

    if (theme === 'dark') {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
        toggleButton.setAttribute('aria-label', 'Switch to Light Mode');
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
        toggleButton.setAttribute('aria-label', 'Switch to Dark Mode');
    }
}

// Initial Load Check
document.addEventListener('DOMContentLoaded', () => {
    console.log('Script loaded, identifying theme...');
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const htmlElement = document.documentElement;

    if (savedTheme) {
        htmlElement.setAttribute('data-theme', savedTheme);
        updateIcon(savedTheme);
    } else if (prefersDark) {
        htmlElement.setAttribute('data-theme', 'dark');
        updateIcon('dark');
    }
});
