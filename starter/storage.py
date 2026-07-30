import json
import os

SCORE_FILE = os.path.join(os.path.dirname(__file__), "static", "data", "scores.json")


def ensure_scores_file():
    score_dir = os.path.dirname(SCORE_FILE)
    os.makedirs(score_dir, exist_ok=True)

    if not os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)


def load_scores():
    ensure_scores_file()

    try:
        with open(SCORE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, ValueError):
        return []


def save_score(score):
    ensure_scores_file()

    scores = load_scores()
    scores.append(score)

    # Sort by fastest time and keep only top 10 scores
    scores.sort(key=lambda x: x.get("time", float("inf")))
    scores = scores[:10]

    with open(SCORE_FILE, "w", encoding="utf-8") as file:
        json.dump(scores, file, indent=4)


def get_top_scores():
    return load_scores()