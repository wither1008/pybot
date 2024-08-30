import asyncio
import websockets
import requests
import Twitchrq as rq
import json
import obs
import time
import battle
import functions as func
from functions import msg
from random import randrange
import cookies
#from datetime import timedelta
streamername="langosdev"
obs.settext("theme","")
can_stream_screen=input("can stream screen (press enter if no,press any button then enter if yes)> ")
if can_stream_screen!="":
	can_stream_screen=True
else:
	can_stream_screen=False
theme=input("theme:")
print(can_stream_screen)
id=""
streamerid=""
running=True
#file=open("oauth.txt")

battles=[]
endedbattle=None
hydrotime=0
randommessagetime=time.time()+60*15
randommessage=["Join on my discord server here : https://discord.gg/yUdgv3kEfD","If you like what you see or wanna keep me entertained follow me(dont reach 50 so no ads)","use !commands for.. well i guess u should know","there are commands made for controlling my stream, you can use them as well","the game i am making right now is up on itch: https://m125.itch.io/duck"]
players=[]
	


async def handle_event(event):
	event=json.loads(event)
	type=event["metadata"]["message_type"]
	if type=="session_welcome":
		global id
		id=event["payload"]["session"]["id"]
		global streamerid
		streamerid=json.loads(rq.get("users",rq.usertoken,{}))["data"][0]["id"]
		func.streamerid=streamerid
		postsub()
		print(msg("bot connected"))
	elif type=="notification":
		match event["metadata"]["subscription_type"]:
			case "channel.chat.message":
				text=event["payload"]["event"]["message"]["text"]
				name=event["payload"]["event"]["chatter_user_login"]
				message(text,name)
			case "channel.follow":
				print(event)
				follower=event["payload"]["event"]["user_login"]
				func.follow(follower)
	global randommessagetime
	global randommessage
	if randommessagetime<time.time():
		randommessagetime=time.time()+60*15
		msg(randommessage[randrange(0,len(randommessage))])
		save_nomsg()

async def connect_to_websocket():
	obs.settext("battlestatus","no battles happened yet")
	async with websockets.connect('wss://eventsub.wss.twitch.tv/ws') as websocket:
		global running
		while running:
			event = await websocket.recv()
			await handle_event(event)
		msg("bot stopped")

def save():
	for e in players:
		e.save()
		msg("saving "+e.name+"'s coins&items")
		time.sleep(0.5)
def save_nomsg():
	for e in players:
		e.save()
		msg("saving "+e.name+"'s coins&items")
		time.sleep(0.5)

def battleend(batl,player:battle.player):
	msg(player.name+" won the battle with "+str(player.hp)+" hp")
	battles.remove(batl)
	global endedbattle
	endedbattle=batl
	obs.settext("winner",player.name)
	obs.settext("battlestatus","last winner: \n"+player.name)
	obs.switchscene("win")
	time.sleep(4)
	obs.undoswitchscene()

def player_in_list(name):
	for e in players:
		if e.name==name:
			return True
	return False
def getplayer(name):
	for e in players:
		if e.name==name:
			return e
	return False

def getparam(text,param=0):
	params=text.split(" ")
	params.append("")
	return params[param+1]

def message(text,name):#triggers on message in chat to reward active people in chat :)
	#i want guys to be in chat XD
	global battles
	global players
	
	if player_in_list(name):
		getplayer(name).money+=1
	else:
		players.append(cookies.Player(name))
		if name!=streamername:
			msg("Welcome to the stream "+name)

	match text.split(" ")[0].lower():
		#case "!2137":
			#time.
		case "!commands":
			msg("!hydrate,!code,!unity,!godot,!screen,!roll,!battle player:{!attack 0-50,!dodge},!kitchen,!duck")
		case "!screen":
			if can_stream_screen:
				obs.switchscene("whole screen")
				msg("Showing whole screen")
			else:
				msg("sorry but screen is disabled for this chatbot session")
		case "!unity":
			obs.switchscene("unitysetup")
			msg("Switching to Unity")
		case "!duck":
			obs.switchscene("duck")
			msg("Switching to Duck")
		case "!code":
			obs.switchscene("codesetup")
			msg("Switching to VSC")
		case "!godot":
			obs.switchscene("godotsetup")
			msg("Switching to Godot")
		case "!stop":
			if name==streamername:
				global running
				running=False
				msg("stopping bot")
				save()
			else:
				msg("sorry u cant dothis")
		case "!roll":
			obs.switchscene("chefroll")
			time.sleep(2)
			obs.undoswitchscene()
		case "!hydrate":
			global hydrotime
			if abs(hydrotime-time.time())>15*60:
				func.playsfx("notif.wav")
				hydrotime=time.time()
			else:
				msg("hydrated already")
		case "!battle":
			try:
				opponent=json.loads(rq.get("users",rq.usertoken,{"login":text.split(" ")[1]}))["data"]
				if opponent!=[]:
					msg(opponent[0]["login"]+" is being challanged by "+name)
					global battle
					battles.append(battle.battle(name,opponent[0]["login"],battleend))
					obs.switchscene("battle")
					
					obs.settext("player1",name)
					obs.settext("player2",opponent[0]["login"])
					obs.settext("battlestatus","current battle:\n"+name+" vs "+opponent[0]["login"])
					time.sleep(4)
					obs.undoswitchscene()
				else:
					msg("idk who do u want to challange >:(")
			except Exception as e:
				print(str(e))
				msg("u wanna battle the spacebar?? He's much stronget then u so dont try it")
		case "!attack":
			Battle=None
			
			for b in battles:
				for p in b.players:
					if p.name==name:
						Battle=b
						break
				if Battle!=None:break
			try:
				if Battle.queue!=0:msg(name+" has been damaged by "+str(Battle.queue)+" hp, and now has "+str(Battle.currentplayer().hp-Battle.queue)+" hp")
				dmg=Battle.attack(name,text.split(" ")[1])
				msg(name+" attacked")
				if dmg==-1:
					msg("it's not ur turn "+name)
				elif dmg==0:
					msg(name+" missed their attack")
				print(dmg)
			except Exception as e:
				
				try:
					for p in endedbattle.players:
						if p.name==name:
							Battle=endedbattle
					if Battle==endedbattle:
						msg(name+" lost")
						endedbattle=None
					else:
						msg("to attack join a battle with !battle")
						msg("and guess a number between 0-50 with !attack num")
				except Exception as e:
					msg("to attack join a battle with !battle")
					msg("and guess a number between 0-50 with !attack num")
					print(e)
		case "!dodge":
			
			Battle=None
			for b in battles:
				for p in b.players:
					print(p.name,name)
					if p.name==name:
						Battle=b
						break
				if Battle!=None:break
			try:
				dmg=Battle.queue
				dodgenum=Battle.dodge(name)
				if dodgenum!=-1:
					msg(name+" has dodged "+str(dmg)+" hp damage")
					msg(str(dodgenum)+" dodges left")
				else:
					msg(str("not ur turn"))
			except Exception as e:
				msg(str(e)+"to dodge join a battle with !battle")
		case "hi":
			msg("HI :D")
		case "!shop":
			if getparam(text)=="":
				msg(getplayer(name).shop())
			else:
				msg(getplayer(name).shop(getparam(text)))
		case "!money":
			msg(name+" has "+str(getplayer(name).money)+" money")
		case "!mix":
			res=getplayer(name).mix(getparam(text,0),getparam(text,1))
			if res!="":
				msg(name+" made "+res)
			else:
				msg(name+"! YOU CANT MIX THESE")
		case "!water":
			res=getplayer(name).water(getparam(text,0))
			if res!="":
				msg(name+" made "+res)
			else:
				msg(name+"! YOU CANT ADD WATER TO THIS")
		case "!heat":
			res=getplayer(name).heat(getparam(text,0))
			if res!="":
				msg(name+" made "+res)
			else:
				msg(name+"! YOU CANT HEAT THIS")
		case "!bake":
			res=getplayer(name).bake(getparam(text,0))
			if res!="":
				msg(name+" made "+res)
			else:
				msg(name+"! YOU CANT BAKE THIS")
		case "!items":
			if len(getplayer(name).items)>0:
				res=getplayer(name).items[0]
				for e in range(1,len(getplayer(name).items)):
					res+=", "+getplayer(name).items[e]
				msg(name+" has "+res)
			else:
				msg(name+" has nothing")
		case "!recipes":
			if getparam(text)=="":
				msg(getplayer(name).recipes())
			else:
				msg(getplayer(name).recipes(getparam(text)))
		case "!eat":
				msg(getplayer(name).eat(getparam(text)))
		case "!drink":
			msg(getplayer(name).drink(getparam(text)))
		case "!info":
			msg(getparam(text)+" info: "+getplayer(name).info(getparam(text)))
		case "!kitchen":
			msg("kitchen commands: !shop !mix [item1] [item2] {!water !heat !bake, !eat, !drink, !info}[item], !items, !money, !recipes[page]")
		case "!lurk":
			msg("have a good lurk "+name)
		case _:
			if not name==streamername:
				func.playsfx("chatsfx.wav",1)
			if text.startswith("!"):
				msg("WHAAT?!?! (try looking at !commands)")
	print(name," ",text)




def postsub():
	transport={
					"method": "websocket",
					"session_id": id
				}
	chat={
				"type": "channel.chat.message",
				"version": "1",
				"transport": transport ,
				"condition": {
					"broadcaster_user_id": streamerid,
					"user_id":streamerid
				}
				  }
	follows={
				"type": "channel.follow",
				"version": "2",
				"transport": transport ,
				"condition": {
					"broadcaster_user_id": streamerid,
					"moderator_user_id":streamerid
				}
				  }


	print(requests.post('https://api.twitch.tv/helix/eventsub/subscriptions',headers={"Authorization":"Bearer "+rq.usertoken,'Client-Id':"9vu3648pml3szlaw91abtxikchwgnz",'Content-Type':'application/json'},
				json=chat).content)
	print(rq.post("eventsub/subscriptions",rq.usertoken,json=follows))
if __name__ == '__main__':
	try:
		obs.settext("theme",theme)
		asyncio.get_event_loop().run_until_complete(connect_to_websocket())
	except KeyboardInterrupt:
		save()
	except websockets.exceptions.ConnectionClosedError:
		save()
