import pygame
import sys
import pymunk
import pymunk.pygame_util

pygame.init()
clock = pygame.time.Clock()

windowSize = (800, 600)

screen = pygame.display.set_mode(windowSize)

running = True

rad = 14
ball_elasticity = 0.8
friction = 0.8
space = pymunk.Space()
space.gravity = (0.0, -900.0)
circles = []


def create_circle(position):
    mass = 1
    inertia = pymunk.moment_for_circle(mass, 0, rad)
    body = pymunk.Body(mass, inertia)
    body.position = position
    # body.position = position
    shape = pymunk.Circle(body, rad)
    shape.elasticity = ball_elasticity
    shape.friction = friction
    space.add(body, shape)
    return shape


def create_line():
    body = pymunk.Body()
    body.position = (400, 600)
    line_shape = pymunk.Segment(body, (-400, -500), (400, -500), 15)
    line_shape.elasticity = 0.5
    space.add(line_shape)
    return line_shape

line = create_line()
line.color = (0, 255, 0)

font = pygame.font.SysFont(None, 48)


while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            originalMousePos = pygame.mouse.get_pos()
            realPos = pymunk.pygame_util.to_pygame(originalMousePos, screen)
            newCircle = create_circle(realPos)
            circles.append(newCircle)
            print(len(circles))

    screen.fill((0, 0, 0))

    #for circle in circles:
        #circlePosition = int(circle.body.position.x), 600 - int(circle.body.position.y)
        #pygame.draw.circle(screen, (255, 0, 0), circlePosition, int(circle.radius), 0)
    pymunk.pygame_util.draw(screen, circles)

    pymunk.pygame_util.draw(screen, line)

    circleCount = font.render(str(len(circles)), 1, (255, 0, 0))
    currentFPS = font.render(str(int(clock.get_fps())), 1, (255, 0, 0))
    screen.blit(circleCount, (10, 10))
    screen.blit(currentFPS, (10, 40))

    pygame.display.flip()
    space.step(1/60.0)

sys.exit()
