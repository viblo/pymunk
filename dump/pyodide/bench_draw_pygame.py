import time

import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()


screen.fill(pygame.Color("lightblue"))

surf = pygame.Surface((100, 100))

line = (10, 20), (50, 70)
center = 30, 60
radius = 25
bg_color = (255, 0, 255, 255)
color = (0, 255, 0, 255)
outline_color = (0, 0, 255, 255)


def draw_pygame(surf: pygame.Surface, screen: pygame.Surface, n: int) -> None:
    for _ in range(n):
        surf.fill(bg_color)
        pygame.draw.circle(surf, color, center, radius, 0)
        pygame.draw.circle(surf, outline_color, center, radius, 1)
        pygame.draw.line(surf, outline_color, line[0], line[1], 3)

    screen.blit(surf, (10, 10))


t1 = time.perf_counter()
while True:
    for event in pygame.event.get():
        if (
            event.type == pygame.QUIT
            or event.type == pygame.KEYDOWN
            and (event.key in [pygame.K_ESCAPE, pygame.K_q])
        ):
            quit()
    deltas = []
    n = 1000

    t1 = time.perf_counter()
    draw_pygame(surf, screen, n)

    pygame.display.flip()
    t2 = time.perf_counter()
    clock.tick()

    deltas.append(t2 - t1)
    d = min(deltas)
    if d == 0:
        d = 0.0000001
    r = f"pygame(n={n}): {1000*d:.0f}ms per frame. FPS: {1/(d):.0f}"
    print(r)
    t1 = t2
