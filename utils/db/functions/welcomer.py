import aiosqlite
import json

DB_PATH = "database.db"


async def initialize_welcomer_table():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS welcomer_settings (
                guild_id INTEGER PRIMARY KEY,
                autorole_id INTEGER,
                welcomer_channel_id INTEGER,
                embed_json TEXT,
                autorole_status TEXT DEFAULT 'disabled',
                welcomer_status TEXT DEFAULT 'disabled'
            );
        """)
        await db.commit()


async def ensure_guild_exists(guild_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR IGNORE INTO welcomer_settings (guild_id)
            VALUES (?)
        """, (guild_id,))
        await db.commit()


async def get_settings(guild_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("""
            SELECT autorole_id, welcomer_channel_id, embed_json,
                   autorole_status, welcomer_status
            FROM welcomer_settings
            WHERE guild_id = ?
        """, (guild_id,)) as cursor:
            row = await cursor.fetchone()

    if not row:
        return None

    embed_data = json.loads(row[2]) if row[2] else None

    return {
        "autorole_id": row[0],
        "welcomer_channel_id": row[1],
        "embed": embed_data,
        "autorole_status": row[3],
        "welcomer_status": row[4]
    }


async def update_autorole(guild_id: int, role_id: int):
    await ensure_guild_exists(guild_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE welcomer_settings
            SET autorole_id = ?
            WHERE guild_id = ?
        """, (role_id, guild_id))
        await db.commit()


async def update_welcomer_channel(guild_id: int, channel_id: int):
    await ensure_guild_exists(guild_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE welcomer_settings
            SET welcomer_channel_id = ?
            WHERE guild_id = ?
        """, (channel_id, guild_id))
        await db.commit()


async def update_embed(guild_id: int, embed_dict: dict):
    await ensure_guild_exists(guild_id)
    embed_json = json.dumps(embed_dict)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE welcomer_settings
            SET embed_json = ?
            WHERE guild_id = ?
        """, (embed_json, guild_id))
        await db.commit()


async def set_autorole_status(guild_id: int, status: str):
    await ensure_guild_exists(guild_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE welcomer_settings
            SET autorole_status = ?
            WHERE guild_id = ?
        """, (status, guild_id))
        await db.commit()


async def set_welcomer_status(guild_id: int, status: str):
    await ensure_guild_exists(guild_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE welcomer_settings
            SET welcomer_status = ?
            WHERE guild_id = ?
        """, (status, guild_id))
        await db.commit()