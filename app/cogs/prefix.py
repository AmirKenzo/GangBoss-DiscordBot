from discord.ext import commands
from app.utils import serversettings as Settings


class Prefix(commands.Cog, name="Prefix"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="prefix", help="Change the command prefix for the bot")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, new_prefix: str):
        settings = Settings.get_settings(ctx.guild.id)
        settings["prefix"] = new_prefix
        Settings.set_guild_settings(ctx.guild.id, settings)
        await ctx.send(f"Prefix changed to `{new_prefix}`")


async def setup(bot: commands.Bot):
    await bot.add_cog(Prefix(bot))
