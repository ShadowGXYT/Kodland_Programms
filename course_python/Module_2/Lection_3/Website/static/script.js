function zeigeInhalt(id){
    document.querySelectorAll("main section").forEach(s=>s.style.display="none");
    document.getElementById(id+"-content").style.display="block";
}

function showGame(name){
    document.querySelectorAll(".game-area").forEach(g=>g.style.display="none");
    document.getElementById(name+"-game-content").style.display="block";

    if(name==="Sudoku") initSudoku();
    if(name==="Kreuzwortraetsel") initCrossword();
}

function hideCookie(){
    document.getElementById("cookie-banner").style.display="none";
}

/* --- Sudoku --- */
const sudoku = [
 [5,3,"","","7","","","",""],
 [6,"","",1,9,5,"","",""],
 ["",9,8,"","","","",6,""]
];

function initSudoku(){
    const grid=document.getElementById("sudoku-grid");
    grid.innerHTML="";
    sudoku.flat().forEach(v=>{
        let i=document.createElement("input");
        if(v!==""){ i.value=v; i.disabled=true; }
        grid.appendChild(i);
    });
}

/* --- Kreuzwort --- */
const crossword=[
 ['C','A','T','',''],
 ['','R','','D','O'],
 ['D','O','G','','G']
];

function initCrossword(){
    const grid=document.getElementById("crossword-grid");
    grid.innerHTML="";
    crossword.flat().forEach(v=>{
        let i=document.createElement("input");
        if(v==="") i.disabled=true;
        grid.appendChild(i);
    });
}

zeigeInhalt("Homepage");
