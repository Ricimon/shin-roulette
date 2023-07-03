"""
A cog for the roulette slash command.
"""

from typing import List, Optional, Union

import discord
from discord.ext import commands


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
            embed.description = "Fight: E8S"
            embed.add_field(name="Roles",
                            value='\n'.join([
                                'Tank (PLD) - ' + player
                                for player in self.players
                            ]))
            buttons = None
        return (embed, buttons)

    def start(self):
        if self.started:
            return
        self.started = True


class RouletteLobbyButtons(discord.ui.View):

    def __init__(self, roulette: RouletteLobby, author: Union[discord.Member,
                                                              discord.User]):
        self.roulette = roulette
        self.author = author
        super().__init__()

    @discord.ui.button(label='Join', style=discord.ButtonStyle.blurple)
    async def join(self, interaction: discord.Interaction,
                   button: discord.ui.Button):
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
            await interaction.message.edit(embed=embed, view=buttons)

        except Exception:
            await interaction.response.send_message(
                "Sorry, something went wrong.", ephemeral=True)
            raise

    @discord.ui.button(label='Leave', style=discord.ButtonStyle.gray)
    async def leave(self, interaction: discord.Interaction,
                    button: discord.ui.Button):
        try:
            if interaction.user.mention not in self.roulette.players:
                await interaction.response.send_message(
                    f'You are not in this roulette {interaction.message.jump_url}',
                    ephemeral=True)
                return

            self.roulette.players.remove(interaction.user.mention)

            (embed, buttons) = self.roulette.build_message()
            await interaction.message.edit(embed=embed, view=buttons)

        except Exception:
            await interaction.response.send_message(
                "Sorry, something went wrong.", ephemeral=True)
            raise

    @discord.ui.button(label='Start Roulette', style=discord.ButtonStyle.green)
    async def start(self, interaction: discord.Interaction,
                    button: discord.ui.Button):
        try:
            if not interaction.user.guild_permissions.administrator and interaction.user.id != self.author.id:
                await interaction.response.send_message(
                    'Only the roulette creator and server admins can start the roulette.',
                    ephemeral=True)
                return

            self.roulette.start()

            (embed, buttons) = self.roulette.build_message()
            await interaction.message.edit(embed=embed, view=buttons)

        except Exception:
            await interaction.response.send_message(
                "Sorry, something went wrong.", ephemeral=True)
            raise


async def setup(bot):
    await bot.add_cog(RouletteCog(bot))
