import pygame

from pymunk.autogeometry import convex_decomposition

pygame.init()
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()
screen.fill(pygame.Color("white"))

p1 = [
    (0, 0),
    (5, 0),
    (10, 10),
    (20, 20),
    (5, 5),
    (0, 10),
    (0, 0),
]

p1 = [
    (-45, 0),
    (-40, 4),
    (-5, 4),
    (-4, 40),
    (0, 45),
    (4, 40),
    (5, 4),
    (40, 4),
    (45, 0),
    (40, -4),
    (5, -4),
    (4, -40),
    (0, -45),
    (-4, -40),
    (-4, -5),
    (-40, -4),
    (-45, 0),
]

p1 = list(reversed([(300 + x * 5, 300 + y * 5) for x, y in p1]))

ps = convex_decomposition(p1, tolerance=0.1)

pygame.draw.lines(screen, pygame.Color("red"), False, p1)
for p2 in ps:
    print(1)
    pygame.draw.lines(screen, pygame.Color("green"), False, p2)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if (
            event.type == pygame.QUIT
            or event.type == pygame.KEYDOWN
            and (event.key in [pygame.K_ESCAPE, pygame.K_q])
        ):
            quit()

    clock.tick(10)
