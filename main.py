import discord
import os
from discord.ext import commands
import json

with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='&',intents=intents)

#Start

@bot.event
async def on_ready():
    print('>> {0.user} 已成功載入。 <<'.format(bot))

#Commands

@bot.command()
async def aireu(ctx):
    await ctx.send(f'WYSI')
@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)} ms')




bot.run(jdata['TOKEN'])