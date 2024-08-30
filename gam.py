def game():
while life>0 and life<6:
	print("Hátralévő életrek száma:"+str(life))
	kerdesnum=input("Add meg a kérdés  számát! []")
	if (int(kerdesnum)==1):
		inp=input("Add meg a kérdéssel kapcsolatos számot! Kérdésed száma:"+kerdesnum+"[]")
		if (i>int(inp)):
			print("A gondolt szám nagyobb mint:"+inp)
			life-=1
		else:
			print(a)
		life-=1
	elif(int(kerdesnum)==2):
		inp=input("Add meg a kérdéssel kapcsolatos számot! Kérdésed száma:"+kerdesnum+"[]")
		if(i<int(inp)):
			print("A gondolt szám kissebb mint:"+inp)
			life-=1
		else:
			print(a)
		life-=1
	elif(int(kerdesnum)==3):
		inp=input("Add meg a kérdéssel kapcsolatos számot! Kérdésed száma:"+kerdesnum+"[]")
		if(i==int(inp)):
			print("Nyertél!")
			life=0
		else:
			print("Vesztettél!")
			life=0
	else:
		print("You are sztupid!")
		life-=1