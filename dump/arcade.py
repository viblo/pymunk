import math

import pyglet

import pymunk
import pymunk.pyglet_util

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
BOX_SIZE = 45


class Main(pyglet.window.Window):
    def __init__(self, width, height):
        pyglet.window.Window.__init__(self, vsync=False)

        self.draw_options = pymunk.pyglet_util.DrawOptions()
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

        # -- Pymunk space
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)

        # Create the floor
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.floor = pymunk.Segment(body, [0, 10], [SCREEN_WIDTH, 10], 0.0)
        self.floor.friction = 10
        self.space.add(self.floor)

        # Create the circle
        player_x = 300
        player_y = 300
        mass = 2
        radius = 25
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        circle_body = pymunk.Body(mass, inertia)
        circle_body.position = pymunk.Vec2d(player_x, player_y)
        self.circle_shape = pymunk.Circle(circle_body, radius, pymunk.Vec2d(0, 0))
        self.circle_shape.friction = 1

        self.space.add(circle_body, self.circle_shape)

        # Create the box
        size = BOX_SIZE
        mass = 5
        moment = pymunk.moment_for_box(mass, (size, size))
        moment = float("inf")
        body = pymunk.Body(mass, moment)
        body.position = pymunk.Vec2d(player_x, player_y + 49)
        self.box_shape = pymunk.Poly.create_box(body, (size, size))
        self.box_shape.friction = 0.3
        self.space.add(body, self.box_shape)

        # Create a joint between them
        constraint = pymunk.constraint.PinJoint(
            self.box_shape.body, self.circle_shape.body, (-20, 0), (0, 0)
        )
        self.space.add(constraint)

        constraint = pymunk.constraint.PinJoint(
            self.box_shape.body, self.circle_shape.body, (20, 0), (0, 0)
        )
        self.space.add(constraint)

        # Make the circle rotate
        constraint = pymunk.constraint.SimpleMotor(
            self.circle_shape.body, self.box_shape.body, -3
        )
        self.space.add(constraint)

    def on_draw(self):
        """
        Render the screen.
        """
        self.clear()
        self.space.debug_draw(self.draw_options)

    def update(self, delta_time):

        # Update physics
        self.space.step(1 / 80.0)


m = Main(SCREEN_WIDTH, SCREEN_HEIGHT)
pyglet.app.run()
