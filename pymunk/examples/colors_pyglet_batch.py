"""
An example of the determinism of pymunk by coloring balls according to their 
position, and then respawning them to verify each ball ends up in the same 
place. Inspired by Pymunk user Nam Dao.

This is also a demonstration of the performance boost from the batch api in 
pymunk.batch.

Running this script for 30 seconds with cProfile, about 57% of the time is 
spent on drawing without batching, but with batching only uses 34% of
the time. The rest of the time is mainly spent on `space.Step` stepping the 
simulation forward.

To try yourself::

    > python -m cProfile -o batch_on.prof -m pymunk.examples.colors_pyglet_batch

"""


import random

import pyglet

import pymunk
import pymunk.batch
import pymunk.pyglet_util


def new_space():
    global space
    space = pymunk.Space()
    space.gravity = 0, -900
    static_body = space.static_body
    walls = [
        pymunk.Segment(static_body, (20, 650), (0, 0), 20),
        pymunk.Segment(static_body, (0, 0), (600, 0), 20),
        pymunk.Segment(static_body, (600, 0), (580, 650), 20),
        pymunk.Segment(static_body, (250, 300), (600, 450), 3),
    ]

    space.add(*walls)
    random.seed(0)
    for _ in range(3000):
        body = pymunk.Body()
        x = random.randint(100, 450)
        y = random.randint(480, 580)
        body.position = x, y
        # shape = pymunk.Circle(body, 6)
        shape = pymunk.Circle(body, 3)
        shape.mass = 1
        space.add(body, shape)

    return space


window = pyglet.window.Window(600, 600, vsync=False)
pyglet.gl.glClearColor(0, 0, 0, 1.0)
fps_display = pyglet.window.FPSDisplay(window, samples=60)

textbatch = pyglet.graphics.Batch()
l1 = pyglet.text.Label(
    "Press r to reset and respawn all balls."
    " Press c to set color of each ball according to its position.",
    x=1,
    y=587,
    batch=textbatch,
    font_size=10,
    color=(100, 100, 100, 255),
)
l2 = pyglet.text.Label(
    "Press b to toggle pymunk.batch to get ball positions.",
    x=1,
    y=567,
    batch=textbatch,
    font_size=10,
    color=(100, 100, 100, 255),
)


draw_options = pymunk.pyglet_util.DrawOptions()

colors = []
batch_colors = []
batch_enabled = True

buffer = pymunk.batch.Buffer()
shader = pyglet.shapes.get_default_shader()
vlist = None
batch = pyglet.graphics.Batch()


def add_color(colors, x, y):
    r = x / 600 * 255
    g = max((600 - y - 400) / 200 * 255, 0)
    if r < 0 or r > 255 or g < 0 or g > 255:
        print(x, y)
        exit()
    colors.extend([int(r), int(g), 150, 255])


@window.event
def on_key_press(symbol, modifiers):
    global colors
    global batch_colors
    global batch_enabled
    global reuse_vlist
    if symbol == pyglet.window.key.P:
        pyglet.image.get_buffer_manager().get_color_buffer().save(
            "colors_pyglet_batch.png"
        )
    elif symbol == pyglet.window.key.R:
        new_space()
    elif symbol == pyglet.window.key.B:
        batch_enabled = not batch_enabled
        print(f"Batch mode enabled: {batch_enabled}")
    elif symbol == pyglet.window.key.C:
        colors.clear()
        batch_colors.clear()

        buffer.clear()
        pymunk.batch.get_space_bodies(
            space,
            pymunk.batch.BodyFields.BODY_ID | pymunk.batch.BodyFields.POSITION,
            buffer,
        )
        ps = list(memoryview(buffer.float_buf()).cast("d"))
        body_ids = list(memoryview(buffer.int_buf()).cast("P"))

        for idx in range(len(body_ids)):
            if space.static_body.id == body_ids[idx]:
                continue
            add_color(batch_colors, ps[idx * 2], ps[idx * 2 + 1])
        for body in space.bodies:
            add_color(colors, body.position.x, body.position.y)


def update(dt):
    dt = 1 / 20 / 5
    space.step(dt)


@window.event
def on_draw():
    global batch
    global colors
    global batch_colors
    global vlist
    pyglet.gl.glPointSize(10)

    window.clear()
    cs = colors
    if batch_enabled:
        ps = []
        buffer.clear()
        pymunk.batch.get_space_bodies(
            space,
            pymunk.batch.BodyFields.BODY_ID | pymunk.batch.BodyFields.POSITION,
            buffer,
        )
        body_ps = list(memoryview(buffer.float_buf()).cast("d"))
        body_ids = list(memoryview(buffer.int_buf()).cast("P"))
        static_id = space.static_body.id
        for idx in range(len(body_ids)):
            if static_id == body_ids[idx]:
                continue
            ps += [body_ps[idx * 2], body_ps[idx * 2 + 1]]
        cs = batch_colors
    else:
        ps = []
        for body in space.bodies:
            ps += [body.position.x, body.position.y]
    if vlist == None:
        vlist = shader.vertex_list(
            len(ps) // 2,
            pyglet.gl.GL_POINTS,
            position=("f", ps),
            colors=("B3n", cs),
            batch=batch,
        )
    else:
        # This could probably be done more efficient if the underlying batch
        # buffer were used directly (when batching is used).
        vlist.set_attribute_data("position", ps)
        vlist.set_attribute_data("colors", cs)
    batch.draw()

    fps_display.draw()
    textbatch.draw()


def reset(dt, colors, batch_colors):
    new_space()
    colors.clear()
    batch_colors.clear()
    colors.extend([0, 255, 150, 255] * len(space.bodies))
    batch_colors.clear()
    batch_colors.extend([0, 255, 150, 255] * len(space.bodies))


pyglet.clock.schedule_interval(update, 1 / 20)
pyglet.clock.schedule_once(reset, 0, colors, batch_colors)
pyglet.clock.schedule_once(lambda x: exit(), 30)  # for benchmarking
pyglet.app.run()
