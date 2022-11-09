"""
Remake of the veritcal stack demo from the box2d testbed.
"""

import pyglet
from pyglet.window import key

import pymunk
import pymunk.pyglet_util
from pymunk import Vec2d


class Main(pyglet.window.Window):
    def __init__(self):

        pyglet.window.Window.__init__(self, vsync=False)
        self.set_caption("Vertical stack from box2d")

        pyglet.clock.schedule_interval(self.update, 1 / 60.0)
        self.fps_display = pyglet.window.FPSDisplay(self)

        self.text = pyglet.text.Label(
            "Press space to fire bullet", font_size=10, x=10, y=400
        )
        self.create_world()

        self.draw_options = pymunk.pyglet_util.DrawOptions()
        self.draw_options.flags = self.draw_options.DRAW_SHAPES

    def create_world(self):
        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0.0, -900.0)
        self.space.sleep_time_threshold = 0.3

        static_lines = [
            pymunk.Segment(self.space.static_body, Vec2d(20, 55), Vec2d(600, 55), 1),
            pymunk.Segment(self.space.static_body, Vec2d(550, 55), Vec2d(550, 400), 1),
        ]
        for l in static_lines:
            l.friction = 0.3
        self.space.add(*static_lines)

        for x in range(5):
            for y in range(10):
                size = 20
                mass = 10.0
                moment = pymunk.moment_for_box(mass, (size, size))
                body = pymunk.Body(mass, moment)
                body.position = Vec2d(300 + x * 50, 105 + y * (size + 0.1))
                shape = pymunk.Poly.create_box(body, (size, size))
                shape.friction = 0.3
                self.space.add(body, shape)

    def update(self, dt):
        # Here we use a very basic way to keep a set space.step dt.
        # For a real game its probably best to do something more complicated.
        step_dt = 1 / 250.0
        x = 0
        while x < dt:
            x += step_dt
            self.space.step(step_dt)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.SPACE:
            mass = 100
            r = 15
            moment = pymunk.moment_for_circle(mass, 0, r, (0, 0))
            body = pymunk.Body(mass, moment)
            body.position = (0, 165)
            shape = pymunk.Circle(body, r, (0, 0))
            shape.friction = 0.3
            shape.color = (255, 150, 150, 255)
            self.space.add(body, shape)
            f = 200000
            body.apply_impulse_at_local_point((f, 0), (0, 0))
        elif symbol == key.ESCAPE:
            pyglet.app.exit()
        elif symbol == pyglet.window.key.P:
            pyglet.image.get_buffer_manager().get_color_buffer().save(
                "box2d_vertical_stack.png"
            )

    def on_draw(self):
        self.clear()
        self.text.draw()
        self.fps_display.draw()
        self.space.debug_draw(self.draw_options)


def main():
    main = Main()
    pyglet.app.run()


if __name__ == "__main__":
    main()
