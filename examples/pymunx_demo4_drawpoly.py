import pygame
from pygame.locals import *
from pygame.color import *

from pymunx import *

def main():
	# PyGame Init
	pygame.init()
	screen = pygame.display.set_mode((800, 800))
	clock = pygame.time.Clock()

	# Create the Physical Space Class
	world = pymunx()
	world.set_info("LMB: Create Polygon\nRMB: Add Ball\nRMB + Shift: Add Square\nSpace: Pause\n1: Add many balls\n2: Add many squares")
	
	# Add A Wall
	world.add_wall((100, 700), (700, 700))
	
	# Default Settings
	running = True
	draw_poly = False
	points = []
	
	# Main Loop
	while running:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				# Bye Bye
				running = False
				
			elif event.type == KEYDOWN:
				print event
				if event.key == K_SPACE:	
					# Pause with SPACE
					world.run_physics = not world.run_physics
				
				elif event.unicode == "1":
					# Add many Balls
					x, y = pygame.mouse.get_pos()
					for i in range(5):
						for j in range(5): world.add_ball((x-i,y-j))

				elif event.unicode == "2":
					# Add many Balls
					x, y = pygame.mouse.get_pos()
					for i in range(5):
						for j in range(5): world.add_square((x-i,y-j))

			elif event.type == MOUSEBUTTONDOWN and event.button == 1:
				# Start/Stop Wall-Drawing 
				if not draw_poly:
					draw_poly = True
					points = []
					points.append(event.pos)
			
			elif event.type == MOUSEBUTTONUP and event.button == 1:
				if draw_poly:
					# Create Polygon
					draw_poly = False
					points.append(event.pos)
					if len(points) > 2: 
						world.add_poly(points)

			elif event.type == MOUSEMOTION and draw_poly:
				points.append(event.pos)
				
			elif event.type == MOUSEBUTTONDOWN and event.button == 3:
				key = pygame.key.get_mods()
#				print key

				if key == 4097 or key == 4098:
					# Shift: Add Square
					world.add_square(event.pos)
				else:				
					# Add Ball
					world.add_ball(event.pos)
			
		# Clear Display
		screen.fill((255,255,255))

		# Update & Draw World
		world.update()
		world.draw(screen)

		# Show line if drawing a wall
		if len(points) > 1 and draw_poly:
			pygame.draw.lines(screen, THECOLORS["black"], False, points)
			
		# Flip Display
		pygame.display.flip()
		
		# Try to stay at 50 FPS
		clock.tick(50)
		
		# output framerate in caption
		pygame.display.set_caption("fps: " + str(clock.get_fps()))

if __name__ == "__main__":
	main()
