import json

from .score import Score
from .score_reader import read_save_data
from ..asset_helper import get_save_data_path

def save_game_data(score: Score):
    scores = read_save_data()
    scores.append(score.to_dict())
    with open(get_save_data_path(), "w") as file:
        json.dump(scores, file, indent=4)