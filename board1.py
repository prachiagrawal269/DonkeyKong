import random
import layout
from random import randint
## the main layout of the game

class game():

    def __init__(self):
	self.generate_board()
	self.generate_layers()
	self.generate_stairs()
#	self.generate_coins()	
	self.gameover=False	
	self.score=0
#	self.coin=[randint(4,5) for i in range(1,8)]
	self.pos=[[] for j in range(7)]

# the game board is a netsed list(layout)
    def generate_board(self):
	self.layout=[[" " for x in range(50)] for y in range(26)]

# generates random numbers(limits) for the y coordinates of different layers for the game according to specific constraints	
# level is a list containing the limiting y coordinates of  different layers
# 'l' and 'r' are left and right y coordinates of the top most layer(the one on which queen resides)
    def generate_layers(self):	
	self.level=[0 for i in range(7)]
	self.level[2]=randint(20,30)
	self.level[1]=randint(self.level[2]+4,40)
	self.level[3]=randint(self.level[2]+4,40)
	self.level[4]=randint(10,self.level[3]-6)
	self.level[5]=randint(self.level[4]+2,40)
	self._l=randint(2,self.level[1]/2)
	self._r=randint(self._l+4,self.level[1])
	self._q=(self._l+self._r)/2

	''' stairs '''
# s is the list that stores the frequency of stairs on each layer ,The frequency at ranges between 1 and 2
	self.s=[randint(1,2) for i in range(1,10)]
	self.s5=randint(self._l+1,self._r-2)

# generating walls and queen 
	self.layout[1][self._l]='X'
	self.layout[1][self._r-1]='X'
	self.layout[1][self._q]='Q'
	for i in range(self._l,self._r):
		self.layout[2][i]='X'
	for i in range(50):
		self.layout[0][i]='X'
	for i in range(self.level[1]):
		self.layout[5][i]='X'
	for i in range(self.level[2],50):
		self.layout[9][i]='X'
	for i in range(self.level[3]):
		self.layout[13][i]='X'
	for i in range(self.level[4],50):
		self.layout[17][i]='X'
	for i in range(self.level[5]):
		self.layout[21][i]='X'
	for i in range(50):
		self.layout[25][i]='X'
	for i in range(50):
		self.layout[25][i]='X'
	for i in range(26):
		self.layout[i][0]='X'
	for i in range(26):
		self.layout[i][49]='X'
	for i in range(2,6):
		self.layout[i][self.s5]='H'
	self.level[0]=2
	self.level[6]=2
	self.place=[[0 for i in range(4)] for j in range(7)]
	self.place[0][1]=self.s5
	self.place[0][2]=0

# place is again a nested list that stores the y cordinates of the stairs for each layer 
# e.g. place[1][2] stores the y coordinate of the second stairs on the first floor
	
	for i in range(1,6):
		num=self.s[i]
		for t in range(1,num+1):
			self.place[i][t]=randint(min(self.level[i],self.level[i+1]),max(self.level[i],self.level[i+1])-2) 
 
# random stairs generation, priviledge for broken stairs
# ran is local variable
# ran=1 implies broken stairs  
    def generate_stairs(self):
	for i in range(1,6):
	    num=i+1
	    for k in range(1,self.s[i]+1):
		for j in range((4*num)-3,(4*num)+1):
		    if k == 1 :
			ran=1
		    else:
			if j%4==3:
			    ran=randint(0,1)
			else:
			    ran=1
		    if ran==1:
			self.layout[j][self.place[i][k]]='H'

	
	''' coins '''

# pos is a nested list storing y cordinated of points where the coins are located
# e.g. pos[2] stores all y coordinates for the layer #2 where coins are located 
    def generate_coins(self):
	self.coin=[randint(5,6) for i in range(1,8)]
#	self.pos=[[0 for i in range(90)] for j in range(7)]
	for i in range(1,7):
		coins=self.coin[i]
		for j in range(1,coins+1):
			if i%2==0:	
				self.__rr=randint(self.level[i],48)
				if self.__rr not in self.pos[i]:
					self.pos[i].append(self.__rr)
			else:
				self.__rr=randint(1,self.level[i]-1)
				if self.__rr not in self.pos[i]:
					self.pos[i].append(self.__rr)
			if self.layout[4*i][self.__rr]!='H':
				self.layout[4*i][self.__rr]='C'
			else:
				self.pos[i].remove(self.__rr)

# removes the coins from the board
# function is called at the restart of a new game or a new level 
    def remove_coins(self):
	for i in range(1,7):
		for j in self.pos[i]:
			self.layout[4*i][j]=' '
		self.pos[i]=[]

    def red(self,name):
	print("\033[91m {}\033[00m".format(name))

    def yellow(self,name):	
	print("\033[93m {}\033[00m".format(name))
		
    def cyan(self,name):	
	print("\033[96m {}\033[00m".format(name))

    def regenerate_board(self):
	for i in range(26):
		for j in range(50):
			if i%4==1 and i!=1:
					if j==self.place[i/4][1] or j==self.place[i/4][2]:
						self.layout[i][j]='H'
					
    def trial(self):
	for __f in range(26):
		self.layout[__f][0]='X'

    def checkpl(self):
		for i in range(26):
			for j in range(50):
				if i!=24 and j !=4:
					if self.layout[i][j]=='P':
						self.layout[i][j]=' '
				if i%4!=0 and i>4:
					if j==self.place[i/4][1] or j==self.place[i/4][2]:
						if self.layout[i][j]=='O':
							self.layout[i][j]='H'
				
				elif i>1:
					if j==self.s5:
						if self.layout[i][j]=='O':
							self.layout[i][j]='H'

    def print_board(self):
		for i in range(26):
			for j in range(50):
				if(self.layout[i][j]=='H'):
					print ('\033[1m'+'\033[93m' + 'H' + '\033[0m'),
				elif(self.layout[i][j]=='P'):
					print ('\033[1m'+'\033[95m' + 'P' + '\033[0m'),
				elif(self.layout[i][j]=='D'):
					print ('\033[1m'+'\033[95m' + 'D' + '\033[0m'),
				elif(self.layout[i][j]=='C'):
					print ('\033[1m'+'\033[92m' + 'C' + '\033[0m'),
				elif(self.layout[i][j]=='X'):
					print ('\033[1m'+'\033[96m' + 'X' + '\033[0m'),
				elif(self.layout[i][j]=='O'):
					print ('\033[1m'+'\033[91m' + 'O' + '\033[0m'),
				else:	
					print self.layout[i][j],
			print ""
 		

#L1=l1()



