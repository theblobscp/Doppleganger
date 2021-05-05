import asyncio
import discord
from discord.ext import commands
import random
from discord.ext.commands.core import command
import praw
import wolframalpha
from youtubesearchpython import SearchVideos
from pytube import YouTube
from bot import colors
from youtube_search import YoutubeSearch
import animec
import os

colors=[1752220,3066993,3447003,10181046,15844367,15105570,15158332,16580705]
client1 = wolframalpha.Client("LH6XXP-3U64EU2EHX") 
reddit = praw.Reddit(client_id = "laqA2QEwsdXP9A",
                    client_secret = "z6NHXe06ch_h8Iyn2mtbn1FkIJ4pfg",
                    username  = "DopplegangerCode ",
                    password = "elpsycongree",
                    user_agent = "pythonpraw", check_for_async=False)

memes = ['programminghumor','animememes','weebmemes','goodanimemes','danidev','funnymeme','sarcasticmemes','lolmemes','codinghumor']


class Search(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(aliases = ['lyric'])
    async def lyrics(self,ctx,*,song):
        url = animec.sagasu._searchLyrics_(song)
        await ctx.send(url)

    @commands.command(aliases = ['me'])
    async def meme(self,ctx):
        try:
            subreddit = reddit.subreddit(random.choice(memes)) 
            all_subs = []
            top = subreddit.top(limit = 100)

            for submission in top:
                all_subs.append(submission)

            random_sub = random.choice(all_subs)

            embed = discord.Embed(title = random_sub.title, color = random.choice(colors))
            embed.set_image(url = random_sub.url)
            embed.set_footer(text = f"Requested by {ctx.author.display_name}", icon_url = ctx.author.avatar_url)
            
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send(e)
            em = discord.Embed(title = "No Meme Found :sob:",color = random.choice(colors))
            await ctx.send(embed = em)

    
    @commands.command()
    async def song(self,ctx, *, songname):
        
        result = YoutubeSearch(songname, max_results=1).to_dict()
        name = result[0]["title"]
        url = "http://www.youtube.com"+result[0]["url_suffix"]
        try:
            
            yt = YouTube(url)
            print("trying")
            ys = yt.streams.filter(only_audio=True).first().download()
            print("Downloading")
            audio = name + ".mp3"
            os.rename(name+".mp4", audio)
            await ctx.send(file = discord.File(audio))
            os.remove(audio)
        
        except Exception as e:
            await ctx.send(embed  =discord.Embed(description = "Song Couldn't be Found :(",color = discord.Colour.red()))
              

    @commands.command(aliases = ['img'])
    async def image(self,ctx,*,query):
        try:
            animeresult = animec.charsearch(query)
            title = animeresult.title
            url = animeresult.image_url
            embed = discord.Embed(title = title,color =random.choice(colors))
            embed.set_image(url = url)
            await ctx.send(embed = embed)
        except:
            await ctx.send(embed = discord.Embed(title ="No result found !! :sob:",color = discord.Color.red()))

    @commands.command(aliases = ['que'])
    async def ques(self,ctx,*,ques):
        emerror = discord.Embed(title ="No result found !! :sob:",color = discord.Color.red())
        ques = ques.lower()
        if "who made you" in ques or "who created you" in ques or "who is your creator"in ques :
            em = discord.Embed(title = f"Question : "+ ques +":question:",
                        description = f"answer : "+ "I was made by Code Stacks the great right in his PC!!"+ ":exclamation:",color = random.choice(colors))
            await ctx.send(embed = em) 
        else: 
            try:
                res = client1.query(ques)
                answer = next(res.results).text
            
                em = discord.Embed(title = f"Question : "+ ques +":question:",
                            description = f"answer : "+ str(answer)+ ":exclamation:",color = random.choice(colors))
                await ctx.send(embed = em)  
            except:
                await ctx.send(embed = emerror)
    

    @commands.command(aliases =['yo'])
    async def youtube(self,ctx,*,msg):
        try:
            a = discord.Embed(title ="**Top Results for ** your search :", color = random.choice(colors)  )  
            await ctx.send(embed = a)          
            results = SearchVideos(msg,mode="dict",max_results =1)
            d = discord.Embed(title ='**'+results.result()['search_result'][0]['title']+'**'+'\n'+"Channel : "+results.result()['search_result'][0]['channel']+'\n'+'Duration : '+str(results.result()['search_result'][0]['duration'])+'\n'+'Views : '+str(results.result()['search_result'][0]['views'])+'\n'+"Publish Time : " +str(results.result()['search_result'][0]['publishTime'])+'\n',color = random.choice(colors))
            await ctx.send(embed = d)
            await ctx.send('Link : '+results.result()['search_result'][0]['link']) 
        except Exception as e:
            print(e)
            c = discord.Embed(title ="No results found :sob:",color = discord.Color.red()    )
            await ctx.send(embed = c)
    





def setup(client):
    client.add_cog(Search(client))



