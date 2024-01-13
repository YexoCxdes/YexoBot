import discord
from discord.ext import commands
from discord.utils import get
import random
import os
import asyncio
import json

configfile = open('data/data.json')
data = json.load(configfile)

prefix = data["PREFIX"]
token = data["TOKEN"]
owner = data["OWNER"]
botaccess = data["BOTACCESS"]
intents = discord.Intents.all()
snipe_message_content = None
snipe_message_author = None
no_access_embed = discord.Embed(title="404", description="You cannot run the given command.", colour=discord.Colour.blurple())
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')

# Event when the bot is online.
@bot.event
async def on_ready():
    print(f'Logged on as {bot.user.name} with a prefix as {prefix}')
# Developer

# Snipe
@bot.event
async def on_message_delete(message):
    global snipe_message_content
    global snipe_message_author

    snipe_message_content = message.content
    snipe_message_author = message.author.name
    await asyncio.sleep(180)
    snipe_message_content = None
    snipe_message_author = None

@bot.command(aliases=["snipe"])
async def s(message):
    if message.author.id in botaccess:
        if snipe_message_content == None:
            embed = discord.Embed(
                title='Sniped message',
                description=f'Most recent deleted message within 3 minutes',
                colour=discord.Colour.blurple()
            )
            embed.add_field(name='No recently deleted messages', value=f' ',inline=False)
            embed.add_field(name='Author', value=f'None',inline=False)
            embed.add_field(name='Message', value=f'None',inline=False)
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title='Sniped message',
                description=f'Most recent deleted message within 3 minutes',
                colour=discord.Colour.blurple()
            )
            embed.add_field(name='Author', value=f'{snipe_message_author}',inline=False)
            embed.add_field(name='Message', value=f'{snipe_message_content}',inline=False)
            await message.channel.send(embed=embed)
    else:
        await message.channel.send(embed=no_access_embed)

# Vouches

@bot.command()
async def vouches(ctx):
    f = open('vouches.txt', 'r')
    vouches = -1
    lines = len(f.readlines())
    
    for i in range(lines):
        vouches += 1
    print(vouches)    
    
    embed = discord.Embed(title=f"There are `{vouches}` vouches",
                      description=f"On Yexo Tools",
                      colour=0xfd00be)

    embed.set_author(name="text")

    await ctx.send(embed=embed)
    f.close()

@bot.command()
async def vouch(ctx, *, vouch):
    f = open('vouches.txt', 'a')
    f.write(f'\nVouch added by {ctx.author.name} : {vouch}')
        
    await ctx.send('Vouch added!')
    f.close()

@bot.command()
async def vouchreset(ctx):
    if ctx.author.id == owner:
        f = open('vouches.txt', 'w')
        f.write('idk why but just need it lmao')
        await ctx.send('👍')
    else:
        await ctx.send(embed=no_access_embed)

# End of vouches

# Status
@bot.command()
async def play(ctx, *, stat):
    if ctx.author.id in botaccess:

        await bot.change_presence(activity=discord.Game(name=stat))
        await ctx.send(f'Changed status to `{stat}`')
    else:
        await ctx.send(embed=no_access_embed)

@bot.command()
async def listen(ctx, *, stat):
    if ctx.author.id in botaccess:

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=stat))
        await ctx.send(f'Changed status to `{stat}`')
    else:
        await ctx.send(embed=no_access_embed)

@bot.command()
async def stream(ctx, *, stat):
    if ctx.author.id in botaccess:

        await bot.change_presence(activity=discord.Streaming(name=stat, url='https://twitch.tv/yexo____'))
        await ctx.send(f'Changed status to `{stat}`')
    else:
        await ctx.send(embed=no_access_embed)
# End of status

# Developer Text
@bot.command()
async def clear(ctx, *, amount: int=None):
    if ctx.author.id in botaccess:
        if amount is None:
            await ctx.send(f'Put a value.')
            return
        async for message in ctx.message.channel.history(limit=amount):
            try:
                await message.delete()

            except:
                pass
            print(f"Message Deleted ")
    else:
        await ctx.send(embed=no_access_embed)

@bot.command()
async def shutdown(ctx):
    if ctx.author.id == owner:
        await ctx.send('Shutting down')
        await bot.close()
    else:
        await  ctx.send(embed=no_access_embed)

# Text
@bot.command(aliases=['Rand', 'Random', 'random'])
async def rand(ctx, number1: int, number2: int):
    number = random.randint(number1, number2)
    await ctx.send(f'Random number between `{number1}` and `{number2}` is `{number}`')

@bot.command()
async def say(ctx, *, msg):
    await ctx.send(msg)

# Misc
@bot.command(aliases=['Ping', 'delay', 'Delay'])
async def ping(ctx):
    ping = f'{round(bot.latency * 1000)}ms'
    await ctx.send(ping)

# Help command
@bot.command(aliases=['commands', 'Commands', 'Help'])
async def help(ctx):
    
    embed = discord.Embed(
        title='Help',
            description=f'Prefix is `{prefix}`',
        colour=discord.Colour.blurple()
    )
    embed.add_field(name='⌨ Text', value=' ',inline=False)
    embed.add_field(name='🎲 Misc', value=' ', inline=False)
    embed.add_field(name='👨‍💻 Developer', value='Developer only', inline=False)


    await ctx.send(embed=embed)

@bot.command(aliases=['Text'])
async def text(ctx):
    embed = discord.Embed(
        title='Help',
        description='Text commands',
        colour=discord.Colour.blurple()
    )
    embed.add_field(name=f'`{prefix}rand <number1> <number2>`', value='Generates a random number between number 1 and number 2', inline=False)
    embed.add_field(name=f'`{prefix}say <text>`', value='Bot says your text')

    await ctx.send(embed=embed)

@bot.command(aliases=['Misc'])
async def misc(ctx):
    embed = discord.Embed(
        title='Help',
        description='Misc commands',
        colour=discord.Colour.blurple()
    )
    embed.add_field(name=f'`{prefix}ping`', value='Sends the bots latency', inline=False)

    await ctx.send(embed=embed)

@bot.command(aliases=['Dev', 'Developer', 'developer'])
async def dev(ctx):
    if ctx.author.id == owner:
        embed = discord.Embed(
            title='Help',
            description='Dev commands',
            colour=discord.Colour.blurple()
        )
        embed.add_field(name=f'`{prefix}listen <text>`', value=f'Sets the bots status to `Listening to <text>`', inline=False)
        embed.add_field(name=f'`{prefix}play <text>`', value=f'Sets the bots status to `Playing <text>`', inline=False)
        embed.add_field(name=f'`{prefix}stream <text>`', value=f'Sets the bots status to `Streaming <text>`', inline=False)
        embed.add_field(name=f'`{prefix}clear <number>`', value=f'Deletes <number> messages', inline=False)
        embed.add_field(name=f'`{prefix}snipe`', value=f'Sends the most recent deleted message within 3 minutes', inline=False)



        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=no_access_embed)

bot.run(token)
