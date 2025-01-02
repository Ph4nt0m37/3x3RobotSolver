from itertools import product
import numpy as np
from PIL import Image

img = Image.open("side2.jpg")

arr = np.asarray(img, dtype=np.int16)

# Optional step to reduce the size of the image
arr = arr[::2, ::2, :]
# arr = arr[::4, ::4, :]

target_colors = np.array([
    [i, j, k]
    for i, j, k in product(range(0, 256, 48), range(0, 256, 48), range(0, 256, 48))
], dtype=np.int16)

# colors = {
#     "White": 0x97d393,
#     "Red": 0x782e02,
#     "Yellow": 0x639405,
#     "Orange": 0xb6820e,
#     "Green": 0x7c2900,
#     "Blue": 0x032225,
# }
# _color_map = {i: key for i, key in colors}
# def decompose(color):
#     red, rest = divmod(color, 2**16)
#     green, blue = divmod(rest, 2**8)
#     return [red, green, blue]

# target_colors = np.array([
#     decompose(color)
#     for color in colors.values()
# ], dtype=np.int16)

diffs = (arr[None, ...] - target_colors[:, None, None, :])
colors = np.argmin(np.abs(diffs).mean(axis=-1), axis=0)

painted = Image.fromarray(target_colors[colors].astype(np.uint8))

painted.save("imgFixed.jpg")