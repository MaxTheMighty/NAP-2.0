from discord.ext.commands.core import is_owner
from AudioCog import AudioCog
from attr import __description__, __title__
import discord
import asyncio
import NAP
import discord.ext.commands as commands
import discord.ext.tasks as tasks
import Utility
import re
import traceback
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
        await Utility.save(self.log)
        await self.bot.close()

    @commands.command(is_owner=True,hidden = True)
    async def getcogs(self,ctx):
        cogs = self.bot.cogs.keys()
        str = ("".join(f"`{x}`\n" for x in cogs))
        out = discord.Embed(title = "Cogs", description=str)
        await ctx.send(embed = out)

    @commands.command(is_owner=True,hidden = True)
    async def save(self,ctx):
        await Utility.save(log = self.log)



    # @tasks.loop(minutes=60)
    # async def check_ban(self):
    #     for user in bannedUsers:
    #         if(user.banTime - currentTime >= 24 hours):
    #             bannedUsers.remove(user)
    #             #remove role so they can speak
    @tasks.loop(minutes=15)
    async def autosave(self):
        print("Auto saving")
        await Utility.save(self.log)

    @commands.Cog.listener()
    async def on_command_error(self,ctx, error, *args, **kwargs):
        #this can be much better
        errorChannel = self.bot.get_channel(746100508825092157)
        errorOut = discord.Embed(title=':x: Command Error', colour=0xe74c3c) #Red
        errorOut.timestamp = dt.datetime.utcnow()
        if isinstance(error, commands.CommandOnCooldown):
            print("A command was called when it was on cooldown")
            emOut = discord.Embed(title = "**ERROR**", description = "That command is on a cooldown, try again in `{:.2f}` seconds (this command has a `{:.0f}` second cooldown)".format(error.retry_after, error.cooldown.per), color = discord.Colour.red())
            await ctx.send(embed = emOut)  
        elif isinstance(error, commands.NotOwner):
            await ctx.send(embed = discord.Embed(title = "**ERROR**", description = "That command is for owners only", color = discord.Colour.red()))
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error,commands.BadArgument):
            await ctx.send(embed = discord.Embed(title = "**ERROR**", description = "Invalid input!", color = discord.Colour.red()))

        else:
            errorOut.description = '```py\n%s \n```' % error
            print(error)
            await errorChannel.send(traceback.format_exc())
            await errorChannel.send(embed = errorOut)

    @commands.Cog.listener()
    async def on_command(self,ctx):
        str = f"[{dt.datetime.now()}] {ctx.author.name} called {ctx.message.content} in {ctx.guild.name}\n"
        self.log.append(str)

    @commands.command(is_owner=True,hidden=True)
    async def dump(self,ctx, count=-1, filename="dump"):
        server = ctx.guild
        mentions = ctx.message.mentions
        if(len(mentions) > 0):
            user = mentions[0]
        else:
            user = None
        msg_count = int(count)
        with open(f"./{filename}.txt","w+",encoding='utf8') as f:
            for channel in server.text_channels:
                async for message in channel.history(limit = (None if msg_count == -1 else msg_count)):
                    if(len(message.content) <= 0 or message.content[0] == '!' or message.author.bot):
                        continue
                    
                    if(user != None and user != message.author):
                        continue
                    cont = message.clean_content.replace('@','')
                    if 'http' in cont:
                        cont = re.sub(r'http\S+', '', cont)
                    f.write(cont+'\n')



def setup(bot):
    print("Adding Admin")
    bot.add_cog(AdminCog(bot))