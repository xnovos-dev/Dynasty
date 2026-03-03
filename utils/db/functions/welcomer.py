import sqlite3
import json
from typing import Optional, Dict, Any

DB_PATH = "database.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_welcomer_table():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS welcomer_settings (
                guild_id INTEGER PRIMARY KEY,
                autorole_id INTEGER,
                welcomer_channel_id INTEGER,
                embed_json TEXT,
                autorole_status TEXT DEFAULT 'disabled',
                welcomer_status TEXT DEFAULT 'disabled'
            );
        """)
        conn.commit()


def ensure_guild_exists(guild_id: int):
    with get_connection() as conn:
        conn.execute("""
            INSERT OR IGNORE INTO welcomer_settings (guild_id)
            VALUES (?)
        """, (guild_id,))
        conn.commit()


def get_settings(guild_id: int) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT autorole_id, welcomer_channel_id, embed_json,
                   autorole_status, welcomer_status
            FROM welcomer_settings
            WHERE guild_id = ?
        """, (guild_id,))
        row = cursor.fetchone()

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


def update_autorole(guild_id: int, role_id: int):
    ensure_guild_exists(guild_id)
    with get_connection() as conn:
        conn.execute("""
            UPDATE welcomer_settings
            SET autorole_id = ?
            WHERE guild_id = ?
        """, (role_id, guild_id))
        conn.commit()


def update_welcomer_channel(guild_id: int, channel_id: int):
    ensure_guild_exists(guild_id)
    with get_connection() as conn:
        conn.execute("""
            UPDATE welcomer_settings
            SET welcomer_channel_id = ?
            WHERE guild_id = ?
        """, (channel_id, guild_id))
        conn.commit()


def update_embed(guild_id: int, embed_dict: dict):
    ensure_guild_exists(guild_id)
    embed_json = json.dumps(embed_dict)
    with get_connection() as conn:
        conn.execute("""
            UPDATE welcomer_settings
            SET embed_json = ?
            WHERE guild_id = ?
        """, (embed_json, guild_id))
        conn.commit()


def set_autorole_status(guild_id: int, status: str):
    ensure_guild_exists(guild_id)
    with get_connection() as conn:
        conn.execute("""
            UPDATE welcomer_settings
            SET autorole_status = ?
            WHERE guild_id = ?
        """, (status, guild_id))
        conn.commit()


def set_welcomer_status(guild_id: int, status: str):
    ensure_guild_exists(guild_id)
    with get_connection() as conn:
        conn.execute("""
            UPDATE welcomer_settings
            SET welcomer_status = ?
            WHERE guild_id = ?
        """, (status, guild_id))
        conn.commit()