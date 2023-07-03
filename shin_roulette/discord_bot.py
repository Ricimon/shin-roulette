import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')

intents = discord.Intents.default()
intents.message_content = True

extensions = ['cogs.sync', 'cogs.roulette']

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')


@bot.event
async def setup_hook():
    for extension in extensions:
        await bot.load_extension(extension)
    testing_guild_id = os.getenv("TEST_GUILD_ID")
    if testing_guild_id:
        testing_guild = discord.Object(id=testing_guild_id)
        bot.tree.copy_global_to(guild=testing_guild)


if __name__ == '__main__':
    load_dotenv()  # take environment variables from .env

    bot.run(os.getenv("DISCORD_TOKEN"), log_handler=handler)
