"""
An extension for the roulette slash command.
"""

from interactions import (Embed, Extension, InteractionContext, slash_command)

from core.base import CustomClient


class RouletteExtension(Extension):
    bot: CustomClient

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="roulette", description="Start roulette.")
    async def roulette(self, ctx: InteractionContext):
        embed = Embed(
            title="Shin Roulette",
            Description="React with ✅ to join.",
        )
        await ctx.send(f'Hi, {ctx.user.mention}', embeds=embed)


def setup(bot: CustomClient):
    RouletteExtension(bot)
