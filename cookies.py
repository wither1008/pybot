from pathlib import Path
import json
shop=json.load(open("shop.json"))

mix=json.load(open("recipes.json"))
edible=json.load(open("edible.json"))
drinkable=json.load(open("drinkable.json"))
info=json.load(open("info.json"))
recipes_per_page=5

def player_exists(name):
    my_file = Path("players/"+name+".json")
    return my_file.is_file()
def read_player(name):
    return json.load(open("players/"+name+".json"))
def saveplayer(name,data):
    json.dump(data,open("players/"+name+".json","w"))
def update():
    global shop,mix,edible,drinkable,info
    shop=json.load(open("shop.json"))
    mix=json.load(open("recipes.json"))
    edible=json.load(open("edible.json"))
    drinkable=json.load(open("drinkable.json"))
    info=json.load(open("info.json"))
class Player:
    def __init__(self,name) -> None:
        self.name=name
        if player_exists(name):
            result=read_player(name)
            self.money=result["money"]
            self.items=result["items"]
        else:
            self.money=0
            self.items=[]
        
    def save(self):
        saveplayer(self.name,{
            "money":self.money,
            "items":self.items
        })
    def shop(self,item=""):
        update()
        if item=="":
            text="Now in shop: "
            for e in shop:
                text+=e+": "+str(shop[e])+", "
            text=text.rstrip(", ")
            return text
        else:
            if item in shop and self.money>=shop[item]:
                self.money-=shop[item]
                self.items.append(item)
                return self.name+" bought "+item
            return self.name+" doesnt afford this very expensive thingy"
    def mix(self,item1,item2):
        update()
        for e in mix:
            if e==(item1+"+"+item2) or e==(item2+"+"+item1):
                if item1 in self.items and item2 in self.items:
                    self.items.remove(item1)
                    self.items.remove(item2)
                    self.items.append(mix[e])
                    return mix[e]
        return ""
    def bake(self,item):
        update()
        for e in mix:
            if e==("bake+"+item):
                if item in self.items:
                    self.items.remove(item)
                    self.items.append(mix[e])
                    return mix[e]
        return ""
    def heat(self,item):
        update()
        for e in mix:
            if e==("heat+"+item):
                if item in self.items:
                    self.items.remove(item)
                    self.items.append(mix[e])
                    return mix[e]
        return ""
    def water(self,item):
        update()
        for e in mix:
            if e==("water+"+item):
                if item in self.items:
                    self.items.remove(item)
                    self.items.append(mix[e])
                    return mix[e]
        return ""
    def recipes(self,page="0"):
        update()
        print(mix)
        text="Recipes (page "+page+"): "
        try:
            int(page)
        except:
            return "That's not a number"
        page=(1+int(page))*recipes_per_page
        minpage=page-recipes_per_page
        if page>=len(mix):
            page=len(mix)
        if minpage<0:
            minpage=0
        counter=0
        for e in mix:
            if counter>=minpage and counter<page:
                text+=e+"= "+str(mix[e])+",    "
        text=text.rstrip(", ")
        return text
    def eat(self,item):
        update()
        if item in self.items:
            if item in edible:
                self.items.remove(item)
                return self.name+" ate a(n) "+item
            else:
                return self.name+"tried to eat "+item+" but failed ._."
        else:
            return self.name+" doesnt have "+item
    def drink(self,item):
        update()
        if item in self.items:
            if item in drinkable:
                self.items.remove(item)
                return self.name+" drank a(n) "+item
            else:
                return self.name+"tried to drink "+item+" but failed ._."
        else:
            return self.name+" doesnt have "+item
    def info(self,item):
        update()
        if item in info:
            return info[item]
        return "idk anything about that item"