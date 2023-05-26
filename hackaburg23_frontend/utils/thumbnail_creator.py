import os
from PIL import Image


def create_thumbnail(origin_path: str, new_folder: str, size=32):
    img_name = os.path.basename(origin_path)
    img = Image.open(origin_path)
    img.thumbnail(size)
    img.save(f"{new_folder}/{img_name}", format="png")

def create_thumbnails(root_folder: str, new_folder: str):
    for parent_folder, sub_folders, files in os.walk(root_folder):
        pass
