"""
   pymunx :: A simplification layer for pymunk 0.6.1+ -- with an focus on pygame

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
   
   	pymunx-0.5 (commit: 10. March 2008)
   	   

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

from os import chdir
from os import system
from os.path import isfile

from math import pi
from math import fabs
from math import sqrt
from math import degrees

from sys import exit
from time import sleep
from random import shuffle
from threading import Thread
from traceback import print_exc

# infinite ~ 10^100 :)
inf = 1e100
		
# Some Hex Tools
def hex2dec(hex): return int(hex, 16)
def hex2rgb(hex): 
	if hex[0:1] == '#': hex = hex[1:]; 
	return (hex2dec(hex[:2]), hex2dec(hex[2:4]), hex2dec(hex[4:6]))

# Threaded, delayed function
class delay_function(Thread):
	def __init__(self, delay, callback):
		Thread.__init__(self)
		self.delay = delay
		self.callback = callback
	def run(self):
		sleep(self.delay)
		self.callback()
		
# Encoding should run in the Background :)
class avi_encoder(Thread):
	def __init__(self, dir, fn, callback):
		Thread.__init__(self)
		self.callback = callback
		self.dir = dir
		self.fn = fn
	def run(self):
		print self.dir, self.fn
		try:
			chdir(self.dir)
			print "Writing to %s.avi..." % self.fn
			self.fn = self.fn.replace("%s/" % self.dir, "")
			system('mencoder "mf://%s*.tga" -mf fps=30 -o %s.avi -ovc lavc -lavcopts vcodec=msmpeg4v2:vbitrate=800' % (self.fn, self.fn))
			system("rm %s*.tga" % self.fn)			
			chdir("..")
		except:
			print "Sorry, only working on linux ... and not well tested :/ Error:"
			print_exc()
		# Report that encoding (try) is over
		self.callback()

# pymunx Main Class	
class pymunx:
	element_count = 0	# Approx. Count of current Elements
	fixed_color = None	# Fixed Color in Hex or RGB
	filecounter = 0		# Current Screenshot File Counter
	capture_to = False	# False if no Screencast, filename if record
	info_surface = False	# Info Box for the center of the image (Encoding, ...)
	show_help = True	# Blit Help on Top Left of the Screen	

	def __init__(self, gravity=(0.0,-900.0)):
		""" Init function: init pymunk, get screen size, init space, ...
		    Parameter: gravity == (int(x), int(y))
		    Returns: pymunx()
		"""
		self.run_physics = True 
		self.gravity = gravity
		
		# Python Stuff
	        self.font = pygame.font.Font(None, 32)
	        self.font_xxl = pygame.font.Font(None, 38)
		
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
		""" Init self.colors with a fix set of hex colors 
		"""
		self.cur_color = 0
		self.colors = [
		  "#737934", "#729a55", "#040404", "#1d4e29", "#ae5004", "#615c57",
		  "#6795ce", "#203d61", "#8f932b"
		]
		shuffle(self.colors)
#		for c in THECOLORS:
#			self.colors.append(THECOLORS[c])

	def set_color(self, clr):
		""" Set a color for all future Elements, until reset_color() is called 
		    Parameter: clr == (Hex or RGB)
		"""
		self.fixed_color = clr
	
	def reset_color(self):
		""" All Elements from now on will be drawn in random colors 
		"""
		self.fixed_color = None
		
	def get_color(self):
		""" Get a color - either the fixed one or the next from self.colors 
		    Returns: clr = ((R), (G), (B)) 
		"""
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
			
	def toggle_help(self):
		""" Toggle Help on and off
		"""
		self.show_help = not self.show_help

	def set_info(self, txt):
		""" Create the Surface for the Infotext at the Upper Left Corner 
		    Parameter: txt == str()
		"""
		txt = txt.splitlines()
		self.infostr_surface = pygame.Surface((500, 800))
		self.infostr_surface.fill((255,255,255))
		self.infostr_surface.set_colorkey((255,255,255))
		
	        y = 0
		for line in txt:
        		if len(line.strip()) == 0:
        			y += 16
        		else:
				text = self.font.render(line, 1,THECOLORS["black"])
				self.infostr_surface.blit(text, (0,y))
				y += 26
	
	def messagebox_show(self, txt, delay=None):
		""" Add a message box at the center on drawing 
		    Parameter: txt == str()
		    Optional: delay (in seconds, until box disappears)
		"""
		s = self.font_xxl.render(txt, 1, THECOLORS["black"])
		x,y,w,h = s.get_rect()
		self.info_surface = pygame.Surface((w+40,h+20))
		self.info_surface.fill((255,255,255))
		pygame.draw.rect(self.info_surface, (0,0,0), (x,y,w+40,h+10), 4)
		self.info_surface.blit(s, (20, 8))
		if delay != None:
			x = delay_function(delay, self.messagebox_hide)
			x.start()
		
	def messagebox_hide(self):
		""" Hide the message box
		"""
		self.info_surface = False
		
	def screenshot(self, filename='screenshot', ext='tga'):
		""" Make a Screenshot in .tga format, if there is no screencast running
		    Optional: filename == str() (no extension), ext == str() (does not work -- always saves as .tga)
		"""
		if self.capture_to != False:
			return
			
		if filename[-4:-3] == ".": filename = filename[:-4]
		elif filename[-3:-2] == ".": filename = filename[:-3]

		# Create Surface to Blit Elements on
		surface = pygame.Surface((self.display_width, self.display_height))
		surface.fill((255, 255, 255))
		self.draw(surface, True)
		
		# Save
		try:
			fn = self.save_surface(surface, "snapshots/%s" % filename, ext)
			self.messagebox_show("Saved as: %s" % fn, 2)
		except: pass

	def screencast_start(self, fn='screencast'):
		""" Starts saving one image per frame in snapshots/ (as .tga), for encoding with mencoder
		    Optional: fn == str() (filename without extension)
		"""
		self.capture_to = "snapshots/%s" % fn
		system("rm %s*.tga" % self.capture_to)
	
	def screencast_stop(self):
		""" Stop the image saving and start encoding (mencoder) the images to a .avi video
		"""
		self.run_physics = False
		self.filecounter = 0
		self.messagebox_show("Encoding Video [ %s.avi ]..." % self.capture_to)
		encoder = avi_encoder("snapshots", self.capture_to, self.screencast_encode_callback)
		encoder.start()
		self.capture_to = False
			
	def screencast_encode_callback(self):
		""" Callback function when encoding is done -> remove info & resume physics
		"""
		self.messagebox_hide()
		self.run_physics = True
		
	def save_surface(self, surface, fn='surface', ext='tga'):
		""" Saves a surface to a local file
		    Parameter: surface == pygame.Surface()
		    Optional: fn == str(fn_without_ext), ext == str()
		    Returns: fullname == str(full_name_of_file)
		"""
		fullname = None
		while fullname == None or isfile(fullname):
			self.filecounter += 1
			z = "0" * (5-len(str(self.filecounter)))
			fullname = "%s_%s%i.%s" % (fn, z, self.filecounter, ext)
			
		pygame.image.save(surface, fullname)
		return fullname
	
	def clear(self):
		""" Clear & Reset the Physic Space (Remove all Elements)
		"""
		pm.init_pymunk()

		# Space Init
		self.space = pm.Space()
		self.space.gravity = vec2d(self.gravity)
		self.space.resize_static_hash()
		self.space.resize_active_hash()
		
		self.element_count = 0
		self.filecounter = 0

	def flipy(self, y):
		""" Convert pygame y-coordinate to chipmunk's 
		    Parameter: y == int()
		    Returns: int(y_new)
		"""
		return -y+self.display_height
	
	def vec2df(self, pos):
		""" pos -> vec2d (with flipped y)
		    Parameter: pos == (int(x), int(pygame_y))
		    Returns: vec2d(int(x), int(chipmunk_y))
		"""
		return vec2d(pos[0], self.flipy(pos[1]))
		
	def autoset_screen_size(self, size=None):
		""" Get the current PyGame Screen Size, or sets it manually
		    Optional: size == (int(width), int(height)) 
		"""
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
		""" Check if pos is inside screen + tolerance
		    Parameter: pos == (int(x), int(y))
		    Optional: tolerance == int(pixels)
		    Returns: True if inside, False if outside
		"""
		x, y = pos
		if x < -tolerance or x > self.display_width+tolerance or y < -tolerance or y > self.display_height+tolerance:
			return False
		else:
			return True
			
	def update(self, fps=50.0, steps=5):
		""" Update the Physics Space 
		    Optional: fps == int(fps), steps == int(space_steps_per_udate)
		"""
		# Update physics
		if self.run_physics:
			dt = 1.0/fps/steps
			for _ in range(steps): 
				self.space.step(dt)

	def draw(self, surface, addtext=True):
		""" Draw All Shapes, and removes the ones outside 
		    Parameter: surface == pygame.Surface()
		    Optional: addtext == True/False (if True, also add Info-Text to surface)
		"""
		to_remove = []

		# Draw all Shapes
		for shape in self.space.get_shapes():
			if not self.draw_shape(surface, shape):
				to_remove.append(shape)
		
		# Maybe only add shapes. If so, return now
		if not addtext: 
			return
		
		# Screencast?
		if self.capture_to != False: 
			self.save_surface(surface, self.capture_to)
		
		# Draw Info-Text
		if self.show_help:
			surface.blit(self.infostr_surface, (10,10))
		if self.info_surface != False: 
			surface.blit(self.info_surface, (300,300))
		
		# Remove Outside Shapes
		for shape in to_remove:
			self.space.remove(shape)
			self.element_count -= 1
			
	def draw_shape(self, surface, shape):
		""" Draw a shape (can be either Circle, Segment or Poly).
		    Parameter: surface == pygame.Surface(), shape == pymunk.Shape()
		    Returns: True if shape is inside screen, else False (for removal)
		"""
		s = str(shape.__class__)		
		if 'pymunk.Circle' in s:
			# Get Ball Infos
			r = shape.radius
			v = shape.body.position
			rot = shape.body.rotation_vector
		
			# Draw Ball
			p = int(v.x), int(self.flipy(v.y))
			pygame.draw.circle(surface, shape.color, p, int(r), 3)
	
			# Draw Rotation Vector
			p2 = vec2d(rot.x, -rot.y) * r * 0.9
			pygame.draw.aaline(surface, shape.color2, p, p+p2, 2)
			
			# Remove if outside
			if not self.is_inside(p): return False
			
		elif 'pymunk.Segment' in s:
			p1 = shape.body.position + shape.a.rotated(degrees(shape.body.angle))
			p2 = shape.body.position + shape.b.rotated(degrees(shape.body.angle))
			p1 = (p1[0], self.flipy(p1[1]))
			p2 = (p2[0], self.flipy(p2[1]))	
#			print ">",p1, p2		
			pygame.draw.lines(surface, shape.color, False, [p1, p2], 3)

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
			pygame.draw.polygon(surface, shape.color, points, 3)

			# Remove if outside
			if not self.is_inside(points[0]): return False

#		if len(self.points) > 1:
#			pygame.draw.lines(surface, shape.color, False, self.points, 2)

		return True
		
	def add_wall(self, p1, p2, friction=1.0, elasticity=0.1, mass=inf, inertia=inf):
		""" Adds a fixed Wall pos = (int(x), int(y))
		    Parameter: p1 == pos(startpoint), p2 == pos(endpoint)
		    Optional: See #physical_parameters
		    Returns: pymunk.Shape() (=> .Segment())
		"""
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
		""" Adds a Ball 
		    Parameter: pos == (int(x), int(y))
		    Optional: See #physical_parameters
		    Returns: pymunk.Shape() (=> .Circle())
		"""
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
		""" Adding a Square | Note that a is actually half a side, due to vector easyness :) 
		    Parameter: pos == (int(x), int(y))
		    Optional: a == (sidelen/2) | #physical_parameters
		    Returns: pymunk.Shape() (=> .Poly())
		"""
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
		""" Mass will be calculated out of mass = A * density 
		    Parameter: points == [(int(x), int(y)), (int(x), int(y)), ...]
		    Optional: See #physical_parameters
		    Returns: pymunk.Shape() (=> .Poly())
		"""
		# Make vec2d's out of the points
		poly_points = []
		for p in points:
			poly_points.append(self.vec2df(p))
			
		# Reduce polygon points
		poly_points = util.reduce_poly(poly_points)
#		print "New Polygon: Points reduced from %i to %i" % (len(points), len(poly_points))
		if len(poly_points) < 3: 
			return False
		
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
		""" Apply an Impulse to a given Shape
		    Parameter: shape == pymunk.Shape(), impulse_vector == (int(x), int(y))
		"""
		x, y = impulse_vector
		shape.body.apply_impulse(vec2d(x, self.flipy(y)), vec2d(0,0))

	def get_element_count(self):
		""" Get the current (approx.) element count
		    Returns: int(self.element_count)
		"""
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
		# Add A Multi-Line Segment 
		# Problem: They don't Collide yet

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

	def set_gravity(self, gravity_vector):
		print "New Gravity:", gravity_vector
		self.gravity = gravity_vector
		self.space.set_gravity(gravity_vector)
		