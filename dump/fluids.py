"""A very basic flipper game.
"""
__docformat__ = "reStructuredText"

import pygame

import pymunk
import pymunk.pygame_util

pygame.init()


def main():
    fps = 60
    dt = 1 / fps
    w, h = 600, 600
    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    space = pymunk.Space()
    space.gravity = 0, 982
    space.use_spatial_hash(4, 100000)

    static_lines = [
        pymunk.Segment(space.static_body, (11.0, 546.0), (507.0, 580.0), 5.0),  # -----
        pymunk.Segment(space.static_body, (507.0, 580.0), (507.0, 343.0), 5.0),  #     |
        pymunk.Segment(space.static_body, (11.0, 580.0), (11.0, 343.0), 5.0),  # |
    ]
    # for l in static_lines:
    # l.friction = 0.5
    space.add(*static_lines)

    particles = []
    for x in range(10):
        for y in range(500):
            b = pymunk.Body()
            s = pymunk.Circle(b, 2)
            s.mass = 1
            b.position = (
                100 + x * 3,
                500 - y * 2,
            )
            space.add(b, s)
            particles.append(b)

    fluid_scale = 1 / 3.0
    fw, fh = int(w * fluid_scale), int(h * fluid_scale)
    fluid_surface = pygame.Surface((fw, fh))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "fluid.png")

        screen.fill(pygame.Color("white"))

        color = 4885759  # 74, 140, 255
        half_color = 4885758  # 74, 140, 254
        no_color = 0  # (0, 0, 0)
        fluid_surface.fill((0, 0, 0))

        with pygame.PixelArray(fluid_surface) as pa:

            # pa[1, 1] = 74, 140, 254
            # print(pa[1, 1])

            for p in particles:

                x = int(p.position.x * fluid_scale)
                y = int(p.position.y * fluid_scale)

                if x < 2 or x > fw - 3 or y < 2 or y > fh - 3:
                    continue
                # print(x, y)
                try:
                    pa[x, y] = color

                    if pa[x, y + 1] == half_color:
                        pa[x, y + 1] = color
                    elif pa[x, y + 1] == no_color:
                        pa[x, y + 1] = half_color

                    if pa[x + 1, y] == half_color:
                        pa[x + 1, y] = color
                    elif pa[x + 1, y] == no_color:
                        pa[x + 1, y] = half_color

                    if pa[x - 1, y] == half_color:
                        pa[x - 1, y] = color
                    elif pa[x - 1, y] == no_color:
                        pa[x - 1, y] = half_color

                    if pa[x, y - 1] == half_color:
                        pa[x, y - 1] = color
                    elif pa[x, y - 1] == no_color:
                        pa[x, y - 1] = half_color
                except Exception as e:
                    print(x, y)
                    raise e

        s = pygame.transform.scale(fluid_surface, (w, h))
        # fluid_surface.
        screen.blit(s, (0, 0))

        # space.debug_draw(draw_options)
        steps = 1
        for x in range(steps):
            space.step(dt / steps)

        pygame.display.flip()
        clock.tick(fps)
        pygame.display.set_caption(f"fps: {clock.get_fps():.1f}")


if __name__ == "__main__":
    main()