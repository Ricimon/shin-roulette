import asyncio
import logging
import os

from cogwatch import watch
import discord
from discord.ext import commands
from dotenv import load_dotenv

from shin_roulette.core.init_logging import init_logging


class RouletteBot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned,
                         intents=intents)

    @watch(path="shin_roulette/cogs", preload=True)
    async def on_ready(self):
        logging.info('Logged in as %s (ID: %s)', self.user, self.user.id)
        await self.change_presence(activity=discord.Game("/roulette"))

    async def setup_hook(self):
        testing_guild_id = os.getenv("TEST_GUILD_ID")
        if testing_guild_id:
            testing_guild = discord.Object(id=testing_guild_id)
            self.tree.copy_global_to(guild=testing_guild)


async def main():
    # take environment variables from .env
    load_dotenv()

    # suppress an irrelevant warning
    discord.VoiceClient.warn_nacl = False

    # initialize generic logging
    init_logging()

    # initialize discord.py console logging
    discord.utils.setup_logging(level=logging.INFO, root=False)

    client = RouletteBot()

    await client.start(os.getenv("DISCORD_TOKEN"))


if __name__ == '__main__':
    asyncio.run(main())
