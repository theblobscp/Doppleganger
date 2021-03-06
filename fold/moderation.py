import discord
from discord.ext import commands
import random
import asyncio
from bot import colors
from discord.utils import get

error = discord.Embed(title = "Invalid input or arguments !!\nType `.help` or `.more_help` for more info",color = discord.Colour.red()) 
        

class Moderation(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(aliases= ['b'])
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, member :discord.Member,*,reason = "No reason Provided"):
        em = discord.Embed(description = f"{member.mention} is Banned from {ctx.guild.name} by {ctx.author.mention} \n Reason : {reason}",color = discord.Colour.random() )
        em.set_author(name=ctx.guild.owner.name,icon_url=ctx.guild.owner.avatar_url)
        em.set_thumbnail(url =ctx.guild.icon_url)
        try:
            await member.ban(reason=reason)
            await ctx.send(embed=em)
        except:
            await ctx.send(embed = discord.Embed(title= "Missing Permissions",description = f"Bot doesn't have the required Perms to Ban {member.name}",color = discord.Colour.red()))
        

    @commands.command(aliases= ['k'])
    @commands.has_permissions( kick_members=True)
    async def kick(self,ctx, member :discord.Member,*,reason = "No reason Provided"):
        em = discord.Embed(description = f"{member.mention} is Kicked from {ctx.guild.name} by {ctx.author.mention} \n Reason : {reason}",color = discord.Colour.random() )
        em.set_author(name=ctx.guild.owner.name,icon_url=ctx.guild.owner.avatar_url)
        
        try:
            await member.send("https://discord.gg/UckPYtvqqc")
        except:
            pass
        try:
            await member.kick(reason=reason)
            await ctx.send(embed=em)
        except:
            await ctx.send(embed = discord.Embed(title= "Missing Permissions",description = f"Bot doesn't have the required Perms to Ban {member.name}",color = discord.Colour.red()))
    @commands.command(aliases = ['ub'])
    @commands.has_permissions(ban_members=True, kick_members=True)
    async def unban(self,ctx, member):
        member_nam ,member_dis = member.split('#')
        em = discord.Embed(description = f"{member_nam} is Unbanned from {ctx.guild.name} by {ctx.author.name} ",color = discord.Colour.random() )
        em.set_author(name=ctx.guild.owner.name,icon_url=ctx.guild.owner.avatar_url)
        banned = await ctx.guild.bans()
        member_nam ,member_dis = member.split('#')

        for banned_entry in banned:
            user = banned_entry.user

            if(user.name ,user.discriminator) == (member_nam,member_dis):
                await ctx.guild.unban(user)
                await ctx.send(embed = em)
                return

            await ctx.send(member + ' was not found',delete_after =4)
    @commands.command(aliases= ['m'])
    @commands.has_permissions(ban_members=True, kick_members=True)
    async def mute(self,ctx,member:discord.Member,amount = 2):
        
        prefix = await self.client.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        try:
            muted = get(ctx.guild.roles,name="Muted")
        except:
            await ctx.send(embed = discord.Embed(title = "No role Named Muted",description= f"Type `{prefix}mutedrole` or `{prefix}createmute` to create a muted Role \nThe bot will automatically Take it's messaging rights",color = random.choice(colors)))
            return
        if muted in member.roles:
            await ctx.send(f"{member.name} is already Muted !!")
        else:
            em2 = discord.Embed(title = "Member Muted !",description =f"{member.mention} is muted by {ctx.author.mention} for {amount} min(s)   ",color = discord.Colour.random())   
            em2.set_thumbnail(url=ctx.guild.icon_url) 
            em2.set_footer(icon_url= ctx.guild.icon_url, text= f"From {ctx.guild.id}")   
            em3 = discord.Embed(title = "Member Unmuted !",description =f"{member.mention} is Unmuted Now",color = discord.Colour.random())   
            em3.set_thumbnail(url=ctx.guild.icon_url) 
            em3.set_footer(icon_url= ctx.guild.icon_url, text= f"From {ctx.guild.id}")  
            try:
                amount = float(amount)*60

                await member.add_roles(muted)
                await ctx.send(embed=em2)
                try:
                    await member.send(embed = em2)
                except:
                    pass
                await asyncio.sleep(amount)
                await member.remove_roles(muted)
                await ctx.send(embed=em3)
            except:
                await ctx.send(embed=error)

    
    @commands.command(aliases= ['um'])
    @commands.has_permissions(ban_members=True, kick_members=True)
    async def unmute(self,ctx,member:discord.Member):
        
        prefix = await self.client.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",ctx.guild.id)
        prefix = prefix[0]
        try:
            muted = get(ctx.guild.roles,name="Muted")
        except:
            await ctx.send(embed = discord.Embed(title = "No role Named Muted",description= f"Type `{prefix}mutedrole` or `{prefix}createmute` to create a muted Role \nThe bot will automatically Take it's messaging rights",color = random.choice(colors)))
            return
        em3 = discord.Embed(title = "Member Unmuted !",description =f"{member.mention} is Unmuted Now",color = discord.Colour.random())   
        em3.set_thumbnail(url=ctx.guild.icon_url) 
        em3.set_footer(icon_url= ctx.guild.icon_url, text= f"From {ctx.guild.name}")  
        if muted in member.roles:
            await member.remove_roles(muted)
            await ctx.send(embed=em3)

        else:
            await ctx.send("Member is already Unmuted !!",delete_after=4)
    
    @commands.command(aliases= ['c'])
    @commands.has_permissions(ban_members=True, kick_members=True)
    async def clear(self,ctx,amount):
        try:
            amount = int(amount)
            if amount < 1:
                await ctx.send('Amount should be at least 1!!')
            else:
                await ctx.channel.purge(limit = amount+1)
        except:
            await ctx.send(embed = error)



def setup(client):
    client.add_cog(Moderation(client))
