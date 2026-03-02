from discord.ext import commands
from discord import app_commands
from datetime import datetime
import discord

COG = True

class UtilityCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    Utility = app_commands.Group(name="utility", description="Utility commands")

    @Utility.command(name="ping", description="Check bot latency")
    async def ping(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="<:stats:1473332978074648638> | Dynasty | Latency",
            description=f"> **API Latency:** ``{round(self.bot.latency * 1000)}ms``",
            color=100,
            timestamp=datetime.now()
        )
        await interaction.response.send_message(embed=embed)

    @Utility.command(name="avatar", description="Get a users avatar from the server")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        if member == None:
            member = interaction.user
        try:
            embed = discord.Embed(
                title=f"{member.display_name}'s Avatar",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_image(url=member.avatar.url)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title=f"Avatar | Error",
                description=f"> **It appears this user ({member.mention}) does not have an avatar uploaded**",
                color=100,
                timestamp=datetime.now()
            )
            await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(UtilityCog(bot))