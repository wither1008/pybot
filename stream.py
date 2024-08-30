import sys
import time

import logging

logging.basicConfig(level=logging.DEBUG)

sys.path.append('../')
from obswebsocket import obsws, events,requests  # noqa: E402

host = "localhost"
port = 4455
password = "fpGrSXIXFTg3PGvv"


def on_event(message):
	print("Got message: {}".format(message))


def on_switch(message):
	print("You changed the scene to {}".format(message.getSceneName()))


ws = obsws(host, port, password)
ws.register(on_event)
ws.register(on_switch, events.SwitchScenes)
ws.register(on_switch, events.CurrentProgramSceneChanged)
ws.connect()

try:
	while True:
		print("OK")
		time.sleep(10)
		print("END")

except KeyboardInterrupt:
	pass
def switchscene():
	try:
		scenes = ws.call(requests.GetSceneList())
		for s in scenes.getScenes():
			name = s['sceneName']
			print("Switching to {}".format(name))
			ws.call(requests.SetCurrentProgramScene(sceneName=name))
			time.sleep(2)

		print("End of list")
	except Exception:
		print("nyah")
ws.disconnect()