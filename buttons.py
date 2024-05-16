def new_button_controls():
	global reload_btn,scroll_but,leave_but,select_enemy_btn,btn_g1,btn_g2,click_bomb_btn,play_type_change_btn,get_out_btn,bomb_btn,fire_btn
	from players import Button,p
	reload_btn=Button((609, 1192),size=100,text="reload",image="bullets.png")
	reload_btn.size=100
	scroll_but=Button((648, 600),text="Scroll")
	scroll_but.size=40
	leave_but=Button((649, 768),text="Leave")
	leave_but.size=40
	select_enemy_btn=Button((524, 778),text="select en")
	select_enemy_btn.size=40
	btn_g1=GunButton((205, 452),text=p.guns[0].name)
	btn_g1.size=100
	btn_g2=GunButton((183, 890),text=p.guns[1].name)
	btn_g2.size=100
	click_bomb_btn=Button((189, 1060),text="Put")
	click_bomb_btn.size=40
	play_type_change_btn=Button((688, 28),text="Change")
	play_type_change_btn.size=70
	get_out_btn=Button((600, 900),text="remove")
	get_out_btn.size=40
	bomb_btn=Button((379, 1157),text="bomb")
	bomb_btn.size=60
	fire_btn=Button((707, 304),text="Fire")
	fire_btn.size=100