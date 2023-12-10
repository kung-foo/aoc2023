#!/usr/bin/env python3

from PIL import Image, ImageOps, ImageDraw

img = Image.open("turtle_output.png")
img = img.crop([x + 1 for x in ImageOps.invert(img).getbbox()])  # pad by one pixel
img.save("cropped.png")

# red all the things!!!
ImageDraw.floodfill(img, (0, 0), (255, 0, 0))

# AC/DC Back in Black 🤘🤘
ImageDraw.floodfill(img, (0, 0), (0, 0, 0))

img.save("flooded.png")

for count, color in img.getcolors():
    if color == (255, 0, 0):
        print("part2:", count)
