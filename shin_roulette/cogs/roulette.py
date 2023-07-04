"""
A cog for the roulette slash command.
"""

import logging
import re
from typing import List, Optional, Union

import discord
from discord.ext import commands

from shin_roulette.core.shin_roulette import ShinRoulette, RoleIndex


class RouletteCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command()
    async def roulette(self, interaction: discord.Interaction):
        roulette = RouletteLobby(interaction.user)
        (embed, buttons) = roulette.build_message()
        await interaction.response.send_message(embed=embed, view=buttons)


class RouletteLobby:

    def __init__(self,
                 author: Union[discord.Member, discord.User],
                 players: Optional[List[str]] = None):
        self.author = author
        self.players = players or []
        self.max_size = 8
        self.started = False
        self.fight = ''
        self.team = {}

    def is_full(self) -> bool:
        return len(self.players) >= self.max_size

    def build_message(self) -> (discord.Embed, discord.ui.View):
        embed = discord.Embed(title="Shin Roulette 🎲", )
        if not self.started:
            embed.add_field(
                name=f"Players ({len(self.players)}/{self.max_size})",
                value='\n'.join(self.players))
            buttons = RouletteLobbyButtons(self, self.author)
        else:
            embed.description = f"Fight: {self.fight}"
            embed.add_field(name="Roles", value='\n'.join(self.team))
            buttons = None
        return (embed, buttons)

    async def start(self, message: discord.Message, assign_jobs: bool,
                    standard_composition: bool):
        if self.started:
            return

        logging.info(
            'Starting roulette with options [players:%s] [assign_jobs:%s] [standard_composition:%s]',
            self.players, assign_jobs, standard_composition)

        # A bunch of string manipulation that can be tidied with Model classes
        (self.fight, team) = ShinRoulette(self.players, assign_jobs,
                                          standard_composition)
        team_list = [f'{role} - {player}' for (player, role) in team.items()]
        team_list = sorted(team_list,
                           key=lambda x: RoleIndex(x.partition(',')[0]))
        self.team = [
            x.replace(',', ' (').replace(' -', ') -') for x in team_list
        ]

        self.started = True

        (embed, buttons) = self.build_message()
        await message.edit(embed=embed, view=buttons)


class RouletteLobbyButtons(discord.ui.View):

    def __init__(self, roulette: RouletteLobby, author: Union[discord.Member,
                                                              discord.User]):
        self.roulette = roulette
        self.author = author
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
            if not interaction.user.guild_permissions.administrator and interaction.user.id != self.author.id:
                await interaction.response.send_message(
                    'Only the roulette creator and server admins can start the roulette.',
                    ephemeral=True)
                return

            options = RouletteStartOptions(self.roulette, interaction.message)

            await interaction.response.send_message(view=options,
                                                    ephemeral=True)

        except Exception:
            await interaction.response.send_message(
                "Sorry, something went wrong.", ephemeral=True)
            raise


class RouletteStartOptions(discord.ui.View):

    def __init__(self, roulette: RouletteLobby, message: discord.Message):
        super().__init__()
        self.roulette = roulette
        self.message = message
        self.assign_jobs_flag = True
        self.standard_composition_flag = True

    @discord.ui.select(options=[
        discord.SelectOption(
            label="Assign Jobs",
            description="Assigns random jobs in addition to roles",
            default=True),
        discord.SelectOption(label="Don't Assign Jobs",
                             description="Only assign roles")
    ],
                       row=0)
    async def assign_jobs(self, interaction: discord.Interaction,
                          select: discord.ui.Select):
        self.assign_jobs_flag = select.values[0] == select.options[0].value
        await interaction.response.defer()

    @discord.ui.select(options=[
        discord.SelectOption(label="Standard Composition",
                             description="At least one melee/caster/pranged",
                             default=True),
        discord.SelectOption(label="Nonstandard Composition",
                             description="Challenge mode")
    ],
                       row=1)
    async def standard_composition(self, interaction: discord.Interaction,
                                   select: discord.ui.Select):
        self.standard_composition_flag = select.values[0] == select.options[
            0].value
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.primary,
                       label="Confirm",
                       row=2)
    async def confirm(self, interaction: discord.Interaction,
                      _button: discord.ui.Button):
        try:
            # this line is necessary to delete ephemeral messages
            await interaction.response.defer()
            await interaction.delete_original_response()
            await self.roulette.start(self.message, self.assign_jobs_flag,
                                      self.standard_composition_flag)
        except:
            await interaction.response.send_message(
                "Sorry, something went wrong.", ephemeral=True)
            raise


async def setup(bot):
    await bot.add_cog(RouletteCog(bot))
