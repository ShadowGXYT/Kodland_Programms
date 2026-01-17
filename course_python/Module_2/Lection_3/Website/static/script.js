function zeigeInhalt(contentId){
  document.querySelectorAll('main section').forEach(s=>s.style.display="none");
  document.getElementById(contentId+"-content").style.display="block";
  if(contentId==="Minigames") showGame('Zahlenraten');
}

function showGame(gameName){
  document.querySelectorAll('#game-container .game-area').forEach(a=>a.style.display="none");
  document.getElementById(gameName+"-game-content").style.display="block";
  // hier kannst du Spiele-Init aufrufen
}

// Sudoku & Kreuzworträtsel Logik hier übernehmen
// plus AJAX-Aufrufe an /check_sudoku und /check_crossword
  