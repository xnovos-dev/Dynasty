import discord
from discord.ext import commands, tasks
from colorama import Fore, Style, init
from datetime import datetime, timezone
import json
import os

init(autoreset=True)
COG = True

restart_channel_ID = 1479724097783992351
UPTIME_FILE = "uptime.json"


class OnReady(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = datetime.now(timezone.utc)
        self.sent_restart_embed = False
        self.save_uptime.start()

    def cog_unload(self):
        self.save_uptime.cancel()

    @tasks.loop(seconds=30)
    async def save_uptime(self):
        data = {
            "start_time": self.start_time.isoformat()
        }
        with open(UPTIME_FILE, "w") as f:
            json.dump(data, f)

    def get_previous_uptime(self):
        if not os.path.exists(UPTIME_FILE):
            return "Unknown"

        with open(UPTIME_FILE, "r") as f:
            data = json.load(f)

        old_start = datetime.fromisoformat(data["start_time"])
        uptime = datetime.now(timezone.utc) - old_start

        seconds = int(uptime.total_seconds())
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        return f"{days}d {hours}h {minutes}m {seconds}s"

    @commands.Cog.listener()
    async def on_ready(self):

        print(f"{Fore.CYAN}[INFO]{Fore.LIGHTBLACK_EX} Logged in as {Fore.GREEN}{self.bot.user}")

        synced = await self.bot.tree.sync()
        print(f"{Fore.CYAN}[INFO]{Fore.LIGHTBLACK_EX} Synced {Fore.GREEN}{len(synced)} commands{Style.RESET_ALL}")

        print(f"{Fore.CYAN}[INFO]{Fore.LIGHTBLACK_EX} Command Tree Visualiser")

        for cmd in self.bot.tree.get_commands():
            if hasattr(cmd, "commands") and cmd.commands:
                print(f"{Fore.LIGHTBLACK_EX}/{Fore.CYAN}{cmd.name} - [{Fore.GREEN}{len(cmd.commands)}{Fore.CYAN}]")
                for i, sub in enumerate(cmd.commands):
                    branch = " └─ " if i == len(cmd.commands)-1 else " ├─ "
                    print(f"{Fore.LIGHTBLACK_EX}{branch}{Fore.GREEN}{sub.name}")
            else:
                print(f"{Fore.LIGHTBLACK_EX}/{Fore.CYAN}{cmd.name}")

        if self.sent_restart_embed:
            return

        channel = self.bot.get_channel(restart_channel_ID)
        if channel is None:
            channel = await self.bot.fetch_channel(restart_channel_ID)

        previous_uptime = self.get_previous_uptime()

        embed = discord.Embed(
            title="Dynasty | Bot Restarted",
            description=f"> **Uptime:** {previous_uptime}\n> **Latency:** {round(self.bot.latency * 1000)} ms",
            color=100,
            timestamp=datetime.now(timezone.utc)
        )
        embed.set_footer(text=f"Dynasty | Restart Notifier")

        await channel.send(embed=embed)

        self.start_time = datetime.now(timezone.utc)
        self.sent_restart_embed = True


async def setup(bot: commands.Bot):
    await bot.add_cog(OnReady(bot))