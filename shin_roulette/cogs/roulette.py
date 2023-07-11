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


class RouletteCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command()
    async def roulette(self, interaction: discord.Interaction):
        """
        Starts a roulette lobby
        """

        roulette = RouletteLobby(interaction.user)
        (embed, buttons) = roulette.build_message()
        await interaction.response.send_message(embed=embed, view=buttons)


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
        self.reroll_timer = 30
        self.reroll_timer_end = None
        # Saved roulette data
        self.fight = ''
        self.rerolled_fight = ''
        self.team = []

    def is_full(self) -> bool:
        return len(self.players) >= self.max_size

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
            if not self.rerolled and self.reroll_timer_end > int(time.time()):
                embed.add_field(
                    name='',
                    value=f'Reroll ends <t:{self.reroll_timer_end}:R>',
                    inline=False)
                buttons = RouletteRerollView(self)
            else:
                buttons = None
        return (embed, buttons)

    def run_roulette(self, players: List[str]):
        while len(players) < self.max_size:
            players.append(f'Player{len(players) + 1}')
        roulette_result = roulette_runner.run_roulette(players)
        self.fight = roulette_result.fight.name
        self.team = [
            f'{p.job.role_name} ({p.job.name}) - {p.player_name}'
            for p in roulette_result.players
        ]

    async def start(self, interaction: discord.Interaction):
        if self.started:
            return

        logging.info('Starting roulette with options [players:%s]',
                     self.players)

        self.run_roulette(self.players)

        self.reroll_timer_end = int(time.time()) + self.reroll_timer
        self.started = True

        (embed, buttons) = self.build_message()
        await interaction.response.edit_message(embed=embed, view=buttons)

        # Start reroll timer countdown
        await self.wait_for_reroll_timer(interaction.message)

    async def wait_for_reroll_timer(self, message: discord.Message):
        while self.reroll_timer_end > int(time.time()):
            await asyncio.sleep(self.reroll_timer_end - int(time.time()))

        (embed, buttons) = self.build_message()
        await message.edit(embed=embed, view=buttons)

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
        super().__init__()

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
        super().__init__()
        self.roulette = roulette

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
