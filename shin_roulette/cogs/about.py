"""
A cog to add a command for printing info about the bot.
"""

import importlib.metadata
import logging

import discord
from discord.ext import commands
from discord.ext.commands import Context


class AboutCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def about(self, ctx: Context) -> None:

        logging.debug('about command used')

        version = importlib.metadata.version('shin-roulette')
        await ctx.send(
            f'Shin Roulette v{version}\nhttps://github.com/Ricimon/shin-roulette'
        )


async def setup(bot):
    await bot.add_cog(AboutCog(bot))
