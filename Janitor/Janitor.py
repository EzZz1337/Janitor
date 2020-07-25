import discord
from discord.ext import commands
from discord.ext.commands import Bot
from datetime import datetime, time, timedelta
from Token import * # import Token



client: Bot = commands.Bot(command_prefix='c!')
client.remove_command('help')



@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='your chat')) # change activity
    print('Ready!')



@client.command() # info cmd
async def info(ctx):
    bot = client.get_user(703598893606109244)
    await ctx.send(f'{bot.mention} is an anti-spambot, that keeps your chat(s) clean.')





@client.event # main event
async def on_message(message):
    role = discord.utils.get(message.guild.roles, name='Moderator') # Mod Role
    msg_list = await message.channel.history(limit=10).flatten() # get last 10 msgs in the channel
    time1 = msg_list[0].created_at.strftime('%Y:%m:%d:%H:%M:%S')
    time2 = msg_list[-1].created_at.strftime('%Y:%m:%d:%H:%M:%S')
    n1 = time(hour=0, minute=0, second=10).strftime('%Y:%m:%d:%H:%M:%S')
    n2 = time(hour=0, minute=0, second=2).strftime('%Y:%m:%d:%H:%M:%S')
    fmt = '%Y:%m:%d:%H:%M:%S'
    delta = datetime.strptime(time1, fmt) - datetime.strptime(time2, fmt)
    delta2 = datetime.strptime(n1, fmt) - datetime.strptime(n2, fmt)
    bot = client.get_user(703598893606109244)
    try:
        if message.author == bot:
            return
        if message.channel.slowmode_delay == 21600: 
            await message.delete()
            return
        else:
            if delta < delta2:
                for msg in msg_list:
                    if msg.author == bot:
                        pass
                    else:
                        await msg.delete()
                        await message.channel.edit(slowmode_delay=21600)
                await message.channel.send(f'{role.mention}') # ping the mod role
            else:
                pass
        await client.process_commands(message) # makes other cmds work
    except discord.errors.NotFound: # in case a msg 404s 
        pass



client.run(TOKEN) # end