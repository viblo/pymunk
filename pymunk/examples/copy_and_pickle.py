"""This example shows how you can copy, save and load a space using pickle.
"""
import pickle

import pygame

import pymunk
import pymunk.pygame_util
from pymunk import Vec2d

width, height = 800, 600


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)

    # We will draw two versions of the Pymunk Space, each on a separate surface
    # to make it easy to show both at the same time.
    surf1 = pygame.Surface((300, 300))
    surf2 = pygame.Surface((300, 300))

    # Setup the base Pymunk Space.
    space1 = pymunk.Space()
    space1.gravity = 0, 1000
    space1.sleep_time_threshold = 0.5

    draw_options1 = pymunk.pygame_util.DrawOptions(surf1)
    draw_options2 = pymunk.pygame_util.DrawOptions(surf2)

    box = [(5, 5), (295, 5), (295, 295), (5, 295)]
    for i, p1 in enumerate(box):
        if i + 1 >= len(box):
            p2 = box[0]
        else:
            p2 = box[i + 1]
        l = pymunk.Segment(space1.static_body, p1, p2, 5)
        l.elasticity = 0.5
        l.friction = 1

        space1.add(l)

    template_box = pymunk.Poly.create_box(pymunk.Body(), (20, 20))
    template_box.mass = 1
    template_box.friction = 1

    for x in range(3):
        for y in range(7):
            box = template_box.copy()
            box.body.position = 200 + x * 30, 290 - y * 20
            space1.add(box, box.body)

    b = pymunk.Body()
    b.position = 30, 270
    ball = pymunk.Circle(b, 20)
    ball.mass = 20
    ball.friction = 1
    ball.color = pygame.Color("red")
    space1.add(ball, b)

    # this is the same as space2 = copy.deepcopy(space1)
    space2 = space1.copy()
    space2.sleep_time_threshold = float("inf")

    backup1 = space1.copy()
    backup2 = space2.copy()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and (
                event.key in [pygame.K_ESCAPE, pygame.K_q]
            ):
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                with open("copy_and_pickle.pickle", "wb") as f:
                    pickle.dump([space1, space2], f)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                with open("copy_and_pickle.pickle", "rb") as f:
                    (space1, space2) = pickle.load(f)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                space1 = backup1
                space2 = backup2
                backup1 = space1.copy()
                backup2 = space2.copy()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # find all bodies with a circle shape in all spaces
                for s in space1.shapes + space2.shapes:
                    if isinstance(s, pymunk.Circle) and s.body != None:
                        s.body.apply_impulse_at_local_point((20000, 0))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "copy_and_pickle.png")

        ### Clear screen
        screen.fill(pygame.Color("white"))

        ### Draw stuff
        surf1.fill(pygame.Color("white"))
        surf2.fill(pygame.Color("white"))

        space1.debug_draw(draw_options1)
        space2.debug_draw(draw_options2)

        screen.blit(surf1, (50, 100))
        screen.blit(surf2, (450, 100))

        ### Update physics
        fps = 60
        dt = 1.0 / fps
        space1.step(dt)
        space2.step(dt)

        ### Info and flip screen
        def bt(txt, pos):
            screen.blit(font.render(txt, True, pygame.Color("black")), pos)

        bt("space.sleep_time_threshold set to 0.5 seconds", (50, 80))
        bt("space.sleep_time_threshold set to inf (disabled)", (450, 80))

        bt("fps: " + str(clock.get_fps()), (0, 0))
        bt("Press SPACE to give an impulse to the ball.", (5, height - 50))
        bt(
            "Press S to save the current state to file, press L to load it.",
            (5, height - 35),
        )
        bt("Press R to reset, ESC or Q to quit", (5, height - 20))

        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    import sys

    sys.exit(main())
