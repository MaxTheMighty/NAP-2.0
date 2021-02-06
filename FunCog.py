from inspect import unwrap
import discord
import discord.ext.commands as commands
from discord.ext.commands.core import is_owner
import discord.ext.tasks as tasks
import NAP
import Utility
import asyncio
import random
import os
import requests
# import openai
import dotenv as dev
dev.load_dotenv(dotenv_path = ".//keys.env")
#openai.api_key = os.getenv("OPEN_API_KEY")
BING_KEY = os.getenv("BING_KEY")
class FunCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(description = "Waterboards the user")
    async def waterboard(self,ctx):
        if(len(ctx.message.mentions) > 0):
            user: discord.User = ctx.message.mentions[0]
        else:
            raise TypeError("User to waterboard required!")
        if(user.voice.channel == None):
            raise TypeError("That user is not in a call!")
        original = user.voice.channel
        channels = ctx.guild.voice_channels
        for i in range(5):
            choice = channels.pop(random.randrange(0,len(channels)))
            await user.move_to(choice)
            await asyncio.sleep(0.6)
        await user.move_to(original)
       
    @commands.command(description = "Turns your sentence into a picture story")
    async def image(self, ctx):
        message = (ctx.message.content[7:])
        if(len(message) > 50):
            await ctx.send(embed = discord.Embed(title = "**ERRORR**", description = "Your phrase is too long"))
            return 0
        path = await Utility.download_image(message,message,key=BING_KEY) # ? 
        if(path == 403):
            await ctx.send(embed = discord.Embed(title = "**ERORR**", description = "We have hit the rate limit for the month"))
            return 0
        if(path == -1):
            await ctx.send(embed = discord.Embed(title = "**ERRORR**", description = "No results were found"))
            return 0
        await ctx.send(file=discord.File(fp=str(path)))
        os.remove(path)

    @commands.command(brief = 'Shows the astronomy photo of the day', description = 'Shows the astronomy photo of the day, with a descrption of what it is. Click on the title for the full image')
    async def APOD(self, ctx, date = ""):
        print(f"{ctx.author.name} called APOD in {ctx.author.guild}")
        url = "https://api.nasa.gov/planetary/apod?api_key=ZOxwHM1HExgU20UziqLTpB2kTSklr2yjm7OWD3DO"
        if not date == "":
            url+="&date=" + date
            #print(key)
        stor = requests.get(url).json() 
        if('code' in stor):
            await ctx.send(f"`{stor['msg']}`")
            return
        urlCond = 'hdurl' if 'hdurl' in stor else 'url'

        imageOutput = discord.Embed(title = stor['title'],url = stor[urlCond], color = discord.Color.purple())
        if stor['media_type'] == "video":
            imageOutput.add_field(name = "Video", value=stor[urlCond])
        else:
            imageOutput.set_image(url = stor[urlCond])
        explanationTrunc = (stor['explanation']) if len(stor['explanation']) < 1024 else stor['explanation'][:1021] + "..."
        imageOutput.add_field(name = "Description", value = f"{explanationTrunc}")
       
        await ctx.send(embed = imageOutput)


def setup(bot):
    print("Adding Fun")
    bot.add_cog(FunCog(bot))
   