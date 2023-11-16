"""
A cog for the roulette_again slash command
"""

import logging
import re

import discord
from discord.ext import commands

from shin_roulette.cogs import roulette


async def find_last_roulette_lobby(
        interaction: discord.Interaction,
        bot: commands.Bot) -> roulette.RouletteLobby:
    """
    This parses the text of the last-found bot message. This can break if roulette text formatting is changed.
    """
    try:
        roulette_lobby = roulette.RouletteLobby(None)
        channel = interaction.channel
        async for message in channel.history(limit=100):
            if message.author == bot.user:
                embed = message.embeds[0]

                if not embed.description or not embed.description.startswith(
                        'Fight:'):
                    return None

                players_text = embed.fields[0].value
                players = []
                for l in iter(players_text.splitlines()):
                    mention = re.search(r"(<@[0-9]+>)", l)
                    if mention:
                        players.append(mention[0])
                roulette_lobby.players = players

                if roulette_lobby.is_empty():
                    return None
                else:
                    return roulette_lobby
    except:
        raise
        return None


class RouletteAgainCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='rouletteagain')
    async def roulette_again(self, interaction: discord.Interaction):
        """
        Starts a roulette lobby with the same players
        """

        logging.debug('/rouletteagain used')

        last_lobby = await find_last_roulette_lobby(interaction, self.bot)
        if last_lobby is not None:
            await roulette.start_roulette_lobby(interaction, self.bot,
                                                last_lobby.players)
        else:
            await interaction.response.send_message(
                'Could not find a previously started lobby. Would you like to start a new lobby?',
                view=RouletteAgainButtons(self.bot),
                ephemeral=True)


class RouletteAgainButtons(discord.ui.View):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction,
                  _button: discord.ui.Button):
        try:
            await roulette.start_roulette_lobby(interaction, self.bot)
        except:
            await interaction.response.send_message(
                "Sorry, something went wrong.", ephemeral=True)
            raise

    @discord.ui.button(label='No', style=discord.ButtonStyle.gray)
    async def no(self, interaction: discord.Interaction,
                 _button: discord.ui.Button):
        try:
            await interaction.response.edit_message(
                content='Could not find a previously started lobby.',
                view=None)
        except:
            await interaction.response.send_message(
                "Sorry, something went wrong.", ephemeral=True)
            raise


async def setup(bot):
    await bot.add_cog(RouletteAgainCog(bot))
