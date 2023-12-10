#!/usr/bin/env python3

from PIL import Image, ImageOps, ImageDraw

img = Image.open("turtle_output.png")
img = img.crop([x + 1 for x in ImageOps.invert(img).getbbox()])  # pad by one pixel
img.save("cropped.png")

# wipe out all external red dots
ImageDraw.floodfill(img, (0, 0), (255, 0, 0))

# fill back in with back
ImageDraw.floodfill(img, (0, 0), (0, 0, 0))

img.save("flooded.png")

for count, color in img.getcolors():
    if color == (255, 0, 0):
        print("part2:", count)
