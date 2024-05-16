import pygame
from pygame.locals import *
from players import *
from settings import *

pygame.init()
screen=pygame.display.set_mode((screenX,screenY))
while True:
	screen.fill(WHITE)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit(0)
		if event.type==FINGERMOTION:
			#print((event.x)*screenX)
			print(event.finger_id)
		if event.type==MOUSEMOTION:
			print("mouse",event)