import pygame
from pygame.locals import *
from pygame.color import *

from pymunx import *
from math import fabs
from random import seed
from random import randint

def blit_arrow(surface, a, b):
	xa, ya = a
	xb, yb = b
	dx = xb - xa
	dy = yb - ya
	l = int(sqrt(sqrt((dx*dx) + (dy*dy)))) * 1.5
	print l
	pygame.draw.circle(surface, (l*5, 41, 97), a, 9, 0)
	pygame.draw.line(surface, (l*6, 41, 97), a, b, int(l)/2)

def main():
	# PyGame Init
	pygame.init()
	screen = pygame.display.set_mode((1200, 900))
	clock = pygame.time.Clock()
	seed()
	
	# Create the Physical Space Class
	default_size = 18
	default_elasticity = 0.9
	default_density = 0.1
	default_friction = 0.3
	default_inertia = 10.0
	
	world = pymunx()
	world.set_info("LMB: Add Item, throw Ball or draw Polygon \nRMB: Drag to change Gravity [ (%i, %i) ] \n\nMouseWheel: Size [ %i m ] \nMouseWheel + CTRL: Elasticity [ %.2f ] \nMouseWheel + Shift: Density [ %.2f ] \n\nc: Clear \nf: Fullscreen \nSpace: Pause\n1: Add many balls\n2: Add many squares \n\ns: Screenshot \n[,]: Start Screencast \n[.]: Stop Screencast\nF1: Toggle Help" % (world.space.gravity[0], world.space.gravity[1], default_size, default_elasticity, default_density))

	# Add A Wall
	x,y,w,h = pygame.display.get_surface().get_rect()
	world.add_wall((0, 0), (0, h), default_friction, default_elasticity)
	world.add_wall((0, h), (w, h), default_friction, default_elasticity)
	world.add_wall((w, h), (w, 0), default_friction, default_elasticity)
	world.add_wall((w, 0), (0, 0), default_friction, default_elasticity)

	# Default Settings
	running = True
	draw_poly = False
	draw_arrow = False
	points = []
	
	# Main Loop
	while running:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				# Bye Bye
				running = False
				
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:	
					# Pause with SPACE
					world.run_physics = not world.run_physics

				elif event.key == 282:
					world.toggle_help()

				elif event.unicode == "c": 
					world.clear()
					x,y,w,h = pygame.display.get_surface().get_rect()
					world.add_wall((0, 0), (0, h), default_friction, default_elasticity)
					world.add_wall((0, h), (w, h), default_friction, default_elasticity)
					world.add_wall((w, h), (w, 0), default_friction, default_elasticity)
					world.add_wall((w, 0), (0, 0), default_friction, default_elasticity)
					
				elif event.unicode == "f":
					pygame.display.toggle_fullscreen()

				elif event.unicode == ",":
					world.screencast_start("demo8")
					
				elif event.unicode == ".":
					world.screencast_stop()
					
				elif event.unicode == "s":
					world.screenshot()
				
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
				key = pygame.key.get_mods()
#				print key

				if event.button == 4:
					# MW UP
					if key == 4160 or key == 4224: # Ctrl
						default_elasticity += 0.02
						if default_elasticity > 1.6:
							default_elasticity = 1.6
							
					elif key == 4097 or key == 4098: default_density += 0.02 # Shift
					else: default_size += 2
				else:
					# MW DOWN
					if key == 4160 or key == 4224: # Ctrl
						default_elasticity -= 0.02
						if default_elasticity < 0.0:
							default_elasticity = 0.0
					
					elif key == 4097 or key == 4098: # Shift
						default_density -= 0.02
						if default_density < 0.02:
							default_density = 0.02

					else: 
						default_size -= 2
						if default_size < 2:
							default_size = 2

				world.set_info("LMB: Add Item, throw Ball or draw Polygon \nRMB: Drag to change Gravity [ (%i, %i) ] \n\nMouseWheel: Size [ %i m ] \nMouseWheel + CTRL: Elasticity [ %.2f ] \nMouseWheel + Shift: Density [ %.2f ] \n\nc: Clear \nf: Fullscreen \nSpace: Pause\n1: Add many balls\n2: Add many squares \n\ns: Screenshot \n[,]: Start Screencast \n[.]: Stop Screencast\nF1: Toggle Help" % (world.space.gravity[0], world.space.gravity[1], default_size, default_elasticity, default_density))

			elif event.type == MOUSEBUTTONDOWN and event.button == 1:
				# Start Wall-Drawing 
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
					# Change Gravity
					draw_arrow = False
					x1, y1 = points[0]
					x2, y2 = event.pos
					x = x2 - x1
					y = y2 - y1
					x *= 1.3
					y *= 1.3
					world.set_gravity((x,y*(-1)))
					world.set_info("LMB: Add Ball, throw Ball or draw Polygon \nRMB: Drag to change Gravity [ (%i, %i) ] \n\nMouseWheel: Size [ %i m ] \nMouseWheel + CTRL: Elasticity [ %.2f ] \nMouseWheel + Shift: Density [ %.2f ] \n\nc: Clear \nf: Fullscreen \nSpace: Pause\n1: Add many balls\n2: Add many squares \n\ns: Screenshot \n[,]: Start Screencast \n[.]: Stop Screencast \nF1: Toggle Help" % (world.space.gravity[0], world.space.gravity[1], default_size, default_elasticity, default_density))
								
			elif event.type == MOUSEBUTTONUP and event.button == 1:
				if draw_poly:
					# Create Polygon
					draw_poly = False
					points.append(event.pos)

					if len(points) < 5: 
						i = randint(0,1)
						if i == 0: world.add_ball(event.pos, default_size, default_density, default_inertia, default_friction, default_elasticity)
						else: world.add_square(event.pos, default_size, default_density, default_friction, default_elasticity)
					
					
					else:
						# Draw Poly or Segment
						# Poly if Start and End are close to each other
						x1, y1 = points[0]
						x2, y2 = points[-1]
						x = x2 - x1
						y = y2 - y1

						if fabs(x) > 100 or fabs(y) > 100:
							# Throw Ball
							l = sqrt((x*x)+(y*y)) * 1.8
							ball = world.add_ball(points[0], default_size, default_density, default_inertia, default_friction, default_elasticity)
							world.apply_impulse(ball, (x*l, y*l))

						else:
							world.add_poly(points, default_density, default_friction, default_elasticity)

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

		# Flip Display
		pygame.display.flip()
		
		# Try to stay at 50 FPS
		clock.tick(50)
		
		# output framerate in caption
		pygame.display.set_caption("elements: %i | fps: %s" % (world.get_element_count(), str(int(clock.get_fps()))))

if __name__ == "__main__":
	main()
