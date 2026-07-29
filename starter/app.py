from flask import Flask, render_template, jsonify, request
import sudoku_logic
import storage

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty', 'medium')
    puzzle, solution = sudoku_logic.generate_puzzle(difficulty)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle})
@app.route('/hint')
def get_hint():
    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')

    if puzzle is None or solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            if puzzle[row][col] == 0:
                value = solution[row][col]

                # Update stored puzzle so next hint moves to another cell
                puzzle[row][col] = value

                return jsonify({
                    'row': row,
                    'col': col,
                    'value': value
                })

    return jsonify({'error': 'No hints available'})

    return jsonify({'error': 'No hints available'})
@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})
@app.route('/scores')
def scores():
    return jsonify(storage.get_top_scores())


@app.route('/save-score', methods=['POST'])
def save_score():
    data = request.json
    print("SCORE RECEIVED: - app.py:70", data)

    storage.save_score({
        "name": data.get("name", "Player"),
        "time": data.get("time", 0),
        "difficulty": data.get("difficulty", "medium"),
        "hints": data.get("hints", 0)
    })

    return jsonify({"message": "Score saved"})
if __name__ == '__main__':
    app.run(debug=True)