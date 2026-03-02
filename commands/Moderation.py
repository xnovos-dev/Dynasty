from discord.ext import commands
from discord import app_commands
import discord
from datetime import datetime

COG = True

class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    Moderation = app_commands.Group(name="moderation", description="Moderation commands")

    @Moderation.command(name="purge", description="Delete a number of messages")
    @app_commands.describe(amount="Number of messages to delete")
    async def purge(self, interaction: discord.Interaction, amount: int = 5):
        if not interaction.user.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="<:stats:1473332978074648638> | Dynasty | Purge Error",
                description="> **You need the ``Manage Messages`` permission to use this command!**",
                color=100
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if amount < 1:
            amount = 1
        if amount > 100:
            amount = 100

        deleted = await interaction.channel.purge(limit=amount + 1)
        
        embed = discord.Embed(
            title="<:stats:1473332978074648638> | Dynasty | Purge",
            description=f"> **Deleted:** `{len(deleted)}` messages",
            color=100
        )
        await interaction.response.send_message(embed=embed, delete_after=3)

    @Moderation.command(name="lock", description="Lock a channel")
    @app_commands.describe(channel="The channel to lock (defaults to current channel)")
    async def lock(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        if not interaction.user.guild_permissions.manage_channels:
            embed = discord.Embed(
                title="<:stats:1473332978074648638> | Dynasty | Lock Error",
                description="> **You need the ``Manage Channels`` permission to use this command!**",
                color=100
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if channel is None:
            channel = interaction.channel
        
        everyone_role = interaction.guild.default_role
        
        overwrites = channel.overwrites
        overwrites[everyone_role] = discord.PermissionOverwrite(
            send_messages=False,
            add_reactions=False
        )
        
        await channel.edit(overwrites=overwrites)
        
        embed = discord.Embed(
            title="<:stats:1473332978074648638> | Dynasty | Lock",
            description=f"> **Channel:** {channel.mention}\n> **Status:** Locked 🔒",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Moderation.command(name="unlock", description="Unlock a channel")
    @app_commands.describe(channel="The channel to unlock (defaults to current channel)")
    async def unlock(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        if not interaction.user.guild_permissions.manage_channels:
            embed = discord.Embed(
                title="<:stats:1473332978074648638> | Dynasty | Unlock Error",
                description="> **You need the ``Manage Channels`` permission to use this command!**",
                color=100
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if channel is None:
            channel = interaction.channel
        
        everyone_role = interaction.guild.default_role
        
        overwrites = channel.overwrites
        overwrites[everyone_role] = discord.PermissionOverwrite(
            send_messages=None,
            add_reactions=None
        )
        
        await channel.edit(overwrites=overwrites)
        
        embed = discord.Embed(
            title="<:stats:1473332978074648638> | Dynasty | Unlock",
            description=f"> **Channel:** {channel.mention}\n> **Status:** Unlocked 🔓",
            color=100
        )
        await interaction.response.send_message(embed=embed)

    @Moderation.command(
        name="ban",
        description="Bans a user from the server"
    )
    @app_commands.describe(member="The member to ban", reason="Reason for the ban")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        user = interaction.user
        bot_member = interaction.guild.me
        
        if not user.guild_permissions.ban_members:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You are missing the** ``ban_members`` **permission**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if not bot_member.guild_permissions.ban_members:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **I am missing the** ``ban_members`` **permission**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member == user:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You cannot ban yourself**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member == bot_member:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You cannot ban the bot**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member == interaction.guild.owner:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You cannot ban the server owner**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member.top_role >= user.top_role and user != interaction.guild.owner:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You cannot ban a member with an equal or higher role**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member.top_role >= bot_member.top_role:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **I cannot ban a member with a higher role than me**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        await member.ban(reason=reason)
        
        embed = discord.Embed(
            title="<:ban_hammer:1473324467072667822> | Dynasty | Member Banned",
            description=f"> **{member}** has been banned by **{user}**\n> Reason: ``{reason or 'No reason provided'}``",
            color=100,
            timestamp=datetime.now()
        )
        await interaction.response.send_message(embed=embed)

    @Moderation.command(
        name="unban",
        description="Unbans a user from the server"
    )
    @app_commands.describe(user="The user to unban", reason="Reason for the unban")
    async def unban(self, interaction: discord.Interaction, user: discord.User, reason: str = None):
        author = interaction.user
        bot_member = interaction.guild.me
        
        if not author.guild_permissions.ban_members:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You are missing the** ``ban_members`` **permission**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {author.name} ( ID: {author.id} )",
                icon_url=author.display_avatar.url if author.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if not bot_member.guild_permissions.ban_members:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **I am missing the** ``ban_members`` **permission**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {author.name} ( ID: {author.id} )",
                icon_url=author.display_avatar.url if author.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        try:
            await interaction.guild.unban(user, reason=reason)
        except discord.NotFound:
            embed = discord.Embed(
                title="Dynasty | Error",
                description=f"> **{user}** is not banned from this server",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {author.name} ( ID: {author.id} )",
                icon_url=author.display_avatar.url if author.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        embed = discord.Embed(
            title="<:ban_hammer:1473324467072667822> | Dynasty | Member Unbanned",
            description=f"> **{user}** has been unbanned by **{author}**\n> Reason: ``{reason or 'No reason provided'}``",
            color=100,
            timestamp=datetime.now()
        )
        await interaction.response.send_message(embed=embed)

    @Moderation.command(
        name="kick",
        description="Kicks a user from the server"
    )
    @app_commands.describe(member="The member to kick", reason="Reason for the kick")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        user = interaction.user
        bot_member = interaction.guild.me
        
        if not user.guild_permissions.kick_members:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You are missing the** ``kick_members`` **permission**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if not bot_member.guild_permissions.kick_members:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **I am missing the** ``kick_members`` **permission**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member == user:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You cannot kick yourself**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member == bot_member:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You cannot kick the bot**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member == interaction.guild.owner:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You cannot kick the server owner**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member.top_role >= user.top_role and user != interaction.guild.owner:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You cannot kick a member with an equal or higher role**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member.top_role >= bot_member.top_role:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **I cannot kick a member with a higher role than me**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        await member.kick(reason=reason)
        
        embed = discord.Embed(
            title="<:kick:1473327064458330237> | Dynasty | Member Kicked",
            description=f"> **{member}** has been kicked by **{user}**\n> Reason: ``{reason or 'No reason provided'}``",
            color=100,
            timestamp=datetime.now()
        )
        await interaction.response.send_message(embed=embed)

    @Moderation.command(
        name="softban",
        description="Bans and immediately unbans a user to delete their messages"
    )
    @app_commands.describe(member="The member to softban", reason="Reason for the softban")
    async def softban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        user = interaction.user
        bot_member = interaction.guild.me
        
        if not user.guild_permissions.ban_members:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You are missing the** ``ban_members`` **permission**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if not bot_member.guild_permissions.ban_members:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **I am missing the** ``ban_members`` **permission**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member == user:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You cannot softban yourself**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member == bot_member:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You cannot softban the bot**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member == interaction.guild.owner:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You cannot softban the server owner**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member.top_role >= user.top_role and user != interaction.guild.owner:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You cannot softban a member with an equal or higher role**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member.top_role >= bot_member.top_role:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **I cannot softban a member with a higher role than me**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        await member.ban(reason=reason, delete_message_days=7)
        await member.unban(reason=reason)
        
        embed = discord.Embed(
            title="<:ban_hammer:1473324467072667822> | Dynasty | Member Softbanned",
            description=f"> **{member}** has been softbanned by **{user}**\n> Reason: ``{reason or 'No reason provided'}``\n> (Messages from the last 7 days have been deleted)",
            color=100,
            timestamp=datetime.now()
        )
        await interaction.response.send_message(embed=embed)

    @Moderation.command(
        name="timeout",
        description="Timeout a member"
    )
    @app_commands.describe(member="The member to timeout", duration="Duration of the timeout", reason="Reason for the timeout")
    @app_commands.choices(duration=[
        app_commands.Choice[str](name="5 Minutes", value="5m"),
        app_commands.Choice[str](name="10 Minutes", value="10m"),
        app_commands.Choice[str](name="30 Minutes", value="30m"),
        app_commands.Choice[str](name="1 Hour", value="1h"),
        app_commands.Choice[str](name="6 Hours", value="6h"),
        app_commands.Choice[str](name="12 Hours", value="12h"),
        app_commands.Choice[str](name="1 Day", value="1d"),
        app_commands.Choice[str](name="3 Days", value="3d"),
        app_commands.Choice[str](name="7 Days", value="7d")
    ])
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, duration: str = "10m", reason: str = None):
        user = interaction.user
        bot_member = interaction.guild.me
        
        if not user.guild_permissions.moderate_members:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You are missing the** ``moderate_members`` **permission**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if not bot_member.guild_permissions.moderate_members:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **I am missing the** ``moderate_members`` **permission**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member == user:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You cannot timeout yourself**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member == bot_member:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You cannot timeout the bot**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member == interaction.guild.owner:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You cannot timeout the server owner**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member.top_role >= user.top_role and user != interaction.guild.owner:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You cannot timeout a member with an equal or higher role**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member.top_role >= bot_member.top_role:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **I cannot timeout a member with a higher role than me**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        duration_map = {
            "5m": 5,
            "10m": 10,
            "30m": 30,
            "1h": 60,
            "6h": 360,
            "12h": 720,
            "1d": 1440,
            "3d": 4320,
            "7d": 10080
        }
        
        timeout_duration = duration_map.get(duration, 10)
        from datetime import timedelta
        timeout_until = datetime.now() + timedelta(minutes=timeout_duration)
        
        await member.timeout(timeout_until, reason=reason)
        
        embed = discord.Embed(
            title="<:stats:1473332978074648638> | Dynasty | Member Timed Out",
            description=f"> **{member}** has been timed out by **{user}**\n> **Duration:** `{duration}`\n> Reason: ``{reason or 'No reason provided'}``",
            color=100,
            timestamp=datetime.now()
        )
        await interaction.response.send_message(embed=embed)

    @Moderation.command(
        name="untimeout",
        description="Remove timeout from a member"
    )
    @app_commands.describe(member="The member to remove timeout from", reason="Reason for removing the timeout")
    async def untimeout(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        user = interaction.user
        bot_member = interaction.guild.me
        
        if not user.guild_permissions.moderate_members:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **You are missing the** ``moderate_members`` **permission**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if not bot_member.guild_permissions.moderate_members:
            embed = discord.Embed(
                title="Dynasty | Permission Denied",
                description="> **I am missing the** ``moderate_members`` **permission**",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        if member.is_timed_out() is False:
            embed = discord.Embed(
                title="Dynasty | Error",
                description=f"> **{member}** is not timed out",
                color=100,
                timestamp=datetime.now()
            )
            embed.set_author(
                name=f"{interaction.guild.name} ( ID: {interaction.guild.id} )",
                icon_url=interaction.guild.icon.url if interaction.guild.icon else None
            )
            embed.set_footer(
                text=f"Requested by {user.name} ( ID: {user.id} )",
                icon_url=user.display_avatar.url if user.display_avatar else None
            )
            await interaction.response.send_message(embed=embed)
            return
        
        await member.timeout(None, reason=reason)
        
        embed = discord.Embed(
            title="<:stats:1473332978074648638> | Dynasty | Timeout Removed",
            description=f"> **Timeout removed from** **{member}** by **{user}**\n> Reason: ``{reason or 'No reason provided'}``",
            color=100,
            timestamp=datetime.now()
        )
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
