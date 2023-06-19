import pygame

pygame.init()

screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            quit()
    screen.fill(pygame.Color("white"))
    pygame.draw.circle(screen, (255, 0, 0), (-50, 300), 5)
    pygame.display.flip()
    clock.tick()
