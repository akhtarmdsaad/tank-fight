import pygame,os
import random
from pygame.locals import *
from players import *
from settings import *

filename="MapGenerated.txt"
if not os.path.exists(filename):
	open(filename,"w+")

environment=[
	#Envx(0,0,500)
]
screen=pygame.display.set_mode((500,500))
camera=pygame.Rect(0,0,screenX,screenY)
rooms=[]
tops=[]
rx=140
ry=0
change_x=False
change_y=False
current_row=[]
factor=1
def get_down():
	return
	while True:
		for event in pygame.event.get():
			if event.type==MOUSEBUTTONDOWN:
				return
	
def gen_room(rx):
	#while row not completed add the rooms horizontally
	ry=0
	width=random.randint(500//factor,1400//factor)
	while True:
		height=random.randint(500//factor,2400//factor)
		if height>2400//factor-ry:
			height=2400//factor-ry
			rooms.append(Room(rx-width,ry,width,height))
			print(rx,ry,width,height)
			break
		rooms.append(Room(rx-width,ry,width,height))
		print(rx,ry,width,height)
		ry+=height
	rx-=width
	ry=0
	if rx<0:
		return
	gen_room(rx)

class Room:
	def __init__(self,x,y,width,height):
		self.top=False
		self.rect=pygame.Rect(x,y,width,height)


gen_room(1400//factor)
no=1
for room in rooms[:no]:
	rect=room.rect
	environment.append(Envx(rect.top,rect.left,rect.width))
	environment.append(Envx(rect.bottom,rect.left,rect.width))
	environment.append(Envy(rect.top,rect.left,rect.height))
	environment.append(Envy(rect.top,rect.right,rect.height))

while True:
	
	screen.fill((255,255,255))
	ox=-camera.centerx+screenX/2
	oy=-camera.centery+screenY/2
	for env in environment:
		env.showrect(screen,ox,oy)

	for room in rooms[:no]:
		pygame.draw.rect(screen,(0,200,0),room.rect.move(ox,oy),40//factor)
	
	for event in pygame.event.get():
		if event.type==MOUSEBUTTONDOWN:
			no+=0
		if event.type==FINGERMOTION:
				#x,y=event.x*screenX,event.y*screenY
				camera.centerx-=event.dx*screenX
				camera.centery-=event.dy*screenY
	
	
	
	pygame.display.update()
