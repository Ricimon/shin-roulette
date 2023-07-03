import logging
import os

from cogwatch import watch
import discord
from discord.ext import commands
from dotenv import load_dotenv

from shin_roulette.init_logging import init_logging


class RouletteBot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned,
                         intents=intents)

    @watch(path="shin_roulette/cogs", preload=True)
    async def on_ready(self):
        logging.info('Logged in as %s (ID: %s)', bot.user, bot.user.id)

    async def setup_hook(self):
        testing_guild_id = os.getenv("TEST_GUILD_ID")
        if testing_guild_id:
            testing_guild = discord.Object(id=testing_guild_id)
            bot.tree.copy_global_to(guild=testing_guild)


if __name__ == '__main__':
    load_dotenv()  # take environment variables from .env

    init_logging()

    bot = RouletteBot()

    bot.run(os.getenv("DISCORD_TOKEN"))
