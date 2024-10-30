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

# Definindo o dicionário de cargos
CARGOS = {
    1: 1300853285858578543,  # Cargo para o 1º lugar
    2: 1300850877585690655,  # Cargo para o 2º lugar
    3: 1300854639658270761,  # Cargo para o 3º lugar
}

class RankManager:
    @staticmethod
    async def update_rankings(bot):
        guild = bot.get_guild(1186390028990025820)  # Substitua pelo ID do seu servidor
        if not guild:
            print("Guild não encontrado.")
            return

        top_players = await DatabaseManager.get_top_players(3)  # Obtém o top 3 jogadores

        # Primeiro: Remover cargos antigos de todos os membros com esses cargos
        for member in guild.members:
            for cargo_id in CARGOS.values():
                role = guild.get_role(cargo_id)
                if role in member.roles:
                    await member.remove_roles(role)
                    print(f"Cargo {role.name} removido de {member.display_name}.")

        # Segundo: Adicionar os cargos corretos para o novo top 3
        for i, (user_id, damage) in enumerate(top_players):
            member = guild.get_member(user_id)
            if member:
                cargo_id = CARGOS[i + 1]  # Cargo correspondente à posição no top 3
                top_role = guild.get_role(cargo_id)

                if top_role not in member.roles:
                    await member.add_roles(top_role)
                    print(f"Cargo {top_role.name} adicionado para {member.display_name}.")
            else:
                print(f"Usuário com ID {user_id} não encontrado no servidor.")

# Definindo a tarefa de atualização do ranking que roda a cada 10 minutos
@tasks.loop(minutes=10)
async def update_ranking_task():
    await RankManager.update_rankings(bot)

@bot.event
async def on_ready():
    print(f'{bot.user.name} está online!')
    await DatabaseManager.init_db()
    await bot.add_cog(BossBattle(bot))
    update_ranking_task.start()  # Inicia a tarefa de atualização do ranking a cada 10 minutos

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
