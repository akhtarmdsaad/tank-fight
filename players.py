import pygame, math, time, random,os
from functools import partial
GREEN=(0,150,0)
BLACK=(0,0,0)
st=time.time()
factor=10
pygame.init()
DEBUG=0
buttons=[]
WALL_WIDTH=40



wall_image=pygame.transform.scale(
pygame.image.load("wall.png"),(40,40)
)
player_image=pygame.transform.scale(
pygame.image.load("player.jpg"),(64,64)
)
reload_image=pygame.image.load("bullets.png")

FOntObj=pygame.font.Font(pygame.font.get_default_font(),50)
class PowerBar:
	"""
	USE p.show(screen) and p.action() in while loop	
	USE p.on_click(event.pos) in mousebutton down or finger down
	
	The p.get_val(max_val) returns the valie according to the max value (by default 100)
	use this to get value of this powerbar
	"""
	def __init__(self,pos,length=500):
		self.pos=pos
		self.length=length
		self.width=self.length//10
		self.value=0
		self.max_value=self.length-10
		self.radius=10
		self.clicked=False
		self.offset=50
		self.rect=pygame.Rect(self.pos[0]-self.offset,self.pos[1],self.length+self.offset,self.width)
	
	def show(self,screen):
		surf=pygame.transform.rotate(FOntObj.render(str(self.get()),1,(0,0,0)),-90)
		r=surf.get_rect()
		r.center=self.pos[0]-25,self.rect.centery
		pygame.draw.rect(screen,(125,125,125),self.rect)
		pygame.draw.rect(screen,BLACK,self.rect,1)
		pygame.draw.line(screen,BLACK,(self.pos[0]+10,self.pos[1]+self.width//2),(self.pos[0]+self.length-10,self.pos[1]+self.width//2))
		pygame.draw.circle(screen,BLACK,(self.pos[0]+10+self.value,self.pos[1]+self.width//2),self.radius)
		screen.blit(surf,r)
	
	def on_click(self,pos):
		self.clicked = self.rect.collidepoint(pos)
	
	def action(self):
		if pygame.mouse.get_pressed()[0]==0:
			self.clicked=False
		if self.clicked:
			self.value=pygame.mouse.get_pos()[0]-self.rect.left-10
			if self.value<0:self.value=0
			if self.value>self.max_value:self.value=self.max_value
			
	def get(self, high_limit=100):
		return self.value*high_limit//self.max_value
	def set(self,value,high_limit=100):
		self.value=value*self.max_value//high_limit


class Toast:
	def __init__(self,text,time_max=2,color=(255,0,0)):
		surfObj=FOntObj.render(str(text),1,color)
		self.surfObj=pygame.transform.rotate(surfObj,-90)
		self.surf_rect=self.surfObj.get_rect()
		self.surf_rect.center=50,675
		self.st=time.time()
		self.max_time=time_max
		self.alpha=255
		self.destroy=False
	def show(self,screen):
		screen.blit(self.surfObj,self.surf_rect)
		if time.time()-self.st>self.max_time:
			self.alpha-=3
			self.surfObj.set_alpha(self.alpha)
			if self.alpha<=0:
				self.destroy=True
		

fontObj=pygame.font.Font(pygame.font.get_default_font(),20)


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
def distance(p,q):
	return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

class Environment(pygame.sprite.Sprite):
	
	def __init__(self,x,y,width,height):
		super().__init__()
		self.rect=pygame.Rect(x,y,width,height)
		self.surface=pygame.Surface((width,height))
		self.font_surf=fontObj.render(f"{x},{y}",1,(0,0,0))
		
	def show(self, screen):
		
		pygame.draw.rect(screen,GREEN,self.rect)
	
	def showrect(self,screen,ox,oy):
		pygame.draw.rect(screen,GREEN,self.rect.move(ox,oy))
		#screen.blit(self.font_surf,self.rect.move(ox,oy).topleft)
	
	def show_min_rect(self,screen,ox,oy,px,py):
		rect=self.rect.copy()
		rect.width/=factor
		rect.height/=factor
		rect.left/=factor
		rect.top/=factor
		rect.left+=px
		rect.top+=py
		pygame.draw.rect(screen,GREEN,rect.move(ox,oy))
	
	
class Envx(Environment):
	def __init__(self,x,y,length):
		super().__init__(x,y,length,WALL_WIDTH)
		for x in range(0,self.rect.width,WALL_WIDTH):
			self.surface.blit(wall_image,(x,0))
	def showrect(self,screen,ox,oy):
		#pygame.transform.smoothscale(wall_image,(40,40),DestSurface=self.surface)
		
		screen.blit(self.surface,self.rect.move(ox,oy))
		
		#rect=self.rect.move(ox,oy)
#		a,y=rect.topleft
#		x=rect.width-a
#		no_of_walls=x//40 + 1
#		extra_wall=x%40
#		for i in range(no_of_walls):
#			screen.blit(wall_image,(rect.left+i*40,y))
#		if extra_wall:
#			screen.blit(
#			pygame.transform.scale(wall_image,(extra_wall,40))
#			,(rect.right-extra_wall,y))
#		
		
class Envy(Environment):
	def __init__(self,x,y,height):
		super().__init__(x,y,WALL_WIDTH,height)
		for y in range(0,self.rect.height,WALL_WIDTH):
			self.surface.blit(wall_image,(0,y))
	def showrect(self,screen,ox,oy):
		screen.blit(self.surface,self.rect.move(ox,oy))
		

class Bar:
	def __init__(self,init_pos,length,color,name='',min=0,max=100,orient="horizontal"):
		self.pos=init_pos
		self.length=length
		self.color=color
		self.name=name
		self.max=max
		self.orient=orient
		self.width=5
		self.rect=pygame.Rect(*init_pos,self.length,10)
		self.reverse=None
		self.value=max
		if not orient.startswith("h("):
			self.rect.width,self.rect.height=self.rect.height,self.rect.width
	
	def show(self,screen,ox,oy):
		pygame.draw.rect(screen,(0,0,0),(*self.rect.move(ox,oy).topleft,self.width,self.length),self.width//2)
		pygame.draw.rect(screen,self.color,self.rect.move(ox,oy))
	
	def set_value(self,value):
		self.value=value
		if self.orient.startswith("h"):
			self.rect.width=value*(self.length//self.max)
			if self.rect.width<0:
				self.rect.width=0
		else:
			self.rect.height=value*(self.length//self.max)
			if self.rect.height<0:
				self.rect.height=0
	
	def dec(self,value):
		if value<0:
			self.inc(abs(value))
			return
		if self.orient.startswith("h"):
			self.rect.width-=value*(self.length//self.max)
			if self.rect.width<0:
				self.rect.width=0
		else:
			self.rect.height-=value*(self.length//self.max)
			if self.rect.height<0:
				self.rect.height=0
		self.value-=value
	
	def inc(self,value):
		if self.orient.startswith("h"):
			self.rect.width+=value*(self.length//self.max)
			if self.rect.width>self.length:
				self.rect.width=self.length
		else:
			self.rect.height+=value*(self.length//self.max)
			if self.rect.height>self.length:
				self.rect.height=self.length
		self.value+=value


class Button:
	def __init__(self,pos,*,image=None,shape="circle",text='',text_color=BLACK,size=200):
		
		self.pos=list(pos)
		self.image=pygame.Surface((200,200),pygame.SRCALPHA)
		self.image.fill((0,0,200,150))
		self.has_image=False
		if image:
			self.image=pygame.image.load(image)
			self.has_image=True
		self.shape=shape
		self.color=(0,0,200)
		self.size=size	#or radius
		if self.has_image:
			self.image=pygame.transform.scale(self.image,(self.size,self.size))
		self.text=text
		self.text_color=text_color
		self.font=pygame.font.Font(pygame.font.get_default_font(),30)
		if shape!="circle":
			self.rect=pygame.Rect(*pos,self.size,self.size)
		else:
			self.rect=pygame.Rect(*pos,self.size,self.size)
		self.image.convert()
		self.update_text(text)
		buttons.append(self)
		
	
	def color_inverse(self):
		if self.color==(200,0,0):
			self.color=(0,0,200)
		else:
			self.color=(200,0,0)
	
	def get_pos(self):
		return tuple(self.pos)
	
	def highlight(self,screen):
		pygame.draw.circle(screen,(200,200,0),self.pos,self.size+1,4)
	
	def show(self, screen):
		if self.shape == "circle":
			#pygame.draw.circle(screen,(0,00,0),self.pos,self.size,2)
			if not self.has_image:
				pygame.draw.circle(screen,self.color,self.pos,self.size)
				screen.blit(pygame.transform.rotate(self.font.render(self.text,1,self.text_color),-90),(self.pos[0],self.pos[1]-self.size))
			else:
				if self.color==(200,0,0):
					self.image.set_alpha(125)
				else:
					self.image.set_alpha(255)
				screen.blit(self.image,self.pos)
		else:
			pygame.draw.rect(screen,self.color,(*self.pos,self.size,self.size))
			screen.blit(pygame.transform.rotate(self.font.render(self.text,1,self.text_color),-90),self.rect)#(self.pos[0],self.pos[1]-self.size))
			
	
	def clicked(self,x,y):
		if self.shape== "circle":
			return distance((x,y),self.pos)<self.size
		else:
			return self.rect.collidepoint(x,y)
	
	def update_text(self,text):
		self.text=text
	
class GunButton(Button):
	
	def update_text(self,text):
		self.text=text
		self.has_image=os.path.exists(self.text+".png")
		if self.has_image:
			self.image=pygame.transform.rotate(
			pygame.transform.scale(
			pygame.image.load(self.text+".png"),(200,200)),-90)
			self.image_rect=self.image.get_rect()
			self.image_rect.center=self.rect.center
			self.shape="rectangle"

	def get_pos(self):
		return tuple(self.rect.center)
		
	def highlight(self,screen):
		pygame.draw.rect(screen,(200,200,0),self.rect,4)
	
	
	def show(self, screen):
		if not self.has_image:
			pygame.draw.circle(screen,self.color,self.pos,self.size)
			screen.blit(pygame.transform.rotate(self.font.render(self.text,1,self.text_color),-90),(self.pos[0],self.pos[1]-self.size))
		else:
			if self.color==(200,0,0):
				self.image.set_alpha(255)
			else:
				self.image.set_alpha(125)
			screen.blit(self.image,self.image_rect)
			pygame.draw.rect(screen,self.color,self.rect,2)
		
	
	
class Health:
	def __init__(self,pos):
		self.image=pygame.image.load("health.png")
		self.pos=pos
		self.rect=self.image.get_rect()
		self.rect.center=self.pos
		self.value=random.randint(10,99)
		self.st=time.time()
	
	def showrect(self, screen,ox,oy):
		#self.img=pygame.transform.scale(self.image,(int(self.rect.width*10/(100-self.value)),int(self.rect.height*10/(100-self.value))))
		screen.blit(self.image,self.rect.move(ox,oy))
		screen.blit(fontObj.render(str(self.value),1,(0,0,0)),self.rect.move(ox,oy).center)
		
	def show_min_rect(self,screen,ox,oy,px,py):
		rect=self.rect.copy()
		rect.width/=factor
		rect.height/=factor
		rect.left/=factor
		rect.top/=factor
		rect.left+=px
		rect.top+=py
		screen.blit(self.image,rect.move(ox,oy).topleft)
	

class Enemy(pygame.sprite.Sprite):
	def __init__(self,pos,color=(0,00,0),image_name="enemy.png"):
		self.pos = list(pos)
		self.x,self.y = pos
		self.rect=pygame.Rect(*self.pos,30,30)
		self.fired = False
		self.img=self.rect.copy()
		self.image=pygame.transform.scale(pygame.image.load(image_name),(self.rect.width+30,self.rect.width+30))
		self.st=time.time()
		self.mvst=time.time()
		self.health=100
		self.kills=0
		self.bar=Bar(self.pos,self.health,(200,0,0),name="Health",max=self.health,orient="v")
		_gun=random.choice(list(gun.values()))()
		#while _gun.name=="hand":
#			_gun=random.choice(list(gun.values()))()
		self.surf=pygame.transform.rotate(fontObj.render(_gun.name+"-"+str(self.kills),1,(255,255,255)),-90)
		self.surf_rect=self.surf.get_rect()
		self.gun=_gun
		self.speed=1/_gun.mass
		self.speed*=55 if _gun.mass > 5 else 1
		self.xchange=random.choice([1,-1])*self.speed*random.randint(1,3)
		self.ychange=random.choice([1,-1])*self.speed*random.randint(1,3)
		self.pehchan=self
		self.color=color
		self.collide_env=None
		self.state="random"
		self.states=["random","health","kill"]
		self.kill_st=time.time()
		self.min_health_req = 50
		self.target_health=None
		self.name=self.gun.name
		self.angle=0
		self.move_once=True

		
	def show(self,screen):
		self.bar.show(screen)
		#pygame.draw.rect(screen,(0,0,0),self.img)
		screen.blit(pygame.transform.rotate(self.image,self.angle),self.img.center)
		self.rect=self.img
	
	def change_gun(self,new_gun):
		temp=self.gun
		self.surf=pygame.transform.rotate(fontObj.render(new_gun.name+"-"+str(self.kills),1,(0,0,0)),-90)
		self.surf_rect=self.surf.get_rect()
		self.gun=new_gun
		self.pehchan=self.gun.name
		self.speed=1/_gun.mass if _gun.mass else 1
		self.speed*=55 if self.gun.mass>6 else 1
		return temp
	
	def update_surf(self):
		self.surf=pygame.transform.rotate(fontObj.render(self.gun.name+"-"+str(self.kills),1,(0,0,0)),-90)
		self.surf_rect=self.surf.get_rect()
		
	
	def __str__(self):
		return self.gun.name
	
	def __repr__(self):
		return self.__str__()
	
	def hit(self,damage=0,value=None):
			if value:
				damage=self.health-value
			self.health-=damage
			self.bar.dec(damage)
			

	def showrect(self,screen,ox,oy):
		screen.blit(self.surf,self.surf_rect.move(ox,oy+10))
		self.bar.show(screen,ox,oy+10)
		#pygame.draw.rect(screen,self.color,self.img.move(ox,oy))
		screen.blit(pygame.transform.rotate(self.image,-self.angle*180/3.14-90),self.img.move(ox,oy))
		
		self.rect=self.img
		
	def show_min_rect(self,screen,ox,oy,px,py):
		rect=self.img.copy()
		rect.width/=factor
		rect.height/=factor
		rect.left/=factor
		rect.top/=factor
		rect.left+=px
		rect.top+=py
		pygame.draw.rect(screen,self.color,rect.move(ox,oy))


	def move(self,env_list,health_list,p):
		if self==env_list:
			return
		if self.state=="random":
			if time.time()-self.mvst>2:
				self.mvst=time.time()
				self.xchange=random.choice([1,-1])*self.speed*random.randint(0,2)
				self.ychange=random.choice([1,-1])*self.speed*random.randint(0,2)
			if self.health < self.min_health_req and time.time()-self.kill_st>4:
				self.state="health"
			elif p and distance(p.pos,self.pos) < 800 and time.time()-self.kill_st>1:
				self.state="kill"
		elif self.state=="health":
			disp=float("inf")
			for health in health_list:
				dist=distance(health.pos,self.pos)
				if dist<disp:
					self.target_health=health
					disp=dist
			self.xchange=math.copysign(self.speed,self.target_health.pos[0]-self.pos[0])
			self.ychange=math.copysign(self.speed,self.target_health.pos[1]-self.pos[1])
			if abs(self.target_health.pos[0]-self.pos[0])<2:
				self.xchange=0
			if abs(self.target_health.pos[1]-self.pos[1])<2:
				self.ychange=0
			
			if self.health > self.min_health_req:
				self.state="random"
		elif self.state=="kill":
			temp=-1 if self.gun.reload_st else 1
			self.xchange=math.copysign(1*self.speed,p.pos[0]-self.pos[0])*temp
			self.ychange=math.copysign(1*self.speed,p.pos[1]-self.pos[1])*temp
		
			
			if self.health < self.min_health_req:
				self.state="health"
			elif distance(p.pos,self.pos) > 800:
				self.state="random"
				
		self.pos[0]+=self.xchange
		self.pos[1]+=self.ychange
		for env in env_list:
			if env.rect.collidepoint(*self.pos): # or env.rect.collidepoint(*self.rect.bottomleft) or env.rect.collidepoint(*self.rect.topright) or env.rect.collidepoint(*self.rect.bottomright):# or self.pos[0]>700 or self.pos[0]<50 or self.pos[1]>1250 or self.pos[1]<50:
				if env!=self.collide_env:
					if self.state=="random":
						self.xchange*=-1
						self.ychange*=-1
					elif self.state=="kill":
						self.xchange*=-2
						self.ychange*=-2
						self.kill_st=time.time()
						self.state="random"
					elif self.state=="health":
						self.xchange*=-3
						self.ychange*=-3
						self.kill_st=time.time()
						self.state="random"
						if self.target_health:
							if abs(self.target_health.pos[0]-self.pos[0])<2:
								self.xchange=0
							if abs(self.target_health.pos[1]-self.pos[1])<2:
								self.ychange=0
					self.pos[0]+=self.xchange
					self.pos[1]+=self.ychange
					self.collide_env=env
				else:
					self.collide_env=None
		
		
		self.img.center=tuple(self.pos)
		self.bar.rect.centery=self.img.centery
		self.bar.rect.centerx=self.img.centerx+10
		self.surf_rect.centery=self.img.centery
		self.surf_rect.centerx=self.img.centerx+20
	
	def change_pos(self,pos):
		self.rect.center=list(pos)
		self.pos=list(pos)
	def fire(self,pos1):
		if DEBUG:return
		x,y=pos1
		x-=self.pos[0]
		y-=self.pos[1]
		if x==0:
			x=0.000000001
		angle=math.atan(y/x)
		if x<0:
			angle+=math.radians(180)
		self.angle=angle
		return self.gun.fire(self.pos,math.degrees(angle)+random.randint(-10,10),self)

class GunContainer:
	def __init__(self,pos,gun):
		self.pos=pos
		self.rect=pygame.Rect(*pos,40,40)
		self.gun=gun
		self.surf=pygame.transform.rotate(fontObj.render(self.gun.name,1,(0,0,0)),-90)
		self.surf_rect=self.surf.get_rect()
		self.surf_rect.center=self.rect.center
		self.btn=Button((50,650),text="change to "+gun.name)
		self.btn.size=40
		self.collide=False
		if self.gun.image:
			self.image_rect=self.gun.image.get_rect()
			self.image_rect.center=self.rect.center
		
	
	def showrect(self,screen,ox,oy):
		if self.gun.image:
			#blit_center(
#			screen,
#			self.gun.image,
#			self.rect.move(ox,oy)
#			)
			screen.blit(
					self.gun.image,
					self.image_rect.move(ox,oy)
			)
			#screen.blit(
#			pygame.transform.rotate(self.gun.image,-90),
#			self.rect.move(ox,oy).bottomleft
#			)
		else:
			pygame.draw.rect(screen,(130,60,0),self.rect.move(ox,oy))
			screen.blit(self.surf,self.surf_rect.move(ox,oy))
		
	
	def on_collide(self,screen):
		self.btn.show(screen)
		self.collide=True
		return True
	
	def gun_changed(self):
		self.surf=pygame.transform.rotate(fontObj.render(self.gun.name,1,(0,0,0)),-90)
		self.surf_rect=self.surf.get_rect()
		self.surf_rect.center=self.rect.center
		self.btn.text="change to "+self.gun.name
		if self.gun.image:
			self.image_rect=self.gun.image.get_rect()
			self.image_rect.center=self.rect.center
		
		
	def show_min_rect(self,screen,ox,oy,padx,pady):
		pass
	
class Gun:
	def __init__(self,damage,speed,_time,max=30,rd=1,name='',mass=10):
		self.damage=damage
		self.fire_time=_time
		self.max_bullets=max
		self.available_bullets=self.max_bullets
		self.st=time.time()
		self.reload_time=rd
		self.reload_st=time.time()
		self.name=name
		self.bullet_speed=speed
		self.mass=mass
		self.image=name+".png"
		if os.path.exists(self.image):
			self.image=pygame.transform.scale(
				pygame.image.load(self.image),(200,200)
			)
			self.image=pygame.transform.rotate(self.image,-90)
		else:
			self.image=None
	
	def fire(self,pos,angle,pehchan):
		if self.available_bullets<=0 :
				if not self.reload_st:
					self.reload_st=time.time()
				self.reload()
				return
		if time.time()-self.st>self.fire_time:
			self.st=time.time()
			self.available_bullets-=1
			return Bullet(pos,angle,self.damage,pehchan,speed=self.bullet_speed,from_gun=self.name)
		return None
	
	def reload(self,enemy=True):
		
		if time.time()-self.reload_st>self.reload_time:
			self.available_bullets=self.max_bullets
			self.reload_st=None
		

class Player(pygame.sprite.Sprite):
		
		def __init__(self,pos):
			super().__init__()
			self.pos=list(pos)
			#self.rect=pygame.Rect(*pos,30,20)
			self.image=pygame.transform.scale(pygame.image.load("player.png"),(40,40))
			self.rect=self.image.get_rect()
			self.rect.topleft=self.pos
			self.st=time.time()
			self.angle=0
			self.bomb_thrown=False
			self.rotatedImage=self.image
			self.health=100
			self.lives=3
			self.deaths=0
			self.mass=70
			self.kills=0
			self.bar=Bar((50,400),600,(200,0,0),name="Health",max=self.health,orient="v")
			self.bar.width=30
			self.bar.rect.width=30
			self.health_color=(0,200,0)
			self.disable=False
			self.name="player"
		
		def update_surf(self):
			pass
		
		def change_pos(self,*pos):
			self.rect.center=list(pos)
			self.pos=list(pos)
			
		def show(self,screen):
			#pygame.draw.rect(screen,BLACK,self.rect)
			self.rotatedImage=pygame.transform.rotate(self.image,self.angle)
			screen.blit(self.rotatedImage,tuple(self.pos))
		
		def __str__(self):
			return "player"
		def __repr__(self):
			return self.__str__()

		def showrect(self,screen,ox,oy):
			if not self.disable:
				self.rotatedImage=pygame.transform.rotate(self.image,self.angle)
				screen.blit(self.rotatedImage,self.rect.move(ox,oy).topleft)
				self.surf=pygame.transform.rotate(fontObj.render(self.active_gun.name,1,(255,255,255)),-90)
				self.surf_rect=self.surf.get_rect()
				self.surf_rect.center=(self.rect.centerx+40,self.rect.centery)
				screen.blit(self.surf,self.surf_rect.move(ox,oy))
				self.bar.show(screen,0,0)
				screen.blit(pygame.transform.rotate(FOntObj.render("Need "+str(100-self.health),1,self.health_color),-90),(70,600))
		
		def hit(self, damage=0,value=None):
			if DEBUG:return
			if value:
				damage=self.health-value
			self.health-=damage
			self.bar.dec(damage)
			if self.health>=80:
				self.health_color=(0,200,0)#green
			elif self.health<=30:
				self.health_color=(200,0,0)#red
			else:
				self.health_color=(0,0,0)#black
		
		def show_min_rect(self,screen,ox,oy,px,py):
			rect=self.rect.copy()
			rect.width/=factor
			rect.height/=factor
			rect.left/=factor
			rect.top/=factor
			rect.left+=px
			rect.top+=py
			pygame.draw.rect(screen,(0,0,200),rect)
			#screen.blit(self.rotatedImage,rect.move(ox,oy).topleft)

		def updateMove(self,movex,movey):
			if not self.disable:
				self.rect.left+=movex
				self.rect.top+=movey
				self.pos=list(self.rect.topleft)
		
		def get_component(self,force,angle):
			x=force/(self.mass+self.active_gun.mass)*math.cos(math.radians(angle))
			y=force/(self.mass+self.active_gun.mass)*math.sin(math.radians(angle))
			return x,y
		
		def get_active_gun_index(self):
			if self.active_gun==self.guns[0]:
				return 0
			else:
				return 1
			return 0
		
		def fire(self,angle):
			if time.time()-self.st>0.2 and self.active_gun.available_bullets:
				return self.active_gun.fire(self.rect.topleft,angle,self)
		
		def reset(self,died=True):
			#return	#uncomment in developer mode
			print("You got knocked out")
			self.pos=[100,50]
			self.rect.topleft=self.pos
			#self.disable=True
			if died:
				#self.lives-=1
				self.deaths+=1
				if self.lives<=self.deaths:
					exit(0)
			self.hit(value=100)
			self.active_gun.available_bullets=self.active_gun.max_bullets

class Mines:
	def __init__(self,pos):
		self.pos=pos
		self.range=100
		self.radius=10
		self.bombDistance=800
		self.blastlength=self.bombDistance//2
		self.blasted=False
		self.st=None
		self.blastTime=0.5
		self.rect=pygame.Rect(*self.pos,10,10)
	
	def showrect(self,screen,ox,oy):
		pygame.draw.circle(screen,(200,0,0),self.rect.move(ox,oy).topleft,self.radius)
	
	def show_min_rect(self,screen,ox,oy,px,py):
		return
	
	def blasting(self,screen,ox,oy):
		return pygame.Rect(self.pos[0]-self.blastlength//2,self.pos[1]-self.blastlength//2,self.blastlength,self.blastlength)
	
	def blast(self):
		if not self.blasted:
			self.st=time.time()
		self.blasted=True
		

class Bomb:
	
	def __init__(self,pos,angle,name):
		self.pos=list(pos)
		self.angle=angle
		self.thrownBy=name
		self.radius=5
		self.bombDistance=800
		self.st=time.time()
		self.blastlength=self.bombDistance//2
		self.to_reach=[self.pos[0]-self.bombDistance*math.sin(angle),self.pos[1]-self.bombDistance*math.cos(angle)]
		self.blasted=False
		self.diffx=self.to_reach[0]-self.pos[0]
		self.diffy=self.to_reach[1]-self.pos[1]
		self.blastTime=0.5
		self.rect=pygame.Rect(*self.pos,10,10)
	
	def show(self,screen):
		pygame.draw.circle(screen,(0,0,200),self.rect.topleft,self.radius)
	
	def showrect(self,screen,ox,oy):
		pygame.draw.circle(screen,(0,0,200),self.rect.move(ox,oy).topleft,self.radius)
	
	def show_min_rect(self,screen,ox,oy,px,py):
		rect=self.rect.copy()
		rect.width/=factor
		rect.height/=factor
		rect.left/=factor
		rect.top/=factor
		rect.left+=px
		rect.top+=py
		pygame.draw.circle(screen,(0,0,200),rect.move(ox,oy).topleft,self.radius/factor)
	
	
	def fire(self,screen):
		self.diffx=self.to_reach[0]-self.pos[0]
		self.diffy=self.to_reach[1]-self.pos[1]
		self.pos[0]+=self.diffx/100
		self.pos[1]+=self.diffy/100
		self.rect.topleft=self.pos
		self.st=time.time()
		#self.show(screen)
	
	def blasting(self,screen,ox,oy):
		return pygame.Rect(self.pos[0]-self.blastlength//2,self.pos[1]-self.blastlength//2,self.blastlength,self.blastlength)
		pygame.draw.rect(screen,(200,200,0),rect.move(ox,oy))
	
	def blastingoffset(self,screen,ox,oy):
		rect=pygame.Rect(self.pos[0]-self.blastlength//2,self.pos[1]-self.blastlength//2,self.blastlength,self.blastlength)
		pygame.draw.rect(screen,(200,200,0),rect.move(ox,oy))
		return rect
	
	def blast(self):
		self.blasted=True
		self.damaged=[]
	
class Bullet(pygame.sprite.Sprite):
	def __init__(self,pos,angle,damage,pehchan='',speed=20,from_gun=None):
		super().__init__()
		self.pehchan = pehchan
		self.from_gun=from_gun
		self.pos=pos
		self.image=pygame.image.load("bullet.png")
		self.rect=self.image.get_rect()
		self.speed=speed
		self.rotatedImage=self.image
		self.angle=math.radians(270-angle)
		assert type(damage)==type(5),"Damage should be integer"
		self.damage=damage

	def fire(self,screen):
		x,y=self.pos
		x-=self.speed*math.sin(self.angle)
		y-=self.speed*math.cos(self.angle)
		self.rect.topleft=(x,y)
		self.rotatedImage=pygame.transform.rotate(self.image,math.degrees(self.angle))
		self.pos=[x,y]
		#self.show(screen)
		
	def show(self,screen):
		screen.blit(self.rotatedImage,self.rect.center)
	
	def showrect(self,screen,ox,oy):
		screen.blit(self.rotatedImage,self.rect.move(ox,oy).center)
	
	def show_min_rect(self,screen,ox,oy,px,py):
		return
		rect=self.rect.copy()
		rect.width/=factor
		rect.height/=factor
		rect.left/=factor
		rect.top/=factor
		rect.left+=px
		rect.top+=py
		pygame.draw.rect(screen,GREEN,rect.move(ox,oy))
	
class Joystick:
	
	def __init__(self,pos,size=30):
		self.pos=pos
		self.joypos=pos
		self.size=size
		self.dist=self.size*4
		self.temp_dist=0
		
	def draw(self,screen):
		RED=(255,0,0)
		BLACK=(0,0,0)
		pygame.draw.circle(screen,RED,self.joypos,self.size)
		pygame.draw.circle(screen,BLACK,self.pos,self.size*4,10)
		#print("show",self.joypos)
		
	def getPos(self,x,y):
		''' returns tuple of (distance,direction)
		angle in degrees '''
		l=pygame.mouse.get_pressed()[0]
		a=b=theta=0
		if l==1:
			x-=self.pos[0]
			y-=self.pos[1]
			if x==0:
				x=0.000000001
			self.temp_dist=distance(self.pos,(x+self.pos[0],y+self.pos[1]))
			if self.temp_dist>self.dist:
				self.temp_dist=self.dist
			theta=math.atan(y/x)
			if x<0:
				theta+=math.radians(180)
			a=self.pos[0]+self.temp_dist*math.cos(theta)
			b=self.pos[1]+self.temp_dist*math.sin(theta)
			self.joypos=(a,b)
			#print("func",a,b)
		else:
			self.joypos=self.pos
		return (self.temp_dist//10,math.degrees(theta))
	
	def reset(self):
		self.joypos=self.pos
	
	def clicked(self,x,y):
		return distance((x,y),self.pos)<self.dist

def create_gun(a,b,c,d,e,name,mass):
	assert b<40,"speed less than 30"
	return Gun(a,b,c,d,e,name,mass=mass)
gun={
	#gun parameters - damage, speed, fire time, total bullets, reload time, name to show,mass
	"m249":partial(create_gun,15,25,0.05,100,5,'m249',30),
	"m250":partial(create_gun,18,27,0.07,100,5,"m250",30),
	"m416":partial(create_gun,10,25,0.1,30,1,"m416",8),
	"shotgun":partial(create_gun,110,15,1,2,2,"shotgun",10),
	"shotgun2":partial(create_gun,110,25,1,2,2,"shotgun2",10),
	"m761":partial(create_gun,15,17,0.09,30,1,"m761",15),
	"m762":partial(create_gun,18,15,0.1,40,1,"m762",15),
	"m763":partial(create_gun,20,10,0.15,50,1,"m763",20),
	"slr":partial(create_gun,30,15,0.5,10,2,"slr",8),
	"slt":partial(create_gun,25,15,0.3,15,2,"slt",10),
	"2m249":partial(create_gun,9,28,0.001,500,20,"2m249",50),
	"hand":partial(create_gun,0,0,0,0,0,"hand",1),
	"grounded":partial(create_gun,49,29,0.001,1000,10,"grounded",float("inf")),
	"mi15":partial(create_gun,20,25,0.05,50,4,"mi15",30)
	
#	"rocket":partial(create_gun,0,20,3,4,7,"rocket",100),
	#"saad special":partial(create_gun,30,25,0.001,1000,3,"saad's gun",70)
}

p=Player((100,50))
