import asyncio
import json
from typing import Dict
import discord 
import NAP
import requests
from pathlib import Path


async def save(log):

    with open('bot_file.json','w+') as file:
       json.dump(NAP.bot_data,file,indent=2)
    with open('commands.log','a+') as log_file:
        try:
            log_file.writelines(log)
        except UnicodeEncodeError:
            print("Unicode Decode Error, Passing!")

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

async def download_image(searchterm, filename,key):
    parameters = {"q": searchterm, "license":"public","imageType":"photo","safeSearch":"Off"}
    response = requests.get("https://api.bing.microsoft.com/v7.0/images/search",headers={"Ocp-Apim-Subscription-Key":key},params=parameters)
    print(response)
    responseJson = response.json()
    if(response.status_code == 403):
       return 403
    #this is so inefficient and bad, but i dont really care
    if(len(responseJson['value']) > 0):
        imageURL = responseJson['value'][0]
        print("value used")
    elif('relatedSearches' in responseJson.keys()):
        imageURL = responseJson['relatedSearches'][0]['thumbnail']
        print("related used")
    elif('queryExpansions' in responseJson.keys()):
        imageURL = responseJson['thumbnail'][0]
        print("query expansions")
    elif(len(responseJson['pivotSuggestions'][0]['suggestions']) > 0):
        imageURL = response['pivotSuggestions'][0]['suggestions'][0]['thumbnail']
        print("pivot")
    else:
        return -1
    photoDownload = requests.get(imageURL['thumbnailUrl']).content
    path = Path(f".//Images//{filename}.png")
    with open(path, 'wb') as file:
        file.write(photoDownload)
    return path


