

from discord.errors import ClientException
import pytube
import discord.ext.commands as commands
import discord.ext.tasks as tasks
import discord
import NAP
import os
import asyncio
import Utility
class AudioCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(description = "Joins the call says BRUH")
    async def bruh(self,ctx):
        user = ctx.author
        mentions = ctx.message.mentions
        if(len(mentions)) > 0:
            user = mentions[0]
        await self.play_runner(user=user,source='.//Audio//bruh.mp3')

    @commands.command(description = "Joins the call and says BABABOOEY")
    async def booey(self,ctx):
        user = ctx.author
        mentions = ctx.message.mentions
        if(len(mentions)) > 0:
            user = mentions[0]
        await self.play_runner(user=user,source='.//Audio//bababooey.mp3')

    @commands.Cog.listener('on_voice_state_update')
    async def on_voice_state_update(self,member,before,after):
        if(before.channel == None and after.channel != before.channel):
            await self.play_intro(user=member)

    async def play_intro(self,user: discord.User):
        #lol remember when i said to follow PEP8 
        #print(NAP.bot_data['users'][f'{user.id}'])
        if(str(user.id) in NAP.bot_data['users'].keys() and not user.bot): 
            url = NAP.bot_data['users'][f'{user.id}']['intro_url']
            if(url is not None):
                if(NAP.bot_data['users'][f'{user.id}']['intro_boolean'] is True):
                    await self.play_runner(user,f'.//Audio//{url}.mp4')

    @commands.command(description = "Toggles your intro song on and off")
    async def toggleintro(self,ctx):
        user = ctx.author
        if(str(user.id) in NAP.bot_data['users'].keys()):
            toggle = NAP.bot_data['users'][f'{user.id}']['intro_boolean']
            NAP.bot_data['users'][f'{user.id}']['intro_boolean'] = not toggle
            await ctx.send(embed = discord.Embed(title = "Intro Status Changed", description = "Disabled" if toggle else "Enabled"))






    @commands.command(description = 'Sets your intro theme, requires a youtube URL')
    async def setintro(self,ctx,url):
        print("set intro called")
        if(f'{ctx.author.id}' not in NAP.bot_data['users'].keys()):
            await Utility.create_user(bot_data=NAP.bot_data,user=ctx.author)
        prev_url = NAP.bot_data['users'][f'{ctx.author.id}']['intro_url']
        if(prev_url != None):
            print(f"foudn previous url, deleteing, .//Audio//{prev_url}.mp4")
            #add a try {} except {} here for errors
            os.remove(f'.//Audio//{prev_url}.mp4')
        video_info = await self.download_song(url = url,fname = f'{ctx.author.name}{ctx.author.id%10000}',max=10)
        NAP.bot_data['users'][f'{ctx.author.id}']['intro_url'] = video_info[0]  
        NAP.bot_data['users'][f'{ctx.author.id}']['intro_boolean'] = True
        emOut = discord.Embed(title = "New Intro", description = f"{video_info[1]}")
        emOut.set_image(url = video_info[2])
        await ctx.send(embed = emOut)

    #this gets executed when someone joins a call and has intro set to true   
    async def play_runner(self,user,source):
        voice = user.voice
        if voice is None:
            raise TypeError("You are not in a call!")
        channel = voice.channel
        audio_source = discord.FFmpegOpusAudio(source)
        try:
            client = await channel.connect(reconnect=False)
        except ClientException:
            raise TypeError("Bot already in a call!")
        #this isnt async >:(
        client.play(audio_source)
        while(client.is_playing()):
            await asyncio.sleep(0.1)
        await client.disconnect(force = True)    


    async def download_song(self,url,fname,max = 1000):
        ytObj = pytube.YouTube(url=url)
        length = ytObj.length
        title = ytObj.title
        thumbnail = ytObj.thumbnail_url
        audio_streams = ytObj.streams.filter(only_audio=True)
        stream = audio_streams[0]
        # if(stream.filesize > 7500000):
        #    raise TypeError("The filesize is too big!")
        path = stream.download(output_path = ".//Audio", filename = fname)  
        print(f"downloading song {path}")
        print(path)
        if(length > max):
            process = await asyncio.create_subprocess_exec('ffmpeg', '-i',  f'{path}', '-c', 'copy', '-t' , '00:00:10.0',f'.//Audio//{fname}(t).mp4')
            await asyncio.sleep(4)
            os.remove(path)
            fname+='(t)'
            print(fname)
            
        return (fname,title,thumbnail)

def setup(bot):
    print("Adding Voice")
    bot.add_cog(AudioCog(bot))