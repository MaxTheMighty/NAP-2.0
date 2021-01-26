

from logging import log
import discord
import discord.ext.commands as commands
import os
import dotenv as dev
import json
import AdminCog
import asyncio
import Utility

#---------------variables---------------

bot_data = None
log = []
current_status = ""

#---------------init--------------------
dev.load_dotenv(dotenv_path = ".//keys.env")

bot = discord.ext.commands.Bot(command_prefix = '!', activity = discord.Game(name = current_status),help_command=None)


DISCORD_KEY = os.getenv("DISCORD_KEY")
with open("bot_file.json", 'r+') as file:
    bot_data = json.load(file)


    
#--------------on ready----------------

@bot.event
async def on_ready():
    bot.load_extension('AdminCog')
    bot.load_extension('AudioCog')
    bot.load_extension('FunCog')
    bot.load_extension('UsefulCog')
    print("Ready!")

    
#---------------commands that need to stay here--------------
@bot.command(is_owner=True, hidden= True)
async def reload(ctx):
    await Utility.save(bot_data,log)
    for cog in bot.cogs.copy():
        bot.reload_extension(cog)
#------------------------events-----------------------------

#-----------------------Listener-----------------------------

#make sure it isnt ran when importing from adminCog
if __name__ == '__main__':
    bot.run(DISCORD_KEY)
