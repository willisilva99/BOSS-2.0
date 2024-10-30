import os
import discord
from discord.ext import commands, tasks
from database import DatabaseManager
from boss import BossBattle
from rank import RankManager

# Obtém o token do ambiente Railway
TOKEN = os.getenv('TOKEN')

# Configuração dos intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Necessário para acesso aos membros do servidor

bot = commands.Bot(command_prefix="!", intents=intents)

# Tarefa de atualização automática do ranking a cada 10 minutos
@tasks.loop(minutes=10)
async def update_ranking_task():
    await RankManager.update_rankings(bot)

@bot.event
async def on_ready():
    print(f'{bot.user.name} está online!')
    await DatabaseManager.init_db()
    await bot.add_cog(BossBattle(bot))
    update_ranking_task.start()

@bot.command()
async def ranking(ctx):
    # Exibe o top 10 do ranking de dano
    top_players = await DatabaseManager.get_top_players(10)
    leaderboard = "\n".join([f"<@{user_id}> - {damage} dano" for user_id, damage in top_players])
    await ctx.send(f"**Ranking de dano:**\n{leaderboard}")

@bot.command()
async def atualizar_ranking(ctx):
    # Força a atualização do ranking e cargos (somente para ID autorizado)
    if ctx.author.id == 470628393272999948:  # Verifica se é o seu ID (substitua pelo seu ID de usuário)
        await RankManager.update_rankings(bot)
        await ctx.send("Ranking atualizado manualmente!")
    else:
        await ctx.send("Você não tem permissão para executar este comando.")

# Inicia o bot com o token do Railway
bot.run(TOKEN)
