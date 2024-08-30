oauth=open("oauth.txt").readline()
cli=open("cli.txt").readline()
print(oauth," ",cli)
import requests

def post(req):
    requests.post('https://api.twitch.tv/helix/'+req,headers={"Authorization":oauth,'Client-Id':cli,'Content-Type':'application/json'})
def get(req,param):

    return requests.get('https://api.twitch.tv/helix/'+req,headers={"Authorization":oauth,'Client-Id':cli,'Content-Type':'application/json'},params=param).content
print(get("users",{"login":"m125gamedev"}))