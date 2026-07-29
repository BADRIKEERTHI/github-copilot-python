// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];
let timerInterval;
let seconds = 0;
let hintsUsed = 0;
function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}
function startTimer() {
  clearInterval(timerInterval);
  seconds = 0;

  timerInterval = setInterval(() => {
    seconds++;

    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;

    document.getElementById('timer').innerText =
      `Time: ${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
  }, 1000);
}
async function newGame() {
  const difficulty = document.getElementById('difficulty').value;

  const res = await fetch(`/new?difficulty=${difficulty}`);
  const data = await res.json();
  hintsUsed = 0;

  renderPuzzle(data.puzzle);
  document.getElementById('message').innerText = '';
  startTimer();
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
  }
  if (incorrect.size === 0) {
    msg.style.color = '#388e3c';
    msg.innerText = 'Congratulations! You solved it!';

    saveScore();
}
 else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}
async function getHint() {
  const res = await fetch('/hint');
  const data = await res.json();

  if (data.error) {
    document.getElementById('message').innerText = data.error;
    return;
  }
  hintsUsed++;

  const inputs = document
    .getElementById('sudoku-board')
    .getElementsByTagName('input');

  const index = data.row * SIZE + data.col;

  inputs[index].value = data.value;
  inputs[index].disabled = true;
  inputs[index].className += ' prefilled';

  document.getElementById('message').innerText = 'Hint used!';
}
async function loadLeaderboard() {
  const res = await fetch('/scores');
  const scores = await res.json();

  const list = document.getElementById('score-list');
  list.innerHTML = '';

  scores.forEach(score => {
    const item = document.createElement('li');

    item.innerText =
      `${score.name} - ${score.time}s - ${score.difficulty} - Hints: ${score.hints}`;

    list.appendChild(item);
  });
}
async function saveScore() {
  const name = prompt("Enter your name:");

  const difficulty = document.getElementById('difficulty').value;

  await fetch('/save-score', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: name || "Player",
      time: seconds,
      difficulty: difficulty,
      hints: hintsUsed
    })
  });

  loadLeaderboard();
}
function toggleDarkMode() {
  document.body.classList.toggle('dark');

  const enabled = document.body.classList.contains('dark');

  localStorage.setItem('darkMode', enabled);
}
// Wire buttons
window.addEventListener('load', () => {
  if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark');
}
   
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint-button').addEventListener('click', getHint);
  document.getElementById('dark-toggle').addEventListener('click', toggleDarkMode);

  // initialize
  loadLeaderboard();
  newGame();
});