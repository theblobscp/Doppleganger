import discord
from discord import colour
from discord.ext import commands
import base64
import random
import datetime
from googletrans import Translator
from bot import colors
import string

SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',  '*', '(', ')']



class Crypto(commands.Cog):
    def __init__(self,client):
        self.client = client


    @commands.command(aliases = ['encodeimg'])
    async def imgenc(self, ctx):
        await ctx.message.delete()
        if len(ctx.message.attachments) <= 0:
            await ctx.send(embed = discord.Embed(description = "Make sure your msg have an image attached with it.", color = discord.Colour.red()),delete_after = 6)
            return
        url = ctx.message.attachments[0].url    
        ss = url.encode("ascii") 
        base64_bytes = base64.b64encode(ss) 
        base64_string = base64_bytes.decode("ascii") 
        base64_string = base64_string.replace("==", "")
        embed = discord.Embed(title = "Image Encoded", description = f"```{base64_string}```", color =  random.choice(colors))
        embed.set_footer(text="type .imgdec + encoded_code to get the decoded image")
        await ctx.send(embed = embed)

    @commands.command(aliases = ['decodeimg'])
    async def imgdec(self, ctx,*,string):
        string = f"{string}=="
        try:
            base64_bytes = string.encode("ascii") 
            sample_string_bytes = base64.b64decode(base64_bytes) 
            sample_string = sample_string_bytes.decode("ascii") 
            embed = discord.Embed(color = 0xFFC5A8)
            embed.set_image(url = sample_string)
            embed.set_author(name = ctx.author.name,url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(embed = discord.Embed(description = "Couldn't Decode the Code, make sure that you didn't have a typo.", color = discord.Colour.red()))

    @commands.command(aliases = ["passw","strongpass"])
    async def password(self, ctx, *, passw,length = 8):

        cap_pass = ''.join(random.choice((str.upper, str.lower))(c) for c in passw)
        var1 = ''.join('%s%s' % (x, random.choice((random.choice(SYMBOLS), ""))) for x in cap_pass)
        try:
            var1 = var1.replace(" ","")
        except:
            pass
        while len(var1)<=length:
            var1 += random.choice(SYMBOLS)

        embed = discord.Embed(description = "Generated new password for you!", color = random.choice(colors), timestamp = datetime.datetime.utcnow())
        embed.add_field(name = "Old Password", value = f"```{passw}```", inline = False)
        embed.add_field(name = "New Password", value = f"```{var1}```", inline = False)
        embed.add_field(name = "Length", value = f"```{len(var1)}```")
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(aliases = ['ranpass'])
    async def randompass(self, ctx, number: int = 6):

        if number > 100:
            await ctx.send(embed = discord.Embed(description = "Isn't that digit too long?", color = discord.Colour.red()))

        if number < 6:
            await ctx.send(embed = discord.Embed(description = "Isn't that digit too short?", color = discord.Colour.red()))

        def password(stringLength):
            password_character = string.ascii_letters + string.digits + string.punctuation
            return "".join(random.choice(password_character) for i in range(stringLength))

        embed = discord.Embed(color = random.choice(colors), timestamp = datetime.datetime.utcnow())
        embed.add_field(name = "Random Password", value = f"```{password(number)}```")
        await ctx.send(embed = embed)

    @commands.command(aliases = ['enc'])
    async def encode(self, ctx, *, string):
        await ctx.message.delete()
        try:
            ss = string.encode("ascii") 
            base64_bytes = base64.b64encode(ss) 
            base64_string = base64_bytes.decode("ascii") 
            embed = discord.Embed(color = random.choice(colors))
            embed.add_field(name = "Encoded - ", value = f"```{base64_string}```")
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            embed.set_footer(text="Type .decode + encoded_value to get the translation")
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(e)
            await ctx.send(embed = discord.Embed(description = "Couldn't Encode the given string.", color = discord.Colour.red()))
    
    @commands.command(aliases = ['dec'])
    async def decode(self, ctx,*,string):
        try:
            base64_bytes = string.encode("ascii") 
            sample_string_bytes = base64.b64decode(base64_bytes) 
            sample_string = sample_string_bytes.decode("ascii")
            embed = discord.Embed(color = random.choice(colors))
            embed.add_field(name = "Decoded - ", value = f"```{sample_string}```")
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed= embed)
        except:
            await ctx.send(embed = discord.Embed(description = "Couldn't Decode the Code, make sure that you didn't have a typo.",color =discord.Colour.red()))

    @commands.command(aliases = ['translate'])
    async def lang(self,ctx,*,arg):
        trans = Translator()
        trs = trans.translate(arg, dest="en")
        detected = trans.detect(arg)
        embed = discord.Embed(title = "Here is your translated text", description = f"`{trs.text}`", color = random.choice(colors))
        embed.set_footer(text = f"Translated from {detected.lang} to en.")
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Crypto(client))