"""
A cog to add a command for syncing the command tree.
"""

import logging
from typing import Literal, Optional

import discord
from discord.ext import commands
from discord.ext.commands import Greedy, Context


class SyncCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(
        self,
        ctx: Context,
        guilds: Greedy[discord.Object],
        spec: Optional[Literal["local", "copy", "clear", "global"]] = None
    ) -> None:

        logging.debug('sync command used')

        if not guilds:
            if spec == "local":
                message = await ctx.send("Syncing...")
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "copy":
                message = await ctx.send("Syncing...")
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "clear":
                message = await ctx.send("Syncing...")
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            elif spec == "global":
                message = await ctx.send("Syncing...")
                synced = await ctx.bot.tree.sync()
            else:
                await ctx.send(
                    "Missing sync operator. Options: guild_ids, local, copy, clear, global"
                )
                return

            await message.edit(
                content=
                f"Synced {len(synced)} command(s) {'globally.' if spec == 'global' else 'to the current guild.'}"
            )
            return

        ret = 0
        message = await ctx.send("Syncing...")
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await message.edit(content=f"Synced the tree to {ret}/{len(guilds)}.")


async def setup(bot):
    await bot.add_cog(SyncCog(bot))
