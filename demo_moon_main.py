"""
Note: This code is a straight conversion of the Moonbuggy tutorial code
TODO: Add licence text for it, until then see the original Moonbuggy 
tutorial for licence.
"""

import math, sys

from pyglet import window
from pyglet.gl import *

from pymunk.vec2d import vec2d
from pymunk.util import *
from pymunk import *

from demo_moon_buggy import *

global world

def drawCircle(x, y, r, a):
    segs = 15
    coef = 2.0*math.pi/segs;
    
    glBegin(GL_LINE_LOOP)
    for n in range(segs):
        rads = n*coef
        glVertex2f(r*math.cos(rads + a) + x, r*math.sin(rads + a) + y)
    glVertex2f(x,y)
    glEnd()


def drawCircleShape(circle):
    body = circle.body
    c = body.position + circle.center.cpvrotate(body.rotation_vector)
    drawCircle(c.x, c.y, circle.radius, body.angle)


def drawSegmentShape(seg):
    body = seg.body
    a = body.position + seg.a.cpvrotate(body.rotation_vector)
    b = body.position + seg.b.cpvrotate(body.rotation_vector)

    glBegin(GL_LINES)
    glVertex2f(a.x, a.y)
    glVertex2f(b.x, b.y)
    glEnd()


def drawPolyShape(poly):
    body = poly.body
    
    glBegin(GL_LINE_LOOP)
    for vert in poly.verts:
        v = body.position + vert.cpvrotate(body.rotation_vector)
        glVertex2f(v.x, v.y)
    glEnd()

def drawObject(shape):
    if isinstance(shape, Circle):
        drawCircleShape(shape)
    elif isinstance(shape, Segment):
        drawSegmentShape(shape)
    elif isinstance(shape, Poly):
        drawPolyShape(shape)

def drawCollisions(arb):
    print arb.a.friction
    print arb.b.friction
    for contact in arb.contacts:
        glVertex2f(contact.position.x, contact.position.y)

def display():
    
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(-world.chassis.position.x + 100, -world.chassis.position.y + 200, 0.0)

    glColor3f(0.0, 0.0, 0.0)
    map(drawObject, world.space.shapes)
    map(drawObject, world.space.static_shapes)
    
    glBegin(GL_POINTS)
    glColor3f(0.0, 0.0, 1.0)
    for body in world.space.bodies:
        glVertex2f(body.position.x, body.position.y)
      
    glColor3f(1.0, 0.0, 0.0)
    map(drawCollisions, world.space.arbiters)

    glEnd()

def initGL():
    glClearColor(1.0, 1.0, 1.0, 0.0)

    glPointSize(3.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1000.0, 1000.0, -750.0, 750.0, -1.0, 1.0)
    glScalef(2.0, 2.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    init_pymunk()
    global world
    world = MoonWorld()
    world.moonBuggy_init()
    
    win = window.Window(640, 480)
    
    win.set_caption("Press mouse button to play")
    initGL()
    
    running = True
    win.on_mouse_press = world.moonBuggy_input
    while not win.has_exit:
        win.dispatch_events()
        win.clear()

        display()
        world.moonBuggy_update()
        win.flip()
        
if __name__ == '__main__':
    sys.exit(main())

