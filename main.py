from utils.cog.loader import load_commands, load_events
from utils.client.config import BOT_TOKEN, BOT_PREFIX
import discord; from discord.ext import commands
import sys

sys.dont_write_bytecode = True

class Client(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=BOT_PREFIX,
            intents=discord.Intents.all(),
            help_command=None
        )

    async def setup_hook(self):
        await load_commands(self)
        await load_events(self)

bot = Client()
bot.run(BOT_TOKEN, log_handler=None)
