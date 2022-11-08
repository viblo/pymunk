"""This is an example on how the autogeometry can be used for deformable 
terrain.
"""
__docformat__ = "reStructuredText"

import sys

import pygame

import pymunk
import pymunk.autogeometry
import pymunk.pygame_util
from pymunk import BB


def draw_helptext(screen):
    font = pygame.font.Font(None, 16)
    text = [
        "LMB(hold): Draw pink color",
        "LMB(hold) + Shift: Create balls",
        "g: Generate segments from pink color drawing",
        "r: Reset",
    ]
    y = 5
    for line in text:
        text = font.render(line, 1, pygame.Color("black"))
        screen.blit(text, (5, y))
        y += 10


def generate_geometry(surface, space):
    for s in space.shapes:
        if hasattr(s, "generated") and s.generated:
            space.remove(s)

    def sample_func(point):
        try:
            p = int(point[0]), int(point[1])
            color = surface.get_at(p)
            return color.hsla[2]  # use lightness
        except Exception as e:
            print(e)
            return 0

    line_set = pymunk.autogeometry.march_soft(
        BB(0, 0, 599, 599), 60, 60, 90, sample_func
    )

    for polyline in line_set:
        line = pymunk.autogeometry.simplify_curves(polyline, 1.0)

        for i in range(len(line) - 1):
            p1 = line[i]
            p2 = line[i + 1]
            shape = pymunk.Segment(space.static_body, p1, p2, 1)
            shape.friction = 0.5
            shape.color = pygame.Color("red")
            shape.generated = True
            space.add(shape)


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = 0, 980
    static = [
        pymunk.Segment(space.static_body, (0, -50), (-50, 650), 5),
        pymunk.Segment(space.static_body, (0, 650), (650, 650), 5),
        pymunk.Segment(space.static_body, (650, 650), (650, -50), 5),
        pymunk.Segment(space.static_body, (-50, -50), (650, -50), 5),
    ]
    for s in static:
        s.collision_type = 1
    space.add(*static)

    def pre_solve(arb, space, data):
        s = arb.shapes[0]
        space.remove(s.body, s)
        return False

    space.add_collision_handler(0, 1).pre_solve = pre_solve

    terrain_surface = pygame.Surface((600, 600))
    terrain_surface.fill(pygame.Color("white"))

    color = pygame.color.THECOLORS["pink"]
    pygame.draw.circle(terrain_surface, color, (450, 120), 100)
    generate_geometry(terrain_surface, space)
    for x in range(25):
        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, 10)
        body = pymunk.Body(mass, moment)
        body.position = 450, 120
        shape = pymunk.Circle(body, 10)
        shape.friction = 0.5
        space.add(body, shape)

    draw_options = pymunk.pygame_util.DrawOptions(screen)
    pymunk.pygame_util.positive_y_is_up = False

    fps = 60
    while True:
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and (event.key in [pygame.K_ESCAPE, pygame.K_q])
            ):
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                pass
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                terrain_surface.fill(pygame.Color("white"))
                for s in space.shapes:
                    if hasattr(s, "generated") and s.generated:
                        space.remove(s)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                generate_geometry(terrain_surface, space)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "deformable.png")

        if pygame.mouse.get_pressed()[0]:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                mass = 1
                moment = pymunk.moment_for_circle(mass, 0, 10)
                body = pymunk.Body(mass, moment)
                body.position = pygame.mouse.get_pos()
                shape = pymunk.Circle(body, 10)
                shape.friction = 0.5
                space.add(body, shape)
            else:
                color = pygame.Color("pink")
                pos = pygame.mouse.get_pos()
                pygame.draw.circle(terrain_surface, color, pos, 25)

        space.step(1.0 / fps)

        screen.fill(pygame.Color("white"))
        screen.blit(terrain_surface, (0, 0))
        space.debug_draw(draw_options)
        draw_helptext(screen)
        pygame.display.flip()

        clock.tick(fps)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    sys.exit(main())
