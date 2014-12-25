__author__ = 'Wilson Koder'
 
# Created by Wilson Koder on the 23rd of October 2014
# Inspired by Boxes ;)
# In real life I can't wink.
 
import pymunk
import pygame
import pygame.gfxdraw
import pymunk.pygame_util
import sys
import time
 
white = 255, 255, 255
black = 0, 0, 0
red = 146, 26, 0
green = 0, 255, 0
blue = 0, 0, 255
yellow = 255, 255, 0

pygame.init()
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("PyBoxes v0.3")
clock = pygame.time.Clock()
start_time = time.time()
play_time = 0

space = pymunk.Space()
space.gravity = (0.0, -900.0)  # negative 900 makes for a good simulation.

circle_count = 0
rad = 14
ball_elasticity = 0.8
gravity = -900
wind = 0.0
mouse_down = False
hold_down_mouse = False
 
running = True
debugging = False
paused = False
 
liquid_sim = False
liquid_rad = 1
liquid_particles = []

friction = 0.8

color = red

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
 
 
def create_line(space_temp):
    body = pymunk.Body()
    body.position = (400, 600)
    line_shape = pymunk.Segment(body, (-400, -500), (400, -500), 15)
    line_shape.elasticity = 0.5
    space_temp.add(line_shape)
    return line_shape
 
line = create_line(space)
line.color = blue
circles = []
 
arial = pygame.font.SysFont("Arial", 24)
 
while running:
    for event in pygame.event.get():  # go through every event that frame.
        if event.type == pygame.QUIT:
            running = False  # if the user tries to quit the app, set running to false in order to exit the loop
 
        if event.type == pygame.KEYDOWN:  # check for keyboard input
            if event.key == pygame.K_p:
                if not paused:
                    print("pausing")
                    paused = True
                elif paused:
                    paused = False
            if event.key == pygame.K_n:
                newRad = input("Please input a new radius (int): ")
                try:
                    rad = int(newRad)
                except ValueError:
                    print(str(newRad) + " is not an int. Please input an integer next time.")
            if event.key == pygame.K_g:
                newColor = input("Please choose a new color (green, red, blue, yellow): ")
                if newColor.lower() == "green":
                    color = green
                elif newColor.lower() == "yellow":
                    color = yellow
                elif newColor.lower() == "red":
                    color = red
                elif newColor == "blue":
                    color = blue
                else:
                    print(newColor + " is not a color from the list... Press g to choose again.")
            if event.key == pygame.K_c:  # clear the screen
                space.remove(circles)
                circles = []
            if event.key == pygame.K_x:
                space.remove(liquid_particles)
                liquid_particles = []
            if event.key == pygame.K_a:
                wind -= 100
            if event.key == pygame.K_q:
                wind += 100
            if event.key == pygame.K_w:  # increase size of ball
                rad += 5
            if event.key == pygame.K_s:  # decrease size of ball
                # must check if above 5 so it doesnt throw an error if you go below 0 :p
                if rad > 5:
                    rad -= 5
                else:
                    print("rad is too low to decrease even more.")
            if event.key == pygame.K_e:
                gravity += 100
            if event.key == pygame.K_l:
                if liquid_sim is False:
                    friction = 0.0
                    liquid_sim = True
                    rad = liquid_rad
                    ball_elasticity = 0.5
                else:
                    friction = 0.8
                    liquid_sim = False
                    rad = 4
                    ball_elasticity = 0.8
            if event.key == pygame.K_d:
                gravity -= 100
            if event.key == pygame.K_UP:
                ball_elasticity += 0.25
            if event.key == pygame.K_DOWN:
                if ball_elasticity > 0.5:
                    ball_elasticity -= 0.25
                else:
                    print("e is to low to decrease even more.")
            if event.key == pygame.K_r:
                if hold_down_mouse:
                    hold_down_mouse = False
                else:
                    hold_down_mouse = True
 
            if event.key == pygame.K_f:
                if debugging:
                    debugging = False
                else:
                    debugging = True
 
        if event.type == pygame.MOUSEBUTTONDOWN:  # check if the mouse is clicked
            if hold_down_mouse:
                mouse_down = True
            else:
                pos = pygame.mouse.get_pos()
                if pos[1] < 500:
                    pos = pygame.mouse.get_pos()  # get the mouse pos
                    real_pos = pymunk.pygame_util.to_pygame(pos, screen)
                    new_circle = create_circle(real_pos)  # create a circle object
                    if not liquid_sim:
                        circles.append(new_circle)  # add it to the list
                    else:
                        liquid_particles.append(new_circle)
 
        if event.type == pygame.MOUSEBUTTONUP:
            if hold_down_mouse:
                mouse_down = False
 
    if mouse_down:
        pos = pygame.mouse.get_pos()
        if pos[1] < 500:
            if liquid_sim:
                for i in range(0, 20):
                    pos = pygame.mouse.get_pos()  # get the mouse pos
                    real_pos = pymunk.pygame_util.to_pygame(pos, screen)
                    new_particle = create_circle(real_pos)  # create a circle object
                    liquid_particles.append(new_particle)  # add it to the list
            else:
                pos = pygame.mouse.get_pos()  # get the mouse pos
                real_pos = pymunk.pygame_util.to_pygame(pos, screen)
                new_circle = create_circle(real_pos)  # create a circle object
                circles.append(new_circle)  # add it to the list

    if rad != liquid_rad and liquid_sim is True:
        liquid_sim = False
 
    play_time = round(time.time() - start_time, 0)

    space.gravity = (wind, gravity)

    screen.fill(white)  # clear the screen
    if not paused:
        space.step(1 / 60.0)  # step
 
    pymunk.pygame_util.draw(screen, line)  # draw the floor, couldn't get it working with normal pygame, so using util's
 
    for circle in circles:
        try:
            p_circle = int(circle.body.position.x), 600 - int(circle.body.position.y)  # render each circle in the list
            # pygame.draw.circle(screen, red, p_circle, int(circle.radius), 0)  # render each circle in the list


            pygame.gfxdraw.aacircle(screen, p_circle[0], p_circle[1], int(circle.radius), color)
            if p_circle[0] > (800 + circle.radius) or p_circle[0] < -circle.radius:
                space.remove(circle)
                circles.remove(circle)
        except OverflowError:
            print("ERROR! ERROR! OVERFLOW! Deleting all circles and liquid particles!")
            space.remove(circles)
            circles = []
            space.remove(liquid_particles)
            liquid_particles = []
    if len(liquid_particles) != 0:
        for particle in liquid_particles:
            try:
                p_circle = int(particle.body.position.x), 600-int(particle.body.position.y)  # render each circle in the list

                pygame.gfxdraw.aacircle(screen, p_circle[0], p_circle[1], int(particle.radius), color)
                if p_circle[0] > (800 + particle.radius) or p_circle[0] < -particle.radius:
                    space.remove(particle)
                    liquid_particles.remove(particle)
            except OverflowError:
                print("ERROR! ERROR! OVERFLOW! Deleting all circles and liquid particles!")
                space.remove(circles)
                circles = []
                space.remove(liquid_particles)
                liquid_particles = []

    # pymunk.pygame_util.draw(screen, circles)
    # pymunk.pygame_util.draw(screen, liquid_particles)

    mousePos = pygame.mouse.get_pos()
    pygame.gfxdraw.aacircle(screen, mousePos[0], mousePos[1], rad, black)

    # if you're in debug mode, set text then draw text.
    if debugging:
        debugTextWind = arial.render("Wind Power = " + str(int(wind)), 1, black, None)
        debugTextCount = arial.render("Circle Count = " + str(len(circles)), 1,  black, None)  # count of circles
        debugTextParticleCount = arial.render("Liquid Particle Count = " + str(len(liquid_particles)), 1,  black, None)  # liquid particles
        debugTextColor = arial.render("Color = " + str(color), 1,  black, None)  # color
        debugTextRad = arial.render("Radius = " + str(rad), 1,  black, None)  # radius text
        debugTextElasticity = arial.render("Elasticity = " + str(ball_elasticity), 1,  black, None)  # bounciness text
        debugTextMousePos = arial.render("Mouse Pos = " + str(pygame.mouse.get_pos()), 1, black, None)  # mouse pos text
        debugTextFPS = arial.render("FPS = " + str(round(clock.get_fps(), 1)), 1, black, None)  # fps text
        debugTextGravity = arial.render("Gravity = " + str(gravity), 1, black, None)  # gravity text to one d.p.
        debugTextTime = arial.render("Play Time = " + str(int(play_time)) + " Seconds", 1, black, None)
        if liquid_sim:
            debugLiquidSim = arial.render("Liquid Simulation On", 1, black, None)
        elif not liquid_sim:
            debugLiquidSim = arial.render("Liquid Simulation Off", 1, black, None)
        else:
            debugLiquidSim = arial.render("WAAAAAHHHHHTTTT?!?!?", 1, black, None)
        screen.blit(debugTextCount, (0, 0))
        screen.blit(debugTextRad, (0, 30))
        screen.blit(debugTextElasticity, (0, 60))
        screen.blit(debugTextMousePos, (0, 90))
        screen.blit(debugTextFPS, (0, 120))
        screen.blit(debugTextGravity, (0, 150))
        screen.blit(debugTextTime, (0, 180))
        screen.blit(debugLiquidSim, (0, 210))
        screen.blit(debugTextWind, (0, 240))
        screen.blit(debugTextParticleCount, (0, 270))

    pygame.display.flip()  # draw everything
    clock.tick(60)  # limit fps :)

print("Congrats! You just wasted " + str(int(play_time)) + " seconds of your life!")
sys.exit()  # quit if the user is no longer running the application.
