"""
A cog for the roulette slash command.
"""

import asyncio
import logging
import time
from typing import List, Optional, Union

import discord
from discord.ext import commands

from shin_roulette.core import roulette_runner


async def remove_last_message_buttons(interaction: discord.Interaction,
                                      bot: commands.Bot):
    """
    Removes the buttons on the last message sent by the bot. This aims to remove the reroll button on a roulette that's assumed to already have been attempted.
    """
    try:
        channel = interaction.channel
        async for message in channel.history(limit=100):
            if message.author == bot.user:
                await message.edit(view=None)
                return
    except:
        return


async def start_roulette_lobby(interaction: discord.Interaction,
                               bot: commands.Bot,
                               players: Optional[List[str]] = None):
    await remove_last_message_buttons(interaction, bot)

    roulette = RouletteLobby(interaction.user, players)
    (embed, buttons) = roulette.build_message()
    await interaction.response.send_message(embed=embed, view=buttons)


class RouletteCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command()
    async def roulette(self, interaction: discord.Interaction):
        """
        Starts a roulette lobby
        """

        logging.debug('/roulette used')

        await start_roulette_lobby(interaction, self.bot)


class RouletteLobby:

    # pylint: disable=too-many-instance-attributes

    def __init__(self,
                 author: Union[discord.Member, discord.User],
                 players: Optional[List[str]] = None):
        self.author = author
        self.players = players or []
        self.max_size = 8
        self.started = False
        self.rerolled = False
        # Saved roulette data
        self.fight = ''
        self.rerolled_fight = ''
        self.team = []

    def is_full(self) -> bool:
        return len(self.players) >= self.max_size

    def is_empty(self) -> bool:
        return not self.players or len(self.players) == 0

    def build_message(self) -> (discord.Embed, discord.ui.View):
        embed = discord.Embed(title='Shin Roulette 🎲', )
        if not self.started:
            embed.add_field(
                name=f'Players ({len(self.players)}/{self.max_size})',
                value='\n'.join(self.players))
            buttons = RouletteLobbyButtons(self)
        else:
            description = f'Fight: **{self.fight}**'
            if self.rerolled:
                description += f' *(rerolled from {self.rerolled_fight})*'
            embed.description = description
            embed.add_field(name='Roles', value='\n'.join(self.team))
            if not self.rerolled:
                buttons = RouletteRerollView(self)
            else:
                buttons = None
        return (embed, buttons)

    def run_roulette(self, players: List[str]):
        while len(players) < self.max_size:
            players.append(f'Player{len(players) + 1}')
        roulette_result = roulette_runner.run_roulette(players)
        self.fight = roulette_result.fight.name
        if roulette_result.fight.show_role:
            self.team = [
                f'{p.job.role_name} ({p.job.name}) - {p.player_name}'
                for p in roulette_result.players
            ]
        else:
            self.team = [
                f'{p.job.name} - {p.player_name}'
                for p in roulette_result.players
            ]

    async def start(self, interaction: discord.Interaction):
        if self.started:
            return

        logging.info('Starting roulette with options [players:%s]',
                     self.players)

        self.run_roulette(self.players)

        self.started = True

        (embed, buttons) = self.build_message()
        await interaction.response.edit_message(embed=embed, view=buttons)

    async def reroll(self, interaction: discord.Interaction):
        if not self.started or self.rerolled:
            logging.error(
                "Cannot reroll. Roulette is either unstarted or already rerolled."
            )
            return

        self.rerolled_fight = self.fight

        logging.info('Rerolling roulette with [players:%s]', self.players)

        self.run_roulette(self.players)

        self.rerolled = True

        (embed, buttons) = self.build_message()
        await interaction.response.edit_message(embed=embed, view=buttons)


class RouletteLobbyButtons(discord.ui.View):

    def __init__(self, roulette: RouletteLobby):
        self.roulette = roulette
        super().__init__(timeout=None)

    @discord.ui.button(label='Join', style=discord.ButtonStyle.blurple)
    async def join(self, interaction: discord.Interaction,
                   _button: discord.ui.Button):
        try:
            if interaction.user.mention in self.roulette.players:
                await interaction.response.send_message(
                    f'You have already joined roulette {interaction.message.jump_url}',
                    ephemeral=True)
                return

            if self.roulette.is_full():
                await interaction.response.send_message(
                    f'Sorry, this roulette {interaction.message.jump_url} is full.',
                    ephemeral=True)
                return

            self.roulette.players.append(interaction.user.mention)

            (embed, buttons) = self.roulette.build_message()
            await interaction.response.edit_message(embed=embed, view=buttons)

        except Exception:
            await interaction.response.send_message(
                "Sorry, something went wrong.", ephemeral=True)
            raise

    @discord.ui.button(label='Leave', style=discord.ButtonStyle.gray)
    async def leave(self, interaction: discord.Interaction,
                    _button: discord.ui.Button):
        try:
            if interaction.user.mention not in self.roulette.players:
                await interaction.response.send_message(
                    f'You are not in this roulette {interaction.message.jump_url}',
                    ephemeral=True)
                return

            self.roulette.players.remove(interaction.user.mention)

            (embed, buttons) = self.roulette.build_message()
            await interaction.response.edit_message(embed=embed, view=buttons)

        except Exception:
            await interaction.response.send_message(
                "Sorry, something went wrong.", ephemeral=True)
            raise

    @discord.ui.button(label='Start Roulette', style=discord.ButtonStyle.green)
    async def start(self, interaction: discord.Interaction,
                    _button: discord.ui.Button):
        try:
            if not interaction.user.guild_permissions.administrator and interaction.user.id != self.roulette.author.id:
                await interaction.response.send_message(
                    'Only the roulette creator and server admins can start the roulette.',
                    ephemeral=True)
                return

            await self.roulette.start(interaction)

        except Exception:
            await interaction.response.send_message(
                "Sorry, something went wrong.", ephemeral=True)
            raise


class RouletteRerollView(discord.ui.View):

    def __init__(self, roulette: RouletteLobby):
        self.roulette = roulette
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.primary, label='Reroll')
    async def reroll(self, interaction: discord.Interaction,
                     _button: discord.ui.Button):
        try:
            if not interaction.user.guild_permissions.administrator and interaction.user.id != self.roulette.author.id:
                await interaction.response.send_message(
                    'Only the roulette creator and server admins can reroll the roulette.',
                    ephemeral=True)
                return

            await self.roulette.reroll(interaction)

        except Exception:
            await interaction.response.send_message(
                "Sorry, something went wrong.", ephemeral=True)
            raise


async def setup(bot):
    await bot.add_cog(RouletteCog(bot))
