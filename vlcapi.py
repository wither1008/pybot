import requests
import json
# VLC HTTP interface URL
VLC_URL = 'http://localhost:8080/'

# Optional: If you set a password for the HTTP interface
USERNAME = ''
PASSWORD = 'm125gamedev'

def send_command(command):
    response = requests.get(VLC_URL + command, auth=(USERNAME, PASSWORD))
    return response.text


def status():
    status = json.loads(send_command('requests/status.json') )
    return status