import os

from dotenv import load_dotenv
from interactions import Intents
from interactions.ext import prefixed_commands

from core.init_logging import init_logging
from core.base import CustomClient
from core.extensions_loader import load_extensions

#@bot.event
#async def setup_hook():
#    for extension in extensions:
#        await bot.load_extension(extension)
#    testing_guild_id = os.getenv("TEST_GUILD_ID")
#    if testing_guild_id:
#        testing_guild = discord.Object(id=testing_guild_id)
#        bot.tree.copy_global_to(guild=testing_guild)

if __name__ == '__main__':
    load_dotenv()  # take environment variables from .env

    init_logging()

    bot = CustomClient(intents=Intents.DEFAULT, auto_defer=True)
    prefixed_commands.setup(bot)

    load_extensions(bot=bot)
    bot.load_extension("interactions.ext.jurigged")

    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
