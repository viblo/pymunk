"""
   pymunx :: A simplification class for pymunk 0.6.1+

            Home: http://wiki.laptop.org/go/Pymunx
   Documentation: http://wiki.laptop.org/go/Pymunx/Documentation
   
 Sources & Demos: http://www.linuxuser.at/pymunx
           Forum: http://www.slembcke.net/forums/viewforum.php?f=6
           
             IRC: #pymunk on irc.freenode.net
   	
   
   > About <

	Pymunx was started by Chris Hager (chris@linuxuser.at) in March 2008.
	(Please send me feedback :) I just got started on this, more will come
	frequenty, so check back soon :)
	   
	License: GPL, 2008


   > How-to get the Sources, Examples & Chipmunk Library <
   
   	svn checkout http://pymunk.googlecode.com/svn/trunk pymunk-read-only
      	

   > Version <
   
   	pymunx-0.0.3 (commit: 8. March 2008)
   	   

   > Latest Changes <


   > How to use pymunx <

	pymunx requires the pymunk bindings (in pymunk/) and the chipmunk library for your platform.
	You could simply place pymunx.py in the directory with all the other demos (has pymunk/ as subdirectory :)
	Just make a svn checkout and you'll see :)

      
   > Typical example with pygame <

   	world = pymunx()
   	world.add_wall((100, 200), (300, 200))
   	
   	# Main Game Loop:
   	while running:
   		# Event Checking
   		# ...

		screen.fill((255,255,255))

		# Update & Draw World
		world.update()
		world.draw(screen)

		# Flip Display
		pygame.display.flip()
		
		# Try to stay at 50 FPS
		clock.tick(50)   		


   > Quick Info about the Physical Properties <

   	Inertia:    The moment of inertia is like the mass of an object, but applied to its rotation. 
		    An object with a higher moment of inertia is harder to spin.

   	Elasticity: A value of 0.0 gives no bounce, while a value of 1.0 will give a 'perfect' bounce. 
		    However due to inaccuracies in the simulation using 1.0 or greater is not recommended however.
	
	Friction:   (Friction coefficient): Chipmunk uses the Coulomb friction model, a value of 0.0 is frictionless.
	
	Velocity:   The surface velocity of the object. Useful for creating conveyor belts or players that move around. 
		    This value is only used when calculating friction, not the collision.
"""

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk.pymunk as pm
import pymunk.util as util
from pymunk.vec2d import vec2d

from sys import exit

from random import shuffle

from math import pi
from math import fabs
from math import sqrt
from math import degrees

# infinite ~ 10^100 :)
inf = 1e100

def hex2dec(hex): return int(hex, 16);
def hex2rgb(hex): 
	if hex[0:1] == '#': hex = hex[1:]; 
	return (hex2dec(hex[:2]), hex2dec(hex[2:4]), hex2dec(hex[4:6]))

# pymunx Main Class	
class pymunx:
	element_count = 0
	fixed_color = None
#	points = []
	
	def __init__(self, gravity=(0.0,-900.0)):
		self.run_physics = True 
		self.gravity = gravity
		
		# Python Stuff
	        self.font = pygame.font.Font(None, 18)
		
		# Physics Init
		pm.init_pymunk()

		# Init Colors
		self.init_colors()
		
		# This string will be blit in the top left corner at each update
		self.set_info("")
        
		# Get Screen Size
		self.autoset_screen_size()
		
		# Space Init
		self.space = pm.Space()
		self.space.gravity = vec2d(gravity)
		self.space.resize_static_hash()
		self.space.resize_active_hash()

	def init_colors(self):
		self.cur_color = 0
		self.colors = [
		  "#737934", "#729a55", "#040404", "#1d4e29", "#ae5004", "#615c57",
		  "#6795ce", "#203d61", "#8f932b"
		]
		shuffle(self.colors)
#		for c in THECOLORS:
#			self.colors.append(THECOLORS[c])

	def set_color(self, clr):
		""" All Elements will have the color, until reset_color() is called """
		self.fixed_color = clr
	
	def reset_color(self):
		""" All Elements from now on will be drawn in random color """
		self.fixed_color = None
		
	def get_color(self):
		""" Get a color - either the fixed one or the next from self.colors """
		if self.fixed_color != None:
			return self.fixed_color
			
		if self.cur_color == len(self.colors): 
			self.cur_color = 0
			shuffle(self.colors)
	
		clr = self.colors[self.cur_color]
		if clr[:1] == "#":
			clr = hex2rgb(clr)
		
		self.cur_color += 1
		return clr
			
	def set_info(self, txt):
		""" Create the Surface for the Infotext at the Upper Left Corner """
		txt = txt.splitlines()
		self.infostr_surface = pygame.Surface((300, len(txt)*16))
		self.infostr_surface.fill((255,255,255))
		self.infostr_surface.set_colorkey((255,255,255))
		
	        y = 0
		for line in txt:
        		if len(line.strip()) == 0:
        			y += 6
        		else:
				text = self.font.render(line, 1,THECOLORS["black"])
				self.infostr_surface.blit(text, (0,y))
				y += 16
	
	def clear(self):
		""" Clears the Space """
		pm.init_pymunk()

		# Space Init
		self.space = pm.Space()
		self.space.gravity = vec2d(self.gravity)
		self.space.resize_static_hash()
		self.space.resize_active_hash()
		
		self.element_count = 0
		
	def flipy(self, y):
		""" Convert pygame y-coordinate to chipmunk's """
		return -y+self.display_height
	
	def vec2df(self, pos):
		""" Return a vec2d with flipped y """
		return vec2d(pos[0], self.flipy(pos[1]))
		
	def autoset_screen_size(self, size=None):
		""" Get the current PyGame Screen Size, or Sets it Manually to size=(int(width), int(height)) """
		if size != None:
			self.display_width, self.display_height = size
			return
			
		try:
			x,y,w,h = pygame.display.get_surface().get_rect()
			self.display_width = w
			self.display_height = h
		except:
			print "pymunx Error: Please start pygame.init() before loading pymunx"
			exit(0)

	def is_inside(self, pos, tolerance=3000):
		""" Return True if pos is inside the screen and False if not """
		x, y = pos
		if x < -tolerance or x > self.display_width+tolerance or y < -tolerance or y > self.display_height+tolerance:
			return False
		else:
			return True
			
	def update(self, fps=50.0, steps=5):
		""" Update the Physics Space """
		# Update physics
		if self.run_physics:
			dt = 1.0/fps/steps
			for _ in range(steps): 
				self.space.step(dt)

	def draw(self, surface):
		""" Draw All Shapes on a given Surface, and removes the ones outside """
		to_remove = []

		# Draw all Shapes
		for shape in self.space.get_shapes():
			if not self.draw_shape(surface, shape):
				to_remove.append(shape)

		# Draw Info-Text					
		surface.blit(self.infostr_surface, (10,10))

		# Remove Outside Shapes
		for shape in to_remove:
			self.space.remove(shape)
			self.element_count -= 1
			
	def draw_shape(self, surface, shape):
		""" shape can be either Circle, Segment or Poly. 
		    returns True if shape is inside screen, else False (for removal)"""

		s = str(shape.__class__)		
		if 'pymunk.Circle' in s:
			# Get Ball Infos
			r = shape.radius
			v = shape.body.position
			rot = shape.body.rotation_vector
		
			# Draw Ball
			p = int(v.x), int(self.flipy(v.y))
			pygame.draw.circle(surface, shape.color, p, int(r), 2)
	
			# Draw Rotation Vector
			p2 = vec2d(rot.x, -rot.y) * r * 0.9
			pygame.draw.line(surface, shape.color2, p, p+p2)
			
			# Remove if outside
			if not self.is_inside(p): return False
			
		elif 'pymunk.Segment' in s:
			p1 = shape.body.position + shape.a.rotated(degrees(shape.body.angle))
			p2 = shape.body.position + shape.b.rotated(degrees(shape.body.angle))
			p1 = (p1[0], self.flipy(p1[1]))
			p2 = (p2[0], self.flipy(p2[1]))	
#			print ">",p1, p2		
			pygame.draw.lines(surface, shape.color, False, [p1, p2], 2)

			# Remove if outside
			if not self.is_inside(p1) or not self.is_inside(p2): return False
		
		elif 'pymunk.Poly' in s:
			# Correct Poly y-Coordinates
			points = []
			for p in shape.get_points(): 
				points.append((p.x, self.flipy(p.y)))

			# Close the Polygon
			if points[-1] != points[0]:
				points.append(points[0])
		
			# Draw Poly
			pygame.draw.lines(surface, shape.color, False, points, 2)

			# Remove if outside
			if not self.is_inside(points[0]): return False

#		if len(self.points) > 1:
#			pygame.draw.lines(surface, shape.color, False, self.points, 2)

		return True
		
	def add_wall(self, p1, p2, friction=1.0, elasticity=0.5, mass=inf, inertia=inf):
		""" Adds a fixed Wall """
		body = pm.Body(mass, inertia)
		shape= pm.Segment(body, self.vec2df(p1), self.vec2df(p2), 2.0)	
		shape.set_friction(friction)
		shape.set_elasticity(elasticity)
		
		shape.color = self.get_color()
		shape.color2 = self.get_color()

		self.space.add(shape)
		self.element_count += 1
		return shape
		
	def add_ball(self, pos, radius=15, density=0.1, inertia=1000, friction=0.5, elasticity=0.3):
		""" Adds a Ball """
		mass = density * (radius * radius * pi)

		# Create Body
		body = pm.Body(mass, inertia)
		body.position = self.vec2df(pos)
		
		# Create Shape
		shape = pm.Circle(body, radius, vec2d(0,0))
		shape.set_friction(friction)
		shape.set_elasticity(elasticity)
		
		shape.color = self.get_color()
		shape.color2 = self.get_color()

		# Append to Space
		self.space.add(body, shape)
		self.element_count += 1
		return shape

	def add_square(self, pos, a=18, density=0.1, friction=0.2, elasticity=0.3):
		""" Adding a Square | Note that a is actually half a side, due to vector easyness :) """
		mass = density * (a * a * 4)
		
		# Square Vectors (Clockwise)
	        verts = [vec2d(-a,-a), vec2d(-a, a), vec2d(a, a), vec2d(a,-a)]
		
		# Square Physic Settings
	        inertia = pm.moment_for_poly(mass, verts, vec2d(0,0))
	
		# Create Body
	        body = pm.Body(mass, inertia)
		body.position = self.vec2df(pos)
	
		# Create Shape
	        shape = pm.Poly(body, verts, vec2d(0,0))
		shape.set_friction(friction)
		shape.set_elasticity(elasticity)

		shape.color = self.get_color()
		shape.color2 = self.get_color()
	        
	        # Append to Space
	        self.space.add(body, shape)
		self.element_count += 1
		return shape
        
	def add_poly(self, points, density=0.1, friction=2.0, elasticity=0.3):
		""" Mass will be calculated out of mass = A * density """
		# Make vec2d's out of the points
		poly_points = []
		for p in points:
			poly_points.append(self.vec2df(p))
			
		# Reduce polygon points
		poly_points = util.reduce_poly(poly_points)
#		print "New Polygon: Points reduced from %i to %i" % (len(points), len(poly_points))
		if len(poly_points) < 3: 
			return
		
		# Make a convex hull
		poly_points = util.convex_hull(poly_points)
		
		# Make it counter-clockwise
		if not util.is_clockwise(poly_points):
			poly_points.reverse()
		
		# Change vectors to the point of view of the center
		poly_points_center = util.poly_vectors_around_center(poly_points)
		
		U, A = util.get_poly_UA(poly_points_center)
		A *= 2.5 	# get_poly_UA is not working properly with the area :)
		mass = A * density
		
		# Calculate A Good Momentum
		moment = pm.moment_for_poly(mass, poly_points_center, vec2d(0,0))

		# Create Body
		body = pm.Body(mass, moment)

		center = cx, cy = util.calc_center(poly_points)
		body.position = vec2d((cx, cy))

		# Create Shape
		shape = pm.Poly(body, poly_points_center, vec2d(0,0))
		shape.set_friction(friction)
		shape.set_elasticity(elasticity)

		shape.color = self.get_color()
		shape.color2 = self.get_color()
		
		# Append to Space
		self.space.add(body, shape)
		self.element_count += 1
		return shape

		
	def apply_impulse(self, shape, impulse_vector):
		x, y = impulse_vector
		shape.body.apply_impulse(vec2d(x, self.flipy(y)), vec2d(0,0))

	def get_element_count(self):
		return self.element_count

#
# The functions below are only for experimental usage
#		
	def reduce_points(self, pointlist, tolerance=25):
		# Heavily reduce Line Points
		points_new = []
		x = 0
		y = 0
		for p in pointlist:
			px, py = p
			dx = fabs(x - px)
			dy = fabs(y - py)
			
			if dx > tolerance and dy > tolerance:
				x, y = p
				points_new.append(p)
		
		if points_new[-1] != pointlist[-1]:
			points_new.append(pointlist[-1])
			
		return points_new
		
	def add_segment(self, points, inertia=500, mass=150.0, friction=3.0):
		""" Add A Multi-Line Segment """

		# Reduce Points
		pointlist = self.reduce_points(points)
		print "Reduced Segment Points: %i -> %i" % (len(points), len(pointlist))

		# Get the Center of the Segment
		center = cx, cy = util.calc_center(pointlist)
		
		# Arrange vectors around center
		pointlist = util.poly_vectors_around_center(pointlist, False)

		# Get Moment of Inertia
	        moment = pm.moment_for_poly(mass, pointlist, vec2d(0,0))

		# Create Body
	        body = pm.Body(mass, inertia)	        
		body.position = self.vec2df(center)

		# Create Shapes
		a = b = None
		clr = self.get_color()

		shapes = []
		for p in pointlist:
			if a == None:
				# Starting Point
				a = p
				
			else:
				# Ending Point
				b = p

				# add shape beween a and b
#				print a,b
				shape = pm.Segment(body, vec2d(a), vec2d(b), 2.0)
				shape.set_group(1)
				shape.set_friction(friction)
				shape.color = clr
				shapes.append(shape)
				
				# Last Ending Point gets next starting Point
				a = b
	        
	        # Append to Space
	        self.space.add(body, shapes)
		self.element_count += 1
