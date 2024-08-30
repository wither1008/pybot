import getmusic
import obs
import asyncio
import time
obs.settext("MArtist","")
obs.settext("MTitle","")
try:
    while True:
        
        artist,title=getmusic.get_media_info()
        print("music",artist,title)
        
        if artist!="" or title !="":
            obs.settext("MArtist",artist)
            obs.settext("MTitle",title)
        time.sleep(5)
except Exception as e:
    obs.settext("MArtist","Vlc is not running")
    obs.settext("MTitle","Music display stopped")