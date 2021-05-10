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

    @commands.command(aliases = ['anilyrics'])
    async def lyrics(self, ctx, *, arg):   
        try:    
            await ctx.trigger_typing()

            if arg.lower() == "types":
                await ctx.send(embed = discord.Embed(title = "Available Lyrics Types", description = "Romaji | Kanji | English", color = discord.Color.green()))
                return
    
            if "romaji" in arg.lower():
                song = arg.lower().replace("romaji", "")
                lyrics = animec.anilyrics(song)
                lang = lyrics.romaji
            
            if "english" in arg.lower():
                song = arg.lower().replace("english", "")
                lyrics = animec.anilyrics(song)
                lang = lyrics.english           
            
            if "kanji" in arg.lower():
                song = arg.lower().replace("kanji", "")
                lyrics = animec.anilyrics(song)
                lang = lyrics.kanji
            
            if not any(i in arg for i in ['romaji','english','kanji']):
                song = arg  
                lyrics = animec.anilyrics(arg)
                lang = lyrics.romaji
            
            name_list = lyrics.url.split("/")
            name = name_list.pop(len(name_list) - 1)
            try:
                name = name.replace("-", " ").title()
            except:
                name = name.title()

            if len(lang) >= 2048:
                e1 = discord.Embed(title = name, description = lang[:2000], url = lyrics.url, color = 0xD9A7D4)
                e2 = discord.Embed(title = name, url = lyrics.url, description = lang[2000:], color = 0xD9A7D4)
                if len(lang) >= 2048 * 3:
                    e3 = discord.Embed(title = name, url = lyrics.url, description = lang[4000:], color = 0xD9A7D4)
                msg = await ctx.send(embed = e1)
                await msg.add_reaction("⏪")
                await msg.add_reaction("⏩")
                
                def check(reaction, user):
                    return reaction.message.id == msg.id and user == ctx.author

                page = 1

                while True:
                    try:
                        reaction, _ = await self.client.wait_for('reaction_add', timeout= 200.0, check=check)

                        if reaction.emoji == "⏩":
                            page += 1
                            if page == 1:
                                em = e1
                            elif page == 2:
                                em = e2
                            elif page == 3:
                                try:
                                    em = e3
                                except:
                                    em = e2
                            await msg.edit(embed = em)
                            await msg.remove_reaction("⏩", ctx.author)

                        if reaction.emoji == "⏪":
                            page -= 1
                            if page == 1:
                                em = e1
                            elif page == 2:
                                em = e2
                            elif page == 3:
                                try:
                                    em = e3
                                except:
                                    em = e2
                            await msg.edit(embed = e1)
                            await msg.remove_reaction("⏪", ctx.author)

                    except asyncio.TimeoutError:
                        await msg.clear_reactions() 
            
            else:
                embed = discord.Embed(title = name, description = lang, url = lyrics.url, color = 0xD9A7D4)
                embed.set_footer(text = f"Requested By: {ctx.author}")
                await ctx.send(embed = embed)
        except animec.sagasu.NoResultFound:
            await ctx.send(embed = discord.Embed(description = "No lyrics for such song found.", color = discord.Color.green()))
        
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



