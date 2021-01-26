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
import openai
import dotenv as dev
dev.load_dotenv(dotenv_path = ".//keys.env")
openai.api_key = os.getenv("OPEN_API_KEY")

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



    #BE VERY CAREFUL WITH THIS
    @commands.command(is_owner=True,hidden=True)
    async def think(self,ctx):
        question = ctx.message.content[7:]
        question_send = f"""Marv is a chatbot that reluctantly answers questions.\n
###
User: How many pounds are in a kilogram?
Marv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.
###
User: What does HTML stand for?
Marv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.
###
User: {question}?
Marv: """
        # print(question_send)
        resp = openai.Completion.create(
            engine="davinci",
            prompt=question_send,
            max_tokens=50,
            temperature=0.8,
            top_p=0.7,
            stop='###'
        )
        # print(resp)
        answer = resp.choices[0]['text']
        print(answer)
        try:
            await ctx.send(answer)
        except discord.errors.HTTPException:
            await ctx.send("ERROR: No response")

def setup(bot):
    print("Adding Fun")
    bot.add_cog(FunCog(bot))
   