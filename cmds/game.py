from email import message
from unicodedata import name
import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json

with open('playerdata.json','r',encoding='utf8') as jfile:
    playerdata = json.load(jfile)



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
            playerdata[f"player{playercount}"] = {'ID':'','balance':''}#建立新player data
            cpdata = playerdata[f"player{playercount}"]
            cpdata["ID"] = self.player[:-5]
            cpdata["balance"] = 100
            with open('playerdata.json','w',encoding='utf8') as jfile:
                json.dump(playerdata, jfile,indent=4)
            await ctx.send(f"{self.player[:-5]} ,歡迎加入遊戲")
        else:
            await ctx.send(f"{self.player[:-5]} ,你已經在遊戲中了")








async def setup(bot):
    await bot.add_cog(Game(bot))