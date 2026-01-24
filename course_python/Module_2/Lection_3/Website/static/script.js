// Navigation
function zeigeInhalt(id) {
    document.querySelectorAll('main section').forEach(s => s.style.display = "none");
    document.getElementById(id + "-content").style.display = "block";
}

// Kommunikation mit Python (Flask)
async function sendeZahl() {
    const guess = document.getElementById('num-input').value;
    const response = await fetch('/check_number', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ guess: guess })
    });
    const result = await response.json();
    document.getElementById('game-feedback').innerText = result.message;
}

// Sudoku-Daten von Python abrufen
async function ladeSudoku() {
    const response = await fetch('/get_sudoku');
    const data = await response.json();
    const grid = document.getElementById('sudoku-grid');
    grid.innerHTML = '';

    data.puzzle.forEach((row, rIdx) => {
        row.forEach((val, cIdx) => {
            const input = document.createElement('input');
            input.className = 'cell';
            input.type = 'number';
            if (val !== null) {
                input.value = val;
                input.readOnly = true;
                input.style.background = '#ddd';
            }
            grid.appendChild(input);
        });
    });
}