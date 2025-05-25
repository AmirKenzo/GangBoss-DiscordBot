from discord.ext import commands
import time
import aiohttp


class Ping(commands.Cog, name="ping"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Check the bot's latency")
    async def ping(self, ctx):
        """ping"""
        await ctx.send(
            f"ping: `{round(self.bot.latency * 1000)}ms` | websocket: `{round(self.bot.ws.latency * 1000)}ms`"
        )

    @commands.command(name="ping_api", help="Check the API response time")
    async def ping_api(self, ctx):
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://discord.com/api/v10/gateway") as response:
                if response.status == 200:
                    end_time = time.time()
                    api_latency = (end_time - start_time) * 1000
                    await ctx.send(f"API Latency: {round(api_latency)}ms")
                else:
                    await ctx.send("Failed to reach Discord API")


async def setup(bot):
    await bot.add_cog(Ping(bot))
