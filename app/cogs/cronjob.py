import discord
from discord.ext import commands
import os
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from datetime import datetime, timedelta
from config import CHANNEL_ANNOUNCEMENT, CHANNEL_XP_REPORT, BANNER_LINK, GANG_NAME


def load_users():
    try:
        with open("app/data/rob_xp.json", "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}
    return users


def get_user_info():
    users = load_users()
    user_info = []
    for username, data in users.items():
        user_data = {"username": username, "XP": sum(data.values())}
        user_data.update({f"{rob}": xp for rob, xp in data.items()})
        user_info.append(user_data)
    sorted_user_info = sorted(user_info, key=lambda x: x["XP"], reverse=True)
    return sorted_user_info


def gang_all_xp():
    file_name = "app/data/rob_allxp.json"
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            data = json.load(f)
        return data["all_xp"]


def save_users(users):
    with open("app/data/rob_xp.json", "w") as file:
        json.dump(users, file)


def reset_xp():
    save_users({})


def reset_all_xp():
    file_name = "app/data/rob_allxp.json"
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


class SchedulerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
        self.schedule_jobs()
        self.schedule_cap()

    def schedule_jobs(self):
        trigger = CronTrigger(day_of_week="fri", hour=23, minute=59, timezone=pytz.timezone("Asia/Tehran"))
        self.scheduler.add_job(self.send_weekly_message, trigger)

    async def send_weekly_message(self):
        channel = self.bot.get_channel(CHANNEL_XP_REPORT)
        if channel:
            guild = channel.guild
            icon_url = guild.icon.url if guild.icon else None
            user_info = get_user_info()
            RESULT = ""
            count = 1
            for user in user_info:
                all_xp = user["XP"]
                RESULT += f"{count}- {user['username']} | XP:`{all_xp}`\n"
                count += 1
            total_xp = sum(user["XP"] for user in user_info)
            gang_xp = gang_all_xp()

            today = datetime.now()

            week_ago = today - timedelta(days=7)

            today_str = today.strftime("%Y/%m/%d")
            week_ago_str = week_ago.strftime("%Y/%m/%d")
            embed = discord.Embed(
                title="XP list for the last 7 days",
                description=f"{RESULT}\n**```All Point: {total_xp}\nGang XP: {gang_xp}```**\n**اکس پی لیست از تاریخ : {week_ago_str} تا {today_str} ریست شد.**\n{GANG_NAME}",
                color=discord.Color.random(),
            )
            if icon_url:
                embed.set_thumbnail(url=icon_url)
            await channel.send(embed=embed)

            reset_xp()
            reset_all_xp()
            await channel.send("@everyone")

    def schedule_cap(self):
        trigger = CronTrigger(day_of_week="sat,mon,wed", hour=20, minute=30, timezone=pytz.timezone("Asia/Tehran"))
        self.scheduler.add_job(self.send_message_cap, trigger)

    async def send_message_cap(self):
        channel = self.bot.get_channel(CHANNEL_ANNOUNCEMENT)
        if channel:
            guild = channel.guild
            icon_url = guild.icon.url if guild.icon else None
            embed = discord.Embed(
                title="",
                description="دوستان عزیز، 1 ساعت دیگر کپچر شروع می‌شود.\n\nهمگی در بیس و دیسکورد حضور داشته باشید.\n\nدر صورت نبودن، استرایک دریافت می‌کنید.\n\n",
                color=discord.Color.random(),
            )
            embed.set_author(name="Capture Event", icon_url=BANNER_LINK)
            embed.set_image(url="https://s8.uupload.ir/files/1_6ev9.png")
            embed.set_footer(text=GANG_NAME, icon_url=BANNER_LINK)
            if icon_url:
                embed.set_thumbnail(url=icon_url)
            await channel.send(embed=embed, delete_after=9000)
            await channel.send("@everyone", delete_after=9000)


async def setup(bot):
    await bot.add_cog(SchedulerCog(bot))
