from utils.cog.loader import load
from utils.client.config import BOT_TOKEN, BOT_PREFIX
import discord; from discord.ext import commands


class Client(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=BOT_PREFIX,
            intents=discord.Intents.all(),
            help_command=None
        )

    async def setup_hook(self):
        await load(self)

bot = Client()
bot.run(BOT_TOKEN)
