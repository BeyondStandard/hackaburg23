import os
from PIL import Image


def create_thumbnail(origin_path: str, new_folder: str, size=32):
    img_name = os.path.basename(origin_path)
    img = Image.open(origin_path)
    img.thumbnail((size, size))
    img.save(f"{new_folder}/{img_name}", format="png")

def create_thumbnails(parent_folder: str, thumbnail_folder: str):
    for png_file in os.listdir(parent_folder):
        create_thumbnail(f"{parent_folder}/{png_file}", thumbnail_folder)

if __name__ == "__main__":
    create_thumbnails("/home/ec2-user/data/anomaly", "/home/ec2-user/thumbnails/anomaly")
    create_thumbnails("/home/ec2-user/data/golden", "/home/ec2-user/thumbnails/golden")
