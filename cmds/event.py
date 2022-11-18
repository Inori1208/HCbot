import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json

with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Event(Cog_Extension):

    @commands.Cog.listener()
    async def on_message(self,msg):
        GoodNight_kws = ["早安","午安","晚安"]
        if msg.content in GoodNight_kws and msg.author != self.bot.user:
            await msg.channel.send('晚安')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,rdata):
        print(rdata.emoji)
        print(rdata.member)


async def setup(bot):
    await bot.add_cog(Event(bot))