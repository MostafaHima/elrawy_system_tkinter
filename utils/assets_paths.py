import os

def asset_path(filename):
    assets_folder = os.path.join(os.path.expanduser("~"), "MyProgramData", "elrawy_app", "assets")
    return os.path.join(assets_folder, filename)
