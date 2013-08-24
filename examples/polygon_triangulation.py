"""Quick demo of using triangulate.py to triangulate/convexise(?) a concave 
polygon. Not good code as such, but functional and cheap

display:
thick red line: drawn polygon
medium blue lines: triangles after triangulation
thin white lines: convex polygons after convexisation(?)

input:
click points (in clockwise order)* to draw a polygon
press space to reset

* triangulate() and convexise() actually work on anticlockwise polys to match pymunk,
  but this demo's coords are upside-down compared to pymunk (pygame style),
  so click clockwise to compensate :)
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import pygame
from pygame.locals import *

from pymunk.vec2d import Vec2d
from pymunk.util import *

# init pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('triangulate test')


class PolyPoints(object):
    def __init__(self, points):
        self.poly = [Vec2d(point) for point in points]
        self.triangles = triangulate(self.poly)
        self.convexes = convexise(self.triangles)

# init clicked points
clicked_points = []
poly = PolyPoints(clicked_points)

quit = False
while not(quit):
    # handle imput
    for event in pygame.event.get():
        if event.type == QUIT:
            quit = True
        elif event.type == KEYDOWN and event.key == K_p:
            pygame.image.save(screen, "polygon_triangulation.png")
        elif event.type == MOUSEBUTTONDOWN:
            clicked_points += [event.pos]
            poly = PolyPoints(clicked_points)
        elif event.type == KEYDOWN and event.key == K_SPACE:
            clicked_points = []
            poly = PolyPoints(clicked_points)
         
    # clear screen
    screen.fill((0,0,0))

    # draw poly
    if len(clicked_points) == 1:
        pygame.draw.circle(screen, (150,0,0), clicked_points[0], 10, 0)
    if len(clicked_points) > 1:
        pygame.draw.lines(screen, (150,0,0), True, clicked_points, 20)
      
    # draw triangles
    if len(poly.triangles) > 0:
        for triangle in poly.triangles:
            pygame.draw.lines(screen, (0,0,200), True, triangle, 12)
         
    # draw hulls
    if len(poly.convexes) > 0:
        for convex in poly.convexes:
            pygame.draw.lines(screen, (255,255,255), True, convex, 2)

    # update screen
    pygame.display.update()