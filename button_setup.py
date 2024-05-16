import math, random,pygame
from pygame.locals import *
from players import *
from settings import *
import pickle

pygame.init()
screen=pygame.display.set_mode((screenX,screenY))
clock=pygame.time.Clock()
screenX,screenY=pygame.display.get_window_size()#-----------------------------------------------

def save():
	to_write=f'''
def new_button_controls():
	global reload_btn,scroll_but,leave_but,select_enemy_btn,btn_g1,btn_g2,click_bomb_btn,play_type_change_btn,get_out_btn,bomb_btn,fire_btn
	from players import Button,p
	reload_btn=Button({reload_btn.get_pos()},size=100,text="reload",image="bullets.png")
	reload_btn.size={reload_btn.size}
	scroll_but=Button({scroll_but.get_pos()},text="Scroll")
	scroll_but.size={scroll_but.size}
	leave_but=Button({leave_but.get_pos()},text="Leave")
	leave_but.size={leave_but.size}
	select_enemy_btn=Button({select_enemy_btn.get_pos()},text="select en")
	select_enemy_btn.size={select_enemy_btn.size}
	btn_g1=GunButton({btn_g1.get_pos()},text=p.guns[0].name)
	btn_g1.size={btn_g1.size}
	btn_g2=GunButton({btn_g2.get_pos()},text=p.guns[1].name)
	btn_g2.size={btn_g2.size}
	click_bomb_btn=Button({click_bomb_btn.get_pos()},text="Put")
	click_bomb_btn.size={click_bomb_btn.size}
	play_type_change_btn=Button({play_type_change_btn.get_pos()},text="Change")
	play_type_change_btn.size={play_type_change_btn.size}
	get_out_btn=Button({get_out_btn.get_pos()},text="remove")
	get_out_btn.size={get_out_btn.size}
	bomb_btn=Button({bomb_btn.get_pos()},text="bomb")
	bomb_btn.size={bomb_btn.size}
	fire_btn=Button({fire_btn.get_pos()},text="Fire")
	fire_btn.size={fire_btn.size}
	'''.strip()
	filename="buttons.py"
	f=open(filename,"w")
	f.truncate()
	f.write(to_write)
	f.close()
	return to_write

exec(open("buttons.py").read())
'''reload_btn=Button((600,screenY-100),size=100,text="reload",image="bullets.png")
reload_btn.size=100
#shield_btn=Button((100,screenY-600),text="shield")
#shield_btn.size=70
scroll_but=Button((screenX-100,600),text="Scroll")
scroll_but.size=40
leave_but=Button((screenX-100,800),text="Leave")
leave_but.size=40
select_enemy_btn=Button((screenX-200,800),text="select en")
select_enemy_btn.size=40
btn_g1=GunButton((100,550),text="gun 1")
btn_g1.size=40
btn_g2=GunButton((100,850),text="gun 2",type="rectangle")
btn_g2.size=40
click_bomb_btn=Button((screenX-100,1000),text="Put")
click_bomb_btn.size=40
play_type_change_btn=Button((screenX-60,60),text="Change")
play_type_change_btn.size=40
get_out_btn=Button((screenX-200,1000),text="remove")
get_out_btn.size=40
bomb_btn=Button((200,800),text="bomb")
bomb_btn.size=40
fire_btn=Button((600,400),text="Fire")
fire_btn.size=70
'''
p.guns=[list(gun.values())[0](),list(gun.values())[1]()]
new_button_controls()
to_move=to_zoom=None
save_btn=Button((600,700),text="Save")
save_btn.size=40
save_btn.color=(255,255,0)
scale=PowerBar((200,200))
while True:
	screen.fill((255,255,255))
	for b in buttons:
		b.show(screen)
	scale.show(screen)
	scale.action()
		
	for event in pygame.event.get():
		if event.type==MOUSEBUTTONDOWN:
			x,y=event.pos
			scale.on_click(event.pos)
			for b in buttons:
					if b.clicked(x,y) and b!=save_btn:
						to_move=b
						to_zoom=b
						scale.set(to_zoom.size)
						break

		elif event.type==MOUSEMOTION:
			dx,dy=event.rel
			
			if isinstance(to_move,GunButton):
				to_move.rect.centerx+=dx
				to_move.rect.centery+=dy
				to_move.update_text(to_move.text)
			elif to_move:
				to_move.pos[0]+=dx
				to_move.pos[1]+=dy
		elif event.type==MOUSEBUTTONUP:
			x,y=event.pos
			to_move=None
			if save_btn.clicked(x,y):
				save()
				exit(0)
	if to_zoom:
		to_zoom.highlight(screen)
		to_zoom.size=scale.get()
	pygame.display.update()