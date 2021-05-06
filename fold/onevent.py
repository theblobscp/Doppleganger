import discord
from discord.colour import Color, Colour
from discord.ext import commands, tasks
from PIL import Image, ImageDraw,ImageFont,ImageChops
from io import BytesIO
import random
import os
import asyncio
from discord.ext.commands.core import command
from discord.utils import get
from chatterbot.trainers import ChatterBotCorpusTrainer,ListTrainer
from chatterbot import ChatBot
from bot import colors


chatbot = ChatBot("DoppleGanger")
listtrainer = ListTrainer(chatbot)
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english.greetings", 
              "chatterbot.corpus.english.conversations" )


with open("train.txt",'r',encoding="utf-8") as train:
    training = train.read().splitlines()

def circle(pfp,size = (220,220)):
    
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


invite = ["discord.gg","discord.com/invite"]
trainid = 21345654324
randomitem = [':soccer:',':boomerang:',':yo_yo:',':badminton:',':lacrosse:',':roller_skate:',':musical_keyboard:',':video_game:',':dart:',':jigsaw:',':violin:',':microphone:',':trophy:',':video_camera:',':film_frames:',':fire_extinguisher:',':syringe:',':magic_wand:',':pill:',':sewing_needle:']
prefixes = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',  '*', '(', ')','&','`',"!",'-','~',"+"]
roles = {"Commoners":400,"Gamer":400,"Anime Weeb":400,"Superior Coder":600,"Mods":400,"Partners":200,"Owner":1000}

def revert(time):
    if time <= 86000 and time >3600:
        hrs = time//3600
        mins = (time%3600)/60
        return f"{int(hrs)} hr(s) {int(mins)} min(s)"
    elif time <= 3600 and time >60:
        times = time//60
        secs = (time%60)
        secs = str(secs)[:2]
        times = f"{int(times)} min(s) {secs} sec(s)"
        return times
    elif time<=60:
        return f"Only {int(time)} sec(s) Left !"
class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def train_data(self):
        data = await self.client.pg_con.fetchrow("SELECT train FROM users WHERE userid = $1",trainid)
        if data is None:
            return []
        return data[0]

    async def append(self,string):
        data = await self.client.pg_con.fetchrow("SELECT train FROM users WHERE userid = $1",trainid)
        if data is None:
            data = []
        else:
            data = data[0]
        data.append(string)
        await self.client.pg_con.execute("UPDATE users SET train = $1 WHERE userid = $2",data,trainid)
    
    async def check_guilds(self):
        columns = await self.client.pg_con.fetch("SELECT guildid FROM guild")
        guilds = []
        if columns is None:
            pass
        else:
            for i in columns:
                guilds.append(i[0])


        for i in self.client.guilds:
            if i.id not in guilds:
                await self.client.pg_con.execute("INSERT INTO guild (guildid,prefix) VALUES ($1,$2)", i.id,".")


    async def starting(self):
        await self.client.pg_con.execute("CREATE TABLE IF NOT EXISTS users (userid BIGINT NOT NULL, credits BIGINT , train TEXT[],inventory TEXT[],bg TEXT[])")
        await self.client.pg_con.execute("CREATE TABLE IF NOT EXISTS guild (guildid BIGINT NOT NULL, prefix TEXT , mainchannel BIGINT,suggestionchannel BIGINT,aichannel BIGINT,logchannel BIGINT)")
        

    async def add(self,id,amount = 2000):
        user = await self.client.pg_con.fetchrow("SELECT * FROM users WHERE userid = $1",id)
        await self.client.pg_con.execute("UPDATE users SET credits = $1 WHERE userid = $2",user[1]+amount,id)

    async def get(self,id):
        user = await self.client.pg_con.fetchrow("SELECT * FROM users WHERE userid = $1",id)
        return user[1]

    async def check(self,id):
        user = await self.client.pg_con.fetch("SELECT * FROM users WHERE userid = $1",id)
        if not user:
            await self.client.pg_con.execute("INSERT INTO users (userid, credits,bg) VALUES ($1,$2,$3)",id,2000,['default'])

    
    async def plus(self,id,name):
        data = await self.client.pg_con.fetchrow("SELECT inventory FROM users WHERE userid = $1",id)
        data = list(data[0])
        data.insert(0,name)
        await self.client.pg_con.execute("UPDATE users SET inventory = $1 WHERE userid = $2 ",data,id)

    
    async def available(self,id):
        urls = await self.client.pg_con.fetchrow("SELECT bg FROM users WHERE userid = $1",id)
        return urls[0]

    
    async def update(self,id,List):
        await self.client.pg_con.execute("UPDATE users SET bg = $1 WHERE userid = $2",List,id)

    
    async def createlist (self):
        data = await self.client.pg_con.fetch("SELECT train FROM users WHERE userid = $1",trainid)
        if not data:
            await self.client.pg_con.execute("INSERT INTO users (userid, train) VALUES ($1,$2)",trainid,training)

    @commands.Cog.listener()
    async def on_ready(self):  
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Yall with Smartness Overloaded ^-^"))   
        print("Here bot Comes :)")
        await self.starting()
        await self.createlist()
        await self.check_guilds()
        listtrainer.train(await self.train_data())
        await self.interest.start()

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        columns = await self.client.pg_con.fetch("SELECT guildid FROM guild")
        guilds=[]
        if columns==None:
            pass
        else:
            for i in columns:
                guilds.append(i)
        if guild.id not in guilds:
            await self.client.pg_con.execute("INSERT INTO guild (guildid,prefix) VALUES ($1,$2)", guild.id,".")

        prefix = await self.client.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",guild.id)
        prefix = prefix[0]
        for channel in guild.channels:
            if str(channel.type) == "text":
                if "general" in channel.name or "main" in channel.name:
                    await channel.send(f"Hi I am DoppleGanger :wave:\nThanks for Adding me Into {guild.name}. My Bot Prefix is `{prefix}` (Change it anytime By `{prefix}setprefix`) :partying_face: \nEnjoy Economy, Moderation, Welcome, Logs and many other such Commands :star_struck:\nType `{prefix}help` For more info\n\n-Code Stacks")
                    await self.client.pg_con.execute("UPDATE guild SET mainchannel = $1 WHERE guildid = $2",channel.id,guild.id)
                    break
        await guild.create_role(name = "Muted",colour = 0xFF0C00)
        muted = get(guild.roles, name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(muted, send_messages = False) 


    @tasks.loop(seconds=3600*10)   
    async def interest(self):
        members = self.client.get_all_members()
        for i in members:
            id = i.id
            try:
                
                
                member = get(channel.guild.members , id = id)
                if member.guild.id == 779743464774434857:
                    total=100
                else:
                    total= 500
                await self.check(id)
                for role in member.roles: 
                    if role.name in roles.keys():
                        total += roles[role.name]
                await self.add(id,total)
                bgs = await self.available(id)
                if len(bgs)==0:
                    bgs = ['default']
                await self.update(id,bgs)
            except:
                pass



    @commands.Cog.listener()
    async def on_member_join(self,member:discord.Member):
        guildid = member.guild.id
        channelid = await self.client.pg_con.fetchrow("SELECT mainchannel FROM guild WHERE guildid = $1",guildid)
        if channelid[0] is None:
            return
        welcome = Image.open('welcome.png')
        asset = member.avatar_url_as(size = 256)
        asset2 = member.guild.icon_url_as(size = 256)
        data = BytesIO(await asset.read())
        data2 = BytesIO(await asset2.read())
        pfp = Image.open(data).convert("RGB")
        logo = Image.open(data2).convert("RGB")
        pfp.save("profilereal.png")

        joined_at = "Joined at "+member.joined_at.strftime('%a, %#d %B %Y')
        logo = circle(logo,(200,200))
        pfp = circle(pfp,(296,296))
        welcome = Image.open('welcome.png')
        welcome.paste(pfp,(898,216),pfp)
        welcome.paste(logo, (18, 18), logo)
        pfp.save("profilereal.png")
        draw = ImageDraw.Draw(welcome)
        myFont = ImageFont.truetype('Roboto-Regular.ttf', 110)
        myFont2 = ImageFont.truetype('Roboto-Regular.ttf', 50)
        myFont3 = ImageFont.truetype('DrumNBass-ywGy2.ttf', 80)
        draw.text((60,270),member.name.title(),font = myFont,fill = (0,0,0))
        draw.text((110,400),joined_at,font = myFont2,fill = (0,0,0))
        draw.text((60,580),f"To {member.guild.name.title()}",font = myFont3,fill = (255,255,255), stroke_width=3, stroke_fill=(0,0,0))
        welcome.save("profile.png") 
        wchannel = get(member.guild.channels, id=channelid[0])
        embed = discord.Embed(description = f"{member.mention}** Welcome to {member.guild.name.title()} !!** \n Why not start with introducing yourself in Chats!",color = random.choice(colors))
        embed.set_image(url="attachment://profile.png")
        
        await wchannel.send(file = discord.File('profile.png'),embed = embed)
        os.remove("profile.png")

        emb = discord.Embed(title = "Welcome to {}".format(member.guild.name),color = random.choice(colors))
        emb.set_thumbnail(url= member.guild.icon_url)
        emb.add_field(name = "Thanks for joining " , value =":slight_smile:",inline =False)
        try:
            await member.send(embed =emb)
            await member.send("Check out my Youtube Channel ,Give it Subscribe if you like -\nhttps://www.youtube.com/channel/UCBwVvFWzp01YMD9ibqhSkEg")
        except:
            pass
        await self.check(member.id)
    
    
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        prefix = await self.client.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        if not isinstance(error, commands.CommandOnCooldown):
            try:
                ctx.command.reset_cooldown(ctx)
            except:
                pass
        if isinstance(error ,commands.MissingPermissions):
            await ctx.send(embed = discord.Embed(description = "You do not have the required Permissions to Use this command, Contact the Admin/Mods for the following",color=0x2F3136),delete_after = 10)
            await ctx.message.delete() 
        elif isinstance(error ,commands.errors.NotOwner):
            em = discord.Embed(title ="You Do Not own this Bot!! ",description =f"Ask the Bot Owner for More info - {str(self.client.get_user(self.client.owner_id))}",color = 0x2F3136)
            await ctx.send(embed = em,delete_after = 8)
        elif isinstance(error,commands.errors.ChannelNotFound):
            await ctx.send(embed = discord.Embed(title = "Channe not found!",description = "No such Text Channel exists\nPlease Type #channel_name to Mention a Channel",color = 0x2F3136))
        elif isinstance(error ,commands.MissingRequiredArgument):
            em = discord.Embed(title = "Missing Required Arguments!",description =f"Type `{prefix}help + command_name` for more info",color = 0x2F3136)
            await ctx.send(embed = em,delete_after = 8)
        elif isinstance(error , commands.errors.MemberNotFound):
            await ctx.send(embed = discord.Embed(description="Member not found!!",color= 0x2F3136,delete_after = 4))
            await ctx.message.delete()
        elif isinstance(error , commands.errors.CommandNotFound):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            msg = revert(error.retry_after)
            embed = discord.Embed(title = "Cooldown", description = str(msg), color = 16580705)
            embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
            embed.set_thumbnail(url = 'https://cdn.pixabay.com/photo/2012/04/13/00/22/red-31226_640.png')
            await ctx.send(embed = embed ,delete_after = 5)
            await ctx.message.delete()
        else:
            raise error
        
        
    @commands.Cog.listener()
    async def on_message(self,msg):
        user_id = self.client.user.id
        if msg.guild is None:
            return
        ai_id = await self.client.pg_con.fetchrow("SELECT aichannel FROM guild WHERE guildid = $1",msg.guild.id)
        
        if ai_id != None:
            ai_id = ai_id[0]
            if msg.channel.id == ai_id:
                if not msg.author.bot:
                    listtrainer.train([msg.content])
                    await self.append(msg.content)
                    await msg.reply(chatbot.get_response(msg.content))
        prefix = await self.client.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",msg.guild.id)
        if msg.content in (f"<@{user_id}>", f"<@!{user_id}>"):
            return await msg.reply(
                "My prefix here is `{}`".format(prefix[0])
            )
        
        

def setup(client):
    client.add_cog(Events(client))

