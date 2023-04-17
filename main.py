import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import tracemalloc
from discord import Activity, ActivityType

# Load environment variables from .env file
load_dotenv()

# Get bot token from environment variable
TOKEN = os.getenv('BOT_TOKEN')

# Define intents
intents = discord.Intents.all()

# Create bot instance
bot = commands.Bot(command_prefix='-', intents=intents,help_command=None)


# Load cogs on startup
@bot.event
async def on_ready():
    print('Bot is ready.')
    await bot.change_presence(activity=Activity(type=ActivityType.listening, name='your mom moan'))
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'{filename[:-3]} loaded successfully.')
            except Exception as e:
                print(f'Error loading {filename}: {e}')

@bot.command()
async def statsguide(ctx):
    embed = discord.Embed(title="Command List", description="how do i use the bot ser?", color=0x00ff00)

    embed.add_field(name="-mmm #asset_number", value="query Militia NFT"
    "eg: -mmm #1 will display HM Monster #1", inline=False)
    embed.add_field(name="-prio #asset_number", value="query Prio Gang NFT"
    "eg: -prio #1 will display HM Prio Monster #1", inline=False)
    embed.add_field(name="-proto #asset_number", value="query Prototype NFT"
    "eg: -proto #1 will display HM Prototype #1", inline=False)

    await ctx.send(embed=embed)

# Catch errors and throw helpful explanations
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('Invalid command. Type !help for a list of available commands.')
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('Missing required argument.')
    elif isinstance(error, commands.errors.CommandOnCooldown):
        await ctx.send(f'This command is on cooldown. Please try again in {error.retry_after:.2f} seconds.')
    else:
        await ctx.send('An error occurred while executing the command.')


tracemalloc.start()

async def main():# Run the bot
    await bot.start(TOKEN)
asyncio.run(main())

