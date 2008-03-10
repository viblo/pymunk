import pygame
from pygame.locals import *
from pygame.color import *

from math import fabs
from pymunx import *

from time import sleep
from threading import Thread

class ShowFPS(Thread):
	def __init__(self, seconds, pygame_clock):
		Thread.__init__(self)
		self.running = True
		self.clock = pygame_clock
		self.delay = seconds
		
	def run(self):
		i = 0
		m = 5.0
		while self.running:
			sleep(self.delay / m)
			i += 1
			if i == m:
				print "%i FPS" % int(self.clock.get_fps())
				i = 0

def blit_arrow(surface, a, b):
	pygame.draw.line(surface, (237, 248, 247), a, b, 6)
	
def main():
	# PyGame Init
	pygame.init()
	screen = pygame.display.set_mode((1200, 900))
	clock = pygame.time.Clock()

	# Create the Physical Space Class
	default_size = 18
	default_elasticity = 0.6
	default_density = 0.1
	default_friction = 0.3
	default_inertia = 10.0
	
	world = pymunx()
	world.set_info("LMB: Add Ball, throw Ball or draw Polygon \nRMB: Add Box, or throw one \n\nMouseWheel: Size [ %i m ] \nMouseWheel + CTRL: Elasticity [ %.2f ] \nMouseWheel + Shift: Density [ %.2f ] \n\nc: Clear \nf: Fullscreen \nSpace: Pause\n1: Add many balls\n2: Add many squares \n\ns: Screenshot \n[,]: Start Screencast \n[.]: Stop Screencast \nF1: Toggle Help " % (default_size, default_elasticity, default_density))
	
	FPSX = ShowFPS(3.0, clock)
#	FPSX.start()
	
	# Add A Wall
	world.add_wall((200, 800), (1000, 800))

	# Default Settings
	running = True
	draw_poly = False
	draw_arrow = False
	points = []
	filecounter = 0
	
	# Main Loop
	while running:
		for event in pygame.event.get():
#			print event
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				# Bye Bye
				running = False
				FPSX.running = False
				
			elif event.type == KEYDOWN:
#				print event
				if event.key == K_SPACE:	
					# Pause with SPACE
					world.run_physics = not world.run_physics
					
				elif event.key == 282:
					world.toggle_help()

				elif event.unicode == "c": 
					world.clear()
					world.add_wall((200, 800), (1000, 800), default_friction, default_elasticity)
					
				elif event.unicode == "f":
					pygame.display.toggle_fullscreen()
	
				elif event.unicode == "s":
					world.screenshot()

				elif event.unicode == ",":
					world.screencast_start("demo6")
					
				elif event.unicode == ".":
					world.screencast_stop()
				
				elif event.unicode == "1":
					# Add many Balls
					x, y = pygame.mouse.get_pos()
					for i in range(5):
						for j in range(5): 
							world.add_ball((x-i,y-j), default_size, default_density, default_inertia, default_friction, default_elasticity)

				elif event.unicode == "2":
					# Add many Balls
					x, y = pygame.mouse.get_pos()
					for i in range(5):
						for j in range(5): 
							world.add_square((x-i,y-j), default_size, default_density, default_friction, default_elasticity)

				elif event.unicode == "3":
					if world.fixed_color:
						world.reset_color()
					else:
						world.set_color((0, 0, 0))

					
			elif event.type == MOUSEBUTTONDOWN and (event.button == 4 or event.button == 5):
				# Change Settings with the Mouse Wheel
				key = pygame.key.get_mods()

				if event.button == 4:
					# MW UP
					if key == 4160 or key == 4224:	# Ctrl
						default_elasticity += 0.02
						if default_elasticity > 1.6:
							default_elasticity = 1.6
							
					elif key == 4097 or key == 4098: # Shift
						default_density += 0.02
						
					else: default_size += 2
					
				else:
					# MW DOWN
					if key == 4160 or key == 4224: 		# Ctrl
						default_elasticity -= 0.02
						if default_elasticity < 0.0:
							default_elasticity = 0.0
					
					elif key == 4097 or key == 4098: 	# Shift
						default_density -= 0.02
						if default_density < 0.02:
							default_density = 0.02

					else: 
						default_size -= 2
						if default_size < 2:
							default_size = 2

				# Update Info-Text
				world.set_info("LMB: Add Ball, throw Ball or draw Polygon \nRMB: Add Box, or throw one \n\nMouseWheel: Size [ %i m ] \nMouseWheel + CTRL: Elasticity [ %.2f ] \nMouseWheel + Shift: Density [ %.2f ] \n\nc: Clear \nf: Fullscreen \nSpace: Pause\n1: Add many balls\n2: Add many squares \n\ns: Screenshot \n[,]: Start Screencast \n[.]: Stop Screencast \nF1: Toggle Help " % (default_size, default_elasticity, default_density))

			elif event.type == MOUSEBUTTONDOWN and event.button == 1:
				# Start/Stop Wall-Drawing 
				if not draw_poly:
					draw_poly = True
					points = []
					points.append(event.pos)

			elif event.type == MOUSEBUTTONDOWN and event.button == 3:
				if not draw_arrow:
					draw_arrow = True
					points = []
					points.append(event.pos)
			
			elif event.type == MOUSEBUTTONUP and event.button == 3:
				if draw_arrow:
					# Throw Box
					draw_arrow = False
					x1, y1 = points[0]
					x2, y2 = event.pos
					x = x2 - x1
					y = y2 - y1
					l = sqrt((x*x)+(y*y)) * 1.8
					box = world.add_square(points[0], default_size, default_density, default_friction, default_elasticity)
					world.apply_impulse(box, (x*l, y*l))
					print "New Square: %i kg" % (box.body.mass)
					
			elif event.type == MOUSEBUTTONUP and event.button == 1:
				if draw_poly:
					# Create Ball, Thrown Ball or Polygon
					draw_poly = False
					points.append(event.pos)

					if len(points) < 5: 
						ball = world.add_ball(event.pos, default_size, default_density, default_inertia, default_friction, default_elasticity)
						print "New Ball: %i kg" % ball.body.mass
					
					else:
						# Throw Ball if End and Start Points are not close
						x1, y1 = points[0]
						x2, y2 = points[-1]
						x = x2 - x1
						y = y2 - y1

						if fabs(x) > 90 or fabs(y) > 90:
							# Throw Ball
							l = sqrt((x*x)+(y*y)) * 1.8
							ball = world.add_ball(points[0], default_size, default_density, default_inertia, default_friction, default_elasticity)
							world.apply_impulse(ball, (x*l, y*l))
							
						else:
							# Add Polygon
							poly = world.add_poly(points, default_density, default_friction, default_elasticity)
							if poly != False:
								print "New Polygon: %i kg" % (poly.body.mass)

			elif event.type == MOUSEMOTION and (draw_poly or draw_arrow):
				points.append(event.pos)
			
		# Clear Display
		screen.fill((255,255,255))

		# Update & Draw World
		world.update()
		world.draw(screen)

		# Show line if drawing a wall
		if len(points) > 1:
			if draw_poly:
				pygame.draw.lines(screen, THECOLORS["black"], False, points)
			elif draw_arrow:
				blit_arrow(screen, points[0], points[-1])
		
#		if world.run_physics:
#			filecounter += 1
#			z = "0" * (5-len(str(filecounter)))
#			fn = "s/mov1_%s%i.tga" % (z, filecounter)
#			pygame.image.save(screen, fn)

		# Flip Display
		pygame.display.flip()
		
		# Try to stay at 50 FPS
		clock.tick(50)
		
		# output framerate in caption
		pygame.display.set_caption("elements: %i | fps: %s" % (world.get_element_count(), str(int(clock.get_fps()))))

if __name__ == "__main__":
	main()
