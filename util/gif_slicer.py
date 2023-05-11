import os
from PIL import Image, ImageSequence
if not os.path.exists("sliced"):
    os.mkdir("sliced")

name = r"./resources/resources/menu/8094957"
image = Image.open(name + '.gif')
i = 0
for frame in ImageSequence.Iterator(image):
    i += 1
    # img = frame.resize((512, 512)) # size of gif (x, y)
    frame.save(name + "_" + str(i) + ".png")
