import os  #To access environment variables/ .env files
import discord
from dotenv import load_dotenv  #Library for working with .env files, load_dotenv() loads environment variables
                                #from a .env file into your shell’s environment variables so that you can use them in your code.
import random #To access random.choice
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix = '!') #Bot is a subclass, Client is a superclass

@bot.event #Event handler for when the Bot has made a connection to Discord and prepared its response data using client.event decorator
async def on_ready():
    guild = discord.utils.get(bot.guilds, name = GUILD)
    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event #Event handler for when a new user joins the guild
async def on_member_join(member):
    await member.create_dm() #await suspends the execution of the surrounding coroutine until the execution of each coroutine has finished
    await member.dm_channel_send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@bot.command(name = 'roll_dice', help = 'Simulates a rolling dice')
async def roll(ctx, number_of_sides: int, number_of_dice: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for i in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name = 'DN', help = 'Responds with a random quote from Death Note')
async def death_note(ctx): #ctx = context, A Context holds data such as the channel and guild that the user called the Command from

    death_note_quotes = [
    '“This world is rotten, and those who are making it rot deserve to die. Someone has to do it, so why not me?” - Light Yagami',
    '“When you die, I will be the one writing your name in my Death Note.“ - Ryuk',
    '“I am justice!” - Light Yagami and L Lawliet',
    '“I’ll take a potato chip AND EAT IT!” - Light Yagami',
    '"Yagami-san, if I die in the next few days, your son is Kira.” - L Lawliet',
    '”He who strikes first wins.” - L Lawliet',
    '"The human whose name is written in this note shall die." - First rule of the Death Note',
    '“An eye for an eye my friend” - L Lawliet',
    '“In all things, one cannot win with defense alone. To win, you must attack.” - Light Yagami',
    '“Kira is childish and he hates losing... I am also childish and I hate to lose. That is how I know.” - L Lawliet']

    response = random.choice(death_note_quotes)
    await ctx.send(response)

@bot.command(name = 'create_channel', help = 'To create a new discord channel')
@commands.has_role('King')
async def create_channel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name = channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)
