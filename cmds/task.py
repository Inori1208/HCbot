import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json,asyncio,datetime

class Task(Cog_Extension):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.counter1 = 0
        self.counter2 = 0
#可設定時間提供回應
        async def time_task():
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(1025052102063554580)
            while not self.bot.is_closed():
                current_time = datetime.datetime.now().strftime('%H%M')
                with open('setting.json','r',encoding='utf8') as jfile:
                    jdata = json.load(jfile)
                if current_time == jdata['time'] and self.counter1 == 0:
                    await self.channel.send('諸君早安，今天又是新的一天呢。')
                    await asyncio.sleep(1)
                    self.counter1 = 1
                else:
                    await asyncio.sleep(1)
                    pass
        self.bg_task = self.bot.loop.create_task(time_task()) 
#學測倒數
        async def exam_task():
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(1033618860663918632)

            while not self.bot.is_closed():
                current_time = datetime.datetime.now().strftime('%H%M%S')
                current_year = datetime.datetime.now().strftime('%Y')
                current_month = datetime.datetime.now().strftime('%m')
                current_day = datetime.datetime.now().strftime('%d')
                
                with open('setting.json','r',encoding='utf8') as jfile:
                    jdata = json.load(jfile)
                exam1_day = jdata['exam1']
                d1 = datetime.date(int(current_year),int(current_month),int(current_day))
                #print(d1)
                d2 = datetime.date(exam1_day['year'],exam1_day['month'],exam1_day['day'])
                #print(d2)
                d_days = d2 - d1
                jdata['d_days'] = d_days.days
                with open('setting.json','w',encoding='utf8') as jfile:
                    json.dump(jdata,jfile,indent=4)
                #print(d_days.days)

                if current_time == '000001' and self.counter2 == 0:
                    await self.channel.send(f'注意!距離學測只剩下{d_days.days}天!')
                    await asyncio.sleep(1)
                    self.counter2 = 1
                else:
                    await asyncio.sleep(1)
                    self.counter2 = 0
                    pass
        self.bg_task = self.bot.loop.create_task(exam_task())
#設定時間指令
    @commands.command()
    async def settime(self, ctx, time):
        with open('setting.json','r',encoding='utf8') as jfile:
            jdata = json.load(jfile)
        jdata['time'] = time
        with open('setting.json','w',encoding='utf8') as jfile:
            json.dump(jdata,jfile,indent=4)
        self.counter1 = 0
        await ctx.send(f'set "time" as {time}')






async def setup(bot):
    await bot.add_cog(Task(bot))