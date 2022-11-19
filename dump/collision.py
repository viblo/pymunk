import pygame

import pymunk
import pymunk.pygame_util

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

draw_options = pymunk.pygame_util.DrawOptions(screen)

space = pymunk.Space()

b1 = pymunk.Body(body_type=pymunk.Body.STATIC)
b1.position = 300, 300
b1.angle = 1
s1 = pymunk.Poly.create_box(b1, (100, 100), 10)
# s1.color = pygame.Color(100, 100, 100)
space.add(b1, s1)

b2 = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
b2.position = 100, 100
s2 = pymunk.Poly.create_box(b2, (50, 50))
# s2 = pymunk.Circle(b2, 50)
# s2.color = pygame.Color("red")
space.add(b2, s2)


def pre_solve(arb, space, data):
    points = arb.contact_point_set.points
    print(len(points))
    s1, s2 = arb.shapes
    for p, color in zip(points, [pygame.Color("red"), pygame.Color("pink")]):

        pygame.draw.circle(screen, color, (p.point_a.x, p.point_a.y), 4)
        pygame.draw.circle(screen, color, (p.point_b.x, p.point_b.y), 4, 1)

    return False


h = space.add_default_collision_handler()
h.pre_solve = pre_solve

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            quit()

    mouse_position = pymunk.pygame_util.from_pygame(
        pymunk.Vec2d(*pygame.mouse.get_pos()), screen
    )

    b2.position = mouse_position

    screen.fill(pygame.Color("white"))
    space.debug_draw(draw_options)
    space.step(1 / 50.0)

    pygame.display.flip()

    clock.tick(50)
