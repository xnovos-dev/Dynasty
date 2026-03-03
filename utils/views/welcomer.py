import discord
from discord import ui
from utils.db.functions import welcomer as db


class WelcomerPanel(ui.LayoutView):

    def __init__(self, bot, guild, author):
        super().__init__(timeout=300)
        self.bot = bot
        self.guild = guild
        self.author = author
        self.data = {}

    async def setup(self):
        settings = await db.get_settings(self.guild.id) or {}
        embed_data = settings.get("embed") or {}

        self.data = {
            "enabled": settings.get("welcomer_status") == "enabled",
            "channel_id": settings.get("welcomer_channel_id"),
            "auto_role_id": settings.get("autorole_id"),
            "embed": embed_data
        }

        self.build_view()

    def parse_variables(self, text, user):
        if not text:
            return text
        text = text.replace("{user.mention}", user.mention)
        text = text.replace("{user.name}", user.name)
        text = text.replace("{user.id}", str(user.id))
        text = text.replace("{member.number}", str(self.guild.member_count))
        return text

    def build_view(self):
        self.clear_items()

        container = ui.Container(accent_color=0x64)

        status = "Enabled" if self.data.get("enabled") else "Disabled"
        channel = f"<#{self.data.get('channel_id')}>" if self.data.get("channel_id") else "Not set"
        role = f"<@&{self.data.get('auto_role_id')}>" if self.data.get("auto_role_id") else "Not set"
        embed_title = self.data['embed'].get("title") or "Not set"
        embed_desc = self.data['embed'].get("description") or "Not set"

        container.add_item(ui.TextDisplay(
            f"### Welcomer Panel\n"
            f"> **Status:** {status}\n"
            f"> **Channel:** {channel}\n"
            f"> **Auto Role:** {role}\n"
            f"> **Embed Title:** {embed_title}\n"
            f"> **Embed Description:** {embed_desc}\n"
            f"### Available Variables\n"
            f"> {{user.mention}}\n"
            f"> {{user.name}}\n"
            f"> {{user.id}}\n"
            f"> {{member.number}}"
        ))

        row1 = ui.ActionRow()

        set_channel = ui.Button(label="Set Channel", style=discord.ButtonStyle.secondary)
        set_role = ui.Button(label="Set Auto Role", style=discord.ButtonStyle.secondary)
        edit_embed = ui.Button(label="Edit Embed", style=discord.ButtonStyle.secondary)

        set_channel.callback = self.set_channel_callback
        set_role.callback = self.set_role_callback
        edit_embed.callback = self.edit_embed_callback

        row1.add_item(set_channel)
        row1.add_item(set_role)
        row1.add_item(edit_embed)

        row2 = ui.ActionRow()
        enable_btn = ui.Button(label="Enable", style=discord.ButtonStyle.secondary)
        disable_btn = ui.Button(label="Disable", style=discord.ButtonStyle.secondary)
        preview_btn = ui.Button(label="Preview Embed", style=discord.ButtonStyle.secondary)

        enable_btn.callback = self.enable_callback
        disable_btn.callback = self.disable_callback
        preview_btn.callback = self.preview_callback

        row2.add_item(enable_btn)
        row2.add_item(disable_btn)
        row2.add_item(preview_btn)

        container.add_item(row1)
        container.add_item(row2)

        self.add_item(container)

    async def interaction_check(self, interaction):
        return interaction.user.id == self.author.id

    async def enable_callback(self, interaction):
        if not interaction.user.guild_permissions.manage_guild:
            embed = discord.Embed(
                title="Dynasty | Error",
                description="> **You need** ``manage_server`` **permission to use this**",
                color=0x64
            )
            return await interaction.response.send_message(embed=embed)
        await db.set_welcomer_status(self.guild.id, "enabled")
        self.data["enabled"] = True
        self.build_view()
        await interaction.response.edit_message(view=self)

    async def disable_callback(self, interaction):
        if not interaction.user.guild_permissions.manage_guild:
            embed = discord.Embed(
                title="Dynasty | Error",
                description="> **You need** ``manage_server`` **permission to use this**",
                color=0x64
            )
            return await interaction.response.send_message(embed=embed)
        await db.set_welcomer_status(self.guild.id, "disabled")
        self.data["enabled"] = False
        self.build_view()
        await interaction.response.edit_message(view=self)

    async def set_channel_callback(self, interaction):
        if not interaction.user.guild_permissions.manage_guild:
            embed = discord.Embed(
                title="Dynasty | Error",
                description="> **You need** ``manage_server`` **permission to use this**",
                color=0x64
            )
            return await interaction.response.send_message(embed=embed)
        panel = self

        class ChannelModal(ui.Modal, title="Set Welcomer Channel"):
            channel_id = ui.TextInput(label="Channel ID", required=True)

            async def on_submit(modal_self, modal_interaction: discord.Interaction):
                try:
                    channel_id = int(modal_self.channel_id.value)
                    if not panel.guild.get_channel(channel_id):
                        raise ValueError
                except:
                    return await modal_interaction.response.send_message("Invalid channel ID.", ephemeral=True)

                await db.update_welcomer_channel(panel.guild.id, channel_id)
                panel.data["channel_id"] = channel_id
                panel.build_view()
                await modal_interaction.response.edit_message(view=panel)

        await interaction.response.send_modal(ChannelModal())

    async def set_role_callback(self, interaction):
        if not interaction.user.guild_permissions.manage_guild:
            embed = discord.Embed(
                title="Dynasty | Error",
                description="> **You need** ``manage_server`` **permission to use this**",
                color=0x64
            )
            return await interaction.response.send_message(embed=embed)
        panel = self

        class RoleModal(ui.Modal, title="Set Auto Role"):
            role_id = ui.TextInput(label="Role ID", required=True)

            async def on_submit(modal_self, modal_interaction: discord.Interaction):
                try:
                    role_id = int(modal_self.role_id.value)
                    if not panel.guild.get_role(role_id):
                        raise ValueError
                except:
                    return await modal_interaction.response.send_message("Invalid role ID.", ephemeral=True)

                await db.update_autorole(panel.guild.id, role_id)
                panel.data["auto_role_id"] = role_id
                panel.build_view()
                await modal_interaction.response.edit_message(view=panel)

        await interaction.response.send_modal(RoleModal())

    async def edit_embed_callback(self, interaction):
        if not interaction.user.guild_permissions.manage_guild:
            embed = discord.Embed(
                title="Dynasty | Error",
                description="> **You need** ``manage_server`` **permission to use this**",
                color=0x64
            )
            return await interaction.response.send_message(embed=embed)
        panel = self

        class EmbedModal(ui.Modal, title="Edit Welcome Embed"):
            embed_title = ui.TextInput(label="Embed Title", required=False)
            description = ui.TextInput(label="Description", style=discord.TextStyle.paragraph, required=False)
            color = ui.TextInput(label="Color (hex)", required=False)
            author = ui.TextInput(label="Author Content", required=False)
            footer = ui.TextInput(label="Footer Content", required=False)

            async def on_submit(modal_self, modal_interaction: discord.Interaction):
                embed_data = panel.data.get("embed") or {}

                embed_data["title"] = modal_self.embed_title.value
                embed_data["description"] = modal_self.description.value
                embed_data["author"] = modal_self.author.value
                embed_data["footer"] = modal_self.footer.value

                if modal_self.color.value:
                    try:
                        embed_data["color"] = int(modal_self.color.value.replace("#", ""), 16)
                    except:
                        embed_data["color"] = 0x5865F2

                await db.update_embed(panel.guild.id, embed_data)

                panel.data["embed"] = embed_data
                panel.build_view()
                await modal_interaction.response.edit_message(view=panel)

        await interaction.response.send_modal(EmbedModal())

    async def preview_callback(self, interaction):
        if not interaction.user.guild_permissions.manage_guild:
            embed = discord.Embed(
                title="Dynasty | Error",
                description="> **You need** ``manage_server`` **permission to use this**",
                color=0x64
            )
            return await interaction.response.send_message(embed=embed)
        embed_data = self.data.get("embed") or {}

        title = self.parse_variables(embed_data.get("title"), interaction.user)
        description = self.parse_variables(embed_data.get("description"), interaction.user)
        author_text = self.parse_variables(embed_data.get("author"), interaction.user)
        footer_text = self.parse_variables(embed_data.get("footer"), interaction.user)

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

        await interaction.response.send_message(
            content=self.parse_variables("{user.mention}", interaction.user),
            embed=embed,
            ephemeral=True
        )