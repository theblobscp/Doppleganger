from asyncpg.pool import create_pool
import discord
import os
from discord.ext import commands
import cogs
import random
import asyncpg

client = commands.Bot(command_prefix = ".", intents =discord.Intents.all(),case_insensitive = True,help_command= None)

colors = [0x0dd2ff,0x03f5ff,0x2affa9,0x18e6ff,0x17ffc2,0x03f5ff,0x30e79d]

os.environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")

client.load_extension('jishaku')
DATABASE_URL = os.environ["DATABASE_URL"]
    
async def create_db_pool():
    #client.pg_con = await asyncpg.create_pool(database = "Code Stacks",user = "postgres",password = "12382692")
    client.pg_con = await asyncpg.create_pool(DATABASE_URL,ssl = "require")

def ifpy(filename):
    for files in os.listdir('./fold'):
        if files.endswith('.py'):
            if filename == files[:-3]:
                ispy = True
                break
    else:   
        ispy = False
    return ispy

@client.command()
@commands.is_owner()
async def reload(ctx,extension = "onevent"):
    if ifpy(extension) == True:
        client.unload_extension(f"fold.{extension}")
        client.load_extension(f"fold.{extension}")
        try:    
            await ctx.message.delete()  
            await ctx.send("Done :)",delete_after = 3)
        except:

            pass
        
    else:
        await ctx.send("Incorrect filename :( ",delete_after  = 3)

for files in os.listdir('./fold'):
    if files.endswith('.py'):
        client.load_extension(f"fold.{files[:-3]}")


client.loop.run_until_complete(create_db_pool())

async def determine_prefix(bot, message):
    guild_id = message.guild.id
    
    prefix = await client.pg_con.fetchrow("SELECT prefix FROM guild WHERE guildid = $1",guild_id)
    return [prefix[0]]

client.command_prefix = determine_prefix
client.run(os.environ["TOKEN"])   

