import discord
from discord.ext import commands
from discord import app_commands
from app.utils import serversettings as Settings, setting
import asyncio
import sys
from discord.ext import tasks
from collections import deque
from config import ACTIVITY_BOT, TOKEN, SERVER_GUILD_ID


activity_queue = deque(ACTIVITY_BOT)


bot = commands.Bot(command_prefix=commands.when_mentioned_or(""), intents=setting.intents, help_command=None)
tree = bot.tree


async def load_cogs():
    cogs = setting.get_cogs()
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"[+] Successfully loaded {cog}")
        except Exception as e:
            print(f"[-] An error occurred while loading {cog}: {e}")


@tasks.loop(seconds=75)
async def myLoop():
    Dis = bot.get_guild(SERVER_GUILD_ID)

    if activity_queue:
        current_activity = activity_queue.popleft()

        try:
            await bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name=f"👥 {Dis.member_count:,} Members"),
                status=discord.Status.dnd,
            )
            await asyncio.sleep(15)

            await bot.change_presence(
                activity=discord.Streaming(name=current_activity, url="https://www.twitch.tv/amirkenzor6")
            )
            await asyncio.sleep(15)

            await bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.listening, name=current_activity),
                status=discord.Status.dnd,
            )
            activity_queue.append(current_activity)

        except Exception as e:
            print(f"Error in myLoop: {e}")


@bot.event
async def on_ready():
    await load_cogs()
    await tree.sync()
    print(f"[+] Booted {bot.user}...")
    myLoop.start()

    settings = Settings.get_settings_all()

    try:
        for guild in bot.guilds:
            if Settings.get_settings(guild.id) is None:
                settings[str(guild.id)] = Settings.default_settings
        Settings.set_all_settings(settings)
        print("[+] Successfully initialized bot settings")
    except Exception as e:
        print("[!] Error initializing bot settings: ", e)

    oauth_url = discord.utils.oauth_url(bot.application_id, permissions=discord.Permissions(permissions=8))
    print(f"[+] Invite URL: {oauth_url}")


@bot.event
async def on_guild_join(guild):
    Settings.set_guild_settings(guild.id, Settings.default_settings)
    print(f"[+] Joined {guild.name} with id {guild.id}")
    print(f"[+] Successfully initialized config/serversettings.json for {guild.name}")


@bot.event
async def on_message(message: discord.Message):
    if message.guild is not None:
        prefix = Settings.get_settings(message.guild.id)["prefix"]
        if message.content.startswith(prefix):
            message.content = message.content[len(prefix) :]
            await bot.process_commands(message)
    else:
        await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            f":x: You need to have `{', '.join(error.missing_permissions)}` permissions to use this command.",
            ephemeral=True,
        )
        return
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.CheckFailure):
        await ctx.send(":x: You do not have permission to use this command.")
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(":x: You do not have permission to use this command.")
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":x: Missing required argument.")
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send(":x: Invalid argument.")
        return
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f":x: Command on cooldown. Try again in {error.retry_after:.2f} seconds.")
        return
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(":x: An error occurred while executing the command.")
        return
    raise error


@bot.tree.error
async def error_slash(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingAnyRole):
        await interaction.response.send_message(str(error), ephemeral=True)
        return
    elif isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(str(error), ephemeral=True)
        return
    else:
        await interaction.response.send_message(f"An error occurred. e:{error}", ephemeral=True)
        return


def main(*args):
    try:
        setting.init()
        bot.run(TOKEN, reconnect=True)
        # bot.run(TOKEN, reconnect=True, log_handler=None)
    except Exception as e:
        print(f"[-] An error occurred while running the bot: {e}")
        return


if __name__ == "__main__":
    args = sys.argv[1:]
    main(*args)
