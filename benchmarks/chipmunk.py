import math

import pygame

import pymunk
import pymunk.pygame_util

"""
Benchmarks

# Higher is better tests (stability/accuracy) tests

- Stack boxes and see how tall until fall down
- Newtons pendulum

# Perf tests

- Big body with high velocity hit group of circle in zero gravity. 1000? bodies

- Slow explosion

"""


class Benchmark:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = 0, 10

    def update(self, dt):
        self.space.step(dt)

    def draw(self, draw_options):
        self.space.debug_draw(draw_options)


class FallingSquares(Benchmark):
    def __init__(self, size):
        super().__init__()
        self.space.static_body.position = 0, 10
        ground = pymunk.Poly.create_box(self.space.static_body, (200, 20))
        self.space.add(ground)

        for i in range(15):
            a = 0.5 + i / 15 * 2.5
            for j in range(size):
                b = pymunk.Body()
                b.position = i * 7 - 60, -2 * a * (size - j)

                p = pymunk.Poly.create_box(b, (a, a))
                p.density = 5
                self.space.add(b, p)


class FallingCircles(Benchmark):
    def __init__(self, size):
        super().__init__()
        self.space.static_body.position = 0, 10
        ground = pymunk.Poly.create_box(self.space.static_body, (200, 20))
        self.space.add(ground)

        for i in range(15):
            a = 0.5 + i / 15 * 2.5
            for j in range(size):
                b = pymunk.Body()
                b.position = i * 7 + j * 0.25 - 60, -2 * a * (size - j)
                c = pymunk.Circle(b, a / 2)
                c.density = 5
                self.space.add(b, c)


class SlowExplosion(Benchmark):
    def __init__(self, size):
        super().__init__()
        self.space.gravity = 0, 0

        for i in range(size):
            b = pymunk.Body()
            c = pymunk.Circle(b, 0.5)
            c.density = 0.5
            s = i * 30 / size
            x = math.cos(s * 30) * (s * 30 + 5)
            y = math.sin(s * 30) * (s * 30 + 5)
            b.position = pymunk.Vec2d(x, y)
            b.velocity = 0.2 * b.position
            self.space.add(b, c)


class MildN2(Benchmark):
    def __init__(self, size):
        super().__init__()
        ground = pymunk.Segment(self.space.static_body, (-50, 0), (50, 0), 1)
        self.space.add(ground)

        # table
        for i in range(size):
            b = pymunk.Body()
            b.position = -5, -1

            top = pymunk.Poly.create_box_bb(
                b,
                pymunk.BB(-3, -3, 3, -4),
            )
            left = pymunk.Poly.create_box_bb(
                b,
                pymunk.BB(-3, -3, -2, 2),
            )
            right = pymunk.Poly.create_box_bb(
                b,
                pymunk.BB(2, -3, 3, 2),
            )
            top.density = 2
            left.density = 2

            self.space.add(top, left, right, b)

        # triangle
        for i in range(size):
            b = pymunk.Body()
            b.position = 15, -1
            left = pymunk.Poly(b, [(-2, 0), (1, -2), (0, -4)])
            left.density = 3

            right = pymunk.Poly(b, [(2, 0), (-1, -2), (0, -4)])
            right.density = 3

            self.space.add(b, left, right)


class N2(Benchmark):
    def __init__(self, size):
        super().__init__()
        # ground = pymunk.Segment(space.static_body, (-50, 0), (50, 0), 1)
        # space.add(ground)

        for i in range(size):
            b = pymunk.Body()
            b.position = (i * 0.01, -i * 0.01)
            c = pymunk.Circle(b, 1)
            c.density = 1
            self.space.add(b, c)


class Diagonal(Benchmark):
    def __init__(self, size):
        super().__init__()

        a = 0.5
        N = size
        M = size / 2
        position = pymunk.Vec2d(0, 0)
        for j in range(int(M)):
            position = pymunk.Vec2d(-N * a * 3, position.y)

            for i in range(N):
                b = pymunk.Body(body_type=pymunk.Body.STATIC)
                # (float hx, float hy, const b2Vec2 &center, float angle)

                b.position = position
                b.angle = math.pi / 4
                s = pymunk.Poly.create_box(b, (a, ((3 * j + 1) * a)))
                self.space.add(b, s)
                position = position + ((8 * a), 0)
            position = position - (0, 8 * a)

        for i in range(3000):
            b = pymunk.Body()
            b.position = (i / 15) * 2 - 75, -(i % 15 * 2) - 50

            c = pymunk.Circle(b, 0.5)
            c.density = 1

            self.space.add(b, c)


class Tumbler(Benchmark):
    def __init__(self, size):
        super().__init__()

        self.m_count = 0
        self.e_count = size

        b = pymunk.Body()
        b.position = 0, 10
        s1 = pymunk.Segment(b, (-10, 10), (10, 10), 0.5)
        s2 = pymunk.Segment(b, (10, 10), (10, -10), 0.5)
        s3 = pymunk.Segment(b, (10, -10), (-10, -10), 0.5)
        s4 = pymunk.Segment(b, (-10, -10), (-10, 10), 0.5)
        s1.density = 5
        s2.density = 5
        s3.density = 5
        s4.density = 5

        j1 = pymunk.constraints.SimpleMotor(self.space.static_body, b, 1)
        j2 = pymunk.constraints.PinJoint(self.space.static_body, b, (0, 0), (0, 0))
        self.space.add(b, s1, s2, s3, s4, j1, j2)

    def update(self, dt):
        super().update(dt)
        if self.m_count < self.e_count:
            b = pymunk.Body()
            b.position = 0, 10
            s = pymunk.Poly.create_box(b, (0.125, 0.125))
            s.density = 1
            self.space.add(b, s)
            self.m_count += 1


class Multifixture(Benchmark):
    def __init__(self, size):
        super().__init__()

        s1 = pymunk.Segment(self.space.static_body, (-35, 0), (35, 0), 1)
        s2 = pymunk.Segment(self.space.static_body, (-36, -50), (-36, 0), 1)
        s3 = pymunk.Segment(self.space.static_body, (36, -50), (36, 0), 1)

        self.space.add(s1, s2, s3)

        for i in range(size):
            b = pymunk.Body()
            b.position = -20 + (i % 6) * 7 + i / 10, 1 + (i / 6) * 5
            c = int(50 - i / 2)
            for z in range(c):
                bs = 2 / 2
                ps = 2 * z * bs + bs

                top = pymunk.Poly.create_box_bb(
                    b,
                    pymunk.BB(-3, -3, 3, -4),
                )
                left = pymunk.Poly.create_box_bb(
                    b,
                    pymunk.BB(-3, -3, -2, 2),
                )
                right = pymunk.Poly.create_box_bb(
                    b,
                    pymunk.BB(2, -3, 3, 2),
                )
                top.density = 2
                left.density = 2

                self.space.add(top, left, right, b)


class AddPair(Benchmark):
    def __init__(self, size):
        super().__init__()
        self.space.gravity = 0, 0
        self.space.iterations = 50
        minX = -9.0
        maxX = 9.0
        minY = 4.0
        maxY = 6.0

        for i in range(size):
            b = pymunk.Body()
            b.position = (
                minX + (maxX - minX) * i / size,
                minY + (maxY - minY) * (i % 32) / 32,
            )

            shape = pymunk.Circle(b, 0.1)
            shape.density = 0.01
            self.space.add(b, shape)

        b = pymunk.Body()
        b.position = -40, 5
        shape = pymunk.Poly.create_box(b, (1.5, 1.5))
        shape.density = 1

        b.velocity = 175, 0
        self.space.add(b, shape)


class MostlyStaticSingleBody(Benchmark):
    def __init__(self, size):
        super().__init__()

        a = 0.5

        N = size
        M = size

        position = pymunk.Vec2d(0, 0)

        for j in range(M):
            position = pymunk.Vec2d(-N * a, position.y)

            for i in range(N):
                print(position)
                if abs(j - i) > 3:

                    shape = pymunk.Poly.create_box_bb(
                        self.space.static_body,
                        pymunk.BB(
                            position.x - a,
                            position.y - a,
                            position.x + a,
                            position.y + a,
                        ),
                    )
                    self.space.add(shape)
                elif i == j:
                    b = pymunk.Body()
                    b.position = position
                    shape = pymunk.Circle(b, a * 2)
                    shape.density = 1
                    self.space.add(b, shape)

                position = position + (2 * a, 0)
            position = position - (0, 2 * a)


class MostlyStaticMultiBody(Benchmark):
    def __init__(self, size):
        super().__init__()

        a = 0.5

        N = size
        M = size

        position = pymunk.Vec2d(0, 0)

        for j in range(M):
            position = pymunk.Vec2d(-N * a, position.y)

            for i in range(N):
                print(position)
                if abs(j - i) > 3:
                    b = pymunk.Body(body_type=pymunk.Body.STATIC)
                    b.position = position
                    shape = pymunk.Poly.create_box(b, (a * 2, a * 2))
                    self.space.add(b, shape)
                elif i == j:
                    b = pymunk.Body()
                    b.position = position
                    shape = pymunk.Circle(b, a * 2)
                    shape.density = 1
                    self.space.add(b, shape)

                position = position + (2 * a, 0)
            position = position - (0, 2 * a)


class MixedStaticDynamic(Benchmark):
    def __init__(self, size):
        super().__init__()

        N = 150
        M = 150
        cntr = pymunk.Vec2d(M / 2, N / 2)
        a = 0.5

        for j in range(M):
            for i in range(N):
                pos = pymunk.Vec2d(i, j)

                if (pos - cntr).dot(pos - cntr) > 67 * 67:
                    shape = pymunk.Circle(self.space.static_body, a, pos)
                    self.space.add(shape)

        for i in range(size):
            s = i / size

            pos = pymunk.Vec2d(
                math.cos(s * 30) * (s * 50 + 10), math.sin(s * 30) * (s * 50 + 10)
            )
            b = pymunk.Body()
            b.position = pos + cntr
            b.velocity = pos
            shape = pymunk.Circle(b, a)
            shape.density = 0.5
            self.space.add(b, shape)


tests = [
    FallingSquares,
    FallingCircles,
    Tumbler,
    AddPair,
    MildN2,
    N2,
    Multifixture,
    MostlyStaticSingleBody,
    MostlyStaticMultiBody,
    Diagonal,
    MixedStaticDynamic,
    SlowExplosion,
]


screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

# space = pymunk.Space()

draw_options = pymunk.pygame_util.DrawOptions(screen)
draw_options.flags = draw_options.DRAW_SHAPES

# FallingSquares(space, 200)
# FallingCircles(space, 200)
# sim = Tumbler(1000)
# sim = Multifixture(100)
# MildN2(space, 50)
# N2(space, 500)
# Diagonal(space, 100)
# SlowExplosion(space, 5000)
# sim = AddPair(2000)
# sim = MostlyStaticSingleBody(50)
# sim = MostlyStaticMultiBody(50)
sim = MixedStaticDynamic(6000)


translation = pymunk.Transform()
scaling = 2

steps = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            quit()

    keys = pygame.key.get_pressed()
    zoom_in = int(keys[pygame.K_a])
    zoom_out = int(keys[pygame.K_z])
    zoom_speed = 0.1
    scaling *= 1 + (zoom_speed * zoom_in - zoom_speed * zoom_out)

    draw_options.transform = pymunk.Transform.translation(
        300, 300
    ) @ pymunk.Transform.scaling(scaling)

    fps = 60.0
    dt = 1.0 / fps
    sim.update(dt)
    steps += 1

    screen.fill(pygame.Color("white"))
    sim.draw(draw_options)
    pygame.display.flip()

    clock.tick(fps)
    pygame.display.set_caption(f"step {steps} fps {clock.get_fps():.2f}")


class Stacking:

    def __init__(self):
        self.space = pymunk.Space()

        s = pymunk.Segment(self.space.static_body, (0, 500), (500, 500), 5)

    def update(self, dt):
        pass

    def draw(self):
        pass
