import os
from PIL import Image
from PIL.ImageOps import grayscale

level_screenshots = [
    "./level_screenshots/" + file for file in os.listdir("./level_screenshots/")
]
for screenshot in level_screenshots:
    with Image.open(screenshot) as img:
        bw = grayscale(img)
        bw.save(screenshot.replace(".png", "_bw.png"))
