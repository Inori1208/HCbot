import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import datetime

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

    @commands.command()
    async def cat(self,ctx):
        with open('setting.json','r',encoding='utf8') as jfile:
            jdata = json.load(jfile)
            vid = jdata['catvideo']
        await ctx.send(vid)

    @commands.command()
    async def 重要日期(self,ctx,page:int=0):
        if page == 0 or page == 1:
            embed=discord.Embed(title='重要日期', description='目前有列出的重要日期', color=0xb8f7ff, timestamp=datetime.datetime.now())
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/772807504798810123.webp?size=96&quality=lossless')
            embed.add_field(name='學測', value='**2023/1/13~15**', inline=True)
            embed.add_field(name='分科測驗', value='**2023/7/12~13**', inline=True)
            embed.add_field(name='◆', value='◇', inline=True)
            embed.add_field(name='學測成績公布', value='2023/2/23', inline=True)
            embed.add_field(name='分科成績公布', value='2023/7/28', inline=True)
            embed.add_field(name='◆', value='◇', inline=True)
            embed.add_field(name='第二次期中考', value='2022/11/28~30', inline=True)
            embed.add_field(name='第四次模擬考', value='2022/12/6~7', inline=True)
            embed.add_field(name='◆', value='◇', inline=True)
            await ctx.send(embed=embed)
        elif page == 2 :
            embed=discord.Embed(title='重要日期', description='目前有列出的重要日期', color=0xb8f7ff, timestamp=datetime.datetime.now())
            embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/772807504798810123.webp?size=96&quality=lossless')
            embed.add_field(name='test1', value='1', inline=True)
            embed.add_field(name='test2', value='2', inline=True)
            embed.add_field(name='◆', value='◇', inline=True)
            embed.add_field(name='test3', value='3', inline=True)
            embed.add_field(name='test4', value='4', inline=True)
            embed.add_field(name='◆', value='◇', inline=True)
            embed.add_field(name='test5', value='5', inline=True)
            embed.add_field(name='test6', value='6', inline=True)
            embed.add_field(name='◆', value='◇', inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send('page not found.')


async def setup(bot):
    await bot.add_cog(Main(bot))