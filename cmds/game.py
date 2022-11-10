from unicodedata import name
import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json

with open('HC_RPG\playerdata.json','r',encoding='utf8') as jfile:
    playerdata = json.load(jfile)
with open('HC_RPG\itemdata.json','r',encoding='utf8') as jfile:
    itemdata = json.load(jfile)



class Game(Cog_Extension):

    @commands.command()
    async def signup(self,ctx):

        self.player = str(ctx.author)
        cplayers = list(playerdata["players"])
        playercount = len(cplayers)
        if self.player not in cplayers:
            cplayers.append(self.player)
            #print(cplayers)
            playerdata["players"] = cplayers
            playercount += 1
            #print(playercount)

            #建立新player data
            playerdata[f"player{playercount}"] = {
                'ID':f'{self.player[:-5]}',
                'balance':100,
                'LVL':1,
                'items':{
                        'weapon':1,
                        'axe':2,
                        'pickaxe':3,
                        'other':{}
                        }
                }
            
            with open('playerdata.json','w',encoding='utf8') as jfile:
                json.dump(playerdata, jfile,indent=4)
            await ctx.send(f"{self.player[:-5]} ,歡迎加入遊戲")
        else:
            await ctx.send(f"{self.player[:-5]} ,你已經在遊戲中了")

    @commands.command()
    async def backpack(self,ctx):
        self.player = str(ctx.author)
        cplayer = list(playerdata["players"])
        if self.player in cplayer:
            cp_num = cplayer.index(f'{self.player}') + 1 #玩家編號
            cp_data = playerdata[f"player{cp_num}"] #取得玩家總資料
            bp = dict(cp_data["items"]) #取得玩家背包資料
            #print(bp)

            cweapon = itemdata[f"{bp['weapon']}"]
            caxe = itemdata[f"{bp['axe']}"]
            cpickaxe = itemdata[f"{bp['pickaxe']}"]

            #print(cweapon,caxe,cpickaxe)
            await ctx.send(f"{self.player[:-5]} 您現在擁有:\n{cweapon}\n{caxe}\n{cpickaxe}")
        else:
            await ctx.send(f"{self.player[:-5]}你不在遊戲內")
            await ctx.send("使用指令&signup加入遊戲吧！")

            

    







async def setup(bot):
    await bot.add_cog(Game(bot))