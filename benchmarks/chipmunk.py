import argparse
import gc
import math

import pymunk

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
    steps = 500
    default_size = 10
    size_start = 10
    size_end = 10
    size_inc = 1

    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = 0, -10

    def update(self, dt):
        self.space.step(dt)

    def draw(self, draw_options):
        self.space.debug_draw(draw_options)


class FallingSquares(Benchmark):
    steps = 1300
    default_size = 300
    size_start = 10
    size_end = 300
    size_inc = 10

    def __init__(self, size):
        super().__init__()

        self.space.static_body.position = 0, -10
        ground = pymunk.Poly.create_box(self.space.static_body, (100 * 2, 3 * 2))
        self.space.add(ground)

        for i in range(15):
            a = 0.5 + i / 15 * 2.5
            for j in range(size):
                b = pymunk.Body()
                b.position = i * 7 - 30, 2 * a * (size - j)

                p = pymunk.Poly.create_box(b, (a * 2, a * 2))
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


class BigMobile(Benchmark):
    def __init__(self, size):
        super().__init__()

        self.max_depth = size
        self.space.static_body.position = 0, 20

        a = 0.25
        h = pymunk.Vec2d(0, a)

        root = self.add_node(self.space.static_body, pymunk.Vec2d.zero(), 0, 200.0, a)

        self.space.add(pymunk.PinJoint(self.space.static_body, root, (0, 0), h))

    def add_node(
        self,
        parent: pymunk.Body,
        local_anchor: pymunk.Vec2d,
        depth: int,
        offset: float,
        a: float,
    ) -> pymunk.Body:

        density = 20.0
        h = pymunk.Vec2d(0, a)
        p = parent.position + local_anchor - h
        body = pymunk.Body()
        body.position = p

        if depth == self.max_depth:
            shape = pymunk.Poly.create_box(body, (0.25 * a * 2, a * 2))
            shape.density = density + p.x * 0.02
            self.space.add(body, shape)
            return body

        bb = pymunk.BB(-offset, -0.25 * a - a, offset, 0.25 * a - a)
        shape = pymunk.Poly.create_box_bb(body, bb)

        shape.density = density
        self.space.add(body, shape)

        a1 = pymunk.Vec2d(offset, -a)
        a2 = pymunk.Vec2d(-offset, -a)
        body1 = self.add_node(body, a1, depth + 1, 0.5 * offset, a)
        body2 = self.add_node(body, a2, depth + 1, 0.5 * offset, a)

        self.space.add(
            pymunk.PinJoint(body, body1, a1, h), pymunk.PinJoint(body, body2, a2, h)
        )

        return body


benchmarks = [
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
    BigMobile,
    SlowExplosion,
]


import timeit


def run(bench_cls, size, interactive):
    steps = 0
    fps = 60
    sim = bench_cls(size)
    gc.collect()

    start_time = timeit.default_timer()

    if interactive:
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((600, 600))
        draw_options = pymunk.pygame_util.DrawOptions(screen)
        draw_options.flags = draw_options.DRAW_SHAPES

        translation = pymunk.Transform.translation(300, 300)
        scaling = 2

    while steps < bench_cls.steps:
        if interactive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    quit()

            keys = pygame.key.get_pressed()
            left = int(keys[pygame.K_LEFT])
            up = int(keys[pygame.K_UP])
            down = int(keys[pygame.K_DOWN])
            right = int(keys[pygame.K_RIGHT])

            zoom_in = int(keys[pygame.K_a])
            zoom_out = int(keys[pygame.K_z])
            zoom_speed = 0.1

            scaling *= 1 + (zoom_speed * zoom_in - zoom_speed * zoom_out)

            translate_speed = 10 / scaling

            translation = translation.translated(
                translate_speed * left - translate_speed * right,
                translate_speed * down - translate_speed * up,
            )

            # to zoom with center of screen as origin we need to offset with
            # center of screen, scale, and then offset back
            draw_options.transform = (
                pymunk.Transform.translation(300, 300)
                @ pymunk.Transform.scaling(scaling)
                @ translation
                @ pymunk.Transform.translation(-300, -300)
            )

            screen.fill(pygame.Color("white"))
            sim.draw(draw_options)
            pygame.display.flip()

            clock.tick(fps)
            pygame.display.set_caption(
                f"step {steps} fps {clock.get_fps():.2f} total {timeit.default_timer()-start_time:.2f}s"
            )

        sim.update(1 / fps)
        steps += 1

    time_s = timeit.default_timer() - start_time
    return {"Benchmark": bench_cls.__name__, "size": size, "time": time_s}


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Benchmark suite.")
    benchmark_names = [benchmark.__name__ for benchmark in benchmarks]
    parser.add_argument(
        "-b",
        "--benchmarks",
        choices=benchmark_names,
        nargs="*",
        help="Run these benchmarks",
        default=benchmark_names[0:1],
    )
    parser.add_argument(
        "-s",
        "--size",
        type=int,
        help="Size of simulation (e.g. number of items). Set to -1 to iterate the sizes",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        help="Run in interactive mode with display",
        action="store_true",
    )

    args = parser.parse_args()

    for name in args.benchmarks:
        if args.interactive:
            import pygame

            import pymunk.pygame_util

            pymunk.pygame_util.positive_y_is_up = True

        bench_cls = [bench for bench in benchmarks if bench.__name__ == name][0]

        if args.size == None:
            sizes = [bench_cls.default_size]
        elif args.size == -1:
            sizes = range(
                bench_cls.size_start, bench_cls.size_end + 1, bench_cls.size_inc
            )
        else:
            sizes = [args.size]
        print(
            f"Running {bench_cls.__name__} with sizes {sizes} for {bench_cls.steps} steps."
        )

        for size in sizes:

            res = run(bench_cls, size, args.interactive)
            print(res)


class Stacking:

    def __init__(self):
        self.space = pymunk.Space()

        s = pymunk.Segment(self.space.static_body, (0, 500), (500, 500), 5)

    def update(self, dt):
        pass

    def draw(self):
        pass
