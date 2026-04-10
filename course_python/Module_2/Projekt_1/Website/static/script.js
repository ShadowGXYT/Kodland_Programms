function zeigeOS(id, buttonElement) {
    const boxen = document.querySelectorAll('.info-box');
    boxen.forEach(box => box.classList.add('hidden'));

    const zielBox = document.getElementById(id);
    if (zielBox) {
        zielBox.classList.remove('hidden');
    }

    const buttons = document.querySelectorAll('.hoverboard button');
    buttons.forEach(btn => btn.classList.remove('active'));

    if (buttonElement) {
        buttonElement.classList.add('active');
    }
}
