from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Sudoku Daten ---
sudoku_puzzles = [
    {
        "puzzle": [
            [5,3,None,None,7,None,None,None,None],
            [6,None,None,1,9,5,None,None,None],
            [None,9,8,None,None,None,None,6,None],
            [8,None,None,None,6,None,None,None,3],
            [4,None,None,8,None,3,None,None,1],
            [7,None,None,None,2,None,None,None,6],
            [None,6,None,None,None,None,2,8,None],
            [None,None,None,4,1,9,None,None,5],
            [None,None,None,None,8,None,None,7,9]
        ],
        "solution": [
            [5,3,4,6,7,8,9,1,2],
            [6,7,2,1,9,5,3,4,8],
            [1,9,8,3,4,2,5,6,7],
            [8,5,9,7,6,1,4,2,3],
            [4,2,6,8,5,3,7,9,1],
            [7,1,3,9,2,4,8,5,6],
            [9,6,1,5,3,7,2,8,4],
            [2,8,7,4,1,9,6,3,5],
            [3,4,5,2,8,6,1,7,9]
        ]
    }
]

# --- Kreuzworträtsel Daten ---
crossword_puzzle = {
    "grid":[
        ['C','A','T',None,None],
        [None,'R',None,'D','O'],
        ['D','O','G',None,'G'],
        [None,'W',None,'I',None],
        [None,'E','A','R',None]
    ],
    "clues":{
        "across":["1. Katze (engl.)","3. Hund (engl.)","5. Ohr (engl.)"],
        "down":["1. Karte (engl.)","2. Holz (engl.)","4. Insekt (engl., bug)"]
    }
}

# --- Routen ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check_sudoku", methods=["POST"])
def check_sudoku():
    user_grid = request.json.get("grid")
    solution = sudoku_puzzles[0]["solution"]
    correct = True
    feedback = []
    for r in range(9):
        row_feedback = []
        for c in range(9):
            if user_grid[r][c] == solution[r][c]:
                row_feedback.append(True)
            else:
                row_feedback.append(False)
                correct = False
        feedback.append(row_feedback)
    return jsonify({"correct": correct, "feedback": feedback})

@app.route("/check_crossword", methods=["POST"])
def check_crossword():
    user_grid = request.json.get("grid")
    solution = crossword_puzzle["grid"]
    correct = True
    feedback = []
    for r in range(len(solution)):
        row_feedback = []
        for c in range(len(solution[0])):
            if solution[r][c] is None:
                row_feedback.append(None)
            elif str(user_grid[r][c]).upper() == solution[r][c]:
                row_feedback.append(True)
            else:
                row_feedback.append(False)
                correct = False
        feedback.append(row_feedback)
    return jsonify({"correct": correct, "feedback": feedback})

if __name__ == "__main__":
    app.run(debug=True)
