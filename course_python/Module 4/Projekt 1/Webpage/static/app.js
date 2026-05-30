console.log("SWISS Inspired Search gestartet");

function toggleTheme() {
    const body = document.getElementById('theme-body');
    const btn = document.getElementById('theme-toggle');
    
    if (body.classList.contains('dark-mode')) {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        btn.innerHTML = "🌙 Dark Mode";
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.remove('light-mode');
        body.classList.add('dark-mode');
        btn.innerHTML = "☀️ Light Mode";
        localStorage.setItem('theme', 'dark');
    }
}

// Beim Neuladen der Seite den gespeicherten Zustand laden
window.onload = function() {
    const savedTheme = localStorage.getItem('theme');
    const body = document.getElementById('theme-body');
    const btn = document.getElementById('theme-toggle');
    
    if (savedTheme === 'light') {
        body.classList.remove('dark-mode');
        body.classList.add('light-mode');
        if(btn) btn.innerHTML = "🌙 Dark Mode";
    }
}