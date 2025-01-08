import json
from typing import List

from .score import Score
from ..asset_helper import get_save_data_path

def read_save_data() -> List[Score]:
    data = []

    try:
        with open(get_save_data_path(), "r") as file:
            data = json.load(file)  # Load JSON data (assumed to be a list)

            try:
                for item in data:
                    Score.from_dict(item) # Check integrity of each entry (make sure it is a valid "Score" object)
            except (ValueError, KeyError) as e:
                print(f"Error in save data: {e}")
                generate_save_file() # reset corrupted file
                data = [] # ensure we return an empty list rather than the "bad" data
    except Exception:
        print("Error loading save data, making new file and starting with empty list")
        generate_save_file()

    return data # Either list of scores or empty list if error/not exist
    
def generate_save_file():
    with open(get_save_data_path(), "w") as file:
        file.write("[]")