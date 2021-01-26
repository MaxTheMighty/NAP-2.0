import asyncio
import json
from typing import Dict
import discord 
import NAP

bot_file = open('bot_file.json','w+')
log_file = open('commands.log','a')

async def save(bot_data,log):
    if(bot_file.closed):
        bot_file = open('bot_file.json','w+')
    if(log_file.closed):
        log_file = open('commands.log','a')
    json.dump(bot_data,bot_file,indent=2)
    log_file.writelines(log)

    NAP.log.clear()


async def create_user(bot_data: Dict,user: discord.User):
    bot_data['users'].update(
        {
            f'{user.id}': {
                'name':user.name,
                'intro_url':None,
                'intro_boolean':False,
            }
        }
    )



