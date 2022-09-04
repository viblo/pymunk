"""Showcase of a elastic spiderweb (drawing with pyglet)

It is possible to grab one of the crossings with the mouse
"""


__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import pyglet

import pymunk
from pymunk.vec2d import Vec2d

config = pyglet.gl.Config(sample_buffers=1, samples=2, double_buffer=True)
window = pyglet.window.Window(config=config, vsync=False)
space = pymunk.Space()

space.gravity = 0, -900
space.damping = 0.999
c = Vec2d(window.width / 2.0, window.height / 2.0)

### WEB
web_group = 1
bs = []
dist = 0.3

cb = pymunk.Body(1, 1)
cb.position = c
s = pymunk.Circle(cb, 15)  # to have something to grab
s.filter = pymunk.ShapeFilter(group=web_group)
s.ignore_draw = True
space.add(cb, s)

# generate each crossing in the net
for x in range(101):
    b = pymunk.Body(1, 1)
    v = Vec2d(1, 0).rotated_degrees(x * 18)
    scale = window.height / 2.0 / 6.0 * 0.5

    dist += 1 / 18.0
    dist = dist ** 1.005

    offset = 0.0
    offset = [0.0, -0.80, -1.0, -0.80][((x * 18) % 360) // 18 % 4]
    offset = 0.8 + offset

    offset *= dist ** 2.8 / 100.0

    v = v.scale_to_length(scale * (dist + offset))

    b.position = c + v
    s = pymunk.Circle(b, 15)
    s.filter = pymunk.ShapeFilter(group=web_group)
    s.ignore_draw = True
    space.add(b, s)
    bs.append(b)


def add_joint(a, b):
    rl = a.position.get_distance(b.position) * 0.9
    stiffness = 5000.0
    damping = 100
    j = pymunk.DampedSpring(a, b, (0, 0), (0, 0), rl, stiffness, damping)
    j.max_bias = 1000
    # j.max_force = 50000
    space.add(j)


for b in bs[:20]:
    add_joint(cb, b)

for i in range(len(bs) - 1):
    add_joint(bs[i], bs[i + 1])

    i2 = i + 20
    if len(bs) > i2:
        add_joint(bs[i], bs[i2])


### WEB ATTACH POINTS
static_bs = []
for b in bs[-17::4]:
    static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    static_body.position = b.position
    static_bs.append(static_body)

    # j = pymunk.PivotJoint(static_body, b, static_body.position)
    j = pymunk.DampedSpring(static_body, b, (0, 0), (0, 0), 0, 0, 0)
    j.damping = 100
    j.stiffness = 20000
    space.add(j)

### ALL SETUP DONE


def update(dt):
    # Note that we dont use dt as input into step. That is because the
    # simulation will behave much better if the step size doesnt change
    # between frames.
    r = 10
    for _ in range(r):
        space.step(1.0 / 30.0 / r)


pyglet.clock.schedule_interval(update, 1 / 30.0)

selected = None
selected_joint = None
mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)


@window.event
def on_mouse_press(x, y, button, modifiers):
    mouse_body.position = Vec2d(x, y)
    hit = space.point_query_nearest((x, y), 10, pymunk.ShapeFilter())
    if hit != None:
        global selected
        body = hit.shape.body
        rest_length = mouse_body.position.get_distance(body.position)
        stiffness = 1000
        damping = 10
        selected = pymunk.DampedSpring(
            mouse_body, body, (0, 0), (0, 0), rest_length, stiffness, damping
        )
        space.add(selected)


@window.event
def on_mouse_release(x, y, button, modifiers):
    global selected
    if selected != None:
        space.remove(selected)
        selected = None


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    mouse_body.position = x, y


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.P:
        pyglet.image.get_buffer_manager().get_color_buffer().save("spiderweb.png")


fps_display = pyglet.window.FPSDisplay(window)


@window.event
def on_draw():
    pyglet.gl.glClearColor(240, 240, 240, 255)
    window.clear()

    fps_display.draw()

    # static attach points
    pyglet.gl.glColor3f(1, 0, 1)
    pyglet.gl.glPointSize(6)
    a = []
    for b in static_bs:
        a += [b.position.x, b.position.y]
        pyglet.graphics.draw(len(a) // 2, pyglet.gl.GL_POINTS, ("v2f", a))

    # web crossings / bodies
    pyglet.gl.glColor3f(0.8, 0.8, 0.8)
    a = []
    for b in bs:
        a += [b.position.x, b.position.y]
    pyglet.gl.glPointSize(4)
    pyglet.graphics.draw(len(a) // 2, pyglet.gl.GL_POINTS, ("v2f", a))

    # web net / constraints
    a = []
    for j in space.constraints:
        a += [j.a.position.x, j.a.position.y, j.b.position.x, j.b.position.y]
    pyglet.graphics.draw(len(a) // 2, pyglet.gl.GL_LINES, ("v2f", a))

    # anything else


pyglet.app.run()
