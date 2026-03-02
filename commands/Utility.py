from discord.ext import commands
from discord import app_commands
import discord
import time

COG = True

class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = time.time()

    Utility = app_commands.Group(name="utility", description="Utility commands")

    @Utility.command(name="ping", description="Check bot latency")
    async def ping(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="<:stats:1473332978074648638> | Dynasty | Latency",
            description=f"> **API Latency:** `{round(self.bot.latency * 1000)}ms`",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Utility.command(name="avatar", description="Get a user's avatar from the server")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        try:
            embed = discord.Embed(
                title=f"{member.display_name}'s Avatar",
                color=100
            )
            embed.set_image(url=member.avatar.url)
            await interaction.response.send_message(embed=embed)
        except Exception:
            embed = discord.Embed(
                title="Avatar | Error",
                description=f"> **It appears this user ({member.mention}) does not have an avatar uploaded**",
                color=100
            )
            await interaction.response.send_message(embed=embed)

    @Utility.command(name="userinfo", description="Get information about a user")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user

        created_ts = int(member.created_at.timestamp())
        joined_ts = int(member.joined_at.timestamp())

        roles = [r.mention for r in member.roles if r.name != "@everyone"]

        description = (
            f"**__User Overview__**\n"
            f"> **ID:** {member.id}\n"
            f"> **Top Role:** {member.top_role.mention}\n"
            f"> **Account Created:** <t:{created_ts}:R>\n"
            f"> **Joined Server:** <t:{joined_ts}:R>\n\n"
            f"**__Roles__**\n"
            f"> {', '.join(roles) if roles else 'None'}"
        )

        embed = discord.Embed(
            title=f"{member.display_name} | User Info",
            description=description,
            color=100
        )
        embed.set_thumbnail(url=member.avatar.url)
        await interaction.response.send_message(embed=embed)

    @Utility.command(name="serverinfo", description="Get information about the server")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        created_ts = int(guild.created_at.timestamp())

        total_members = guild.member_count
        bot_count = len([m for m in guild.members if m.bot])
        human_count = total_members - bot_count

        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)

        description = (
            f"**__Guild Overview__**\n"
            f"> **ID:** {guild.id}\n"
            f"> **Owner:** {guild.owner.mention}\n"
            f"> **Boost Tier:** {guild.premium_tier}\n"
            f"> **Boosts:** {guild.premium_subscription_count}\n"
            f"> **Created:** <t:{created_ts}:R>\n\n"
            f"**__Guild Channels__**\n"
            f"> **Categories:** {categories}\n"
            f"> **Text Channels:** {text_channels}\n"
            f"> **Voice Channels:** {voice_channels}\n\n"
            f"**__Guild Members__**\n"
            f"> **Total:** {total_members}\n"
            f"> **Humans:** {human_count}\n"
            f"> **Bots:** {bot_count}"
        )

        embed = discord.Embed(
            title=f"{guild.name} | Server Info",
            description=description,
            color=100
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        await interaction.response.send_message(embed=embed)

    @Utility.command(name="roleinfo", description="Get information about a role")
    @app_commands.describe(role="The role to get info about")
    async def roleinfo(self, interaction: discord.Interaction, role: discord.Role):
        created_ts = int(role.created_at.timestamp())
        members = len(role.members)
        
        position = len(interaction.guild.roles) - role.position

        perms = []
        for perm, value in role.permissions:
            if value:
                perms.append(perm.replace("_", " ").title())
        
        perms_text = ", ".join(perms) if perms else "None"

        description = (
            f"**__Role Overview__**\n"
            f"> **Name:** {role.mention}\n"
            f"> **ID:** {role.id}\n"
            f"> **Color:** `{role.color}`\n"
            f"> **Position:** {position}\n"
            f"> **Members:** {members}\n"
            f"> **Created:** <t:{created_ts}:R>\n\n"
            f"**__Permissions__**\n"
            f"> {perms_text}"
        )

        embed = discord.Embed(
            title=f"{role.name} | Role Info",
            description=description,
            color=role.color
        )
        await interaction.response.send_message(embed=embed)

    @Utility.command(name="channelinfo", description="Get information about a channel")
    @app_commands.describe(channel="The channel to get info about")
    async def channelinfo(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        if channel is None:
            channel = interaction.channel
        
        created_ts = int(channel.created_at.timestamp())
        
        topic = channel.topic if channel.topic else "No topic set"
        
        slowmode = channel.slowmode_delay

        description = (
            f"**__Channel Overview__**\n"
            f"> **Name:** {channel.mention}\n"
            f"> **ID:** {channel.id}\n"
            f"> **Category:** {channel.category.mention if channel.category else 'None'}\n"
            f"> **Topic:** {topic}\n"
            f"> **Slowmode:** {slowmode} seconds\n"
            f"> **NSFW:** {'Yes' if channel.is_nsfw() else 'No'}\n"
            f"> **Created:** <t:{created_ts}:R>"
        )

        embed = discord.Embed(
            title=f"{channel.name} | Channel Info",
            description=description,
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Utility.command(name="botinfo", description="Get information about the bot")
    async def botinfo(self, interaction: discord.Interaction):
        uptime = int(time.time() - self.start_time)
        hours, remainder = divmod(uptime, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        total_servers = len(self.bot.guilds)
        total_members = sum(len(guild.members) for guild in self.bot.guilds)
        
        app_info = await self.bot.application_info()
        owner = app_info.owner

        description = (
            f"**__Bot Overview__**\n"
            f"> **Name:** {self.bot.user.mention}\n"
            f"> **ID:** {self.bot.user.id}\n"
            f"> **Owner:** {owner.mention}\n"
            f"> **Created:** <t:{int(self.bot.user.created_at.timestamp())}:R>\n\n"
            f"**__Statistics__**\n"
            f"> **Servers:** {total_servers}\n"
            f"> **Total Members:** {total_members}\n"
            f"> **Uptime:** {hours}h {minutes}m {seconds}s"
        )

        embed = discord.Embed(
            title=f"{self.bot.user.name} | Bot Info",
            description=description,
            color=100
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    @Utility.command(name="uptime", description="Check bot uptime")
    async def uptime(self, interaction: discord.Interaction):
        uptime = int(time.time() - self.start_time)
        hours, remainder = divmod(uptime, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        embed = discord.Embed(
            title="<:stats:1473332978074648638> | Dynasty | Uptime",
            description=f"> **Uptime:** `{hours}h {minutes}m {seconds}s`",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Utility.command(name="emotes", description="List server emotes")
    async def emotes(self, interaction: discord.Interaction):
        guild = interaction.guild
        
        if not guild.emojis:
            embed = discord.Embed(
                title="<:stats:1473332978074648638> | Dynasty | Emotes",
                description="> **This server has no custom emotes**",
                color=100
            )
            await interaction.response.send_message(embed=embed)
            return
        
        animated = [str(e) for e in guild.emojis if e.animated]
        static = [str(e) for e in guild.emojis if not e.animated]
        
        description = ""
        
        if static:
            description += f"**__Static Emotes ({len(static)})__**\n"
            description += " ".join(static) + "\n\n"
        
        if animated:
            description += f"**__Animated Emotes ({len(animated)})__**\n"
            description += " ".join(animated)
        
        embed = discord.Embed(
            title=f"{guild.name} | Emotes",
            description=description,
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Utility.command(name="steal", description="Add an emote to the server")
    @app_commands.describe(emoji="The emoji to add (can be a custom emoji)", name="The name for the emote")
    async def steal(self, interaction: discord.Interaction, emoji: str, name: str):
        if not interaction.user.guild_permissions.manage_emojis:
            embed = discord.Embed(
                title="<:stats:1473332978074648638> | Dynasty | Steal Emote Error",
                description="> **You need the ``Manage Emojis`` permission to use this command!**",
                color=100
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if emoji.startswith("<") and emoji.endswith(">"):
            animated = emoji.startswith("<a:")
            emoji_id = emoji.split(":")[-1].rstrip(">")
            url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{'gif' if animated else 'png'}"
        else:
            url = None
        
        try:
            if url:
                response = await self.bot.session.get(url)
                image = await response.read()
            else:
                embed = discord.Embed(
                    title="<:stats:1473332978074648638> | Dynasty | Steal Emote",
                    description="> **Please provide a custom emoji to steal**",
                    color=100
                )
                await interaction.response.send_message(embed=embed)
                return
            
            guild = interaction.guild
            await guild.create_custom_emoji(name=name, image=image)
            
            embed = discord.Embed(
                title="<:stats:1473332978074648638> | Dynasty | Steal Emote",
                description=f"> **Added emote:** `{name}`\n> **Emoji:** {emoji}",
                color=100
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="<:stats:1473332978074648638> | Dynasty | Steal Emote Error",
                description=f"> **Failed to add emote:** {str(e)}",
                color=100
            )
            await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))
