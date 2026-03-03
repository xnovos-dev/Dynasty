import discord
from discord.ext import commands
from discord import app_commands
from utils.views.welcomer import WelcomerPanel
from utils.db.functions import welcomer as db

COG = True


class Welcomer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        await db.initialize_welcomer_table()

    @app_commands.command(name="welcomer")
    async def welcomer(self, interaction: discord.Interaction):
        await db.ensure_guild_exists(interaction.guild.id)
        view = WelcomerPanel(self.bot, interaction.guild, interaction.user)
        await view.setup()
        await interaction.response.send_message(view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Welcomer(bot))