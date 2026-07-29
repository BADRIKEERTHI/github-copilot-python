import json
import os

SCORE_FILE = "static/data/scores.json"


def load_scores():
    if not os.path.exists(SCORE_FILE):
        return []

    with open(SCORE_FILE, "r") as file:
        return json.load(file)


def save_score(score):
    scores = load_scores()

    scores.append(score)

    # Sort by fastest time
    scores.sort(key=lambda x: x["time"])

    # Keep only top 10
    scores = scores[:10]

    with open(SCORE_FILE, "w") as file:
        json.dump(scores, file, indent=4)


def get_top_scores():
    return load_scores()