import requests as r
cli=open("cli").readline().removesuffix("\n")
clis=open("cli_secret").readline().removesuffix("\n")
print(r.post("https://id.twitch.tv/oauth2/token",params={"client_id":cli,"client_secret":clis,"grant_type":"client_credentials"}).content)