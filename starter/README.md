# Flask Sudoku Game

A modern Sudoku web application built using Flask, HTML, CSS, and JavaScript.

## Features

- Random Sudoku puzzle generation
- Unique solution validation
- Easy, Medium, Hard difficulty levels
- Check solution button
- Hint system
- Game timer
- Top 10 leaderboard
- Persistent scores
- Dark mode
- Responsive UI

## Technologies Used

- Python
- Flask
- JavaScript
- HTML
- CSS
- Pytest

## Run Project

### Create virtual environment

```bash
py -m venv .venv
```

### Activate virtual environment

```bash
.\.venv\Scripts\Activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
py app.py
```

Open the application in browser:

```
http://127.0.0.1:5000
```

## Testing

Run tests:

```bash
pytest
```

Test Result:

```
2 passed
```

## Project Structure

```
app.py
sudoku_logic.py
storage.py
requirements.txt
README.md

templates/
    index.html

static/
    main.js
    styles.css

tests/
    test_sudoku.py

screenshots/
```

## GitHub Copilot Usage

GitHub Copilot was used for:

- Code suggestions
- Debugging assistance
- Improving functions
- Generating test cases
- Refactoring code

## Conclusion

This project is a complete Flask-based Sudoku game with puzzle generation, solution checking, hints, timer, leaderboard, dark mode, and automated testing.