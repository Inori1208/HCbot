import discord
import os
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='&',intents=intents)
test_channel = bot.get_channel(1025052102063554580)

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




bot.run('MTAyODY4OTEyNDA5NTQzNDc1Mg.G4zOyC.chsO03Opgpfihs-B0S4O4KvqyOeuGSahQ7VTto')