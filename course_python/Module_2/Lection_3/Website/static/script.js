function zeigeOS(id, buttonElement) {
    // 1. Alle Info-Boxen verstecken
    const boxen = document.querySelectorAll('.info-box');
    boxen.forEach(box => box.classList.add('hidden'));

    // 2. Die gewählte Box anzeigen
    const zielBox = document.getElementById(id);
    if (zielBox) {
        zielBox.classList.remove('hidden');
    }

    // 3. Den Start-Text ("Willkommen") ausblenden
    const startText = document.getElementById('start');
    if (startText) startText.classList.add('hidden');

    // 4. Aktiv-Status der Buttons aktualisieren
    const alleButtons = document.querySelectorAll('.hoverboard button');
    alleButtons.forEach(btn => btn.classList.remove('active'));
    
    // Falls ein Button-Element übergeben wurde, markiere es als aktiv
    if (buttonElement) {
        buttonElement.classList.add('active');
    }
    // Buttons Aktiv-Zustand
        const buttons = document.querySelectorAll('.hoverboard button');
        buttons.forEach(b => b.classList.remove('active'));
        if (btn) {
            btn.classList.add('active');
        }
}