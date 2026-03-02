from discord.ext import commands
from colorama import Fore, Style, init

init(autoreset=True)
COG = True

class OnReady(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

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

async def setup(bot: commands.Bot):
    await bot.add_cog(OnReady(bot))