import discord
from discord.channel import DMChannel
import discord.ext.commands as commands
import os
import requests
class UsefulCog(commands.Cog):
    def __init__(self,bot):    
        self.bot = bot

    @commands.Cog.listener('on_reaction_add')
    async def on_reaction_add(self,reaction,user):
        message: discord.Message = reaction.message
        if(reaction.emoji == '🔖' and not isinstance(message.channel,discord.DMChannel)):
            embeds: discord.Embed = message.embeds
            attachment: discord.Attachment = message.attachments
            file = None
            out = ""
            if(len(attachment) > 0 and attachment[0].size < 8_000_000):
                await attachment[0].save(f".//Temp//{user.id}{attachment[0].filename}")
                file = f".//Temp//{user.id}{attachment[0].filename}"
            if(len(message.content) > 0):
                out+=message.content
            out+=f"\n`from {message.author.display_name} in {message.guild.name} at {message.created_at}`"
            await user.send(embed = embeds[0] if embeds else None, content = out,file= discord.File(file,spoiler=attachment[0].is_spoiler()) if attachment else None)
            os.remove(file) if file != None else 0
        if(reaction.emoji == '❌' and isinstance(message.channel,discord.DMChannel)):
            await message.delete()


    @commands.command(description = "Displays information about the bot")
    async def help(self,ctx: commands.Context, command_in = None):
        if(command_in in (command.name for command in self.bot.commands)):
            await ctx.send("Parameters: `" + ' '.join(self.bot.get_command(command_in).clean_params.keys()) + "`")
            return
        help_embed = discord.Embed(title = "**COMMANDS**")
        commands = ""
        for command in self.bot.commands:
            choice = command
            if(choice.hidden):
                continue
            commands+=f"`{choice.name}`: {choice.description}\n\n"
        help_embed.add_field(name = "Commands", value = commands)
        await ctx.send(embed = help_embed)

    @commands.command(description = "Shows the status of a Minecraft Server")
    async def serverup(self,ctx: commands.Context, ip: str = "mc.hypixel.net"):
        
        url = "https://api.mcsrvstat.us/2/"+ip
        r = requests.get(url).json()
        if("hostname" not in r.keys()):
            await ctx.send(embed = discord.Embed(title = "**ERROR**", description = "Invalid IP!"))
            return
        msgout = discord.Embed(title = "Server status")
        msgout.add_field(name = "Status", value= "Online" if r['online'] else "Offline")
        if(r['online']):
            msgout.add_field(name = "Version", value = r['version'])
            msgout.set_footer(text = (f"{r['motd']['clean'][0]}"))
            msgout.add_field(name = "Player Count", value = f"{r['players']['online']}/{r['players']['max']}\n")
            if('list' in  r['players']):
                msgout.add_field(name = "Players", value = f"".join(f"`{x}`\n" for x in r['players']['list']))
        await ctx.send(embed = msgout)


def setup(bot):
    print("Adding UsefulCog")
    bot.add_cog(UsefulCog(bot))      