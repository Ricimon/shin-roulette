"""
A cog for the roulette slash command.
"""

import discord
from discord import app_commands
from discord.ext import commands


class RouletteCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def roulette(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Shin Roulette",
            Description="React with ✅ to join.",
        )
        await interaction.response.send_message(
            f'Hi, {interaction.user.mention}')


async def setup(bot):
    await bot.add_cog(RouletteCog(bot))
