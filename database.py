import aiopg
import os

DATABASE_URL = os.getenv("DATABASE_URL")  # Certifique-se de definir a URL do Postgres no Railway

class DatabaseManager:
    @staticmethod
    async def init_db():
        async with aiopg.connect(DATABASE_URL) as conn:
            async with conn.cursor() as cur:
                await cur.execute('''
                    CREATE TABLE IF NOT EXISTS players (
                        id SERIAL PRIMARY KEY, 
                        user_id BIGINT UNIQUE, 
                        damage INTEGER DEFAULT 0
                    )
                ''')
                await conn.commit()

    @staticmethod
    async def add_damage(user_id, damage):
        async with aiopg.connect(DATABASE_URL) as conn:
            async with conn.cursor() as cur:
                await cur.execute("INSERT INTO players (user_id, damage) VALUES (%s, %s) ON CONFLICT (user_id) DO UPDATE SET damage = players.damage + %s",
                                  (user_id, damage, damage))
                await conn.commit()

    @staticmethod
    async def get_top_players(limit=3):
        async with aiopg.connect(DATABASE_URL) as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT user_id, damage FROM players ORDER BY damage DESC LIMIT %s", (limit,))
                return await cur.fetchall()
