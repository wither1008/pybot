id=open("cli").readline()
uri=open("url").readline()
scope=open("scope").read()
print(scope,"\n\n")
scop=scope.split(":")
realscope=scop[0]

for e in range(1,len(scop)):
	realscope=realscope+"%3A"+scop[e]
scop=realscope.split("\n")

completescope=scop[0]
for e in range(1,len(scop)):
	completescope=completescope+"%20"+scop[e]
print("https://id.twitch.tv/oauth2/authorize?response_type=token&client_id="+id+"&redirect_uri="+uri+"&scope="+completescope)