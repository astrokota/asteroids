import os

def get_asset_path(filename):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(project_root, "assets", filename)

def get_save_data_path():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    save_path = os.path.join(project_root, "asteroids_save_data", "asteroids_save_data.txt")
    save_dir = os.path.dirname(save_path)

    # Ensure the directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    return save_path