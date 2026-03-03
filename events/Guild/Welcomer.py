import discord
from discord.ext import commands
from utils.db.functions import welcomer as db

COG = True


class WelcomerEvents(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def parse_variables(self, text: str, guild: discord.Guild, member: discord.Member):
        if not text:
            return text
        text = text.replace("{user.mention}", member.mention)
        text = text.replace("{user.name}", member.name)
        text = text.replace("{user.id}", str(member.id))
        text = text.replace("{member.number}", str(guild.member_count))
        return text

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        settings = db.get_settings(member.guild.id)
        if not settings:
            return

        if settings.get("autorole_status") == "enabled" and settings.get("autorole_id"):
            role = member.guild.get_role(settings["autorole_id"])
            if role:
                try:
                    await member.add_roles(role)
                except:
                    pass

        if settings.get("welcomer_status") != "enabled":
            return

        channel_id = settings.get("welcomer_channel_id")
        if not channel_id:
            return

        channel = member.guild.get_channel(channel_id)
        if not channel:
            return

        embed_data = settings.get("embed") or {}

        title = self.parse_variables(embed_data.get("title"), member.guild, member)
        description = self.parse_variables(embed_data.get("description"), member.guild, member)
        author_text = self.parse_variables(embed_data.get("author"), member.guild, member)
        footer_text = self.parse_variables(embed_data.get("footer"), member.guild, member)

        embed = discord.Embed(
            title=title,
            description=description,
            color=embed_data.get("color", 0x5865F2)
        )

        if author_text:
            embed.set_author(name=author_text)

        if footer_text:
            embed.set_footer(text=footer_text)

        embed.timestamp = discord.utils.utcnow()

        try:
            await channel.send(content=member.mention, embed=embed)
        except:
            pass


async def setup(bot):
    await bot.add_cog(WelcomerEvents(bot))