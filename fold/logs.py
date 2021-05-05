import discord
from discord import client
from discord import message
from discord import activity
from discord.ext import commands
import random
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import command
import datetime
from bot import colors


class Logs(commands.Cog):
    def __init__(self,client):
        self.client = client


    @commands.Cog.listener()
    async def on_member_update(self,before,after):
        try:
            id = await self.client.pg_con.fetchrow("SELECT logchannel FROM guild WHERE guildid = $1",after.guild.id)
            if id == None:
                print("none")
                return
            log = self.client.get_channel(id[0])
                        
            old_roles = " ".join([role.mention for role in before.roles])

            new_roles  =" ".join([role.mention for role in after.roles])

            em = discord.Embed(title ="Member Edited Info ",color = 0xffb432)
            def func(state):
                activity = ""
                if isinstance(state.activities,tuple):
                    for i in state.activities:
                        try:
                            activity =  activity+ i.name+" "
                            
                        except:
                            pass
                        try:
                            activity = activity+"**"+i.title+"**"
                        except:
                            pass
                        activity += "\n"
                else:
                    activity = state.activities[0]
                if activity == "":
                    activity = None
                return activity
            em.add_field(name = "Old Info : ",value = f"Status : {str(before.status).upper()} \nActivity : {func(before)} \nNickname : {before.display_name} \nRoles : {old_roles} \nPending : {before.pending}")
            em.add_field(name = "New Info : ",value = f"Status : {str(after.status).upper()} \nActivity : {func(after)} \nNickname : {after.display_name} \nRoles : {new_roles} \nPending : {after.pending}")
            em.timestamp = datetime.datetime.utcnow()
            em.set_author(name = after,icon_url = after.avatar_url)
            if str(before.status).upper() == str(after.status).upper() and func(before) == func(after) and before.display_name == after.display_name and old_roles==new_roles and before.pending ==after.pending :
                pass
            else:
                await log.send(embed = em)
        except Exception as e :
            pass
    
    @commands.Cog.listener()
    async def on_message_delete(self,message):
        id = await self.client.pg_con.fetchrow("SELECT logchannel FROM guild WHERE guildid = $1",message.guild.id)
        if id[0] is None:
            return
        log = self.client.get_channel(id[0])
        embed = discord.Embed(title = "Message Deleted",color = random.choice(colors),timestamp = datetime.datetime.utcnow())
        embed.add_field(name="Message",value=message.content,inline=False)
        embed.add_field(name="Author",value=message.author.name,inline=False)
        embed.add_field(name="Channel",value=message.channel.name,inline=False)
        embed.set_thumbnail(url="https://icons.iconarchive.com/icons/cornmanthe3rd/plex/512/System-recycling-bin-full-icon.png")
        await log.send(embed = embed)
    
    @commands.Cog.listener()
    async def on_message_edit(self,old,new):
        id = await self.client.pg_con.fetchrow("SELECT logchannel FROM guild WHERE guildid = $1",old.guild.id)
        if id[0] is None:
            return
        print(id[0])
        log = self.client.get_channel(id[0])
        embed = discord.Embed(title = "Message Edited",description = f"[Jump to the Message]({new.jump_url})",color = random.choice(colors),timestamp = datetime.datetime.utcnow())
        embed.add_field(name="Old Message",value=old.content)
        embed.add_field(name="New Message",value=new.content)
        embed.add_field(name="Channel",value=old.channel.name,inline=False)
        embed.add_field(name="Author",value=old.author.name,inline=False)
        embed.set_thumbnail(url="https://th.bing.com/th/id/R66dbcbb7f70864efa5e4e8097e865a28?rik=KbhIVKRoP5CCLw&riu=http%3a%2f%2fwww.recycling.com%2fwp-content%2fuploads%2f2016%2f06%2frecycling-symbol-icon-outline-solid-dark-green.png&ehk=uUs07SqPyEepr2jBZhiGSUkO1QbzTCvEobnhAM%2fddU8%3d&risl=&pid=ImgRaw")
        await log.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_emojis_update(self,guild,before,after):
        
        id = await self.client.pg_con.fetchrow("SELECT logchannel FROM guild WHERE guildid = $1",guild.id)
        if id[0] is None:
            return
        log = self.client.get_channel(id[0])
        before_emotes = ""
        after_emote = ""
        for i in before:
            name = f"<:{i.name}:{i.id}>"
            before_emotes += name + " "
            
        for i in after:
            name = f"<:{i.name}:{i.id}>"
            after_emote += name + " "
            
        try:
            em = discord.Embed(title ="New Emotes :) available : ",color = 0xffb432)
            em.add_field(name = "Old Server Emotes : ",value = before_emotes)
            em.add_field(name = "New Server Emotes : ",value = after_emote)
            em.timestamp = datetime.datetime.utcnow()
            em.set_author(name = self.client.user,icon_url = self.client.user.avatar_url)
            await log.send(embed = em)
        except:
            pass


def setup(client):
    client.add_cog(Logs(client))