import discord
from discord.ext import commands
from discord import app_commands
from config import GANG_NAME, ROLE_FAMILY


class _Plan(commands.Cog, name="_Plan"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    plans = {
        "Quest": "app/img/quest.png",
        "Jazire": "app/img/jazzire.png",
        "House Robbery": "app/img/houserobbery.png",
        "Car Rob": "app/img/carrob.jpg",
    }
    plan_choices = [app_commands.Choice(name=plan, value=index) for index, plan in enumerate(plans, start=1)]

    @app_commands.command(name="plan", description="Plan Quest")
    @app_commands.choices(plan=plan_choices)
    @app_commands.checks.has_any_role(*ROLE_FAMILY)
    async def plan_quest(
        self, interaction: discord.Interaction, plan: app_commands.Choice[int], tedad: int, players: str
    ):
        plan_name = list(self.plans.keys())[plan.value - 1]
        image_path = self.plans[plan_name]

        embed = discord.Embed(
            title=plan_name,
            description=f"`Tedad Plan: {tedad}`\n``Players:`` {players}\n\n{GANG_NAME}",
            color=discord.Color.green(),
        )
        file = discord.File(image_path, filename=image_path.split("/")[-1])
        embed.set_thumbnail(url=f"attachment://{file.filename}")
        await interaction.response.send_message(embed=embed, file=file)


async def setup(bot: commands.Bot):
    await bot.add_cog(_Plan(bot))
