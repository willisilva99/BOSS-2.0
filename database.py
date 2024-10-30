import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")

class DatabaseManager:
    @staticmethod
    async def init_db():
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY, 
                user_id BIGINT UNIQUE, 
                damage INTEGER DEFAULT 0
            )
        ''')
        await conn.close()

    @staticmethod
    async def add_damage(user_id, damage):
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute(
            "INSERT INTO players (user_id, damage) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET damage = players.damage + $3",
            user_id, damage, damage
        )
        await conn.close()

    @staticmethod
    async def get_top_players(limit=3):
        conn = await asyncpg.connect(DATABASE_URL)
        rows = await conn.fetch("SELECT user_id, damage FROM players ORDER BY damage DESC LIMIT $1", limit)
        await conn.close()
        return rows
