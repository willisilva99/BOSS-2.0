import aiosqlite

class DatabaseManager:
    @staticmethod
    async def init_db():
        async with aiosqlite.connect("damage_ranking.db") as db:
            await db.execute('''CREATE TABLE IF NOT EXISTS players 
                                (id INTEGER PRIMARY KEY, 
                                 user_id INTEGER UNIQUE, 
                                 damage INTEGER)''')
            await db.commit()

    @staticmethod
    async def add_damage(user_id, damage):
        async with aiosqlite.connect("damage_ranking.db") as db:
            await db.execute("INSERT OR IGNORE INTO players (user_id, damage) VALUES (?, 0)", (user_id,))
            await db.execute("UPDATE players SET damage = damage + ? WHERE user_id = ?", (damage, user_id))
            await db.commit()

    @staticmethod
    async def get_top_players(limit=3):
        async with aiosqlite.connect("damage_ranking.db") as db:
            async with db.execute("SELECT user_id, damage FROM players ORDER BY damage DESC LIMIT ?", (limit,)) as cursor:
                return await cursor.fetchall()
