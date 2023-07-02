import logging
import discord
from discord.ext import commands

from shin_roulette.constants import DISCORD_BOT_TOKEN, TESTING_GUILD

handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')

intents = discord.Intents.default()

extensions = ['cogs.sync', 'cogs.roulette']

bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')


@bot.event
async def setup_hook():
    for extension in extensions:
        await bot.load_extension(extension)
    bot.tree.copy_global_to(guild=TESTING_GUILD)


if __name__ == '__main__':
    bot.run(DISCORD_BOT_TOKEN, log_handler=handler)
