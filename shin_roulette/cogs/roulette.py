"""
A cog for the roulette slash command.
"""

import discord
from discord.ext import commands


class RouletteCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command()
    async def roulette(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Shin Roulette", )
        embed.add_field(name="Players", value="")
        buttons = RouletteButtonView()

        await interaction.response.send_message(embed=embed, view=buttons)
        # response = await interaction.original_response()
        # await response.add_reaction('✅')
        # await buttons.wait()


class RouletteButtonView(discord.ui.View):

    def __init__(self):
        super().__init__()

    @discord.ui.button(label='Join', style=discord.ButtonStyle.green)
    async def join(self, interaction: discord.Interaction,
                   button: discord.ui.Button):
        try:
            embed = interaction.message.embeds[0]
            field = embed.fields[0]
            embed.set_field_at(0,
                               name=field.name,
                               value=interaction.user.mention,
                               inline=field.inline)
            await interaction.message.edit(embed=embed)
            await interaction.response.send_message(
                f'You have joined roulette {interaction.message.jump_url}',
                ephemeral=True)
        except Exception:
            await interaction.response.send_message(
                "Sorry, something went wrong.", ephemeral=True)
            raise


async def setup(bot):
    await bot.add_cog(RouletteCog(bot))
