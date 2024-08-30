from random import randint
class player:
	def __init__(self,name) -> None:
		self.hp=100
		self.name=name
		self.dodge=4
class battle:
	def __init__(self,player1,player2,endcallback) -> None:
		self.players=[player(player1),player(player2)]
		self.round=0
		self.queue=0
		self.end=endcallback
	
	def Round(self):
		currentplayer=self.currentplayer()
		currentplayer.hp-=self.queue
		
		self.queue=0
		self.round+=1
		if self.round>=len(self.players):
			self.round=0
		if currentplayer.hp<=0:
			self.end(self,self.currentplayer())
		
	def currentplayer(self):
		return self.players[self.round]
	
	
	def attack(self,player,num):
		num=int(num)
		if player==self.currentplayer().name:
			attacknum=randint(0,50)
			damage=14-abs(attacknum-num)
			print(attacknum,num)
			if damage<0:damage=0
			if damage==14:
				damage=25
			self.Round()
			self.queue=damage*2
			return damage
		return -1
	def dodge(self,player):
		if player==self.currentplayer().name:
			currentplayer= self.currentplayer()
			
			if currentplayer.dodge>0:
				self.queue=0
				currentplayer.dodge-=1
				self.Round()
				return currentplayer.dodge
		self.Round()
		return -1
			
	

	