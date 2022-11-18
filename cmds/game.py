from unicodedata import name
import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import asyncio

with open('HC_RPG\\playerdata.json','r',encoding='utf8') as jfile:
    playerdata = json.load(jfile)
with open('HC_RPG\\itemdata.json','r',encoding='utf8') as jfile:
    itemdata = json.load(jfile)
with open('HC_RPG\\bossdata.json','r',encoding='utf8') as jfile:
    bossdata = json.load(jfile)

def check(player):#確認玩家是否在遊戲中,並取得該玩家總資料
    cplayer = list(playerdata["players"])
    if player in cplayer:
        cp_num = cplayer.index(f'{player}') + 1
        cp_data = playerdata[f"player{cp_num}"]#該玩家總資料
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
        self.player = str(ctx.author)
        cplayer = list(playerdata["players"])
        if self.player in cplayer:
            await bp(ctx,cplayer,'others')
        else:
            await ctx.send(f"{self.player[:-5]}你不在遊戲內")
            await ctx.send("使用指令&signup加入遊戲吧！")


    @hc.command()
    async def thinking(self,ctx):
        msg = await ctx.send("思考ing")
        for i in range(3):
            for c in range(1,4):
                await asyncio.sleep(.5)
                msg = await msg.edit(content="思考ing"+c*".")
            await asyncio.sleep(.5)
            msg = await msg.edit(content="思考ing")
        await msg.delete()

    @hc.command()
    async def boss(self,ctx,ID):
        self.player = str(ctx.author)
        if check(self.player) == 0:
            await ctx.send(f"{self.player[:-5]}你不在遊戲內")
            await ctx.send("使用指令&signup加入遊戲吧！")
        else:
            cp_data = check(self.player)
            bossname = bossdata[f'{ID}']['Name']
            bosslevel = bossdata[f'{ID}']['LVL']
            bosshealth = bossdata[f'{ID}']['Health']
            bossatk = bossdata[f'{ID}']['ATK']
            bosspic = discord.File(f"{bossdata[f'{ID}']['pic']}")
            msg = await ctx.send(f"**{bossname}[Lv {bosslevel}]**\n血量:[■■■■■■■■■■■■■■■■■■■■]({bosshealth}/{bosshealth})",file=bosspic)
            await asyncio.sleep(1)
            round_msg = await ctx.send(f"現在是{ctx.author.mention}的回合\n血量:[■■■■■■■■■■■■■■■■■■■■](20/20)")
            await battle(ctx,cp_data,msg,self.bot)

#攻擊函式     
async def startatk(msg,user,cp_data):
    await asyncio.sleep(1)
    #print(msg)
    await msg.clear_reactions()#clear反應
    print(f"{user}成功發動攻擊")#print該玩家發動攻擊的訊息(確認用)
    #print(cp_data)
    cweapon_atk = itemdata[f"{cp_data['items']['weapon']['item_id']}"]["atk"]
    print(cweapon_atk)

#背包函式
async def bp(ctx,cplayer,type):
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
async def battle(ctx,cp_data,msg,bot): 
    
    cplayer = list(playerdata["players"])
            
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
            await ctx.send("測試成功")
            await startatk(msg,ctx.author,cp_data)
            break
        if str(reaction) == '📂':
            await ctx.send('測試成功3')
            msg2 = await ctx.send(await bp(ctx,cplayer,"others"))
            await asyncio.sleep(60)
            await msg.clear_reactions()
            await msg2.delete()
            break
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=c)
        except asyncio.TimeoutError:
            await ctx.send("測試成功2")
            await msg.clear_reactions()
            break

    
                    




async def setup(bot):
    await bot.add_cog(Game(bot))