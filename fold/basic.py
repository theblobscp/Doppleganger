import asyncio
import discord
from discord.embeds import Embed
from discord.ext import commands
import random
from discord.utils import get
from bot import colors
import os
import wonderwords
import datetime
import re

def text(description,format,usage):
    return f"**Description** : \n{description}\n\n**Format** : \n{format}\n\n**Usage** : \n```{usage}```"

class Basic(commands.Cog):
    def __init__(self,client):
        self.client = client


    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(description = f"✔️ **|** Pong! I have a client ping of: **{round(self.client.latency * 1000)}ms**", color = 0x2F3136)
        embed.set_footer(text = "It's your turn now!")
        await ctx.send(embed = embed)

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

    @commands.command(aliases= ['th'])
    async def thank(self,ctx ,member: discord.Member,*,reason = "for your help"):
        if await self.get(ctx.author.id)<200:
            em = discord.Embed(title = f"Not Sufficient Credits",description = f"{ctx.author.mention} doesn't have sufficient credits To Thank ",color = random.choice(colors))
            await ctx.send(embed = em,delete_after = 7)
            return
        em = discord.Embed(title = f"Congrataltions {member.name} :partying_face: ",description=f":tada: You have been Thanked by {ctx.author.name} {reason}  :tada:\n200 credits are Thanked to {member.mention} by {ctx.author.mention}",color = random.choice(colors) )
        await self.add(ctx.author.id,-200)
        await self.add(member.id,200)
        await ctx.send(embed=em)


        
    @commands.command(aliases= ['hel','h'])
    async def help(self,ctx,cmd = "none"):
        prefix = await self.client.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        cmd = cmd.lower()
        if cmd is "none":
            em = discord.Embed(title = "DoppleGanger Commands :- ",description = f"`{prefix}setaichatbot + #channel` To enjoy chatbot features\n`{prefix}setlogs + #channel` To get Logging Updates\n`{prefix}setmain + #channel` To get Welcome,member in and out Updates\n`{prefix}setsuggestion + #channel` To Be able to use suggestion command",color = 0x2F3136)
            em.set_thumbnail(url=self.client.user.avatar_url)    
            em.add_field(name = ":red_circle:   Search  ",value = "  \n\n`image`  `song` `youtube` `ques` `meme` `lyrics`",inline = False)
            em.add_field(name = ":blue_circle:   Economy  ",value ="  \n\n`leaderboard` `locallb` `donate` `earn` `work` `credits` `shop` `slots` `gamble` `shop` `beg` `inventory` `sell` `buy` `hunt` `fish`" ,inline = False)
            em.add_field(name = ":green_circle:   Information  ",value ="  \n\n`profile` `pfp` `afk` `afkoff` `backgrounds` `setbg` `serverinfo`",inline = False)
            em.add_field(name = ":brown_circle:   Utility  ",value ="  \n\n`createmute` `setprefix` `setsuggestion` `setaichatbot` `setlogs` `remove_logs` `remove_sug` `remove_aibot` `remove_main` ",inline = False)
            em.add_field(name = ":purple_circle:   Moderators  ",value ="  \n\n`ban` `unban` `kick` `mute` `unmute` `clear`",inline = False)
            em.add_field(name = ":yellow_circle:   Basics  ",value ="  \n\n`thank` `typerace` `suggest` `ping` `reportbug`",inline = False)
            em.add_field(name = ":orange_circle:   Crypto  ",value ="  \n\n`encode` `decode` `imgenc` `imgdec` `password` `randompass` `lang`",inline = False)            
            em.add_field(name = ":red_circle:   Fun  ",value ="  \n\n`beer` `coffee` `roast` `kill` ",inline = False)                     
            em.add_field(name = ":white_circle:   Invite  ",value ="  \n\n`join` `invite` ",inline = False)        
            em.set_footer(icon_url= ctx.guild.icon_url, text= f"Type {prefix}help + command_name for more info and usage")
            await ctx.send(embed = em)
            return

        elif cmd == "setbg":
            await ctx.send(embed = discord.Embed(title = f"{prefix}setbg or {prefix}swap or {prefix}switch",description = text(f"Change your Profile Background, You can buy 'em through `{prefix}shop` if you don't have any other then than the default one",f"{prefix}swapbg + background_img_name",f"{prefix}swap binary"),color = 0x2F3136))
        elif cmd == "backgrounds":
            await ctx.send(embed = discord.Embed(title = f"{prefix}backgrounds or {prefix}backs or {prefix}background",description = text("See towards your Available backrgounds",f"{prefix}background",f"{prefix}backs"),color = 0x2F3136))
        elif cmd == "profile":
            await ctx.send(embed = discord.Embed(title = f"{prefix}profile or {prefix}whois",description = text("Check Yours/others Profile and Stats in Image format ",f"{prefix}profile + @memberName",f"{prefix}profile @Code Stacks"),color = 0x2F3136))
        elif cmd == "afk":
            await ctx.send(embed = discord.Embed(title = f"{prefix}afk or {prefix}afkset",description = text("Away From KeyBoard",f"{prefix}afk + time(in mins, can be in Decimals)",f"{prefix}afk 3 "),color = 0x2F3136))
        elif cmd == "afkoff":
            await ctx.send(embed = discord.Embed(title = f"{prefix}afkoff or {prefix}removeafk",description = text("Turn Off the AFK(Away From KeyBoard)",f"{prefix}afkoff",f"{prefix}afkoff"),color = 0x2F3136))
        elif cmd == "serverinfo":
            await ctx.send(embed = discord.Embed(title = f"{prefix}serverinfo or {prefix}si",description = text("Know more about the server you are in",f"{prefix}si",f"{prefix}serverinfo"),color = 0x2F3136))
        elif cmd == "pfp":
            await ctx.send(embed = discord.Embed(title = f"{prefix}pfp or {prefix}profilepic",description = text("See others and yours Profile Picture",f"{prefix}pfp",f"{prefix}pfp @Code Stacks"),color = 0x2F3136))
        
        elif cmd == "kill":
            await ctx.send(embed = discord.Embed(title = f"{prefix}kill or {prefix}kills",description = text("Kill others For Fun in different ways every time",f"{prefix}kill + @member_name",f"{prefix}kill @Code Stacks"),color = 0x2F3136))
        elif cmd == "beer":
            await ctx.send(embed = discord.Embed(title = f"{prefix}beer or {prefix}drink",description = text("Have a Beer party alone or with others , react to join with others in the party",f"{prefix}beer + @member_name",f"{prefix}beer @Drift Asimov"),color = 0x2F3136))
        elif cmd == "coffee":
            await ctx.send(embed = discord.Embed(title = f"{prefix}coffee or {prefix}cafe",description = text("Enjoy Coffee WIth Others , and others need to react to join you",f"{prefix}coffee + @member_name",f"{prefix}coffee @Drift Asimov"),color = 0x2F3136))
        elif cmd == "roast":
            await ctx.send(embed = discord.Embed(title = f"{prefix}roast",description = text("Roast a member in server",f"{prefix}roast + @member_name",f"{prefix}roast @Drift Asimov"),color = 0x2F3136))
        
        elif cmd == "youtube":
            await ctx.send(embed = discord.Embed(title = f"{prefix}youtube or {prefix}yo",description = text("Search Youtube",f"{prefix}youtube + SearchQuery",f"{prefix}youtube Code Stacks"),color = 0x2F3136))
        elif cmd == "image":
            await ctx.send(embed = discord.Embed(title = f"{prefix}image or {prefix}img",description = text("Search am Anime Character Image",f"{prefix}image + SearchQuery",f"{prefix}image Itadori Yuuji"),color = 0x2F3136))
        elif cmd == "meme":
            await ctx.send(embed = discord.Embed(title = f"{prefix}meme or {prefix}me",description = text("Get the Top random memes",f"{prefix}meme",f"{prefix}meme"),color = 0x2F3136))
        elif cmd == "ques":
            await ctx.send(embed = discord.Embed(title = f"{prefix}que or {prefix}ques",description = text("Ask any Question from Bot",f"{prefix}ques + Question",f"{prefix}ques Value of pi"),color = 0x2F3136))
        elif cmd == "lyrics":
            await ctx.send(embed = discord.Embed(title = f"{prefix}lyrics or {prefix}lyric",description = text("Search Any anime song lyrics",f"{prefix}lyrics + song_name",f"{prefix}lyrics My war"),color = 0x2F3136))
        elif cmd == "song":
            await ctx.send(embed = discord.Embed(title = f"{prefix}song",description = text("Download a Mp3 song",f"{prefix}song + Song_name",f"{prefix}song In my feelings"),color = 0x2F3136))
        
        elif cmd == "createmute":
            await ctx.send(embed = discord.Embed(title = f"{prefix}createmute or {prefix}mutedrole",description = text("Create the muted role through Bot or disable the perms of muted role in all Channels",f"{prefix}mutedrole",f"{prefix}createmute"),color = 0x2F3136))
        elif cmd == "setprefix":
            await ctx.send(embed = discord.Embed(title = f"{prefix}setprefix",description = text("Set a New Bot prefix",f"{prefix}setprefix + New_prefix",f"{prefix}setprefix >"),color = 0x2F3136))
        elif cmd == "setsuggestion":
            await ctx.send(embed = discord.Embed(title = f"{prefix}setsuggestion or {prefix}sugchannel",description = text("Set the suggestion channel to use suggestion command",f"{prefix}setsuggestion + #channelName",f"{prefix}setsuggestion #Suggestions"),color = 0x2F3136))
        elif cmd == "setaichatbot":
            await ctx.send(embed = discord.Embed(title = f"{prefix}setaichatbot or {prefix}aichannel",description = text("Set the Ai chatbot channel to be able to use AI chatbot",f"{prefix}aichannel + #channelname",f"{prefix}aichannel #ai-chatbot"),color = 0x2F3136))
        elif cmd == "setlogs":
            await ctx.send(embed = discord.Embed(title = f"{prefix}setlogs or {prefix}logchannel",description = text("Set the logs channel to get the logging updates",f"{prefix}logchannel + #channelname",f"{prefix}logchannel #logs"),color = 0x2F3136))
        elif cmd == "remove_logs":
            await ctx.send(embed = discord.Embed(title = f"{prefix}remove_logs or {prefix}remove_log",description = text("Remove the Logs feature",f"{prefix}remove_logs",f"{prefix}remove_logs"),color = 0x2F3136))
        elif cmd == "remove_sug":
            await ctx.send(embed = discord.Embed(title = f"{prefix}remove_sug or {prefix}remove_suggestion",description = text("Remove the suggestion channel and the feature For this guild/server",f"{prefix}remove_sug",f"{prefix}remove_sug"),color = 0x2F3136))
        elif cmd == "remove_aibot":
            await ctx.send(embed = discord.Embed(title = f"{prefix}remove_aibot or {prefix}remove_aichatbot",description = text("Remove the AI-chatbot Feature For this guild/server",f"{prefix}remove_aibot",f"{prefix}remove_aichatbot"),color = 0x2F3136))
        elif cmd == "remove_main":
            await ctx.send(embed = discord.Embed(title = f"{prefix}remove_main or {prefix}remove_general",description = text("Remove the mail channel features like Welcome Image, member in and out info etc",f"{prefix}remove_main",f"{prefix}remove_general"),color = 0x2F3136))
        elif cmd == "setmain":
            await ctx.send(embed = discord.Embed(title = f"{prefix}setmain or {prefix}mainchannel",description = text("Set the Main Channel to enjoy certain features",f"{prefix}setmain",f"{prefix}setmain"),color = 0x2F3136))
        elif cmd == "join" or cmd == "invite":
            await ctx.send(embed = discord.Embed(title = f"{prefix}invite or {prefix}join",description = text("Join the main server or Invite the bot in Your server",f"{prefix}join",f"{prefix}invite"),color = 0x2F3136))
        
        elif cmd == "clear":
            await ctx.send(embed = discord.Embed(title =f"{prefix}clear or {prefix}c",description = text("Clear Chats",f"{prefix}c + no_of_Chats",f"{prefix}c 3"),color = 0x2F3136))
        elif cmd == "mute":
            await ctx.send(embed = discord.Embed(title = f"{prefix}mute or {prefix}m",description = text("Mute a Member",f"{prefix}mute + @membername + amount(in mins)",f"{prefix}mute @Code Stacks 2"),color = 0x2F3136))
        elif cmd == "unmute":
            await ctx.send(embed = discord.Embed(title = f"{prefix}unmute or {prefix}um",description = text("Unmute Member",f"{prefix}unmute + @Membername",f"{prefix}um @Code Stacks"),color = 0x2F3136))
        elif cmd == "kick":
            await ctx.send(embed = discord.Embed(title = f"{prefix}kick or {prefix}k",description = text("Kick Member",f"{prefix}kick + @memberName + reason(optional)",f"{prefix}kick @Code Stacks For Spamming chat"),color = 0x2F3136))
        elif cmd == "ban":
            await ctx.send(embed = discord.Embed(title = f"{prefix}ban or {prefix}b",description = text("Ban A Member",f"{prefix}ban + @Membername + reason(optional)",f"{prefix}ban @Code Stacks For Misusing Powers"),color = 0x2F3136))
        elif cmd == "unban":
            await ctx.send(embed = discord.Embed(title = f"{prefix}unban or {prefix}ub",description = text("Unban A Member",f"{prefix}unban @membername",f"{prefix}unban @Code Stacks"),color = 0x2F3136))
        
        elif cmd == "suggest":
            await ctx.send(embed = discord.Embed(title = f"{prefix}suggest or {prefix}suggestion",description = text("Give a Suggestion",f"{prefix}suggest + Suggestion",f"{prefix}suggest Add New Roles"),color = 0x2F3136))
        elif cmd == "reportbug":
            await ctx.send(embed = discord.Embed(title = f"{prefix}reportbug or {prefix}bug",description =text("Report a Bug/query/issue to My Owner",f"{prefix}reportbug + Bug",f"{prefix}reportbug Search music function in the bot is too slow"),color = 0x2F3136))
        elif cmd == "thank":
            await ctx.send(embed = discord.Embed(title = f"{prefix}thanks or {prefix}th",description = text("Thank A Member",f"{prefix}thank + @member + Reason(not necessary)",f"{prefix}thank @Code Stacks for Helping me out"),color = 0x2F3136))
        elif cmd == "typerace":
            await ctx.send(embed = discord.Embed(title = f"{prefix}typerace",description = text("Check your words per minute through TypeRace",f"{prefix}typerace",f"{prefix}typerace"),color = 0x2F3136))
        elif cmd == "ping":
            await ctx.send(embed = discord.Embed(title = f"{prefix}ping",description = text("Check the Bot's Ping",f"{prefix}ping",f"{prefix}ping"),color = 0x2F3136))
        

        elif cmd == "lang":
            await ctx.send(embed = discord.Embed(title = f"{prefix}lang or {prefix}language",description = text("Translate any Language to English",f"{prefix}lang + Language_text",f"{prefix}lang Ohayo Gozaimasu"),color = 0x2F3136))
        elif cmd == "decode":
            await ctx.send(embed = discord.Embed(title = f"{prefix}decode or {prefix}dec",description = text("Decode A Encoded Text",f"{prefix}decode + Encoded_text",f"{prefix}decode euhFOUHosUOSWH...."),color = 0x2F3136))
        elif cmd == "encode":
            await ctx.send(embed = discord.Embed(title = f"{prefix}encode or {prefix}enc",description = text("Encode A Text to Decode in future",f"{prefix}encode + Text",f"{prefix}encode Hi there , M Code Stacks"),color = 0x2F3136))
        elif cmd == "randompass":
            await ctx.send(embed = discord.Embed(title = f"{prefix}randompass or {prefix}ranpass",description = text("Get a Random Passoword",f"{prefix}ranpass + Length",f"{prefix}randompass 8"),color = 0x2F3136))
        elif cmd == "password":
            await ctx.send(embed = discord.Embed(title = f"{prefix}password or {prefix}passw",description = text("Get a Complex Password From Keyword Provided",f"{prefix}password + Keyword",f"{prefix}passw Code Stacks"),color = 0x2F3136))
        elif cmd == "imgdec":
            await ctx.send(embed = discord.Embed(title = f"{prefix}imgdec or {prefix}decodeimg",description = text("Decode an Encoded Image text",f"{prefix}imgdec + Code",f"{prefix}imgdec aHR0cHM6Ly9jZG4uZGlzY29yZ..........."),color = 0x2F3136))
        elif cmd == "imgenc":
            await ctx.send(embed = discord.Embed(title = f"{prefix}imgenc or {prefix}encodeimg",description = text("Encode An Image",f"{prefix}imgenc <image attachment>",f"{prefix}imgenc <image>"),color = 0x2F3136))
        
        elif cmd == "gamble":
            await ctx.send(embed = discord.Embed(title = f"{prefix}gamble or {prefix}bet",description = text("Gamble Credits",f"{prefix}gamble + amount",f"{prefix}gamble 10000"),color = 0x2F3136))
        elif cmd == "inventory":
            await ctx.send(embed = discord.Embed(title = f"{prefix}inventory or {prefix}inven",description = text("Check Yours/others Inventory",f"{prefix}inven @member_name",f"{prefix}inventory @code Stacks"),color = 0x2F3136))
        elif cmd == "hunt":
            await ctx.send(embed = discord.Embed(title = f"{prefix}hunt or {prefix}hunting",description = text("Hunt Animals to Sell them for credits or to save them in you inventory",f"{prefix}hunt",f"{prefix}hunt"),color = 0x2F3136))
        elif cmd == "fish":
            await ctx.send(embed = discord.Embed(title = f"{prefix}fish or {prefix}fishing",description = text("Capture Fishes to Sell or store them in inventory",f"{prefix}fish",f"{prefix}fish"),color = 0x2F3136))
        elif cmd == "sell":
            await ctx.send(embed = discord.Embed(title = f"{prefix}sell",description = text("Sell Items from your Inventory",f"{prefix}sell + Product_name",f"{prefix}sell rabbit"),color = 0x2F3136))
        elif cmd == "credits":
            await ctx.send(embed = discord.Embed(title = f"{prefix}credits or {prefix}credit",description =text("Check Your Credits",f"{prefix}credits",f"{prefix}credit"),color = 0x2F3136))
        elif cmd == "shop":
            await ctx.send(embed = discord.Embed(title = f"{prefix}shop",description = text("CHeck what all is there to Buy",f"{prefix}shop",f"{prefix}shop"),color = 0x2F3136))
        elif cmd == "earn":
            await ctx.send(embed = discord.Embed(title = f"{prefix}earn",description = text("See all the ways to Earn",f"{prefix}earn",f"{prefix}earn"),color = 0x2F3136))
        elif cmd == "slots":
            await ctx.send(embed = discord.Embed(title = f"{prefix}slots or {prefix}slot",description = text("Earn Money Through Luck ",f"{prefix}slots + amount",f"{prefix}slot 10000"),color = 0x2F3136))
        elif cmd == "work":
            await ctx.send(embed = discord.Embed(title = f"{prefix}work",description = text("Work to Earn Money",f"{prefix}work",f"{prefix}work"),color = 0x2F3136))
        elif cmd == "buy":
            await ctx.send(embed = discord.Embed(title = f"{prefix}buy",description = text("Buy An Item from Shop",f"{prefix}buy + ItemID",f"{prefix}buy 2"),color = 0x2F3136))
        elif cmd == "donate":
            await ctx.send(embed = discord.Embed(title = f"{prefix}donate",description = text("Donate A member Some Credits",f"{prefix}donate + @member + amount",f"{prefix}donate @Code Stacks 2000"),color = 0x2F3136))
        elif cmd == "leaderboard":
            await ctx.send(embed = discord.Embed(title = f"{prefix}leaderboard or {prefix}lb",description = text("Check the Global Leaderboard of DoppleGanger",f"{prefix}leaderboard",f"{prefix}lb"),color = 0x2F3136))
        elif cmd == "locallb":
            await ctx.send(embed = discord.Embed(title = f"{prefix}locallb or {prefix}localleaderboard",description = text("Check the Local Leaderboard of Your server",f"{prefix}locallb",f"{prefix}locallb"),color = 0x2F3136))
        elif cmd == "beg":
            await ctx.send(embed = discord.Embed(title = f"{prefix}beg",description = text("Beg for Credits",f"{prefix}beg",f"{prefix}beg"),color = 0x2F3136))
        

    @commands.command()
    async def typerace(self, ctx):
        emojified = ''

        sentence = wonderwords.RandomSentence().sentence().replace(".","")
        length = len(sentence.split())
        formatted = re.sub(r'[^A-Za-z ]+', "", sentence).lower()
        
        for i in formatted:
            if i == ' ':
                emojified += '   '
            else:
                emojified += ':regional_indicator_{}: '.format(i)
        sent = await ctx.send(f"{emojified}.")

        def check(msg):
            return msg.content.lower() == sentence.lower()
        try:
            s = await self.client.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(embed = discord.Embed(description = "No one answered Correct in time.", color = discord.Colour.red()))
        else:
            
            time =  str(datetime.datetime.utcnow() - sent.created_at)
            time_format = time[:-5][5:]
            if time_format[0] == '0':
                time_format = time_format[1:]
            
            embed = discord.Embed(description = f"{s.author.mention} Completed the typerace in **{time_format}** seconds.", color=random.choice(colors))
            time_in_mins = float(time_format)/60
            embed.add_field(name = "WPM (Words Per Minute) : ", value = int(length/time_in_mins))
            await ctx.send(embed = embed)
            
  
    @commands.command(aliases = ["suggestion"])
    async def suggest(self,ctx,*,suggestion):
        prefix = await self.client.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        await ctx.message.delete()
        id = await self.client.pg_con.fetchrow("SELECT suggestionchannel FROM guild WHERE guildid = $1",ctx.guild.id)
        id = id[0]
        if id == None:
            await ctx.send(embed = discord.Embed(title = "Suggestion Channel Not Synced",description = f"You need to set the suggestion channel by sayin `{prefix}set_suggestion + #channel_name` to set the channel\nThen Type `{prefix}suggestion + suggestion` to send a suggestion into that specific channel ",color = 0x2F3136))
            return
        channel = self.client.get_channel(id)
        em = discord.Embed(title = "Sugesstion : ",description = suggestion,timestamp = datetime.datetime.utcnow(),color = random.choice(colors))
        
        em.set_thumbnail(url = ctx.author.avatar_url)
        em.set_author(name = ctx.author.name)
        em.set_footer(text = f"Change the suggestion channel by {prefix}set_suggestion #channel_name and remove suggestion command by {prefix}remove_sug")
        message = await channel.send(embed = em)
        await channel.send(ctx.guild.owner.mention)
        await message.add_reaction("✅")
        await message.add_reaction("❎")
        await ctx.send(f"Your Suggestion have been succesfully sent ! :)\nCheck <#{id}>",delete_after = 10)
        await asyncio.sleep(36000)
        agmessage = await channel.fetch_message(message.id)
        positive = await agmessage.reactions[0].users().flatten()
        positive.pop(positive.index(self.client.user))
        negative = await agmessage.reactions[1].users().flatten()
        negative.pop(negative.index(self.client.user))
        if len(positive)>len(negative):
            winner = "Proposition shall be followed"

        elif len(positive)<len(negative):
            winner = "Proposition shalln't be followed"

        else:
            winner = f"That was a Tie, Now all depends on {ctx.guild.owner.mention}"
        
        positive = "\n".join([str(i.mention) for i in positive]) 
        negative = "\n".join([str(i.mention) for i in negative]) 

        em2 = discord.Embed(title = "Poll Closed 🔒",color = 0x2F3136,timestamp = datetime.datetime.utcnow())
        em2.add_field(name = "Suggestion : ",value = suggestion,inline=False)
        em2.add_field(name = "People in Support : ",value=positive,inline=True)
        em2.add_field(name = "People in Opposition : ",value=negative,inline=True)
        em2.add_field(name = "Result",value=winner,inline=False)
        em2.set_footer(text=f"Remove suggestion command by {prefix}remove_sug")
        await channel.send(embed = em2)
        
    @commands.command(aliases = ['bug'])
    async def reportbug(self,ctx,*,bug):
        owner = get(self.client.get_all_members(), id=779743087572025354)
        em = discord.Embed(title = "Bug Report",description = bug,color = random.choice(colors))
        em.set_author(name = ctx.author.display_name , icon_url=ctx.author.avatar_url)
        try:
            await owner.send(embed = em)
            await ctx.send("Bug was Succesfully Recorded :slight_smile:  ",delete_after = 5)
        except Exception as e:

            await ctx.send(f"Message could not be sent , Try again later :( \n{e}",delete_after = 6)

    
def setup(client):
    client.add_cog(Basic(client))
