import discord
from discord.ext import commands
from discord import app_commands
import os
import re
import json
from config import CHANNEL_STATUS_ROB, GANG_NAME, ROLE_FAMILY, ROLE_XP_MANAGER


white_list_rob = [
    "Maze",
    "Blane",
    "JawShahr",
    "JawShams",
    "JawSanvitus",
    "Bime",
    "Cbank",
    "AirPort",
    "Flat",
    "Cargo",
    "Benny",
]

XPS = {
    "normal": {
        "Shop": 18,
        "GunShop": 35,
        "MiniBank": 35,
        "Maze": 85,
        "Blane": 130,
        "JawShahr": 50,
        "JawShams": 50,
        "JawSanvitus": 50,
        "Bime": 150,
        "Cbank": 180,
        "AirPort": 150,
        "Flat": 180,
        "Cargo": 180,
        "Benny": 100,
        "Hostage": 100,
    },
    "skillup": {
        "Shop": 22,
        "GunShop": 55,
        "MiniBank": 43,
        "Maze": 110,
        "Blane": 170,
        "JawShahr": 65,
        "JawShams": 65,
        "JawSanvitus": 65,
        "Bime": 195,
        "Cbank": 235,
        "AirPort": 195,
        "Flat": 235,
        "Cargo": 235,
        "Benny": 150,
        "Hostage": 100,
    },
}


def load_users(file_name="./app/data/rob_xp.json"):
    try:
        with open(file_name, "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}
    return users


def save_users(users, file_name="./app/data/rob_xp.json"):
    with open(file_name, "w") as file:
        json.dump(users, file, indent=4)


def save_xp(username, rab_type, xp=None, skillup=False):
    rob_users = load_users("./app/data/rob_xp.json")
    event_users = load_users("./app/data/event_xp.json")

    xp_dict = XPS["skillup"] if skillup else XPS["normal"]

    if xp is None:
        xp = xp_dict.get(rab_type, 0)

    for users in [rob_users, event_users]:
        if username not in users:
            users[username] = {}
        users[username][rab_type] = users[username].get(rab_type, 0) + xp

    save_users(rob_users, "./app/data/rob_xp.json")
    save_users(event_users, "./app/data/event_xp.json")

    return xp


def reset_xp(file_name="./app/data/rob_xp.json"):
    save_users({}, file_name=file_name)


def decrease_user_xp(username, decrease_xp, file_name="./app/data/rob_xp.json"):
    users = load_users(file_name)
    if username in users:
        for rob, xp in users[username].items():
            if decrease_xp >= xp:
                decrease_xp -= xp
                users[username][rob] = 0
            else:
                users[username][rob] -= decrease_xp
                decrease_xp = 0
                break
    else:
        print("کاربر یافت نشد!")
    save_users(users, file_name)


def get_user_info(file_path="./app/data/rob_xp.json"):
    users = load_users(file_path)
    user_info = []
    for username, data in users.items():
        user_data = {"username": username, "XP": sum(data.values())}
        user_data.update({f"{rob}": xp for rob, xp in data.items()})
        user_info.append(user_data)
    sorted_user_info = sorted(user_info, key=lambda x: x["XP"], reverse=True)
    return sorted_user_info


def update_all_xp(item, skillup=False):
    xp_dict = XPS["skillup"] if skillup else XPS["normal"]
    files = ["./app/data/rob_allxp.json", "./app/data/event_allxp.json"]

    for file_name in files:
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                data = json.load(f)

                if item in xp_dict:
                    data["all_xp"] += xp_dict[item]
                    with open(file_name, "w") as f:
                        json.dump(data, f, indent=4)
                else:
                    print(f"Item not found in {'SKILLUP_XPS' if skillup else 'DEFAULT_XPS'}.")
        else:
            data = {"all_xp": xp_dict.get(item, 0)}
            with open(file_name, "w") as f:
                json.dump(data, f, indent=4)
                print(f"File {file_name} created with initial value")


def kasr_all_xp(tedad, file_name="./app/data/rob_allxp.json"):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            data = json.load(f)
            if "all_xp" in data:
                data["all_xp"] -= tedad
                with open(file_name, "w") as f:
                    json.dump(data, f, indent=4)
            else:
                print("Key 'all_xp' not found in the JSON file.")
    else:
        print("File not found.")


def reset_all_xp(file_name="./app/data/rob_allxp.json"):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            data = json.load(f)
            data["all_xp"] = 0
        with open(file_name, "w") as f:
            json.dump(data, f, indent=4)
    else:
        data = {"all_xp": 0}
        with open(file_name, "w") as f:
            json.dump(data, f, indent=4)
            print("File created with initial value")


def gang_all_xp(file_path="./app/data/rob_allxp.json"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        return data["all_xp"]


def rejex(user_string):
    users = re.findall(r"<@[^>]+>|\B@\w+(?:\s+\w+)*", user_string)
    return users


class _Rub(commands.Cog, name="_Rob"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    Rob_name = [
        "Shop",
        "GunShop",
        "MiniBank",
        "Maze",
        "Blane",
        "JawShahr",
        "JawShams",
        "JawSanvitus",
        "Bime",
        "Cbank",
        "AirPort",
        "Flat",
        "Cargo",
        "Benny",
        "Hostage",
    ]
    choices_Rob_name = []
    for index, name in enumerate(Rob_name, start=1):
        choices_Rob_name.append(app_commands.Choice(name=name, value=index))

    status_rob = ["Win", "Win + SKILLUP", "Lose", "NoPD"]
    choices_status_rob = []
    for index, name in enumerate(status_rob, start=1):
        choices_status_rob.append(app_commands.Choice(name=name, value=index))

    @app_commands.command(name="rob", description="RobPoint")
    @app_commands.choices(rub_name=choices_Rob_name, status=choices_status_rob)
    @app_commands.checks.has_any_role(*ROLE_FAMILY)
    async def rub(
        self,
        interaction: discord.Interaction,
        rub_name: app_commands.Choice[int],
        status: app_commands.Choice[int],
        robbers: str,
        comander: str = None,
    ):
        if status.name == "Win":
            Users = rejex(robbers)
            xp = ""
            for i in Users:
                xp = save_xp(i, rub_name.name, skillup=False)

            update_all_xp(rub_name.name, skillup=False)
            if comander is not None:
                file = discord.File("app/img/win.png", filename="win.png")
                embed = discord.Embed(
                    title=f"Win {rub_name.name}",
                    description=f"`XP: {xp}`\n``Robbers:`` {robbers}\n\n``Commander:`` {comander}\n\n{GANG_NAME}",
                    color=discord.Color.green(),
                )
                embed.set_thumbnail(url="attachment://win.png")
                await interaction.response.send_message(embed=embed, file=file)
                message = await interaction.original_response()
                if rub_name.name in white_list_rob:
                    log_url = message.jump_url
                    file = discord.File("app/img/win.png", filename="win.png")
                    embed = discord.Embed(
                        title=f"Win | {rub_name.name}",
                        description=f"[**Check Log**]({log_url})",
                        color=discord.Color.green(),
                    )
                    embed.set_thumbnail(url="attachment://win.png")
                    target_channel = interaction.guild.get_channel(CHANNEL_STATUS_ROB)
                    if target_channel:
                        await target_channel.send(embed=embed, file=file)

            else:
                file = discord.File("app/img/win.png", filename="win.png")
                embed = discord.Embed(
                    title=f"Win {rub_name.name}",
                    description=f"`XP: {xp}`\n``Robbers:`` {robbers}\n\n{GANG_NAME}",
                    color=discord.Color.green(),
                )
                embed.set_thumbnail(url="attachment://win.png")
                await interaction.response.send_message(embed=embed, file=file)
                message = await interaction.original_response()

                if rub_name.name in white_list_rob:
                    log_url = message.jump_url
                    file = discord.File("app/img/win.png", filename="win.png")
                    embed = discord.Embed(
                        title=f"Win | {rub_name.name}",
                        description=f"[**Check Log**]({log_url})",
                        color=discord.Color.green(),
                    )
                    embed.set_thumbnail(url="attachment://win.png")
                    target_channel = interaction.guild.get_channel(CHANNEL_STATUS_ROB)
                    if target_channel:
                        await target_channel.send(embed=embed, file=file)

        elif status.value == 2:
            Users = rejex(robbers)
            xp = ""
            for i in Users:
                xp = save_xp(i, rub_name.name, skillup=True)

            update_all_xp(rub_name.name, skillup=True)
            if comander is not None:
                file = discord.File("app/img/win.png", filename="win.png")
                embed = discord.Embed(
                    title=f"Win ({rub_name.name}) SkillUP",
                    description=f"`XP: {xp}`⭐\n``Robbers:`` {robbers}\n\n``Commander:`` {comander}\n\n{GANG_NAME}",
                    color=discord.Color.green(),
                )
                embed.set_thumbnail(url="attachment://win.png")
                await interaction.response.send_message(embed=embed, file=file)
                message = await interaction.original_response()
                if rub_name.name in white_list_rob:
                    log_url = message.jump_url
                    file = discord.File("app/img/win.png", filename="win.png")
                    embed = discord.Embed(
                        title=f"Win | {rub_name.name}",
                        description=f"[**Check Log**]({log_url})",
                        color=discord.Color.green(),
                    )
                    embed.set_thumbnail(url="attachment://win.png")
                    target_channel = interaction.guild.get_channel(CHANNEL_STATUS_ROB)
                    if target_channel:
                        await target_channel.send(embed=embed, file=file)
            else:
                file = discord.File("app/img/win.png", filename="win.png")
                embed = discord.Embed(
                    title=f"Win ({rub_name.name}) SkillUP",
                    description=f"`XP: {xp}`⭐\n``Robbers:`` {robbers}\n\n{GANG_NAME}",
                    color=discord.Color.green(),
                )
                embed.set_thumbnail(url="attachment://win.png")
                await interaction.response.send_message(embed=embed, file=file)
                message = await interaction.original_response()
                if rub_name.name in white_list_rob:
                    log_url = message.jump_url
                    file = discord.File("app/img/win.png", filename="win.png")
                    embed = discord.Embed(
                        title=f"Win | {rub_name.name}",
                        description=f"[**Check Log**]({log_url})",
                        color=discord.Color.green(),
                    )
                    embed.set_thumbnail(url="attachment://win.png")
                    target_channel = interaction.guild.get_channel(CHANNEL_STATUS_ROB)
                    if target_channel:
                        await target_channel.send(embed=embed, file=file)

        elif status.name == "Lose":
            file = discord.File("app/img/lose.png", filename="lose.png")
            embed = discord.Embed(
                title=f"Lose | {rub_name.name}",
                description=f"``Robbers:`` {robbers}\n\n{GANG_NAME}",
                color=discord.Color.red(),
            )
            embed.set_thumbnail(url="attachment://lose.png")
            await interaction.response.send_message(embed=embed, file=file)
            message = await interaction.original_response()

            if rub_name.name in white_list_rob:
                log_url = message.jump_url
                file = discord.File("app/img/lose.png", filename="lose.png")
                embed = discord.Embed(
                    title=f"Lose | {rub_name.name}",
                    description=f"[**Check Log**]({log_url})",
                    color=discord.Color.red(),
                )
                embed.set_thumbnail(url="attachment://lose.png")
                target_channel = interaction.guild.get_channel(CHANNEL_STATUS_ROB)
                if target_channel:
                    await target_channel.send(embed=embed, file=file)

        elif status.name == "NoPD":
            file = discord.File("app/img/nopd.png", filename="nopd.png")
            embed = discord.Embed(
                title=f"NoPD | {rub_name.name}",
                description=f"``Robbers:`` {robbers}\n\n{GANG_NAME}",
                color=discord.Color.orange(),
            )
            embed.set_thumbnail(url="attachment://nopd.png")
            await interaction.response.send_message(embed=embed, file=file)
            message = await interaction.original_response()

            if rub_name.name in white_list_rob:
                log_url = message.jump_url
                file = discord.File("app/img/nopd.png", filename="nopd.png")
                embed = discord.Embed(
                    title=f"NoPD | {rub_name.name}",
                    description=f"[**Check Log**]({log_url})",
                    color=discord.Color.orange(),
                )
                embed.set_thumbnail(url="attachment://nopd.png")
                target_channel = interaction.guild.get_channel(CHANNEL_STATUS_ROB)
                if target_channel:
                    await target_channel.send(embed=embed, file=file)

    @app_commands.command(name="xp-list", description="XP List")
    @app_commands.checks.has_any_role(*ROLE_FAMILY)
    async def xp(self, interaction: discord.Interaction):
        user_info = get_user_info("./app/data/rob_xp.json")
        RESULT = ""

        count = 1
        for user in user_info:
            all_xp = user["XP"]
            RESULT += f"{count}- {user['username']} | XP:`{all_xp}`\n"
            count += 1
        total_xp = sum(user["XP"] for user in user_info)
        gang_xp = gang_all_xp("./app/data/rob_allxp.json")

        embed = discord.Embed(
            title="XP List",
            description=f"{RESULT}\n**```All Point: {total_xp}\nGang XP: {gang_xp}```**\n\n{GANG_NAME}",
            color=discord.Color.random(),
        )
        if interaction.guild.icon:
            embed.set_thumbnail(url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="xp-event", description="XP List (Event)")
    @app_commands.checks.has_any_role(*ROLE_FAMILY)
    async def xp_event(self, interaction: discord.Interaction):
        user_info = get_user_info("./app/data/event_xp.json")
        RESULT = ""

        count = 1
        for user in user_info:
            all_xp = user["XP"]

            RESULT += f"{count}- {user['username']} | XP:`{all_xp}`\n"
            count += 1
        total_xp = sum(user["XP"] for user in user_info)
        gang_xp = gang_all_xp("./app/data/event_allxp.json")

        embed = discord.Embed(
            title="XP Event",
            description=f"{RESULT}\n**```All Point: {total_xp}\nGang XP: {gang_xp}```**\n\n{GANG_NAME}",
            color=discord.Color.random(),
        )
        if interaction.guild.icon:
            embed.set_thumbnail(url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="xp-reset", description="ریست تمام اکس پی ها")
    @app_commands.describe(confirms="برای تایید Y ارسال کنید")
    @app_commands.checks.has_any_role(*ROLE_XP_MANAGER)
    async def xpreset(self, interaction: discord.Interaction, confirms: str):
        if confirms.lower() == "y":
            reset_xp("./app/data/rob_xp.json")
            reset_all_xp("./app/data/rob_allxp.json")
            embed = discord.Embed(title="تمام اکس پی ها ریست شد", description=GANG_NAME, color=discord.Color.random())
            if interaction.guild.icon:
                embed.set_thumbnail(url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="لغو شد", description=GANG_NAME, color=discord.Color.random())
            if interaction.guild.icon:
                embed.set_thumbnail(url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="xp-reset-event", description="Event Reset XP")
    @app_commands.describe(confirms="برای تایید Y ارسال کنید")
    @app_commands.checks.has_any_role(*ROLE_XP_MANAGER)
    async def xpresetevent(self, interaction: discord.Interaction, confirms: str):
        if confirms.lower() == "y":
            reset_xp("./app/data/event_xp.json")
            reset_all_xp("./app/data/event_allxp.json")
            embed = discord.Embed(
                title="تمام اکس پی های ایونت ریست شد", description=GANG_NAME, color=discord.Color.random()
            )
            if interaction.guild.icon:
                embed.set_thumbnail(url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="لغو شد", description=GANG_NAME, color=discord.Color.random())
            if interaction.guild.icon:
                embed.set_thumbnail(url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.checks.has_any_role(*ROLE_XP_MANAGER)
    @app_commands.command(name="xp-decrease", description="کسر کردن اکس پی چندنفر")
    async def xpdecrease(self, interaction: discord.Interaction, xp: int, robbers: str, reason: str):
        Users = rejex(robbers)
        for i in Users:
            decrease_user_xp(i, xp, file_name="./app/data/rob_xp.json")
        for i in Users:
            decrease_user_xp(i, xp, file_name="./app/data/event_xp.json")
        kasr_all_xp(xp, file_name="./app/data/rob_allxp.json")
        kasr_all_xp(xp, file_name="./app/data/event_allxp.json")
        embed = discord.Embed(
            title="Kasr Xp User",
            description=f"Tedad `{xp}XP` Az {robbers} Kasr Shod\nreason: {reason}\n\n{GANG_NAME}",
            color=discord.Color.random(),
        )
        if interaction.guild.icon:
            embed.set_thumbnail(url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(_Rub(bot))
