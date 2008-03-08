"""
   pymunx :: A simplification class for pymunk 0.6.1+

   http://www.linuxuser.at/pymunx
   http://www.slembcke.net/forums/viewforum.php?f=6
      
   > About <

	   Started by Chris Hager (chris@linuxuser.at) - March 2008 - (please send me feedback :)
	   I just got started on this, more will come the next days. So check back again :)
	   License: GPL
      	

   > Version <
   
   	pymunx-0.0.2 (commit: 7. March 2008)
   	   

   > Latest Changes <
   
	* in update(): remove body.reset_forces()
	* in update(): split one update into 5 smaller steps for space.step(dt)

   	* backward compatibility: added pymunk_flags to check pymunk version specific things,
   	  to be able to handle all pymunk versions starting from 0.6.1.
   	  (For example in svn-48: the change in poly.get_points to vec2d)
   		   

   > Overview <
	
	class pymunx:
		def __init__(self, gravity=(0.0,-900.0))
	   		# Init function. Init pymunk, get flags, get screen size, init space
	   		# Parameters: gravity = (int(x), int(y))
	   		# Returns: class pymunx
	   		
		def set_info(self, txt)
			# Sets the Info Text which will be blit at the upper left corner each update
			# Parameters: txt = str (break lines with \n)
			# Returns: -
		
   		def flipy (self, y)
			# Converts Chipmunk y-coordinate to pyGame (y = -y + self.display_height)
			# Parameters: y = int
			# Returns: int(y_new)

		def vec2df(self, pos)
			# Converts a pygame pos to a vec2d with flipped y coordinate
			# Parameters: pos = (int(x), int(y))
			# Returns: class vec2d((pos[0], self.flipy(pos[1])))
			
	   	def autoset_screen_size (self)  
	   		# Gets screensize from pygame. Call this only on resize
	   		# Returns: -

		def get_pymunk_flags (self)	
			# Checks pymunk version, adjusts settings and returns new flagset
			# Returns: class pymunk_flags
	
		def update (self, fps=50.0, steps=5)
			# Updates thy physics. fps is optional and by default set to 50.0 - steps is substeps per update
			# Returns: -
			
		def draw (self, surface)	
			# Iterates through all elements and calls draw_shape with each
			# Parameters: surface = pygame.Surface
			# Returns: -
			
		def draw_shape (self, surface, shape)	
			# Draws a given shape (circle, segment, poly) on the surface
			# Parameters: surface = pygame.Surface | shape = pymunk.Shape
			# Returns: -
	
		def add_wall (self, p1, p2, friction=10.0)	
			# Adds a fixed wall between points p1 and p2. friction is a optional parameter
			# Parameters: p = (int(x), int(y))
			# Returns: -
			
		def add_ball (self, pos, radius=15, mass=10.0, inertia=1000, friction=0.5)	
			# Adds a ball at pos. Other parameters are optional
			# Parameters: pos = (int(x), int(y))
			# Returns: -
			
		def add_square (self, pos, a=18, mass=5.0, friction=0.2)	
			# Adds a square at pos.
			# Parameters: pos = (int(x), int(y))
			# Returns: -

		def add_poly(self, points, mass=150.0, friction=10.0)
			# Adds a polygon from given a given pygame pointlist
			# Parameters: points = [(int(x), int(y)), (int(x), int(y)), ...]
			# Returns: -

		def get_element_count(self)
			# Returns the current element count
			# Returns: int(n)
			

   > Installation of Chipmunk & PyMunk <
   
   	Chipmunk 4.0.2 is included in pymunk 0.6.1, and will be loaded as a dll (.so). You need the library
   	compiled for your platform -- you can also do it easily on your own:
   		
		Step 1: 'gcc -O3 -std=gnu99 -ffast-math -c *.c' (or 'gcc -O3 -std=gnu99 -ffast-math -fPIC -c *.c')
		Step 2: 'gcc -shared -o chipmunk.so *.o'

	Pymunk Downloads:

		1. pymunk_0.6.1, demos, chipmunk: http://code.google.com/p/pymunk/downloads/list

		2. Latest pymunk via SVN (update a svn dir with 'svn up'):
		   2.1. Complete source + demos: svn checkout http://pymunk.googlecode.com/svn/trunk pymunk-read-only
		   2.2. pymunk bindings - demos: svn checkout http://pymunk.googlecode.com/svn/trunk/pymunk pymunk_dev


   > How to use pymunx <

	pymunx requires the pymunk bindings (in pymunk/) and the chipmunk library for your platform.
	You could simply place pymunx.py in the directory with all the other demos (has pymunk/ as subdirectory :)

      
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

# infinite ~ 10^100 :)
inf = 1e100

# Standard Settings for pymunk 0.6.1
# This will be checked and changed in get_pymunk_flags() to handle other pymunk versions
class pymunk_flags:
	version = "0.6.1"
	poly_return_vec2d = False

# pymunx Main Class	
class pymunx:
	element_count = 0
	
	def __init__(self, gravity=(0.0,-900.0)):
		self.run_physics = True 

		# Python Stuff
	        self.font = pygame.font.Font(None, 18)
		
		# Physics Init
		pm.init_pymunk()

		# Get PyMunk Flags to be able to handle changes in a backward compatible manner :)
		self.pymunk_flags = self.get_pymunk_flags()
				
		# This string will be blit in the top left corner at each update
		self.set_info("")
        
		# Get Screen Size
		self.autoset_screen_size()
		print "detected pymunk version:", self.pymunk_flags.version
		
		# Space Init
		self.space = pm.Space()
		self.space.gravity = vec2d(gravity)
		self.space.resize_static_hash()
		self.space.resize_active_hash()

	def set_info(self, txt):
		txt = txt.splitlines()
		self.infostr_surface = pygame.Surface((300, len(txt)*16))
		self.infostr_surface.fill((255,255,255))
		self.infostr_surface.set_colorkey((255,255,255))
		
	        y = 0
        	for line in txt:
	            text = self.font.render(line, 1,THECOLORS["black"])
        	    self.infostr_surface.blit(text, (0,y))
	            y += 16
		
	def flipy(self, y):
		""" Converts Chipmunk y-coordinate to pyGame y """
		return -y+self.display_height
	
	def vec2df(self, pos):
		""" Returns a vec2d with flipped y """
		return vec2d(pos[0], self.flipy(pos[1]))
		
	def autoset_screen_size(self):
		""" Gets the current PyGame Screen Size """
		try:
			x,y,w,h = pygame.display.get_surface().get_rect()
			self.display_width = w
			self.display_height = h
		except:
			print "pymunx Error: Please start pygame.init() before loading pymunx"
			exit(0)

	def is_inside(self, pos):
		""" Returns True if pos is inside the screen and False if not """
		x, y = pos
		if x < 0 or x > self.display_width or y < 0 or y > self.display_height:
			return False
		else:
			return True
			
	def get_pymunk_flags(self):
		""" Find and save flags for functions in the latest pymunk releases, so pymunx can
		use all pymunk versions starting at 0.6.1"""
		
		# Start with the 0.6.1 flags and check newer versions
		flags = pymunk_flags()

		# Init Classes and Variables to retrieve infos
		a = 5
	        verts = [vec2d(-a,-a), vec2d(-a, a), vec2d(a, a), vec2d(a,-a)]
		body =  pm.Body(0.1, 0.1)
	        poly = pm.Poly(body, verts, vec2d(0,0))
		
		# 0.6.1 -> svn-48: poly.get_get_points() returns vec2d instead of tuple
		p = poly.get_points()
		if "vec2d" in str(type(p[0])): 
			flags.poly_return_vec2d = True
			flags.version = "svn > 0.6.1"
		
		return flags
				
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
		""" shape can be either Circle, Segment or Poly """
		s = str(shape.__class__)
		
		if 'pymunk.Circle' in s:
			# Get Ball Infos
			r = shape.radius
			v = shape.body.position
			rot = shape.body.rotation_vector
		
			# Draw Ball
			p = int(v.x), int(self.flipy(v.y))
			pygame.draw.circle(surface, THECOLORS["blue"], p, int(r), 2)
	
			# Draw Rotation Vector
			p2 = vec2d(rot.x, -rot.y) * r * 0.9
			pygame.draw.line(surface, THECOLORS["red"], p, p+p2)
			
			# Remove if outside
			if not self.is_inside(p): return False
			
		elif 'pymunk.Segment' in s:
			a = shape.get_a()
			b = shape.get_b()
			pygame.draw.lines(surface, THECOLORS["blue"], False, [(a[0], self.flipy(a[1])), (b[0],self.flipy(b[1]))], 2)

			# Remove if outside
			if not self.is_inside(a) or not self.is_inside(b): return False
		
		elif 'pymunk.Poly' in s:
			# Correct Poly y-Coordinates
			points = []
			if self.pymunk_flags.poly_return_vec2d:
				for p in shape.get_points(): points.append((p.x, self.flipy(p.y)))					
			else:
				for p in shape.get_points(): points.append((p[0], self.flipy(p[1])))

			# Close the Polygon
			if points[-1] != points[0]:
				points.append(points[0])
		
			# Draw Poly
			pygame.draw.lines(surface, THECOLORS["blue"], False, points, 2)

			# Remove if outside
			if not self.is_inside(points[0]): return False

		return True
		
	def add_wall(self, p1, p2, friction=1.0):
		""" Adds a fixed Wall """
		mass = inf
		inertia = inf
			
		body = pm.Body(mass, inertia)
		shape= pm.Segment(body, self.vec2df(p1), self.vec2df(p2), 2.0)	
		shape.friction = friction
		self.space.add(shape)
		self.element_count += 1

	def add_ball(self, pos, radius=15, mass=10.0, inertia=1000, friction=0.5):
		""" Adds a Ball """
		# Create Body
		body = pm.Body(mass, inertia)
		body.position = self.vec2df(pos)
		
		# Create Shape
		shape = pm.Circle(body, radius, vec2d(0,0))
		shape.friction = friction
		
		# Append to Space
		self.space.add(body, shape)
		self.element_count += 1

	def add_square(self, pos, a=18, mass=5.0, friction=0.2):
		""" Adding a Square """
		# Square Vectors (Clockwise)
	        verts = [vec2d(-a,-a), vec2d(-a, a), vec2d(a, a), vec2d(a,-a)]
		
		# Square Physic Settings
	        moment = pm.moment_for_poly(mass, verts, vec2d(0,0))
	
		# Create Body
	        body = pm.Body(mass, moment)
		body.position = self.vec2df(pos)
	
		# Create Shape
	        shape = pm.Poly(body, verts, vec2d(0,0))
	        shape.friction = friction
	        
	        # Append to Space
	        self.space.add(body, shape)
		self.element_count += 1
        
	def add_poly(self, points, mass=5.0, friction=3.0):
		# Make vec2d's out of the points
		poly_points = []
		for p in points:
			poly_points.append(self.vec2df(p))
			
		# Reduce polygon points
		poly_points = util.reduce_poly(poly_points)
		if len(poly_points) < 3: 
			return
		
		# Make a convex hull
		poly_points = util.convex_hull(poly_points)
		
		# Make it counter-clockwise
		if not util.is_clockwise(poly_points):
			poly_points.reverse()
		
		# Change vectors to the point of view of the center
		poly_points_center = util.poly_vectors_around_center(poly_points)
		
		# Calculate A Good Momentum
		moment = pm.moment_for_poly(mass, poly_points_center, vec2d(0,0))

		# Create Body
		body = pm.Body(mass, moment)

		center = cx, cy = util.calc_center(poly_points)
		body.position = vec2d((cx, cy))

		# Create Shape
		shape = pm.Poly(body, poly_points_center, vec2d(0,0))
		shape.friction = friction
		
		# Append to Space
		self.space.add(body, shape)
		self.element_count += 1

	def get_element_count(self):
		return self.element_count
		