import sys
#import threading
import random
import os
import time
import fireball1
import board1
from random  import randint
import read_in


#valid_move function is the checkwall function here 

# the function checkcollision() has been written in parts


class person():
    
    def __init__(self,x,y):
	self.x=x
	self.y=y
    def valid_move(self,x,y,game_state,flag):
	if x >= 25 or x <= 0 or y <= 0 or y >=49:
	    return False
	if 'X' in game_state.layout[x][y]:
	    return False
	if 'O' in game_state.layout[x][y] and flag==0:
	#    game_state.gameover=True
	    return False
	if 'D' in game_state.layout[x][y] and flag==0:
	    game_state.gameover=True
	    return False
	return True


class donkey(person):

  #  global game_state
    def __init__(self,game_state):
	x=4
	y=randint(2,game_state.level[1])
	person.__init__(self,x,y)  
	game_state.layout[x][y]='D'

# fetches position of donkey
    def donkeypos(self,game_state):
	self.xdonkey=self.x
	self.ydonkey=self.y
    
    def remove_donkey(self,game_state):
	game_state.layout[self.xdonkey][self.ydonkey]=' '

#  enables donkey to change its position
    def move_donkey(self,game_state,flag):
	_aa=randint(1,2)
	if _aa == 1:
	    if self.valid_move(self.x,self.y+1,game_state,flag):
		if self.y +1 < game_state.level[1]:
		    game_state.layout[self.x][self.y+1]='D'
		    game_state.layout[self.x][self.y]=' '
		    self.y=self.y+1
		    if self.y == game_state.s5:
			pass
		    else:
			game_state.layout[self.x][game_state.s5]='H'
	    else:
		_aa=2
	
	if _aa == 2:
	    if self.valid_move(self.x,self.y-1,game_state,flag):
		game_state.layout[self.x][self.y-1]='D'
		game_state.layout[self.x][self.y]=' '
		self.y=self.y-1
		if self.y == game_state.s5:
		    pass
		else:
		    game_state.layout[self.x][game_state.s5]='H'
	
class player(person):

    def __init__(self,game_state):
	x=24
	y=4
	self.won=0
	person.__init__(self,x,y)
	game_state.layout[x][y]='P'
	self.__choice=0


    def getposition(self):
	self.xplayer=self.x
	self.yplayer=self.y

# check if a coin is present on the current position 
    def checkcoin(self,xx,yy,game_state):
	if game_state.layout[xx][yy]=='C':
	    return True
	else:
	    return False

# collect the coin and update the spot with player position
    def collectcoin(self,game_state,x,y):
	if y in game_state.pos[x/4]:
		game_state.pos[x/4].remove(y)
	#	print "removed " + str(self.y)
	game_state.score=game_state.score+5
	game_state.layout[x][y]='P'

    def printcoin(self,game_state):
	for i in range(1,7):
		for j in game_state.pos[i]:
			print j,
		print "\n"

# print the score on the screen
    def printscore(self,game_state):
	print "Score: " + str(game_state.score)

# flag==0 indicates that the collision is being checked between player and fireball
    def checkcollision(self,x,y,game_state,flag):
	if flag==0:
		if game_state.layout[x][y]=='O' or game_state.layout[x][y]=='D':
			game_state.gameover=True
			return True
		else:
			return False
# flag indicates whether the movement corresponds to player or the fireball

# flag=1 : fireball
# flag=0 : player
    def move_left(self,key_in,game_state,Fireball,x,y,flag):
	if x%4==0:
	        if (x/4) % 2 == 0:
		        if self.valid_move(x,y-1,game_state,flag):
			    if y > game_state.level[(x)/4]:
			    	if self.valid_move(x,y,game_state,flag):
					if self.checkcoin(x ,y-1,game_state):
					    game_state.layout[x][y]=' '
					    y=y-1
					    if flag==0:
						self.collectcoin(game_state,x,y)
					    else:
						if x==24 and y==2:
							game_state.layout[x][y]=' '
						else:
							game_state.layout[x][y]='O'	
					else:
					   
					    game_state.layout[x][y]=' '
					    y=y-1
					    if flag==0:
						game_state.layout[x][y]='P'
					    else:
						if x==24 and y==2:
							game_state.layout[x][y]=' '
						else:
							game_state.layout[x][y]='O'						
				else:
					if flag==0:
						if ((self.x,self.y),1) in Fireball.fireballpos:
							game_state.gameover=True
						else:
							if self.checkcoin(x ,y-1,game_state):
								self.collectcoin(game_state,x,y)
							else:
								game_state.layout[x][y-1]='P'
							y=y-1
				
			    else:
				if (x)/4!=6:
				    if self.checkcoin(x+4 ,y-1,game_state):
					game_state.layout[x][y]=' '
					y=y-1
					x=x+4
					if flag==0:
				    		self.collectcoin(game_state,x,y)
				        else:
						if x==24 and y==2:
							game_state.layout[x][y]=' '
						else:
							game_state.layout[x][y]='O'	
							Fireball.d=randint(0,1)
				    else:
					game_state.layout[x][y]=' '
					y=y-1
					x=x+4
					if flag==0:
						game_state.layout[x][y]='P'
					else:
						game_state.layout[x][y]='O'
						Fireball.d=randint(0,1)
				else:
				    if self.checkcoin(x, y-1,game_state):
					game_state.layout[x][y]=' '
					y=y-1
					if flag==0:
				    		self.collectcoin(game_state,x,y)
				        else:
						if x==24 and y==2:
							game_state.layout[x][y]=' '
						else:
							game_state.layout[x][y]='O'	
				    else:
					game_state.layout[x][y]=' '
					y=y-1
					if flag==0:
						game_state.layout[x][y]='P'
					else:
						if x==24 and y==2:
							game_state.layout[x][y]=' '
						else:
							game_state.layout[x][y]='O'	

			    if y == game_state.place[(x)/4-1][1] or y == game_state.place[(x)/4-1][2]:
				pass
			    else:
				if x > 4:			
				    if game_state.s[(x)/4]==1:
					game_state.layout[x][game_state.place[(x)/4-1][1]]='H'
				    else:
					game_state.layout[x][game_state.place[(x)/4-1][1]]='H'
					game_state.layout[x][game_state.place[(x)/4-1][2]]='H'

			    if flag==1:
			    	if y in game_state.pos[x/4]:
					pass
			    	else:
					for var in game_state.pos[x/4]:
						game_state.layout[x][var]='C'
		        else:
			    	Fireball.d=0
		else:
			if self.valid_move(x,y-1,game_state,flag):
				if self.valid_move(x,y,game_state,flag):	
				    if self.checkcoin(x,y-1,game_state):
					game_state.layout[x][y]=' '
					y=y-1
					if flag==0:
						self.collectcoin(game_state,x,y)
					else:
						if x==24 and y==2:
							game_state.layout[x][y]=' '
						else:
							game_state.layout[x][y]='O'	
				    else:
					game_state.layout[x][y]=' '
					y=y-1
					if flag==0:
						game_state.layout[x][y]='P'
					else:
						if x==24 and y==2:
							game_state.layout[x][y]=' '
						else:
							game_state.layout[x][y]='O'	
				else:
					if flag==0:
						if ((self.x,self.y),1) in Fireball.fireballpos:
							game_state.gameover=True
						else:
							if self.checkcoin(x ,y-1,game_state):
								self.collectcoin(game_state,x,y)
							else:
								game_state.layout[x][y-1]='P'
							y=y-1
			else:		
			    Fireball.d=1

	
			if y == game_state.place[(x)/4-1][1] or y == game_state.place[(x)/4-1][2]:
			    pass
			else:
			    if self.x > 4:
				if game_state.s[(x)/4]==1:
				    game_state.layout[x][game_state.place[(x)/4-1][1]]='H'
				else:
				    game_state.layout[x][game_state.place[(x)/4-1][1]]='H'
				    game_state.layout[x][game_state.place[(x)/4-1][2]]='H'
	
			if y in game_state.pos[x/4]:
				pass
			else:
				if flag==0:
					for var in game_state.pos[x/4]:
						game_state.layout[x][var]='C'

		d=Fireball.d
	else:
		d=Fireball.d
    
	return (x,y,d)

    def move_right(self,key_in,game_state,Fireball,x,y,flag):
	if x%4==0:
		    if (x/4) % 2 == 1:
			if self.valid_move(x,y+1,game_state,flag):
			    if y < game_state.level[(x)/4]:
			    	if self.valid_move(x,y,game_state,flag):
					if self.checkcoin(x ,y+1,game_state):
					    game_state.layout[x][y]=' '
					    y=y+1
					    if flag==0:
						self.collectcoin(game_state,x,y)
					    else:
						if x==24 and y==2:
							game_state.layout[x][y]=' '
						else:
							game_state.layout[x][y]='O'	
					else:
			
					    game_state.layout[x][y]=' '
					    y=y+1
					    if flag==0:
						game_state.layout[x][y]='P'
					    else:
						if x==24 and y==2:
							game_state.layout[x][y]=' '
						else:
							game_state.layout[x][y]='O'						  
				else:
					if flag==0:
						if ((self.x,self.y),0) in Fireball.fireballpos:
							print "move_right 1"
							game_state.gameover=True
						else:
							if self.checkcoin(x ,y+1,game_state):
								self.collectcoin(game_state,x,y)
							else:
								game_state.layout[x][y+1]='P'
							y=y+1
						
			    else:
				if (x)/4!=6:
				    if self.checkcoin(x+4 ,y+1,game_state):
					game_state.layout[x][y]=' '
					y=y+1
					x=x+4
					if flag==0:
				    		self.collectcoin(game_state,x,y)
				        else:
						if x==24 and y==2:
							game_state.layout[x][y]=' '
						else:
							game_state.layout[x][y]='O'	
							Fireball.d=randint(0,1)
				    else:
					game_state.layout[x][y]=' '
					y=y+1
					x=x+4
					if flag==0:
						game_state.layout[x][y]='P'
					else:
						if x==24 and y==2:
							game_state.layout[x][y]=' '
						else:
							game_state.layout[x][y]='O'	
							Fireball.d=randint(0,1)
				else:
				    if self.checkcoin(x, y+1,game_state):
					game_state.layout[x][y]=' '
					y=y+1
					if flag==0:
				    		self.collectcoin(game_state,x,y)
				        else:
						if x==24 and y==2:
							game_state.layout[x][y]=' '
						else:
							game_state.layout[x][y]='O'	
				    else:
					game_state.layout[x][y]=' '
					y=y+1
					if flag==0:
						game_state.layout[x][y]='P'
					else:
						if x==24 and y==2:
							game_state.layout[x][y]=' '
						else:
							game_state.layout[x][y]='O'	

			    if y == game_state.place[(x)/4-1][1] or y == game_state.place[(x)/4-1][2]:
				pass
			    else:
				if x > 4:			
				    if game_state.s[(x)/4]==1:
					game_state.layout[x][game_state.place[(x)/4-1][1]]='H'
				    else:
					if game_state.place[x/4][1]!=0:
						game_state.layout[x][game_state.place[(x)/4-1][1]]='H'
					if game_state.place[x/4][2]!=0:
						game_state.layout[x][game_state.place[(x)/4-1][2]]='H'

			    if y in game_state.pos[x/4]:
				pass
			    else:
				for var in game_state.pos[x/4]:
					game_state.layout[x][var]='C'
		    else:
			if self.valid_move(x,y+1,game_state,flag):
				if self.valid_move(x,y,game_state,flag):
				    if self.checkcoin(x,y+1,game_state):
					game_state.layout[x][y]=' '
					y=y+1
					if flag==0:
						self.collectcoin(game_state,x,y)
					else:
						if x==24 and y==2:
							game_state.layout[x][y]=' '
						else:
							game_state.layout[x][y]='O'	
				    else:
					game_state.layout[x][y]=' '
					y=y+1
					if flag==0:
						game_state.layout[x][y]='P'
					else:
						if x==24 and y==2:
							game_state.layout[x][y]=' '
						else:
							game_state.layout[x][y]='O'	
				else:
					if flag==0:
						if ((self.x,self.y),0) in Fireball.fireballpos:
							print "move_right 1"
							game_state.gameover=True
						else:
							if self.checkcoin(x ,y+1,game_state):
								self.collectcoin(game_state,x,y)
							else:
								game_state.layout[x][y+1]='P'
							y=y+1
			else:
			    Fireball.d=0

	
			if y == game_state.place[(x)/4-1][1] or y == game_state.place[(x)/4-1][2]:
			    pass
			else:
			    if self.x > 4:
				if game_state.s[(x)/4]==1:
				    game_state.layout[x][game_state.place[(x)/4-1][1]]='H'
				else:
				    if game_state.place[x/4][1]!=0:
				    	game_state.layout[x][game_state.place[(x)/4-1][1]]='H'
				    if game_state.place[x/4-1][2]!=0:
				    	game_state.layout[x][game_state.place[(x)/4-1][2]]='H'
			if y in game_state.pos[x/4]:
				pass
			else:
				if flag==0:
					for var in game_state.pos[x/4]:
						game_state.layout[x][var]='C'
		   
		    d=Fireball.d
	else:
		d=Fireball.d
	return (x,y,d)

	
# moveplayer function allows player/fireball to move according to their specified directions 

    def move_player(self,key_in,game_state,Fireball,flag,Player,Donkey):	

	#	x=24
	#	y=3
		d=1
		if key_in == 'q':
	    		exit()
	
		if key_in != 'w' and key_in!= 's' and key_in!= ' ' and key_in!= 'h' and key_in!= 'g':
			if key_in == 'a' or Fireball.d==0 :
				if key_in=='a' and flag==0:
					self.__choice=0
					x=self.x
					y=self.y
					x,y,d=self.move_left(key_in,game_state,Fireball,x,y,0)
					self.x=x
					self.y=y
					Fireball.d=d
				if Fireball.d==0 and flag==1:
					x=Fireball.px
					y=Fireball.py
					if y == game_state.place[x/4][1] or y == game_state.place[(x)/4][2]:
						if game_state.layout[x+3][y]=='H':
							self.__choice=randint(0,1)
						else:
							self.__choice=0
						if self.__choice==0:
							x,y,d=self.move_left(key_in,game_state,Fireball,x,y,1)
					else:
						x,y,d=self.move_left(key_in,game_state,Fireball,x,y,1)
					Fireball.px=x
					Fireball.py=y
					Fireball.d=d
					
			
			
			if key_in == 'd' or Fireball.d==1:
				if key_in=='d' and flag==0:
					self.__choice=0
					x=self.x
					y=self.y
					x,y,d=self.move_right(key_in,game_state,Fireball,x,y,0)
					self.x=x
					self.y=y
					Fireball.d=d
				if Fireball.d==1 and flag==1:
					x=Fireball.px
					y=Fireball.py
					if y == game_state.place[x/4][1] or y == game_state.place[(x)/4][2]:
						if x%4==0:
							if game_state.layout[x+3][y]=='H':
								self.__choice=randint(0,1)
							else:
								self.__choice=0
						else:
							self.__choice=1
						if self.__choice==0:
							x,y,d=self.move_right(key_in,game_state,Fireball,x,y,1)
					else:
						x,y,d=self.move_right(key_in,game_state,Fireball,x,y,1)
					Fireball.px=x
					Fireball.py=y
					Fireball.d=d


		if key_in == 'w' and flag==0:
			self.__choice=0
			x=self.x
			y=self.y
			if x > 2:
				if x%4==0:
	    				if y == game_state.place[(x)/4-1][1] or y == game_state.place[(x)/4-1][2]:
						if game_state.layout[x-1][y]=='H':
		        				game_state.layout[x][y]='H'
		    					game_state.layout[x-1][y]='P'
		    					x=x-1

						elif self.checkcollision(x-1,y,game_state,0):
							game_state.layout[x-1][y]='H'
						else:
							print "moved normally"
							pass
				else:
					if y == game_state.place[(x)/4][1] or y == game_state.place[(x)/4][2]:
						if game_state.layout[x-1][y]=='H':
		        				game_state.layout[x][y]='H'
		    					game_state.layout[x-1][y]='P'
		    					x=x-1
					
						elif self.checkcollision(x-1,y,game_state,0):
							game_state.layout[x-1][y]='H'
					
						else:
							game_state.layout[x][y]='H'
							if self.checkcoin(x-1,y,game_state):
								x=x-1
								self.collectcoin(game_state,x,y)
							else:
								game_state.layout[x-1][y]='P'
								x=x-1	
										

			else:
				x=x-1
				game_state.layout[x][y]='P'
				game_state.layout[x+1][y]='H'	
				self.won=1	
			self.x=x
			self.y=y	

	
		if key_in == 's' or self.__choice==1 :
		#	print "entered s"
			self.__checkk=0
			if self.__choice==1 and flag==1:
				x=Fireball.px
				y=Fireball.py
			elif key_in == 's' and flag==0:
				x=self.x
				y=self.y
			else:
				self.__checkk=1
	#		if self.choice!=1 and flag==0:
	#			print x
	#			print y
                        if self.__checkk!=1:
                                if y == game_state.place[(x)/4][1] or y == game_state.place[(x)/4][2]:
                                # check for broken stairs
                                #	if game_state.layout[x+3][y]=='H':
                                                if game_state.layout[x+1][y]=='H':
                                                        if x%4==0:						
                                                                if y == game_state.place[(x)/4-1][1] or y == game_state.place[(x)/4-1][2]:
                                                                        game_state.layout[x][y]='H'
                                                                else:
                                                                        game_state.layout[x][y]=' '
                                                                if self.__choice==1 and flag==1:
                                                                        game_state.layout[x+1][y]='O'
                                                                else:
                                                                        game_state.layout[x+1][y]='P'
                                                        
                                                        else:
                                                                if game_state.layout[x+1][y]=='H':
                                                                        game_state.layout[x][y]='H'
                                                                        if self.__choice==1 and flag==1:
                                                                                game_state.layout[x+1][y]='O'
                                                                        else:
                                                                                game_state.layout[x+1][y]='P'
                                                elif game_state.layout[x+1][y]=='O' or game_state.layout[x+1][y]=='D':
                                                        if flag==0:
                                                                game_state.gameover=True
                                                elif game_state.layout[x+1][y]==' ':
                                                        if flag==1:
                                                                game_state.layout[x][y]='H'
                                                                del Fireball.fireballpos[Fireball.count]
                                                elif game_state.layout[x+1][y]=='P' and flag==1:
                                                        game_state.layout[x+1][y]='O'
                                                x=x+1		 

                                if flag==0:
                                        self.x=x
                                        self.y=y
                                elif flag==1:
                                        Fireball.px=x
                                        Fireball.py=y
                                        d=Fireball.d
                    

		if key_in == 'h' and flag==0:
			self.jump(game_state,Fireball,Player,Donkey,2)
			x=self.x
			y=self.y
			d=Fireball.d

		if key_in == 'g' and flag==0:
			self.jump(game_state,Fireball,Player,Donkey,0)
			x=self.x
			y=self.y
			d=Fireball.d
		if key_in == ' ' and flag==0:
			self.jump(game_state,Fireball,Player,Donkey,1)
			x=self.x
			y=self.y
			d=Fireball.d

		
		self.markk=0     		     	
		if key_in!='z' and key_in!='a'and  key_in!='s' and  key_in!='d' and  key_in!='g'and  key_in!='h' and  key_in!='w' and key_in!=' ':
			self.markk=1
			x=Donkey.xdonkey
			y=Donkey.ydinkey
		return (x,y,d)

# id=2 for right jump
# idd=2 jump right
# idd=1 jump on spot
# idd=0 jump left  


    def jump(self,game_state,Fireball,Player,Donkey,idd):
	# jump only allowed if player is on any of the layers not from stairs
	self.varr=2
	self.mark=0	
	self.varx=self.x
	while self.varr>0:
		Fireball.move_fireball(game_state,Player,Fireball,Donkey)
		if idd==2:
			self.__xx=self.x-1
			self.__yy=self.y+1
		elif idd==0:
			self.__xx=self.x-1
			self.__yy=self.y-1
		else:
			self.__xx=self.x-1
			self.__yy=self.y
		if self.valid_move(self.__xx,self.__yy,game_state,0):
			if game_state.layout[self.__xx][self.__yy]==" ":
				game_state.layout[self.x][self.y]=" "
				game_state.layout[self.__xx][self.__yy]="P"
				self.x=self.__xx
				self.y=self.__yy
				os.system("clear")
				game_state.trial()
				game_state.print_board()
				print "Enter move:"
				self.printscore(game_state)
				time.sleep(0.3)
			#	os.system("clear")
				self.varr=self.varr-1
			else:	
				self.mark=1
				if (self.x/4)*4 !=self.x:
					self.varx=(self.x/4)*4+4
				else:
					self.varx=self.x
				game_state.layout[self.x][self.y]=" "
				if self.checkcoin(self.varx,self.y,game_state):
					self.x=self.varx
					self.collectcoin(game_state,self.x,self.y)
				else:	
					game_state.layout[self.varx][self.y]="P"
					self.x=self.varx	
				break
		else:
			if game_state.layout[self.__xx][self.__yy]=="X":
				self.mark=1
				if (self.x/4)*4 !=self.x:
					self.varx=(self.x/4)*4+4
				else:
					self.varx=self.x
				game_state.layout[self.x][self.y]=" "
				if self.checkcoin(self.varx,self.y,game_state):
					self.x=self.varx
					self.collectcoin(game_state,self.x,self.y)
				else:	
					game_state.layout[self.varx][self.y]="P"
					self.x=self.varx	
			else:
				self.mark=1
				game_state.gameover=True
			break

	if self.mark!=1:
		self.varr=2
		while self.varr>0:
			Fireball.move_fireball(game_state,Player,Fireball,Donkey)
			if idd==2:
				self.__xx=self.x+1
				self.__yy=self.y+1
			elif idd==0:
				self.__xx=self.x+1
				self.__yy=self.y-1
			else:
				self.__xx=self.x+1
				self.__yy=self.y
			if self.valid_move(self.__xx,self.__yy,game_state,0) or game_state.layout[self.__xx][self.__yy]=='C':
				if game_state.layout[self.__xx][self.__yy]==" ":
					game_state.layout[self.x][self.y]=" "
					game_state.layout[self.__xx][self.__yy]="P"
					self.x=self.__xx
					self.y=self.__yy
					self.__yes=0
					if self.x%4==0 and self.x/4 % 2==1 and self.x!=24 and idd==2:
						#if idd==2:
						if self.y >= game_state.level[self.x/4]:
							self.__yes=1
						#elif idd==0:
					elif self.x%4==0 and self.x/4 % 2==0 and self.x!=24 and idd==0:
						if self.y< game_state.level[self.x/4]:
							self.__yes=1
						#	self.x=self.x+4
					if self.__yes==1:
						if self.valid_move(self.x+4,self.y,game_state,0):
							game_state.layout[self.x][self.y]=" "
							if self.checkcoin(self.x,self.y,game_state):
								self.collectcoin(game_state,self.x,self.y)
							else:
								game_state.layout[self.x+4][self.y]="P"
						elif game_state.layout[self.x+4][self.y]=='O' or game_state.layout[self.x+4][self.y]=='D':
							game_state.layout[self.x][self.y]=' '					
							game_state.gameover=True
						self.x=self.x+4
					os.system("clear")
					game_state.trial()
					game_state.print_board()
					print "Enter move:"
					self.printscore(game_state)
					time.sleep(0.3)
					os.system("clear")
					self.varr=self.varr-1
				else:	
					self.mark=1
					if (self.x/4)*4 !=self.x:
						self.varx=(self.x/4)*4+4
					else:
						self.varx=self.x
					game_state.layout[self.x][self.y]=" "
					if self.checkcoin(self.varx,self.y,game_state):
						self.x=self.varx
						self.collectcoin(game_state,self.x,self.y)
					else:	
						game_state.layout[self.varx][self.y]="P"
						self.x=self.varx	
					break
			else:
				if game_state.layout[self.__xx][self.__yy]=="X":
					self.mark=1
					if (self.x/4)*4 !=self.x:
						self.varx=(self.x/4)*4+4
					else:
						self.varx=self.x
					game_state.layout[self.x][self.y]=" "
					if self.checkcoin(self.varx,self.y,game_state):
						self.x=self.varx
						self.collectcoin(game_state,self.x,self.y)
					else:	
						game_state.layout[self.varx][self.y]="P"
						self.x=self.varx	
				else:
					game_state.gameover=True
				break
	
def main():
	validlist=['a','d','w','s',' ','q']
	game_state=board1.game()
#	a player can play a game thrice i.e. player has three lives
	lives=3
	levell=1
	freq=10
	os.system("clear")
	while lives>0 :
		freq=freq-2
		print "level" + " " + str(levell)
		Donkey=donkey(game_state)
		Donkey.donkeypos(game_state)
		game_state.remove_coins()
		game_state.regenerate_board()
		game_state.generate_coins()
		Player=player(game_state)
		Fireball=fireball1.fireball(game_state)
		count=0
		game_state.trial()
		game_state.checkpl()
		game_state.print_board()
		# continue the game untill the player dies or the player wins
#		generate a new fireball after every 11 moves
		while game_state.gameover==False and Player.won!=1:
	    		if count%freq==0:
				Fireball.generate_fireball(game_state,Player,Donkey)
	    		print "Enter Move: "
	    		key_input=read_in.getchar()
	    		count=count+1
	    		Donkey.move_donkey(game_state,1)
	    		Fireball.move_fireball(game_state,Player,Fireball,Donkey)
			ff=0
			if key_input in validlist:
				if key_input==" ":
					print "Enter Move:"
					key_input=read_in.getchar()
					if key_input=='a':
						key_input='g'
					elif key_input=='d':
						key_input='h'
					else:
						ff=1
				if ff!=1:
					x,y,d=Player.move_player(key_input,game_state,Fireball,0,Player,Donkey)
			os.system("clear")
			game_state.trial()
	    		game_state.print_board()
	    		Player.printscore(game_state)
			Player.getposition()
# if the player dies anf he/she has lives left , then restart the game with same layout but different position of fireballs and donkey and coins
# also player gets penalised by 25 points
		if game_state.gameover==True:
			game_state.layout[Donkey.xdonkey][Donkey.ydonkey]=' '
			Player.getposition()
			game_state.layout[Player.xplayer][Player.yplayer]=' '
			Fireball.remove_fireball(game_state,Player,Fireball)
			
			os.system("clear")
			game_state.cyan("Try Again")
			lives=lives-1
			game_state.score=game_state.score-25
			Donkey.remove_donkey(game_state)
			game_state.gameover=False
# if the player wins then regenerate the game with a new layout representing a new level 
		if Player.won==1:
			os.system("clear")
			game_state.cyan("Queen Rescued")
			game_state.yellow("New Game")
		#	os.system("clear")
			game_state=board1.game()
			levell=levell+1
	if lives==0:
		os.system("clear")
		game_state.red("GAME OVER")
		Player.printscore(game_state)
	    
if __name__=="__main__":
	main()
#	p1=threading.Thread(target=main_func)
#	p1.start()
#	p2=threading.Thread(target=Donkey.donkey_movement)
#	p2.start()