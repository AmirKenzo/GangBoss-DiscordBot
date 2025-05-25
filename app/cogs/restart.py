from discord.ext import commands
import sys
import os


def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator

    return commands.check(predicate)


def restart_bot():
    python = sys.executable
    os.execl(python, python, *sys.argv)


class Restart(commands.Cog, name="Restart"):
    def __init__(self, bot):
        self.bot = bot

    @is_admin()
    @commands.command(name="restart", description="Restart Robot")
    async def restart(self, ctx: commands.Context):
        await ctx.send("Restarting bot...!", ephemeral=False)
        restart_bot()


async def setup(bot):
    await bot.add_cog(Restart(bot))
