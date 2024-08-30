import requests
apptoken=open("apptoken").readline().removesuffix("\n")
usertoken=open("usertoken").readline().removesuffix("\n")
cli=open("cli").readline().removesuffix("\n")
#head={"Authorization":"Bearer "+token,"Client-id":cli,
#"Content_type":"application/json"}

params={"login":"m125gamedev"}
def get(url,token,params):
    head={"Authorization":"Bearer "+token,"Client-id":cli,
        "Content_type":"application/json"}
    return requests.get("https://api.twitch.tv/helix/"+url,headers=head,params=params).content


def post(url,token,params={}, json={} ):
    head={"Authorization":"Bearer "+token,"Client-id":cli,
        "Content_type":"application/json"}
    return requests.post("https://api.twitch.tv/helix/"+url,headers=head,params=params, json=json).content