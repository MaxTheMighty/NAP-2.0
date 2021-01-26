import asyncio
import json
from typing import Dict
import discord 




async def save(bot_data):
    with open('bot_file.json','w+') as file:
        json.dump(bot_data,file,indent=2)

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



