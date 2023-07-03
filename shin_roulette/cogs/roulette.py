"""
A cog for the roulette slash command.
"""

from typing import List, Optional

import discord
from discord.ext import commands


class RouletteCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command()
    async def roulette(self, interaction: discord.Interaction):
        roulette = RouletteLobby()
        (embed, buttons) = roulette.build_message()
        await interaction.response.send_message(embed=embed, view=buttons)


class RouletteLobby:

    def __init__(self, players: Optional[List[str]] = None):
        self.players = players or []
        self.max_size = 8

    def build_message(self) -> (discord.Embed, discord.ui.View):
        embed = discord.Embed(title="Shin Roulette 🎲", )
        embed.add_field(name=f"Players ({len(self.players)}/{self.max_size})",
                        value='\n'.join(self.players))
        buttons = RouletteButtonView()
        return (embed, buttons)

    def is_full(self) -> bool:
        return len(self.players) >= self.max_size


class RouletteButtonView(discord.ui.View):

    def __init__(self):
        super().__init__()

    @discord.ui.button(label='Join', style=discord.ButtonStyle.green)
    async def join(self, interaction: discord.Interaction,
                   button: discord.ui.Button):
        try:
            embed = interaction.message.embeds[0]
            field = embed.fields[0]
            players = field.value.splitlines()

            roulette = RouletteLobby(players)

            if interaction.user.mention in roulette.players:
                await interaction.response.send_message(
                    f'You have already joined roulette {interaction.message.jump_url}',
                    ephemeral=True)
                return

            if roulette.is_full():
                await interaction.response.send_message(
                    f'Sorry, this roulette {interaction.message.jump_url} is full.',
                    ephemeral=True)
                return

            roulette.players.append(interaction.user.mention)

            (embed, buttons) = roulette.build_message()
            await interaction.message.edit(embed=embed, view=buttons)
            await interaction.response.send_message(
                f'You have joined roulette {interaction.message.jump_url}',
                ephemeral=True)

        except Exception:
            await interaction.response.send_message(
                "Sorry, something went wrong.", ephemeral=True)
            raise


async def setup(bot):
    await bot.add_cog(RouletteCog(bot))
