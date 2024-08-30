import sys
import time


currentscene=""
previousscene=""



sys.path.append('../')
from obswebsocket import obsws,requests  # noqa: E402

host = "localhost"
port = 4455
password = open("obspass").readline().removesuffix("\n")

try:ws = obsws(host, port, password)
except Exception:print("OBS NOT RUNNING")

def switchscene(name:str):
 try:
     ws.connect()
     ws.call(requests.SetCurrentProgramScene(sceneName=name))
     global currentscene
     global previousscene
     previousscene=currentscene
     currentscene=name
     ws.disconnect()
 except Exception:pass
def undoswitchscene():
    switchscene(previousscene)
def settext(textname,content):
 try:
     ws.connect()
     ws.call(requests.SetInputSettings(inputName=textname,inputSettings={"text":content}))
     ws.disconnect()
 except Exception:pass


