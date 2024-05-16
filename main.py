
import math, random,pygame
from pygame.locals import *
from players import *
from settings import *
import pickle
filename="GameSave.pkl"


PLAY_TYPE=False#False for mini militia, True for pubg
NO_OF_MINES=10
SUPPORTERS=10
ENEMIES=10
MAX_BOMBS=5
HEALTHS=5
CAM_SPEED=80




def save():
	l=[env_list,[p],bullets,bombs,bomb_rect,enemies,supporters,gun_container,mines,mines_rect,healths]
	f=open(filename,"wb")
	pickle.dump(l,f,4)
def read():
	f=open(filename,"rb")
	l=pickle.load(f)
	env_list,p,bullets,bombs,bomb_rect,enemies,supporters,gun_container,mines,mines_rect,healths=l
	p=p[0]
def update_gun_buttons():
	global btn_g1,btn_g2,p
	btn_g1.update_text(p.guns[0].name)
	btn_g2.update_text(p.guns[1].name)
	if p.get_active_gun_index()==0:
		btn_g1.color=(200,0,0)
		btn_g2.color=(0,0,200)
	else:
		btn_g1.color=(0,0,200)
		btn_g2.color=(200,0,0)
	
	

pygame.init()
screen=pygame.display.set_mode((screenX,screenY))
clock=pygame.time.Clock()
screenX,screenY=pygame.display.get_window_size()#-----------------------------------------------

def collide_rect(a,b):
	if a.top<b.top and a.top+a.height>b.top:
		if a.left<b.left and a.left+a.width>b.left:
			#a.left-=1
			#a.top-=1
			return True
		elif b.left<a.left and b.left+b.width>a.left:
			#a.left+=1
			#a.top-=1
			return True
	elif a.bottom>b.bottom and a.bottom-a.height<b.bottom:
		if a.left<b.left and a.left+a.width>b.left:
			#a.bottom+=1
			#a.left-=1
			return True
		elif b.left<a.left and b.left+b.width>a.left:
			#a.bottom+=1
			#a.left+=1
			return True
all_rects=[]
def update_all_rect():
	global all_rects
	all_rects=(env_list+[p]+bullets+bombs+bomb_rect+enemies+supporters+gun_container+mines+mines_rect+healths)
def draw_all_rects(rects,cam,p):
	global rmain
	ox=-cam.centerx+screenX/2
	oy=-cam.centery+screenY/2
	for obj in rects:
		#if rmain.colliderect(obj.rect.move(ox,oy)):
			if isinstance(obj,pygame.Rect):
				if not distance(obj.center,p.rect.center) < 20:
					pygame.draw.rect(screen,(255,255,0),obj.move(ox,oy))
				else:
					pygame.draw.rect(screen,(0,150,25),obj.move(ox,oy),5)
				
			else:
				obj.showrect(screen,ox,oy)
	return ox,oy

#Environment
environment=pygame.sprite.Group()
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
#env_list=[
#	Envx(0,0,1400),
#	Envx(0,2800,1400),
#	Envy(0,0,2800),
#	Envy(1400,0,2800+40),
#	Envy(700,0,900),
#	Envx(0,200,500),
#	Envx(700,1300,550),
#	Envy(700,900,400),
#	Envy(500,600,1600),
#	Envx(500,2200,750),
#	Envx(0,2200,350),
#	Envx(0,850,300)
#	
#]


#player
def get_random_gun():
	return random.choice(list(gun.values()))()
p.guns=[get_random_gun(),get_random_gun()]
p.active_gun=p.guns[0]
all_rects.append(p)
move_speed=move_angle=0
fire_speed=fire_angle=0
p.angle=270-fire_angle
p.lives=float("inf")
update_x=update_y=True

#bullets
bullets=[]

#bomb
bombs=[]
bomb_rect=[]
max_bombs=MAX_BOMBS
damaged=[]
click_bomb=None

#mines
mines=[]
mines_rect=[]
x,y=300,400

def genMines(no):
		for i in range(no):
			mines.append(Mines((random.randint(500,1400),random.randint(500,2400))))
genMines(NO_OF_MINES)
#joysticks and buttons
j1=Joystick((150,150))
j2=Joystick((150,screenY-150),25)
fire_btn=None
def default_button_controls():
	global reload_btn,scroll_but,leave_but,select_enemy_btn,btn_g1,btn_g2,click_bomb_btn,play_type_change_btn,get_out_btn,bomb_btn,fire_btn
	if PLAY_TYPE:
		bomb_btn=Button((200,800),text="bomb")
		bomb_btn.size=40
	else:
		bomb_btn=Button((600,400),text="bomb")
		bomb_btn.size=70
	if PLAY_TYPE:
		fire_btn=Button((600,400),text="Fire")
		fire_btn.size=70
	elif fire_btn:
		fire_btn=None
	reload_btn=Button((600,screenY-100),size=100,text="reload",image="bullets.png")
	reload_btn.size=100
	shield_btn=Button((100,screenY-600),text="shield")
	shield_btn.size=70
	scroll_but=Button((screenX-100,600),text="Scroll")
	scroll_but.size=40
	leave_but=Button((screenX-100,800),text="Leave")
	leave_but.size=40
	select_enemy_btn=Button((screenX-200,800),text="select en")
	select_enemy_btn.size=40
	btn_g1=GunButton((100,550),text=p.guns[0].name)
	btn_g1.size=40
	btn_g2=GunButton((100,850),text=p.guns[1].name)
	btn_g2.size=40
	click_bomb_btn=Button((screenX-100,1000),text="Put")
	click_bomb_btn.size=40
	play_type_change_btn=Button((screenX-60,60),text="Change")
	play_type_change_btn.size=40
	get_out_btn=Button((screenX-200,1000),text="Disappear")
	get_out_btn.size=40
	click_bomb_btn.size=40
	show_joystick=False

#New Button Putting#
exec(open("buttons.py").read())
#from buttons import new_button_controls

if PLAY_TYPE:new_button_controls()
else:default_button_controls()




#shield
shield=None
shield_st=time.time()
shield_time=10

#my stuffs
for i in env_list:
	#environment.add(i)
	all_rects.append(i)
	pass
fingerJoy1=fingerJoy2=fire_finger=None

def collide(p,q,pos=True):
	if not pos:
		a,b=p.center
	else:
		a,b=p.pos
	x,y=q.pos
	if math.sqrt((a-x)**2+(b-y)**2)<20:
		return True
def distance(pos1,pos2):
	x,y=pos1
	a,b=pos2
	
	return math.sqrt((x-a)**2+(y-b)**2)
# Enemy
enemies = []
noOfEnemies = ENEMIES
enemyFireTime = 0.5
enemyst=time.time()
enemy_respawn_pos=(500,2300)
def genEn(i,max_x,max_y):
	while i > 0:
		s = Enemy((random.randint(20, max_x), random.randint(250, max_y)))
		for env in environment:
			if env.rect.colliderect(s.rect):
				continue
		i -= 1
		#s.change_gun(gun["shotgun2"]())
		s.move([],[],p)
		enemies.append(s)
		all_rects.append(s)
genEn(ENEMIES,1200,2600)
#player supporter
supporters=[]
noOfSup=SUPPORTERS
def genSup(i,max_x,max_y):
	while i > 0:
		s = Enemy((random.randint(20, max_x), 
							random.randint(250, max_y)),
							color=(0,0,150),
							image_name="supporter1.png"
				)
		#for env in environment:
		for env in env_list:
			if env.rect.colliderect(s.rect):
				continue
		i -= 1
		s.move([],[],p)
		s.name="supporter"
		#s.gun=gun["grounded"]()
		supporters.append(s)
		all_rects.append(s)

genSup(SUPPORTERS,1200,2600)
#health
def genHealth():
	h=Health((random.randint(1,1290),random.randint(1,2700)))
	h.st=time.time()
	all_rects.append(h)
	return h
noOfHealths=HEALTHS
healths=[genHealth() for i in range(noOfHealths)]
healthDisappTime=25
healthComeTime=5



camera=pygame.Rect(*p.pos,screenX,screenY)
cx,cy=camera.center
cam_speed=CAM_SPEED
rmain=pygame.Rect(0,0,screenX,screenY)
restart=False
#text
fontObj=pygame.font.Font(pygame.font.get_default_font(),30)
#p.lives=noOfEnemies//10
reloading=False
#p.gun.reload_time=3
def showMiniMap(rects):
	

	padx=550
	pady=10
	global rmain
	#ox=-cam.centerx+screenX/2
#	oy=-cam.centery+screenY/2
	ox=oy=0
	for obj in rects:
		#if rmain.colliderect(obj.rect.move(ox,oy)):
			#print(obj)
			if isinstance(obj,pygame.Rect):
				pass
			else:
				obj.show_min_rect(screen,ox,oy,padx,pady)
shakeright=True
gun_container=[]
g=get_random_gun()
g.available_bullets=0
gun_container.append(GunContainer((200,100),random.choice(list(gun.values()))()))
gun_container.append(GunContainer((900,500),gun["mi15"]()))
gun_container.append(GunContainer((200,1700),gun["2m249"]()))
gun_container.append(GunContainer((900,1800),gun["m249"]()))
gun_container.append(GunContainer((900,2300),gun["slr"]()))
gun_container.append(GunContainer((200,900),gun["shotgun"]()))
def contain_gun(pos,gun):
	if gun.name=="hand":
		return
	g=GunContainer(pos,gun)
	gun_container.append(g)
	all_rects.append(g)
for ab in gun_container:
	all_rects.append(ab)
	pass
toast=None
update_all_rect()
scrolling=False
enemyGenerated=0
w=170
player_is_firing=False
play=True
FPS=30
if __name__!="__main__":
	play=False
follow_enemy=False
select_follow_enemy=False
clock=pygame.time.Clock()
cangothruwall=False
def truncate_enemies():
	global enemies
	for en in enemies:
		all_rects.remove(en)
	enemies=[]
def follow_camera(p=p,rect=None):
			if rect:
				pass
			else:
				rect=p.rect
			if camera.centerx<rect.centerx:
				camera.centerx+=(rect.centerx-camera.centerx)/1000*cam_speed
			elif camera.centerx>rect.centerx:
				camera.centerx-=-(rect.centerx-camera.centerx)/1000*cam_speed
			if camera.centery<rect.centery:
				camera.centery+=(rect.centery-camera.centery)/1000*cam_speed
			elif camera.centery>rect.centery:
				camera.centery-=-(rect.centery-camera.centery)/1000*cam_speed
		
start_rect=pygame.Rect(1100,00,1,1)
starting_game_show=True
start_speed=20
background=pygame.transform.scale(pygame.image.load("space_big.jpg"),(screenX,screenY))
max_fps=0
total_player_kills=0
total_enemy_kills=0
p.active_gun=p.guns[0]
update_gun_buttons()
while play:
	try:
		#screen.fill((125,125,125))
		#screen.fill((175,175,175))
		#bullets=[]
		screen.fill((w,w,w))
		#screen.blit(background,(0,0))
		for health in healths:
			if time.time()-health.st>healthDisappTime:
				all_rects.remove(health)
				healths.remove(health)
		if len(healths)<noOfHealths:
				healths.append(genHealth())
	#	if len(enemies) < noOfEnemies:
			#enemyGenerated+=1
			#genEn(1,1200,2600)
		#pygame.draw.rect(screen,BLACK,rmain,5)
		#r.topleft=p.rect.center
		#for i in environment:i.show(screen)
		if starting_game_show:
			#follow_camera(rect=start_rect)
			camera.center=start_rect.center
			if start_rect.centery<2300 and start_rect.centerx>300:
				if start_rect.centery < 2200:
					start_rect.centery+=start_speed
				if start_rect.centery>=2200:
					if start_rect.centerx>200:
						start_rect.centerx-=start_speed
			elif start_rect.centery>=0:
				start_rect.centery-=start_speed
			else:
				starting_game_show=False
				
		elif not scrolling:
			if select_follow_enemy:
				pass
			elif follow_enemy:
				follow_camera(follow_enemy)
			elif not p.disable:
				follow_camera(p)
		ofx,ofy=draw_all_rects(all_rects,camera,p)
		#p.bar.show(screen,ox,oy)
		for s in bullets:
			s.fire(screen)
		if not scrolling and not select_follow_enemy:
			j1.draw(screen)
			j2.draw(screen)
			if max_bombs:bomb_btn.show(screen)
			reload_btn.show(screen)
			#shield_btn.show(screen)
			leave_but.show(screen)
			btn_g1.show(screen)
			btn_g2.show(screen)
			play_type_change_btn.show(screen)
			if PLAY_TYPE:fire_btn.show(screen)
			if len(enemies)<3:get_out_btn.show(screen)
		scroll_but.show(screen)
		click_bomb_btn.show(screen)
		select_enemy_btn.show(screen)
		#show_shield()
		
		if shield and time.time()-shield_st>shield_time:
			all_rects.remove(shield)
			shield=None
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit(0)
			if event.type==MOUSEBUTTONDOWN:
				x,y=event.pos
				if select_follow_enemy and not scrolling:
					disp=float("inf")
					ox=-camera.centerx+screenX/2
					oy=-camera.centery+screenY/2
					for en in enemies+supporters:
						dist=distance(en.rect.center,(camera.left+x,camera.top+y))
						if dist<disp:
							disp=dist
							follow_enemy=en
					select_follow_enemy=False
			if event.type==FINGERDOWN:
				x,y=event.x*screenX,event.y*screenY
				#print(x,y)reload_btn.color=(200,0,0)
				show_joystick=True
				
				if y<365 and x<500:
					j1.pos=(x,y)
				if y>910 and x<500:
					j2.pos=(x,y)
				if not shield and bomb_btn.clicked(x,y):
					#if not p.bomb_thrown:
						bomb=Bomb(p.rect.center,math.radians(p.angle),'player')
						if len(bombs)<=3 and max_bombs:
							max_bombs-=1
							bombs.append(bomb)
							all_rects.append(bomb)
							p.bomb_thrown=True
				if select_enemy_btn.clicked(x,y):
						if not select_follow_enemy and not follow_enemy:
							scrolling=True
							follow_enemy=None
							select_follow_enemy=True
							select_enemy_btn.color=(200,0,0)
							scroll_but.color=(200,0,0)
						else:
							scrolling=False
							follow_enemy=None
							select_follow_enemy=False
							select_enemy_btn.color=(0,0,200)
							scroll_but.color=(0,0,200)
				if len(enemies)<3 and get_out_btn.clicked(x,y):
					cangothruwall=True
					truncate_enemies()
					genEn(noOfEnemies,1200,2600)
					if True:
							p.reset(died=False)
							#gun container limit karna
							for g in gun_container[:len(gun_container)-20]:
								gun_container.remove(g)
								all_rects.remove(g)
							genSup(noOfSup,1200,2600)
							cangothruwall=False
							#bullets=[]
							max_bombs=MAX_BOMBS
							for obj in all_rects:
								if isinstance(obj,Bullet):
									all_rects.remove(obj)
					
					
				if reload_btn.clicked(x,y) and not reloading and p.active_gun.available_bullets!=p.active_gun.max_bullets:
						reloading=True
						reload_btn.color=(200,0,0)
						p.active_gun.reload_st=time.time()
				if btn_g1.clicked(x,y):
					p.active_gun=p.guns[0]
					update_gun_buttons()
				if btn_g2.clicked(x,y):
					p.active_gun=p.guns[1]
					update_gun_buttons()
				if PLAY_TYPE and fire_btn.clicked(x,y):
					player_is_firing=True
					fire_finger=event
				if play_type_change_btn.clicked(x,y):
					PLAY_TYPE=not PLAY_TYPE
					if PLAY_TYPE:
						new_button_controls()
					else:
						default_button_controls()
				#if shield_btn.clicked(x,y) and not shield and time.time()-shield_st>20:
#					continue
#					shield=pygame.Rect(0,0,p.rect.width*3,p.rect.height*3)
#					shield.center=p.rect.center
#					shield_st=time.time()
#					all_rects.append(shield)
				if scroll_but.clicked(x,y):
					scrolling=not scrolling
					if scroll_but.color!=(200,00,0):
						scroll_but.color=(200,0,0)
					else:
						scroll_but.color=(0,0,200)
				if click_bomb_btn.clicked(x,y):
					if DEBUG:
						print(p.rect.center)
						continue
					if click_bomb:
						click_bomb_btn.text="Put"
						all_rects.remove(click_bomb)
						click_bomb.blast()
						click_bomb_btn.color=(0,0,200)
						mines.append(click_bomb)
						click_bomb=None
					else:
						click_bomb_btn.text="Blast"
						click_bomb_btn.color=(200,0,0)
						click_bomb=Mines(p.rect.center)
						all_rects.append(click_bomb)
				
				if leave_but.clicked(x,y):
					contain_gun(p.pos,p.active_gun)
					g=gun["hand"]()
					p.guns[p.get_active_gun_index()]=g
					p.active_gun=g
					update_gun_buttons()
					
				#gun change
				for ab in gun_container:
					if ab.collide and ab.btn.clicked(x,y):
						g=ab.gun
						ab.gun=p.guns[p.get_active_gun_index()]
						p.guns[p.get_active_gun_index()]=g
						p.active_gun=g
						
						toast=Toast("Gun changed",color=(200,200,0))
						if ab.gun.name=="hand":
							gun_container.remove(ab)
							all_rects.remove(ab)
						reloading=False
						ab.gun_changed()
						update_gun_buttons()
						
				if j1.clicked(x,y):
					if not fingerJoy1:	#if finger Joy 1 is None
						fingerJoy1=event
				elif j2.clicked(x,y):
					if not fingerJoy2:
						fingerJoy2=event
				
			if event.type==FINGERMOTION:
				x,y=event.x*screenX,event.y*screenY
				if scrolling:
					camera.centerx-=event.dx*screenX
					camera.centery-=event.dy*screenY
					continue
				if fingerJoy2 and fingerJoy2.finger_id==event.finger_id:
					fire_speed,fire_angle=j2.getPos((event.x)*screenX,(event.y)*screenY)
					p.angle=270-fire_angle
				if fingerJoy1 and fingerJoy1.finger_id==event.finger_id:
					move_speed,move_angle=j1.getPos((event.x)*screenX,(event.y)*screenY)
					update_x=update_y=True
				
					
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
				if PLAY_TYPE and fire_finger:
					if fire_finger.finger_id==event.finger_id:
						fire_finger=None
						player_is_firing=False
		if not fingerJoy1:
			move_speed=move_angle=0
			j1.reset()
		if not fingerJoy2:
			fire_speed=0
			j2.reset()
		
		#my extra stuffs like harding the level
		if False and p.rect.bottom>2240 and p.active_gun.name!="slr":
			contain_gun(p.rect.center,p.active_gun)
			g=gun["slr"]()
			p.guns[p.get_active_gun_index()]=g
			p.active_gun=g
			
			update_gun_buttons()
			toast=Toast("Your gun changed to slr",color=(0,200,0))
		
		
		#player fire
		if PLAY_TYPE:
			if player_is_firing:
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
						all_rects.append(_bullet)
						
					if p.active_gun.available_bullets==0 and p.active_gun.name!="hand":
						reloading=True
						reload_btn.color=(200,0,0)
						p.active_gun.reload_st=time.time()
			
		elif fire_speed>=80//10:
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
					all_rects.append(_bullet)
					
				if p.active_gun.available_bullets==0 and p.active_gun.name!="hand":
					reloading=True
					reload_btn.color=(200,0,0)
					p.active_gun.reload_st=time.time()
		
		#handle mines
		for m in mines:
			for en in enemies+supporters+[p]:
				if distance(m.pos,en.pos)<m.range:
					m.blast()
					if m in all_rects:all_rects.remove(m)
			if m.blasted:
				r=m.blasting(screen,ofx,ofy)
				if r not in mines_rect:
					mines_rect.append(r)
					all_rects.append(r)
				if shakeright:
					camera.centerx+=50
					camera.centery+=30
				else:
					camera.centerx-=30
					camera.centery-=50
				shakeright=not shakeright
				for en in enemies:
					if r.collidepoint(en.pos):
						en.hit(5)
						if en.health<=0:
							toast=Toast("Killed in pmines:"+str(enemyGenerated)+f",enem-{en.gun.name}")
							contain_gun(en.pos,en.gun)
							enemies.remove(en)
							all_rects.remove(en)
							if len(enemies)<=0:
								genEn(noOfEnemies,1200,2600)
								p.reset(died=False)
								for g in gun_container[:len(gun_container)-20]:
									gun_container.remove(g)
									all_rects.remove(g)
								genSup(SUPPORTERS,1200,2600)

								cangothruwall=False
				for en in supporters:
					if r.collidepoint(en.pos):
						en.hit(5)
						if en.health<=0:
							supporters.remove(en)
							contain_gun(en.pos,en.gun)
							all_rects.remove(en)
				if r.collidepoint(p.pos):
					p.hit(3)
					if p.health<=0:
						p.reset()
				if time.time()-m.st>m.blastTime:
					mines_rect.remove(r)
					all_rects.remove(r)
					mines.remove(m)
		
		#handle bombs
		for b in bombs:
			if distance(b.pos,b.to_reach)<30:
				b.blast()
			#for env in environment:
			for env in env_list:
				if env.rect.collidepoint(*b.pos):
					b.blast()
			if b.blasted:
				factor=1
				r=b.blasting(screen,ofx,ofy)
				if r not in bomb_rect:
					bomb_rect.append(r)
					all_rects.append(r)
				if shakeright:
					camera.centerx+=50
					camera.centery+=30
				else:
					camera.centerx-=30
					camera.centery-=50
				shakeright=not shakeright
				for en in enemies:
					if r.collidepoint(en.pos) and en not in b.damaged:
						b.damaged.append(en)
						en.hit(factor*50/distance(en.pos,r.center)+50)
						if en.health<=0:
							toast=Toast("Killed:"+str(enemyGenerated)+f",enem-{en.gun.name}")
							p.kills+=1
							total_player_kills+=1
							contain_gun(en.pos,en.gun)
							enemies.remove(en)
							all_rects.remove(en)
							if len(enemies)<=0:
								genEn(noOfEnemies,1200,2600)
								p.reset(died=False)
								for g in gun_container[:len(gun_container)-20]:
									gun_container.remove(g)
									all_rects.remove(g)
								genSup(SUPPORTERS,1200,2600)

				for en in supporters:
					if r.collidepoint(en.pos) and en not in b.damaged:
						b.damaged.append(en)
						en.hit(factor*50/distance(en.pos,r.center)+50)
						if en.health<=0:
							supporters.remove(en)
							contain_gun(en.pos,en.gun)
							all_rects.remove(en)
				if r.collidepoint(p.pos):
					#p.hit(factor*50/distance(en.pos,r.center)+50)
					#p.bar.dec(factor*50/distance(en.pos,r.center)+50)
					p.hit(10)
					if p.health<=0:
						p.reset()
				if time.time()-b.st>b.blastTime:
					bombs.remove(b)
					bomb_rect.remove(r)
					if b in all_rects:
						all_rects.remove(b)
					all_rects.remove(r)
					p.bomb_thrown=False
			else:
				b.fire(screen)
		
		#reloading bullets
		if reloading and time.time()-p.active_gun.reload_st>p.active_gun.reload_time:
			p.active_gun.available_bullets=p.active_gun.max_bullets
			reloading=False
			p.active_gun.reload_st=time.time()
			reload_btn.color=(0,0,200)
		
		if p.disable and len(supporters)==0:
			print("Enemy won")
			exit(0)
		
		for en in enemies:
			#en.show(screen)
			#if distance(en.pos,p.pos) < 800:
			
			if not starting_game_show:
				#for env in environment:
				
				en.move(env_list,healths,p)
				
			disp=float("inf")
			for enemy in (supporters+[p]):
				dist=distance(en.pos,enemy.pos)
				if dist < disp:
					disp=dist
					to_kill=enemy
			if not en.fired:
				if distance(en.pos,to_kill.pos) < 700:
					en_bullet=en.fire(to_kill.pos)
					if en_bullet and not starting_game_show:
						bullets.append(en_bullet)
						all_rects.append(en_bullet)
						en.fired = True
			if time.time()-en.st>en.gun.fire_time:
				en.fired = False
				en.st=time.time()
		
		#supporters fire
		for en in supporters:
			#for env in environment:
			
			if not starting_game_show:
				en.move(env_list,healths,None)
			
			disp=float("inf")
			for enemy in enemies:
				dist=distance(en.pos,enemy.pos)
				if dist < disp:
					disp=dist
					to_kill=enemy
			if not en.fired:
				if distance(en.pos,to_kill.pos) < 700:
					en_bullet=en.fire(to_kill.pos)
					#en_bullet.pehchan=en.gun.name
					if en_bullet and not starting_game_show:
						bullets.append(en_bullet)
						all_rects.append(en_bullet)
						en.fired = True
			if time.time()-en.st>en.gun.fire_time:
				en.fired = False
				en.st=time.time()
	
		#collision - bomb and enemy
		for b in bombs:
			for en in enemies:
				if collide(b,en):
					b.blast()
		#collision bomb and supporter
		for b in bombs:
			for en in supporters:
				if collide(b,en):
					b.blast()
					toast=Toast("Supporter killed in bomb:"+en.gun.name,color=(200,200,0))
		#collision player and health
		for health in healths:
			if p.rect.colliderect(health.rect):
				p.hit(-health.value)
				#p.bar.inc(health.value)
				if p.health>100:
					p.health=100
					p.bar.set_value(100)
					p.hit(0)
				all_rects.remove(health)
				healths.remove(health)
		
		for health in healths:
			for en in enemies+supporters:
				if en.img.colliderect(health.rect):
					en.hit(-health.value)
					#en.bar.inc(health.value)
					if en.health>100:
						en.health=100
						en.bar.set_value(100)
					all_rects.remove(health)
					healths.remove(health)
		
			
		#collision gun container and player
		for ab in gun_container:
			if p.rect.colliderect(ab.rect):
				ab.on_collide(screen)
			else:
				ab.collide=False
		
		
		#collision check for bullets and env
		#for env in environment:
		for env in env_list:
			for bullet in bullets:
				if collide_rect(env.rect,bullet.rect):
					if bullet.from_gun!="rocket":
						bullets.remove(bullet)
						all_rects.remove(bullet)
					else:
						bullets.remove(b)
						all_rects.remove(b)
						#bomb_rect.append(pygame.Rect(b.pos[0]-400//2,b.pos[1]-400//2,400,400))
						bomb=Bomb(b.pos,0,b.pehchan)
						bomb.blast()
						bombs.append(bomb)
						break
		
		#collision - bullet and enemy
		for en in enemies:
			for b in bullets:
				if collide(en,b) and (b.pehchan.name=="player" or b.pehchan.name=="supporter"):
					if b.from_gun!="rocket":
						
						bullets.remove(b)
						all_rects.remove(b)
						en.hit(b.damage)
						#en.bar.dec(b.damage)
						if en.health<0:
							enemies.remove(en)
							b.pehchan.kills+=1
							total_player_kills+=1
							b.pehchan.update_surf()
							if follow_enemy==en:
								follow_enemy=b.pehchan
								select_enemy_btn.color=(200,0,0)
							toast=Toast("Killed:"+str(enemyGenerated)+f",enem-{en.gun.name}")
							contain_gun(en.pos,en.gun)
							all_rects.remove(en)
						if len(enemies)==0:
							genEn(noOfEnemies,1200,2600)
							p.reset(died=False)
							for g in gun_container[:len(gun_container)-20]:
								gun_container.remove(g)
								all_rects.remove(g)
							genSup(noOfSup,1200,2600)
							cangothruwall=False
							#bullets=[]
							max_bombs=MAX_BOMBS
							for obj in all_rects:
								if isinstance(obj,Bullet):
									all_rects.remove(obj)
									pass
					else:
						#bomb_rect.append(pygame.Rect(b.pos[0]-400//2,b.pos[1]-400//2,400,400))
						bomb=Mines(b.rect.center)#,0,b.pehchan)
						bomb.blast()
						mines.append(bomb)
						bullets.remove(b)
						all_rects.remove(b)
		#collision bullet and supporter
		for en in supporters:
			for b in bullets:
				if collide(en,b) and b.pehchan.name!="player" and b.pehchan.name!="supporter":
					bullets.remove(b)
					
					all_rects.remove(b)
					en.hit(b.damage)
					#en.bar.dec(b.damage)
					if en.health<0:
						b.pehchan.kills+=1
						total_enemy_kills+=1
						b.pehchan.update_surf()
						if follow_enemy==en:
							follow_enemy=b.pehchan
							select_enemy_btn.color=(200,0,0)
						toast=Toast(f"Supporter killed by {b.pehchan}:"+en.gun.name,color=(200,200,0))
						supporters.remove(en)
						contain_gun(en.pos,en.gun)
						all_rects.remove(en)
		
		
		#collision - bullet and player
		if True:
			for b in bullets:
				if collide(b,p) and b.pehchan.name!="player"  and b.pehchan.name!="supporter":
					bullets.remove(b)
					
					all_rects.remove(b)
					p.hit(b.damage)
					if p.health<=0:
						b.pehchan.kills+=5
						total_enemy_kills+=5
						b.pehchan.update_surf()
						follow_enemy=b.pehchan
						select_enemy_btn.color=(200,0,0)
						if not follow_enemy and not select_follow_enemy:
							scroll_but.color=(200,0,0)
							scrolling=True
						#p.disable=True
						
						if p.lives<0:
							exit(0)
						p.reset()
						#p.change_pos(-10000,-10000)
						toast=Toast("You were killed by:"+str(b.pehchan),color=(0,160,160))
				#p.reset(b.damage)
		
		#collision for player and env
		if move_speed:
			movex,movey=p.get_component(move_speed*100,move_angle)
			#for env in environment:
			for env in env_list:
				if cangothruwall:
					pass
				elif env.rect.collidepoint(p.rect.centerx,p.rect.top):
					if movey<0:movey=0
				elif env.rect.collidepoint(p.rect.centerx,p.rect.bottom):
					if movey>0:movey=0
				elif env.rect.collidepoint(p.rect.left,p.rect.centery):
					if movex<0:movex=0
				elif env.rect.collidepoint(p.rect.right,p.rect.centery):
					if movex>0:movex=0
			p.updateMove(movex,movey)
		screen.blit(fontObj.render("kills:"+str(p.kills),1,BLACK),(10,200))
		screen.blit(fontObj.render("p kills:"+str(total_player_kills),1,BLACK),(10,100))
		screen.blit(fontObj.render("bullets:"+str(p.active_gun.available_bullets),1,BLACK),(10,0))
		screen.blit(fontObj.render("deaths:"+str(p.deaths),1,BLACK),(300,0))
		screen.blit(fontObj.render("sup:"+str(len(supporters)),1,BLACK),(400,100))
		screen.blit(fontObj.render("en:"+str(len(enemies)),1,BLACK),(400,200))
		screen.blit(fontObj.render("E kills:"+str(total_enemy_kills),1,BLACK),(400,300))
	
		showMiniMap(all_rects)
	
		#assert len(bullets)<52,"bullet length"
		#
		#clock.tick(30)
		if toast:
			toast.show(screen)
			if toast.destroy:
				toast=None
		#save()
		#p.health=150
		#clock.tick(FPS)
		fpsm=clock.get_fps()
		if fpsm>max_fps:
			print(fpsm)
			max_fps=fpsm
		pygame.display.update()
	except ValueError:
		pass
#	except pygame.error:
#		screen=pygame.display.set_mode((500,500))
	except Exception as e:
		print(e)
		raise
		p.reset(died=False)
		
		

		
		
		