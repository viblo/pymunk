import matplotlib.pyplot as plt
from shapes_for_draw_demos import fill_space

import pymunk
import pymunk.matplotlib_util
from pymunk.vec2d import Vec2d

space = pymunk.Space()
captions = fill_space(space, (1, 1, 0, 1))

fig = plt.figure(figsize=(14, 10))
ax = plt.axes(xlim=(0, 1000), ylim=(0, 700))
ax.set_aspect("equal")
for caption in captions:
    x, y = caption[0]
    y = y - 15
    ax.text(x, y, caption[1], fontsize=12)
o = pymunk.matplotlib_util.DrawOptions(ax)
space.debug_draw(o)
fig.savefig("matplotlib_util_demo.png", bbox_inches="tight")
