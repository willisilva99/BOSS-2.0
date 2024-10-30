import os
import discord
from discord.ext import commands, tasks
from database import DatabaseManager
from boss import BossBattle
from rank import RankManager

# Obtém o token do ambiente Railway
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@tasks.loop(minutes=10)
async def update_ranking_task():
    await RankManager.update_rankings(bot)

@bot.event
async def on_ready():
    print(f'{bot.user.name} está online!')
    await DatabaseManager.init_db()
    await bot.add_cog(BossBattle(bot))  # Agora aguardando corretamente
    update_ranking_task.start()

@bot.command()
async def ranking(ctx):
    top_players = await DatabaseManager.get_top_players(10)
    leaderboard = "\n".join([f"<@{user_id}> - {damage} dano" for user_id, damage in top_players])
    await ctx.send(f"**Ranking de dano:**\n{leaderboard}")

bot.run(TOKEN)
