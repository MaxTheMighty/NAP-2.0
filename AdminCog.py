from discord.ext.commands.core import is_owner
from AudioCog import AudioCog
from attr import __title__
import discord
import asyncio
import NAP
import discord.ext.commands as commands
import discord.ext.tasks as tasks
import Utility
import re

import datetime as dt

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_data = NAP.bot_data
        self.bot_key = NAP.DISCORD_KEY
        self.log = NAP.log
        self.autosave.start()
        
    @commands.command(is_owner=True,hidden = True)
    async def updatestatus(self,ctx):
        new_status = ctx.message.content[14:]
        self.bot_data['meta']['current_status'] = new_status
        await self.bot.change_presence(status=discord.Status.online, activity = discord.Game(name=new_status))

    @commands.command(is_owner=True,hidden = True)
    async def shutdown(self,ctx):
        await Utility.save(self.bot_data,self.log)
        await self.bot.close()

    @commands.command(is_owner=True,hidden = True)
    async def getcogs(self,ctx):
        cogs = self.bot.cogs.keys()
        str = ("".join(f"`{x}`\n" for x in cogs))
        out = discord.Embed(title = "Cogs", description=str)
        await ctx.send(embed = out)

    @commands.command(is_owner=True,hidden = True)
    async def save(self,ctx):
        await Utility.save(self.bot_data,self.log)


    @tasks.loop(minutes=15)
    async def autosave(self):
        print("Auto saving")
        await Utility.save(self.bot_data,self.log)

    @commands.command(is_owner=True)
    async def t(self,ctx):
        pass


    @commands.Cog.listener()
    async def on_command(self,ctx):
        str = f"[{dt.datetime.now()}] {ctx.author.name} called {ctx.message.content} in {ctx.guild.name}\n"
        self.log.append(str)

    @commands.command(is_owner=True,hidden=True)
    async def dump(self,ctx, count, filename):
        server = ctx.guild
        with open(f"./{filename}.txt","w+",encoding='utf8') as f:
            for channel in server.text_channels:
                async for message in channel.history(limit = (None if int(count) == -1 else int(count))):
                    if(len(message.content) <= 0 or message.content[0] == '!' or message.author.bot):
                        continue
                    cont = message.clean_content.replace('@','')
                    if 'http' in cont:
                        cont = re.sub(r'http\S+', '', cont)
                    f.write(cont+'\n')

        

def setup(bot):
    print("Adding Admin")
    bot.add_cog(AdminCog(bot))