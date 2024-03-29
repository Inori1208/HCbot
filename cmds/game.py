from unicodedata import name
import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import asyncio
import random
import string

with open('HC_RPG\\playerdata.json','r',encoding='utf8') as jfile:
    playerdata = json.load(jfile)
with open('HC_RPG\\itemdata.json','r',encoding='utf8') as jfile:
    itemdata = json.load(jfile)
with open('HC_RPG\\bossdata.json','r',encoding='utf8') as jfile:
    bossdata = json.load(jfile)
with open('HC_RPG\\rpg_setting.json','r',encoding='utf8') as jfile:
    rpgset = json.load(jfile)

def check(player):#確認玩家是否在遊戲中,並取得該玩家總資料
    print(player)
    cplayer = list(playerdata["players"])
    print(cplayer)
    if f'{player}' in cplayer:
        cp_num = cplayer.index(f'{player}') + 1
        cp_data = playerdata[f"player{cp_num}"]#該玩家總資料
        print("yes")
        return(cp_data)
    else:
        return 0 


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

            #建立新player data
            playerdata[f"player{playercount}"] = {
                'ID':f'{self.player[:-5]}',
                'balance':100,
                'LVL':1,
                'health':20,
                'items':{
                        'weapon':{
                            'item_id':1,
                            'count':1
                            },
                        'axe':{
                            'item_id':2,
                            'count':1
                        },
                        'pickaxe':{
                            'item_id':3,
                            'count':1
                        },
                        'other':{
                            
                        }
                        }
                }
            
            with open('HC_RPG\\playerdata.json','w',encoding='utf8') as jfile:
                json.dump(playerdata, jfile,indent=4)
            await ctx.send(f"{self.player[:-5]} ,歡迎加入遊戲")
        else:
            await ctx.send(f"{self.player[:-5]} ,你已經在遊戲中了")

    @commands.group()
    async def hc(self,ctx):
        pass

    @hc.command()
    async def backpack(self,ctx):
        #print('test')
        self.player = str(ctx.author)
        cplayer = list(playerdata["players"])
        if self.player in cplayer:
            #print('test2')
            await bp(ctx,cplayer,'all')
        else:
            await ctx.send(f"{self.player[:-5]}你不在遊戲內")
            await ctx.send("使用指令&signup加入遊戲吧！")


    @hc.command()
    async def thinking(self,ctx):
        thinkmsg = await ctx.send("思考ing")
        for i in range(3):
            for c in range(1,4):
                await asyncio.sleep(.5)
                thinkmsg = await thinkmsg.edit(content="思考ing"+c*".")
            await asyncio.sleep(.5)
            thinkmsg = await thinkmsg.edit(content="思考ing")
        await thinkmsg.delete()

    @hc.command()
    async def mine(self,ctx):
        print('1')
        print(ctx.author)
        cp_data = check(ctx.author)
        print(cp_data)
        cap = itemdata[f"{cp_data['items']['pickaxe']['item_id']}"]["collect_rate"]
        print(cap)
        #中間計算採集量
        quan = cap
        cother = dict(cp_data['items']['other'])
        print(cother)
        for i in cother:
            if cother[f'{i}']['item_id'] == 5:
                cother[f'{i}']['count'] += quan
                break
            elif i == f'slot{len(cother)-1}':
                print(len(cother))
                cp_data['items']['other'][f'slot{len(cother)}'] ={
                    "item_id": 5,
                    "count": quan
                }
                break
        print(cp_data)
        with open('HC_RPG\\playerdata.json','w',encoding='utf8') as jfile:
                    json.dump(playerdata, jfile,indent=4)
        await ctx.send('測試成功')

    @hc.command()
    async def boss(self,ctx,ID):
        self.player = str(ctx.author)
        if check(self.player) == 0:
            await ctx.send(f"{self.player[:-5]}你不在遊戲內")
            await ctx.send("使用指令&signup加入遊戲吧！")
        else:
            cp_data = check(self.player)
            #boss資料
            bossname = bossdata[f'{ID}']['Name']
            bosslevel = bossdata[f'{ID}']['LVL']
            bosshealth = bossdata[f'{ID}']['Health']
            bossatk = bossdata[f'{ID}']['ATK']
            bosspic = discord.File(f"{bossdata[f'{ID}']['pic']}")
            #玩家資料
            phealth = cp_data['health']
            plevel = cp_data['LVL']
            #發送
            msg = await ctx.send(f"**{bossname}[Lv {bosslevel}]**\n血量:[■■■■■■■■■■■■■■■■■■■■]({bosshealth}/{bosshealth})",file=bosspic)
            ch = msg.channel
            await asyncio.sleep(1)
            round_msg = await ctx.send(f"現在是{ctx.author.mention}的回合\n血量:[■■■■■■■■■■■■■■■■■■■■]({phealth}/{phealth})")
            #給予初始值
            round = "p"
            x = 0
            bnowhealth = bosshealth
            pnowhealth = phealth
            #print(round)
            while bnowhealth > 0 and pnowhealth > 0:#沒有人死掉->執行
                #print('test2')
                while pnowhealth > 0 and round == "p":
                    #print('test1')
                    bnowhealth = await battle(ctx,cp_data,msg,self.bot,bnowhealth)
                    print(bnowhealth)
                    round = "b"
                    #print(round)
                    Boss_Health_point = await HEALTH_POINT(bosshealth,bnowhealth)
                    Player_Health_point = await HEALTH_POINT(phealth,pnowhealth)
                    await asyncio.sleep(1)
                    #print(msg)
                    msg = await msg.edit(content = f"**{bossname}[Lv {bosslevel}]**\n血量:[{Boss_Health_point}]({bnowhealth}/{bosshealth})")
                    await asyncio.sleep(1)
                    round_msg = await round_msg.edit(content = f"現在是**{bossname}**的回合\n玩家血量:[{Player_Health_point}]({pnowhealth}/{phealth})")
                    break
                while bnowhealth > 0 and round == "b":
                    round = "p"
                    await asyncio.sleep(1)
                    Boss_Health_point = await HEALTH_POINT(bosshealth,bnowhealth)
                    msg = await msg.edit(content = f"**{bossname}[Lv {bosslevel}]**\n血量:[{Boss_Health_point}]({bnowhealth}/{bosshealth})")
                    await asyncio.sleep(1)
                    await ctx.send('boss會打架惹\n而且一次打五下(´・ω・`)')
                    await asyncio.sleep(1)
                    for i in range(5):
                        alphabet = random.choice(list(string.ascii_letters))
                        await ctx.send(f'請在 **5** 秒內打出 "{alphabet}"')
                        x = await listen(ctx,f'{alphabet}',self.bot,x,'ATK')
                        await asyncio.sleep(1)
                    await ctx.send(f'倍率為{x}')
                    pnowhealth -= bossatk/5000*x
                    x=0
                    await asyncio.sleep(1)
                    await ch.purge(limit = 2)
                    await asyncio.sleep(1)
                    Player_Health_point = await HEALTH_POINT(phealth,pnowhealth)
                    round_msg = await round_msg.edit(content = f"現在是{ctx.author.mention}的回合\n玩家血量:[{Player_Health_point}]({pnowhealth}/{phealth})")
                    break
            print('戰鬥結束')
            await msg.delete()
            if bnowhealth<=0:
                round_msg = await round_msg.edit(content = f"{ctx.author.mention} 你打敗了 **{bossname}** !")
            else:
                round_msg = await round_msg.edit(content = f"{ctx.author.mention} 你死了:3") 

#攻擊函式     
async def startatk(msg,user,cp_data,bnowhealth):
    await asyncio.sleep(1)
    #print(msg)
    await msg.clear_reactions()#clear反應
    print(f"{user}成功發動攻擊")#print該玩家發動攻擊的訊息(確認用)
    #print(cp_data)
    cweapon_atk = int(itemdata[f"{cp_data['items']['weapon']['item_id']}"]["atk"])
    print(cweapon_atk*1000)
    print(bnowhealth)
    bnowhealth -= cweapon_atk*1000
    print(bnowhealth)
    return(bnowhealth)


#背包函式
async def bp(ctx,cplayer,type:str):
    cp_num = cplayer.index(f'{ctx.author}') + 1 #玩家編號
    cp_data = playerdata[f"player{cp_num}"] #取得玩家總資料
    bp = dict(cp_data["items"]) #取得玩家背包資料
    #print(bp)

    cweapon = itemdata[f"{bp['weapon']['item_id']}"]['name']
    caxe = itemdata[f"{bp['axe']['item_id']}"]['name']
    cpickaxe = itemdata[f"{bp['pickaxe']['item_id']}"]['name']

    cother = dict(bp['other'])
    other_items={}
            
    #print(cother)
    for i in cother:
        id=cother[f'{i}']['item_id']
        itemname=itemdata[f'{id}']['name']
        count=cother[f'{i}']['count']
        #print(id)
        #print(count)
        other_items[f'{itemname}'] = count
    #print(other_items)

    #print(cweapon,caxe,cpickaxe)
    load = f"{str(ctx.author)[:-5]} 您的背包:\n\n所持武器: {cweapon}\n所持斧頭: {caxe}\n所持十字鎬: {cpickaxe}\n"
    #print(load)
    unload=[]
    for i in other_items:
        unload.append(f"{i} x {other_items[i]}")
    unload='\n'.join(unload)
    #print(unload)
    if type == "all":
        await ctx.send(f'```\n{load}\n{unload}\n```')
    if type == "others":
        things = f'```{str(ctx.author)[:-5]} 您所持有的物品有:\n{unload}```'
        return(things)

#戰鬥函式(我的回合)
async def battle(ctx,cp_data,msg,bot,bnowhealth): 
    
    cplayer = list(playerdata["players"])
    #print('test')
    await msg.add_reaction('⚔️')
    await asyncio.sleep(1)
    await msg.add_reaction('📂')

    #偵測反應作者是否為boss戰玩家
    def c(reaction,user):
            return user == ctx.author

    reaction = None
    user = None
    #偵測玩家添加反應
    while True:
                
        if str(reaction) == '⚔️':
            #await ctx.send("測試成功")
            b_health = await startatk(msg,ctx.author,cp_data,bnowhealth)
            return(b_health)
        if str(reaction) == '📂':
            #await ctx.send('測試成功3')
            msg2 = await ctx.send(await bp(ctx,cplayer,"others"))
            await asyncio.sleep(5)
            await msg.clear_reactions()
            await msg2.delete()
            return(bnowhealth)
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=c)
        except asyncio.TimeoutError:
            await ctx.send("測試成功2")
            await msg.clear_reactions()
            break

#擷取玩家對話
async def listen(ctx,word:str,bot,count,mode:str):
    #print('test2')
    print(word)
    def c(msg):
        return msg.channel == ctx.channel and msg.author == ctx.author
    while  True:
        #print('test3')
        try:
            #print('test')
            m = await bot.wait_for('message',timeout = 5.0,check=c)
            print(m)
        except asyncio.TimeoutError:
            #await ctx.send("測試成功")
            await ctx.channel.purge(limit = 1)
            count += 1
            return(count)
        if m.content == f'{word}' and mode == 'ATK':
            print('test1')
            await ctx.channel.purge(limit = 2)
            return(count)
        #print('test5')
        if m.content != f'{word}' and mode == 'ATK':
            await ctx.channel.purge(limit = 2)
            count += 1
            return(count)
        #print('test4')

#寫出血量
async def HEALTH_POINT(health,nowhealth):
    standard_point = health/20
    block = round(nowhealth/standard_point)
    Health_point = rpgset[f'HP_{block}']
    if block < 1 and block > 0:
        Health_point = str(rpgset['HP_1'])
    elif block <= 0:
        Health_point = str(rpgset['HP_0'])
    return(Health_point)

async def setup(bot):
    await bot.add_cog(Game(bot))