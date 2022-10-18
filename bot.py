import discord
import os
from discord.ext import commands
import json
import asyncio

with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='&',intents=intents)

#Start

@bot.event
async def on_ready():
    print('>> {0.user} 已成功載入。 <<'.format(bot))

#load 

@bot.command()
async def load(ctx,extension):
    await bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'{extension} is loaded.')

#unload

@bot.command()
async def unload(ctx,extension):
    await bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'{extension} is unloaded.')

#reload

@bot.command()
async def reload(ctx,extension):
    await bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'{extension} is reloaded.')

#search file in cmds

async def load_extensions():
    for filename in os.listdir('./cmds'):
        print(filename)
        if filename.endswith('.py'):
            await bot.load_extension(f'cmds.{filename[:-3]}')

if __name__ == "__main__":
    async def main():
        async with bot:
            await load_extensions()
            await bot.start(jdata['TOKEN'])

    asyncio.run(main())