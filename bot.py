import os
import discord
from discord.ext import commands, tasks
from database import DatabaseManager
from boss import BossBattle
from rank import RankManager

# Obtém o token do ambiente Railway
TOKEN = os.getenv('TOKEN')

# Configurando intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Necessário para acesso aos membros do servidor

bot = commands.Bot(command_prefix="!", intents=intents)

@tasks.loop(minutes=10)
async def update_ranking_task():
    await RankManager.update_rankings(bot)

@bot.event
async def on_ready():
    print(f'{bot.user.name} está online!')
    await DatabaseManager.init_db()
    await bot.add_cog(BossBattle(bot))
    await RankManager.update_rankings(bot)  # Força uma atualização do ranking ao iniciar o bot
    update_ranking_task.start()

bot.run(TOKEN)
