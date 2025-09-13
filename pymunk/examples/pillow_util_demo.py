"""Showcase what the output of pymunk.pyglet_util draw methods will look like.

See pygame_util_demo.py for a comparison to pygame.
"""

__docformat__ = "reStructuredText"

from PIL import Image, ImageDraw, ImageColor, ImageShow

import pymunk
import pymunk.pillow_util

from .shapes_for_draw_demos import fill_space

img = Image.new("RGB", (1000, 700), ImageColor.getrgb("white"))
draw = ImageDraw.Draw(img)

space = pymunk.Space()
draw_options = pymunk.pillow_util.DrawOptions(img)
captions = fill_space(space)



labels = []

draw.text((5,5),"Demo example of shapes drawn by pillow_util.draw()", fill=(100,100,100))

for caption in captions:
    x, y = caption[0]
    y = y - 10
    draw.text((x,y),caption[1], fill=(50,50,50))

space.debug_draw(draw_options)

img.save("pillow_util_demo.png")
ImageShow.show(img)