from pygame import *

import math, random,pygame
from pygame.locals import *
from players import *
from settings import *


pygame.init()
screen=pygame.display.set_mode((screenX,screenY))
clock=pygame.time.Clock()
fontObj=pygame.font.Font(pygame.font.get_default_font(),50)
p=Player((100,50))
p.guns=[gun["mi15"](),gun["hand"]()]
p.active_gun=p.guns[0]
j1=Joystick((150,150))
j2=Joystick((150,screenY-150),25)
move_speed=move_angle=fire_speed=fire_angle=0
fingerJoy1=fingerJoy2=None
b=Button((600,800),text="Next",shape="square")
b.size=100
b.text_color=(255,255,255)
c=Button((600,600),text="Prev",shape="square")
c.size=100
c.text_color=(255,255,255)
show_text=True
show_text_btn=Button((600,100),text="toggle text",shape="square")
show_text_btn.size=100
reload_btn=Button((600,screenY-100),size=100,text="reload",image="bullets.png")
reload_btn.size=100
show_text_btn.text_color=(255,255,255)
bullets=[]
env_list=[
		Envx(0,0,1400),
		Envx(0,2800,1400),
		Envy(0,0,2800),
		Envy(1400,0,2800+40),
		Envy(700,0,600),
		Envx(0,200,500),
		Envx(500,700,700),
		Envy(500,700,500),
		Envy(800,1100,600),
		Envx(800,1700,400),
		Envx(1100,1200,1400-1100),
		Envx(350,1400,800-350),
		Envy(500,1800,2200-1800),
		Envx(0,2200,900),
		Envx(1100,2200,1400-1100),
		Envy(700,2400,400)
	
]
cam=pygame.Rect(*p.pos,screenX,screenY)
cx,cy=cam.center
cam_speed=80
def follow_cam(p):
			if cam.centerx<p.rect.centerx:
				cam.centerx+=(p.rect.centerx-cam.centerx)/1000*cam_speed
			elif cam.centerx>p.rect.centerx:
				cam.centerx-=-(p.rect.centerx-cam.centerx)/1000*cam_speed
			if cam.centery<p.rect.centery:
				cam.centery+=(p.rect.centery-cam.centery)/1000*cam_speed
			elif cam.centery>p.rect.centery:
				cam.centery-=-(p.rect.centery-cam.centery)/1000*cam_speed
		

def write(text,pos):
	global show_text
	if not show_text:return
	#print(text.count("\n"))
	surf=fontObj.render(str(text),1,(0,0,0))
	r=surf.get_rect()
	r.center=pos
	screen.blit(surf,r)
def step1():
	global fingerJoy1,fingerJoy2,show_text
	text="Hello This is your Tank"
	t2="Try Controlling this Tank"
	t3="by tapping your finger"
	t4="These are walls (very basic)"
	step=1
	reloading=False
	shield=False
	while True:
		screen.fill((255,255,255))
		#setting the cam
		if step>2:
			cam.center=p.rect.center
		
			ofx,ofy=-cam.centerx+screenX/2,-cam.centery+screenY/2
		else:
			ofx,ofy=0,0
		if step==1:
			write(text,(350,150))
			write(t2,(350,350))
			write(t3,(350,450))
		if step!=1:
			j1.draw(screen)
			j2.draw(screen)
			if step==2:
				write("<--This is to move",(450,100))
				write("<--This is to rotate",(450,1200))
				write("<-- This is health bar",(350,600))
			b.show(screen)
			c.show(screen)
			show_text_btn.show(screen)
		if step>2:
			write(t4,(350,300))
			write("Move around to get ",(350,350))
			write("some experience",(350,400))
			write("Slide joystick out to fire",(350,1050))
			
			for bullet in bullets:
				bullet.fire(screen)
				bullet.showrect(screen,ofx,ofy)
			p.active_gun.available_bullets+=1
			for env in env_list:
				env.showrect(screen,ofx,ofy)
		p.showrect(screen,ofx,ofy)
		for event in pygame.event.get():
			if event.type==FINGERDOWN:
				if step==1:
					step=2
				else:
					x,y=event.x*screenX,event.y*screenY
					#print(x,y)reload_btn.color=(200,0,0)
					#show_joystick=True
					if b.clicked(x,y):
						step+=1
						show_text=True
						if step==3:
							p.change_pos(100,100)
						if step==4:
							return
					if c.clicked(x,y):
						if step>0:step-=1
						show_text=True
						#print("B clicked")
					if show_text_btn.clicked(x,y):
						show_text=not show_text
					if y<365 and x<500:
						j1.pos=(x,y)
					if y>910 and x<500:
						j2.pos=(x,y)
					if j1.clicked(x,y):
						if not fingerJoy1:	#if finger Joy 1 is None
							fingerJoy1=event
					elif j2.clicked(x,y):
						if not fingerJoy2:
							fingerJoy2=event
			if event.type==FINGERMOTION:
				x,y=event.x*screenX,event.y*screenY
				
				if fingerJoy2 and fingerJoy2.finger_id==event.finger_id:
					fire_speed,fire_angle=j2.getPos((event.x)*screenX,(event.y)*screenY)
					p.angle=270-fire_angle
				if fingerJoy1 and fingerJoy1.finger_id==event.finger_id:
					move_speed,move_angle=j1.getPos((event.x)*screenX,(event.y)*screenY)
					update_x=update_y=True
					move_speed/=2
			if event.type==FINGERUP:
				x,y=event.x*screenX,event.y*screenY
				#print("Fingerup",event)
				show_joystick=True
				if fingerJoy1:
					if fingerJoy1.finger_id==event.finger_id:
						fingerJoy1=None
				if fingerJoy2:
					if fingerJoy2.finger_id==event.finger_id:
						fingerJoy2=None
		if not fingerJoy1:
			move_speed=move_angle=0
			j1.reset()
		if not fingerJoy2:
			fire_speed=0
			j2.reset()
		if step >= 3 and fire_speed>=80//10:
			#cancel reloading if already bullet is present and player wants to fire
			if p.active_gun.available_bullets!=0 and reloading:
				reloading=False
				reload_btn.color=(0,0,200)
			elif p.active_gun.available_bullets==0 and reloading:
				pass
			else:
				
				_bullet=p.fire(fire_angle) if not shield else None
				
				if isinstance(_bullet,Bullet):
					bullets.append(_bullet)
					
					
				if p.active_gun.available_bullets==0 and p.active_gun.name!="hand":
					reloading=True
					reload_btn.color=(200,0,0)
					p.active_gun.reload_st=time.time()
		
		for env in env_list:
			for bullet in bullets:
				if collide_rect(env.rect,bullet.rect):
					
						bullets.remove(bullet)
				
					#collision for player and env
		if step>=2 and move_speed:
			movex,movey=p.get_component(move_speed*100,move_angle)
			#for env in environment:
			if step>2:
				for env in env_list:
					if env.rect.collidepoint(p.rect.centerx,p.rect.top):
						if movey<0:movey=0
					elif env.rect.collidepoint(p.rect.centerx,p.rect.bottom):
						if movey>0:movey=0
					elif env.rect.collidepoint(p.rect.left,p.rect.centery):
						if movex<0:movex=0
					elif env.rect.collidepoint(p.rect.right,p.rect.centery):
						if movex>0:movex=0
			p.updateMove(movex,movey)
		
		pygame.display.update()
def step2():
	global fingerJoy1,fingerJoy2,show_text
	step=1
	reloading=False
	shield=False
	while True:
		screen.fill((255,255,255))
		#setting the cam
		follow_cam(p)
		ofx,ofy=-cam.centerx+screenX/2,-cam.centery+screenY/2
		j1.draw(screen)
		j2.draw(screen)
		b.show(screen)
		c.show(screen)
		show_text_btn.show(screen)
		for bullet in bullets:
			bullet.fire(screen)
			bullet.showrect(screen,ofx,ofy)
		p.showrect(screen,ofx,ofy)
		for env in env_list:
			env.showrect(screen,ofx,ofy)
		for event in pygame.event.get():
			if event.type==FINGERDOWN:
				x,y=event.x*screenX,event.y*screenY
				#print(x,y)reload_btn.color=(200,0,0)
				#show_joystick=True
				if b.clicked(x,y):
					step+=1
					show_text=True
				if c.clicked(x,y):
					if step>0:step-=1
					show_text=False
					#print("B clicked")
				if show_text_btn.clicked(x,y):
						show_text=not show_text
				if y<365 and x<500:
						j1.pos=(x,y)
				if y>910 and x<500:
						j2.pos=(x,y)
				if j1.clicked(x,y):
						if not fingerJoy1:	#if finger Joy 1 is None
							fingerJoy1=event
				if j2.clicked(x,y):
						if not fingerJoy2:
							fingerJoy2=event
			if event.type==FINGERMOTION:
				x,y=event.x*screenX,event.y*screenY
				
				if fingerJoy2 and fingerJoy2.finger_id==event.finger_id:
					fire_speed,fire_angle=j2.getPos((event.x)*screenX,(event.y)*screenY)
					p.angle=270-fire_angle
				if fingerJoy1 and fingerJoy1.finger_id==event.finger_id:
					move_speed,move_angle=j1.getPos((event.x)*screenX,(event.y)*screenY)
					update_x=update_y=True
					move_speed/=2
			if event.type==FINGERUP:
				x,y=event.x*screenX,event.y*screenY
				#print("Fingerup",event)
				show_joystick=True
				if fingerJoy1:
					if fingerJoy1.finger_id==event.finger_id:
						fingerJoy1=None
				if fingerJoy2:
					if fingerJoy2.finger_id==event.finger_id:
						fingerJoy2=None
		if not fingerJoy1:
			move_speed=move_angle=0
			j1.reset()
		if not fingerJoy2:
			fire_speed=0
			j2.reset()
		if fire_speed>=80//10:
			#cancel reloading if already bullet is present and player wants to fire
			if p.active_gun.available_bullets!=0 and reloading:
				reloading=False
				reload_btn.color=(0,0,200)
			elif p.active_gun.available_bullets==0 and reloading:
				pass
			else:
				_bullet=p.fire(fire_angle) if not shield else None
				if isinstance(_bullet,Bullet):
					bullets.append(_bullet)
				if p.active_gun.available_bullets==0 and p.active_gun.name!="hand":
					reloading=True
					reload_btn.color=(200,0,0)
					p.active_gun.reload_st=time.time()
		
		for env in env_list:
			for bullet in bullets:
				if collide_rect(env.rect,bullet.rect):
					bullets.remove(bullet)
				
					#collision for player and env
		if move_speed:
			movex,movey=p.get_component(move_speed*100,move_angle)
			#for env in environment:
			for env in env_list:
				if env.rect.collidepoint(p.rect.centerx,p.rect.top):
					if movey<0:movey=0
				elif env.rect.collidepoint(p.rect.centerx,p.rect.bottom):
					if movey>0:movey=0
				elif env.rect.collidepoint(p.rect.left,p.rect.centery):
					if movex<0:movex=0
				elif env.rect.collidepoint(p.rect.right,p.rect.centery):
					if movex>0:movex=0
			p.updateMove(movex,movey)
		
		pygame.display.update()
step1()
step2()