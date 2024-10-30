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
                # Remova o conn.commit() daqui

    @staticmethod
    async def add_damage(user_id, damage):
        async with aiopg.connect(DATABASE_URL) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "INSERT INTO players (user_id, damage) VALUES (%s, %s) ON CONFLICT (user_id) DO UPDATE SET damage = players.damage + %s",
                    (user_id, damage, damage)
                )
                # Remova o conn.commit() daqui também
