
try:import pygame
except Exception:pass
import Twitchrq as rq
streamerid=""
try:pygame.init()
except Exception:print("pygame missing")
def playsfx(path,vol=1):
 try:
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.play()
 except Exception:pass
def follow(follower):
    msg("Thank you for following "+follower)
    playsfx("followersfx.wav",0.3)
def msg(m):
	Json={"broadcaster_id":streamerid,"sender_id":streamerid,"message":"[BOT] "+m}
		
	rq.post("chat/messages", rq.usertoken,json=Json) 