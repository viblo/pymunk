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
	world.set_info("LMB: Balls\nRMB: Squares\nSpace: Pause")
	# Add A Wall
	world.add_wall((100, 700), (700, 700))
	
	# Default Settings
	running = True

	# Main Loop
	while running:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				# Bye Bye
				running = False
				
			elif event.type == KEYDOWN and event.key == K_SPACE:	
				# Pause with SPACE
				world.run_physics = not world.run_physics

			elif event.type == MOUSEBUTTONDOWN and event.button == 1:
				# Add Ball
				world.add_ball(event.pos)
				
			elif event.type == MOUSEBUTTONDOWN and event.button == 3:
				# Add Square
				world.add_square(event.pos)

			
		# Clear Display
		screen.fill((255,255,255))

		# Update & Draw World
		world.update()
		world.draw(screen)

		# Flip Display
		pygame.display.flip()
		
		# Try to stay at 50 FPS
		clock.tick(50)
		
		# output framerate in caption
		pygame.display.set_caption("fps: " + str(clock.get_fps()))

if __name__ == "__main__":
	main()
