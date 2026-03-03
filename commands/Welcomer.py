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

    Welcomer = app_commands.Group(
        name="welcomer",
        description="Welcomer commands"
    )

    @Welcomer.command(name="panel", description="Shows the welcomer panel for configurating the welcomer")
    async def panel(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.manage_guild:
            embed = discord.Embed(
                title="Dynasty | Error",
                description="> **You need** ``manage_server`` **permission to use this**",
                color=0x64
            )
            return await interaction.response.send_message(embed=embed)

        await db.ensure_guild_exists(interaction.guild.id)
        view = WelcomerPanel(self.bot, interaction.guild, interaction.user)
        await view.setup()
        await interaction.response.send_message(view=view, ephemeral=True)

    @Welcomer.command(name="enable", description="Enable the welcomer")
    async def enable(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.manage_guild:
            embed = discord.Embed(
                title="Dynasty | Error",
                description="> **You need** ``manage_server`` **permission to use this**",
                color=0x64
            )
            return await interaction.response.send_message(embed=embed)

        await db.ensure_guild_exists(interaction.guild.id)
        await db.set_welcomer_status(interaction.guild.id, "enabled")
        embed = discord.Embed(
            title="Dynasty | Welcomer",
            description="> Welcomer has been **enabled**.",
            color=0x64
        )
        await interaction.response.send_message(embed=embed)

    @Welcomer.command(name="disable", description="Disable the welcomer")
    async def disable(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.manage_guild:
            embed = discord.Embed(
                title="Dynasty | Error",
                description="> **You need** ``manage_server`` **permission to use this**",
                color=0x64
            )
            return await interaction.response.send_message(embed=embed)

        await db.ensure_guild_exists(interaction.guild.id)
        await db.set_welcomer_status(interaction.guild.id, "disabled")
        embed = discord.Embed(
            title="Dynasty | Welcomer",
            description="> Welcomer has been **disabled**.",
            color=0x64
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Welcomer(bot))