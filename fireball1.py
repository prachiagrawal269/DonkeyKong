
import random
from random import randint
import layout
import board1
class fireball():

# fireballpos is a list containing coordinates of all fireballs along with their random direction of motion
	def __init__(self,game_state):
		self.fireballpos=[]


	def generate_fireball(self,game_state,Player,Donkey):
		Donkey.donkeypos(game_state)
		self.d=randint(0,1)
		self.fireballpos.append(((Donkey.xdonkey,Donkey.ydonkey),self.d))

# movefireball function will let the fireballs move in their random chosen directions
# it is basically a loop that lets all the fireballs move by one position in their respective directions

	def move_fireball(self,game_state,Player,Fireball,Donkey):
		self.count=0
		for (((px,py),d)) in self.fireballpos: 
			self.px=px
			self.py=py
			self.d=d
			if px==24 and py==2 and d==0:
				del self.fireballpos[self.count]
			else:
	#		Player.move_player('z',game_state,Fireball,1)
				x,y,d=Player.move_player('z',game_state,Fireball,1,Player,Donkey)
			#	print str(x)+" " + str(y)
				if Player.markk!=1:
					if self.count < len(self.fireballpos):
						self.fireballpos[self.count]=((x,y),d)
						self.count=self.count+1

# remove_fireball function eliminates all the fireballs after the player dies in order to generate a new board for replay
	def remove_fireball(self,game_state,Player,Fireball):
		count=0
		for (((px,py),d)) in self.fireballpos: 
			self.px=px
			self.py=py
			self.d=d
			if px%4!=0:
				if py == game_state.place[(px)/4][1] or py == game_state.place[(px)/4][2]:
					game_state.layout[px][py]='H'
				else:
					game_state.layout[self.px][self.py]=' '
			else:
				if py == game_state.place[(px)/4-1][1] or py == game_state.place[(px)/4-1][2]:
					game_state.layout[px][py]='H'
				else:
					game_state.layout[self.px][self.py]=' '
game_state=board1.game()		
Fireball=fireball(game_state)	
Player=layout.player(game_state)

