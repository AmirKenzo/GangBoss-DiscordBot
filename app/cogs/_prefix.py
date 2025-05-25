import discord
from discord.ext import commands
from discord import app_commands
from app.utils import serversettings as Settings


class _Prefix(commands.Cog, name="_Prefix"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="prefix", description="Set the prefix for the bot !!")
    async def prefix(self, interaction: discord.Interaction, new_prefix: str):
        settings = Settings.get_settings(interaction.guild.id)
        settings["prefix"] = new_prefix
        Settings.set_guild_settings(interaction.guild.id, settings)
        await interaction.response.send_message(f"Prefix changed to `{new_prefix}`")


async def setup(bot: commands.Bot):
    await bot.add_cog(_Prefix(bot))
