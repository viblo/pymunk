"""A basic playground. Most interesting function is draw a shape, basically 
move the mouse as you want and pymunk will approximate a Poly shape from the 
drawing.
"""
__docformat__ = "reStructuredText"

import pygame

import pymunk as pm
import pymunk.util as u
from pymunk import Vec2d

# TODO: Clean up code

COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1


class PhysicsDemo:
    def flipyv(self, v):
        return int(v.x), int(-v.y + self.h)

    def __init__(self):
        self.running = True
        ### Init pygame and create screen
        pygame.init()
        self.w, self.h = 600, 600
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        ### Init pymunk and create space
        self.space = pm.Space()
        self.space.gravity = (0.0, -900.0)

        ### Walls
        self.walls = []
        self.create_wall_segments([(100, 50), (500, 50)])

        ## Balls
        # balls = [createBall(space, (100,300))]
        self.balls = []

        ### Polys
        self.polys = []
        h = 10
        for y in range(1, h):
            # for x in range(1, y):
            x = 0
            s = 10
            p = Vec2d(300, 40) + Vec2d(0, y * s * 2)
            self.polys.append(self.create_box(p, size=s, mass=1))

        self.run_physics = True

        ### Wall under construction
        self.wall_points = []
        ### Poly under construction
        self.poly_points = []

        self.shape_to_remove = None
        self.mouse_contact = None

    def draw_helptext(self):
        font = pygame.font.Font(None, 16)
        text = [
            "LMB: Create ball",
            "LMB + Shift: Create box",
            "RMB on object: Remove object",
            "RMB(hold) + Shift: Create polygon, release to finish (will be converted to a convex hull of the points)",
            "RMB + Ctrl: Create wall, release to finish",
            "Space: Stop physics simulation",
            "k: Spawn a bunch of blocks",
            "f: Fire a ball from the top left corner",
        ]
        y = 5
        for line in text:
            text = font.render(line, True, pygame.Color("black"))
            self.screen.blit(text, (5, y))
            y += 10

    def create_ball(self, point, mass=1.0, radius=15.0):

        moment = pm.moment_for_circle(mass, 0.0, radius)
        ball_body = pm.Body(mass, moment)
        ball_body.position = Vec2d(*point)

        ball_shape = pm.Circle(ball_body, radius)
        ball_shape.friction = 1.5
        ball_shape.collision_type = COLLTYPE_DEFAULT
        self.space.add(ball_body, ball_shape)
        return ball_shape

    def create_box(self, pos, size=10, mass=5.0):
        box_points = [(-size, -size), (-size, size), (size, size), (size, -size)]
        return self.create_poly(box_points, mass=mass, pos=pos)

    def create_poly(self, points, mass=5.0, pos=(0, 0)):

        moment = pm.moment_for_poly(mass, points)
        # moment = 1000
        body = pm.Body(mass, moment)
        body.position = Vec2d(*pos)
        shape = pm.Poly(body, points)
        shape.friction = 0.5
        shape.collision_type = COLLTYPE_DEFAULT
        self.space.add(body, shape)
        return shape

    def create_wall_segments(self, points):
        """Create a number of wall segments connecting the points"""
        if len(points) < 2:
            return []
        points = [Vec2d(*p) for p in points]
        for i in range(len(points) - 1):
            v1 = Vec2d(points[i].x, points[i].y)
            v2 = Vec2d(points[i + 1].x, points[i + 1].y)
            wall_body = pm.Body(body_type=pm.Body.STATIC)
            wall_shape = pm.Segment(wall_body, v1, v2, 0.0)
            wall_shape.friction = 1.0
            wall_shape.collision_type = COLLTYPE_DEFAULT
            self.space.add(wall_body, wall_shape)
            self.walls.append(wall_shape)

    def run(self):
        while self.running:
            self.loop()

    def draw_ball(self, ball):
        body = ball.body
        v = body.position + ball.offset.cpvrotate(body.rotation_vector)
        p = self.flipyv(v)
        r = ball.radius
        pygame.draw.circle(self.screen, pygame.Color("blue"), p, int(r), 2)

    def draw_wall(self, wall):
        body = wall.body
        pv1 = self.flipyv(body.position + wall.a.cpvrotate(body.rotation_vector))
        pv2 = self.flipyv(body.position + wall.b.cpvrotate(body.rotation_vector))
        pygame.draw.lines(self.screen, pygame.Color("lightgray"), False, [pv1, pv2])

    def draw_poly(self, poly):
        body = poly.body
        ps = [p.rotated(body.angle) + body.position for p in poly.get_vertices()]
        ps.append(ps[0])
        ps = list(map(self.flipyv, ps))
        if u.is_clockwise(ps):
            color = pygame.Color("green")
        else:
            color = pygame.Color("red")
        pygame.draw.lines(self.screen, color, False, ps)

    def draw(self):

        ### Clear the screen
        self.screen.fill(pygame.Color("white"))

        ### Display some text
        self.draw_helptext()

        ### Draw balls
        for ball in self.balls:
            self.draw_ball(ball)

        ### Draw walls
        for wall in self.walls:
            self.draw_wall(wall)

        ### Draw polys
        for poly in self.polys:
            self.draw_poly(poly)

        ### Draw Uncompleted walls
        if len(self.wall_points) > 1:
            ps = [self.flipyv(Vec2d(*p)) for p in self.wall_points]
            pygame.draw.lines(self.screen, pygame.Color("gray"), False, ps, 2)

        ### Uncompleted poly
        if len(self.poly_points) > 1:
            ps = [self.flipyv(Vec2d(*p)) for p in self.poly_points]
            pygame.draw.lines(self.screen, pygame.Color("red"), False, ps, 2)

        ### Mouse Contact
        if self.mouse_contact is not None:
            p = self.flipyv(self.mouse_contact)
            pygame.draw.circle(self.screen, pygame.Color("red"), p, 3)

        ### All done, lets flip the display
        pygame.display.flip()

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(self.screen, "playground.png")

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # LMB
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    p = self.flipyv(Vec2d(*event.pos))
                    self.polys.append(self.create_box(pos=p))
                else:
                    # t = -10000
                    p = self.flipyv(Vec2d(*event.pos))
                    self.balls.append(self.create_ball(p))

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # RMB
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    pass

                elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                    p = self.flipyv(Vec2d(*event.pos))
                    self.wall_points.append(p)
                elif self.shape_to_remove is not None:

                    self.balls = list(
                        filter(lambda a: a != self.shape_to_remove, self.balls)
                    )
                    self.walls = list(
                        filter(lambda a: a != self.shape_to_remove, self.walls)
                    )
                    self.polys = list(
                        filter(lambda a: a != self.shape_to_remove, self.polys)
                    )
                    self.space.remove(self.shape_to_remove.body, self.shape_to_remove)

            elif event.type == pygame.KEYUP and event.key in (
                pygame.K_RCTRL,
                pygame.K_LCTRL,
            ):
                ### Create Wall
                self.create_wall_segments(self.wall_points)
                self.wall_points = []
            elif event.type == pygame.KEYUP and event.key in (
                pygame.K_RSHIFT,
                pygame.K_LSHIFT,
            ):
                ### Create Polygon

                if len(self.poly_points) > 0:
                    self.poly_points = u.reduce_poly(self.poly_points, tolerance=5)
                if len(self.poly_points) > 2:
                    self.poly_points = u.convex_hull(self.poly_points)
                    if not u.is_clockwise(self.poly_points):
                        self.poly_points.reverse()

                    center = u.calc_center(self.poly_points)
                    self.poly_points = u.poly_vectors_around_center(self.poly_points)
                    self.polys.append(self.create_poly(self.poly_points, pos=center))
                self.poly_points = []
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.run_physics = not self.run_physics
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                for x in range(-100, 100, 25):
                    for y in range(-100, 100, 25):
                        p = pygame.mouse.get_pos()
                        p = Vec2d(*self.flipyv(Vec2d(*p))) + (x, y)
                        self.polys.append(self.create_box(pos=p))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                p = self.flipyv(Vec2d(*pygame.mouse.get_pos()))
                self.polys.append(self.create_box(p, size=10, mass=1))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                bp = Vec2d(100, 500)
                p = self.flipyv(Vec2d(*pygame.mouse.get_pos())) - bp
                ball = self.create_ball(bp)
                p = p.normalized()
                ball.body.apply_impulse_at_local_point(p * 1000, (0, 0))
                self.balls.append(ball)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                g = self.space.gravity

                self.space.gravity = g.rotated_degrees(45)

        mpos = pygame.mouse.get_pos()

        if pygame.key.get_mods() & pygame.KMOD_SHIFT and pygame.mouse.get_pressed()[2]:
            p = self.flipyv(Vec2d(*mpos))
            self.poly_points.append(p)
        hit = self.space.point_query_nearest(
            self.flipyv(Vec2d(*mpos)), 0, pm.ShapeFilter()
        )
        if hit != None:
            self.shape_to_remove = hit.shape
        else:
            self.shape_to_remove = None

        ### Update physics
        if self.run_physics:
            x = 1
            dt = 1.0 / 60.0 / x
            for x in range(x):
                self.space.step(dt)
                for ball in self.balls:
                    # ball.body.reset_forces()
                    pass
                for poly in self.polys:
                    # poly.body.reset_forces()
                    pass

        ### Draw stuff
        self.draw()

        ### Check for objects outside of the screen, we can remove those
        # Balls
        xs = []
        for ball in self.balls:
            if (
                ball.body.position.x < -1000
                or ball.body.position.x > 1000
                or ball.body.position.y < -1000
                or ball.body.position.y > 1000
            ):
                xs.append(ball)
        for ball in xs:
            self.space.remove(ball, ball.body)
            self.balls.remove(ball)

        # Polys
        xs = []
        for poly in self.polys:
            if (
                poly.body.position.x < -1000
                or poly.body.position.x > 1000
                or poly.body.position.y < -1000
                or poly.body.position.y > 1000
            ):
                xs.append(poly)

        for poly in xs:
            self.space.remove(poly, poly.body)
            self.polys.remove(poly)

        ### Tick clock and update fps in title
        self.clock.tick(50)
        pygame.display.set_caption("fps: " + str(self.clock.get_fps()))


def main():
    demo = PhysicsDemo()
    demo.run()


if __name__ == "__main__":
    doprof = 0
    if not doprof:
        main()
    else:
        import cProfile
        import pstats

        prof = cProfile.run("main()", "profile.prof")
        stats = pstats.Stats("profile.prof")
        stats.strip_dirs()
        stats.sort_stats("cumulative", "time", "calls")
        stats.print_stats(30)
