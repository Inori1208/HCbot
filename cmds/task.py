import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json,asyncio,datetime

class Task(Cog_Extension):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.counter1 = 10
        self.counter2 = 0
        allowed_mentions = discord.AllowedMentions(users = True,everyone = True)
#可設定時間提供回應 + 跨年倒數:)
        async def time_task():
            await self.bot.wait_until_ready()
            self.channel1 = self.bot.get_channel(1025052102063554580)
            while not self.bot.is_closed():
                current_time = datetime.datetime.now().strftime('%H%M%S')
                with open('setting.json','r',encoding='utf8') as jfile:
                    jdata = json.load(jfile)
                if current_time == jdata['time']:
                    while self.counter1 != 0:
                        await self.channel1.send(f'{self.counter1}')
                        await asyncio.sleep(0.8)
                        self.counter1 -= 1
                    await self.channel1.send('@everyone 厚詮機器人在此祝各位新年快樂！｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡',allowed_mentions = allowed_mentions)
                else:
                    await asyncio.sleep(1)
                    pass
        self.bg_task = self.bot.loop.create_task(time_task()) 
#學測倒數
        async def exam_task():
            await self.bot.wait_until_ready()
            self.channel2 = self.bot.get_channel(1033618860663918632)

            while not self.bot.is_closed():
                current_time = datetime.datetime.now().strftime('%H%M%S')
                current_year = datetime.datetime.now().strftime('%Y')
                current_month = datetime.datetime.now().strftime('%m')
                current_day = datetime.datetime.now().strftime('%d')
                
                with open('setting.json','r',encoding='utf8') as jfile:
                    jdata = json.load(jfile)
                exam2_day = jdata['exam2']
                d1 = datetime.date(int(current_year),int(current_month),int(current_day))
                #print(d1)
                d2 = datetime.date(exam2_day['year'],exam2_day['month'],exam2_day['day'])
                #print(d2)
                d_days = d2 - d1
                jdata['d_days'] = d_days.days
                with open('setting.json','w',encoding='utf8') as jfile:
                    json.dump(jdata,jfile,indent=4)
                #print(d_days.days)
                
                
                if current_time == '000001' and self.counter2 == 0 and d_days.days == 1:
                    await self.channel2.send(content =f'@everyone 注意!明天就要分科了!',allowed_mentions = allowed_mentions)
                    await asyncio.sleep(1)
                    self.counter2 = 1
                elif current_time == '000001' and self.counter2 == 0 and d_days.days == 0:
                    await self.channel2.send(content =f'@everyone 注意!今天就要分科了!\n厚詮機器人在此祝各位考試順利。',allowed_mentions = allowed_mentions)
                    await asyncio.sleep(1)
                    self.counter2 = 1
                elif current_time == '000001' and self.counter2 == 0 and d_days.days > 1:
                    await self.channel2.send(f'注意!距離分科測驗只剩下{d_days.days}天!')
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
        #self.counter1 = 0
        await ctx.send(f'set "time" as {time}')






async def setup(bot):
    await bot.add_cog(Task(bot))