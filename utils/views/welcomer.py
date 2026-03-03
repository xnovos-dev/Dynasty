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

        container.add_item(ui.TextDisplay(
            f"### Welcomer Panel\n"
            f"> **Status:** {status}\n"
            f"> **Channel:** {channel}\n"
            f"> **Auto Role:** {role}"
        ))

        row = ui.ActionRow()

        enable_btn = ui.Button(label="Enable", style=discord.ButtonStyle.success)
        disable_btn = ui.Button(label="Disable", style=discord.ButtonStyle.danger)

        enable_btn.callback = self.enable_callback
        disable_btn.callback = self.disable_callback

        row.add_item(enable_btn)
        row.add_item(disable_btn)

        container.add_item(row)
        self.add_item(container)

    async def interaction_check(self, interaction):
        return interaction.user.id == self.author.id

    async def enable_callback(self, interaction):
        await db.set_welcomer_status(self.guild.id, "enabled")
        self.data["enabled"] = True
        self.build_view()
        await interaction.response.edit_message(view=self)

    async def disable_callback(self, interaction):
        await db.set_welcomer_status(self.guild.id, "disabled")
        self.data["enabled"] = False
        self.build_view()
        await interaction.response.edit_message(view=self)