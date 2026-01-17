
function zeigeInhalt(contentId){
  document.querySelectorAll('main section').forEach(s=>s.style.display="none");
  document.getElementById(contentId+"-content").style.display="block";
 ="none");  if(contentId==="Minigames") showGame('Zahlenraten');
  document.getElementById(gameName+"-game-content").style.display="block";
  if(gameName==="Sudoku") initializeSudokuGame();
  if(gameName==="Kreuzwortraetsel") initializeCrosswordGame();
}

/* --- Sudoku Logik --- */
const sudokuGrid=document.getElementById('sudoku-grid');
const sudokuMessage=document.getElementById('sudoku-message');
const sudokuRestartButton=document.getElementById('sudoku-restart-button');

const sudokuPuzzles=[{ puzzle:[
  [5,3,null,null,7,null,null,null,null],
  [6,null,null,1,9,5,null,null,null],
  [null,9,8,null,null,null,null,6,null],
  [8,null,null,null,6,null,null,null,3],
  [4,null,null,8,null,3,null,null,1],
  [7,null,null,null,2,null,null,null,6],
  [null,6,null,null,null,null,2,8,null],
  [null,null,null,4,1,9,null,null,5],
  [null,null,null,null,8,null,null,7,9]
], solution:[
  [5,3,4,6,7,8,9,1,2],
  [6,7,2,1,9,5,3,4,8],
  [1,9,8,3,4,2,5,6,7],
  [8,5,9,7,6,1,4,2,3],
  [4,2,6,8,5,3,7,9,1],
  [7,1,3,9,2,4,8,5,6],
  [9,6,1,5,3,7,2,8,4],
  [2,8,7,4,1,9,6,3,5],
  [3,4,5,2,8,6,1,7,9]
] }];

function initializeSudokuGame(){
  sudokuGrid.innerHTML='';
  sudokuMessage.textContent='';
  sudokuRestartButton.style.display='block';
  const game=sudokuPuzzles[0];
  for(let r=0;r<9;r++){
    for(let c=0;c<9;c++){
      const cell=document.createElement('div');
      cell.classList.add('sudoku-cell');
      const input=document.createElement('input');
      input.type='number'; input.min='1'; input.max='9';
      if(game.puzzle[r][c]!==null){
        input.value=game.puzzle[r][c];
        input.readOnly=true;
        input.style.backgroundColor="#eee";
      }
      input.dataset.row=r; input.dataset.col=c;
      cell.appendChild(input);
      sudokuGrid.appendChild(cell);
    }
  }
  const checkBtn=document.createElement('button');
  checkBtn.textContent="Lösung prüfen";
  checkBtn.classList.add('game-button');
  checkBtn.onclick=()=>checkSudokuSolution(game.solution);
  sudokuMessage.insertAdjacentElement("afterend",checkBtn);
}

function checkSudokuSolution(solution){
  const inputs=sudokuGrid.querySelectorAll('input');
  let correct=true;
  inputs.forEach(i=>{
    const r=i.dataset.row, c=i.dataset.col;
    if(parseInt(i.value)===solution[r][c]){
      if(!i.readOnly) i.style.backgroundColor="#90EE90";
    } else {
      if(!i.readOnly) i.style.backgroundColor="#FFB6C1";
      correct=false;
    }
  });
  sudokuMessage.textContent=correct?"✅ Sudoku korrekt gelöst!":"❌ Da stimmt noch etwas nicht.";
}
sudokuRestartButton.addEventListener('click',initializeSudokuGame);

/* --- Kreuzworträtsel Logik --- */
const crosswordGrid=document.getElementById('crossword-grid');
const crosswordClues=document.getElementById('crossword-clues');
const crosswordMessage=document.getElementById('crossword-message');
const crosswordRestartButton=document.getElementById('crossword-restart-button');

const crosswordPuzzle={ grid:[
  ['C','A','T',null,null],
  [null,'R',null,'D','O'],
  ['D','O','G',null,'G'],
  [null,'W',null,'I',null],
  [null,'E','A','R',null]
], clues:{
  across:["1. Katze (engl.)","3. Hund (engl.)","5. Ohr (engl.)"],
  down:["1. Karte (engl.)","2. Holz (engl.)","4. Insekt (engl., bug)"]
}};

function initializeCrosswordGame(){
  crosswordGrid.innerHTML='';
  crosswordClues.innerHTML='<h4>Hinweise:</h4>';
  crosswordMessage.textContent='';
  crosswordRestartButton.style.display='block';
  const size=crosswordPuzzle.grid.length;
  crosswordGrid.style.gridTemplateColumns=`repeat(${size},30px)`;
  crosswordGrid.style.gridTemplateRows=`repeat(${size},30px)`;
  for(let r=0;r<size;r++){
    for(let c=0;c<size;c++){
      const cell=document.createElement('div');
      cell.classList.add('crossword-cell');
      if(crosswordPuzzle.grid[r][c]===null){
        cell.classList.add('empty');
      } else {
        const input=document.createElement('input');
        input.maxLength=1;
        input.dataset.row=r; input.dataset.col=c;
        cell.appendChild(input);
      }
      crosswordGrid.appendChild(cell);
    }
  }
  crosswordClues.innerHTML+="<strong>Waagerecht:</strong><ul>"+crosswordPuzzle.clues.across.map(c=>`<li>${c}</li>`).join("")+"</ul>";
  crosswordClues.innerHTML+="<strong>Senkrecht:</strong><ul>"+crosswordPuzzle.clues.down.map(c=>`<li>${c}</li>`).join("")+"</ul>";
  const checkBtn=document.createElement('button');
  checkBtn.textContent="Antworten prüfen";
  checkBtn.classList.add('game-button');
  checkBtn.onclick=checkCrosswordSolution;
  crosswordMessage.insertAdjacentElement("afterend",checkBtn);
}

function checkCrosswordSolution(){
  let correct=true;
  crosswordGrid.querySelectorAll('input').forEach(i=>{
    const r=i.dataset.row, c=i.dataset.col;
    if(i.value.toUpperCase()===crosswordPuzzle.grid[r][c]){
      i.style.backgroundColor="#90EE90";
    } else {
      i.style.backgroundColor="#FFB6C1";
      correct=false;
    }
  });
  crosswordMessage.textContent=correct?"✅ Rätsel korrekt gelöst!":"❌ Noch nicht alles richtig.";
}
crosswordRestartButton.addEventListener('click',initializeCrosswordGame);

// Cookie-Banner (optional: einfaches Ausblenden)
const cookieBanner = document.getElementById('cookie-banner');
const acceptBtn = document.getElementById('accept-cookies');
const declineBtn = document.getElementById('decline-cookies');
if (acceptBtn) acceptBtn.addEventListener('click', ()=> cookieBanner.style.display='none');
if (declineBtn) declineBtn.addEventListener('click', ()=> cookieBanner.style.display='none');

// Startseite beim Laden
zeigeInhalt('Homepage');
}

function showGame(gameName){
