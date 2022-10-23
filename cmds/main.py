import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json

class Main(Cog_Extension):
    
    @commands.command()
    async def aireu(self,ctx):
        await ctx.send(f'WYSI')

    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} ms')

    @commands.command()
    async def 學測(self,ctx):
        with open('setting.json','r',encoding='utf8') as jfile:
            jdata = json.load(jfile)
        d = jdata['d_days']
        await ctx.send(f'距離學測還有{d}天')


async def setup(bot):
    await bot.add_cog(Main(bot))