import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json,asyncio,datetime

class Task(Cog_Extension):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.counter = 0

        async def time_task():
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(1025052102063554580)
            while not self.bot.is_closed():
                current_time = datetime.datetime.now().strftime('%H%M')
                with open('setting.json','r',encoding='utf8') as jfile:
                    jdata = json.load(jfile)
                if current_time == jdata['time'] and self.counter == 0:
                    await self.channel.send('time task is running')
                    await asyncio.sleep(1)
                    self.counter = 1
                else:
                    await asyncio.sleep(1)
                    pass
        self.bg_task = self.bot.loop.create_task(time_task())


    @commands.command()
    async def settime(self, ctx, time):
        with open('setting.json','r',encoding='utf8') as jfile:
            jdata = json.load(jfile)
        jdata['time'] = time
        with open('setting.json','w',encoding='utf8') as jfile:
            json.dump(jdata,jfile,indent=4)
        self.counter = 0
        await ctx.send(f'set "time" as {time}')





async def setup(bot):
    await bot.add_cog(Task(bot))