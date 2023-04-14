import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import tracemalloc

# Load environment variables from .env file
load_dotenv()

# Get bot token from environment variable
TOKEN = os.getenv('BOT_TOKEN')

# Define intents
intents = discord.Intents.all()

# Create bot instance
bot = commands.Bot(command_prefix='-', intents=intents)


# Load cogs on startup
@bot.event
async def on_ready():
    print('Bot is ready.')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'{filename[:-3]} loaded successfully.')
            except Exception as e:
                print(f'Error loading {filename}: {e}')


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

