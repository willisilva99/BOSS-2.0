import os
import discord
import random
from discord.ext import commands, tasks
from database import DatabaseManager
from boss import BossBattle
from supremo_boss import SupremoBoss  # Importando a classe do boss supremo

# Obtém o token do ambiente Railway
TOKEN = os.getenv('TOKEN')

# Configuração dos intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Necessário para acesso aos membros do servidor

bot = commands.Bot(command_prefix="!", intents=intents)

# Variável para controlar o tempo até a próxima atualização
tempo_para_proxima_atualizacao = 10  # Em minutos

# Definindo o dicionário de cargos
CARGOS = {
    1: 1300853285858578543,  # Cargo para o 1º lugar
    2: 1300850877585690655,  # Cargo para o 2º lugar
    3: 1300854639658270761,  # Cargo para o 3º lugar
}

class RankManager:
    @staticmethod
    async def update_rankings(bot):
        global tempo_para_proxima_atualizacao
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

        # Redefine o tempo para a próxima atualização
        tempo_para_proxima_atualizacao = 10

# Definindo a tarefa de atualização do ranking para rodar a cada 10 minutos
@tasks.loop(minutes=1)
async def update_ranking_task():
    global tempo_para_proxima_atualizacao
    if tempo_para_proxima_atualizacao <= 1:
        await RankManager.update_rankings(bot)
    else:
        tempo_para_proxima_atualizacao -= 1

@bot.event
async def on_ready():
    print(f'{bot.user.name} está online!')
    await DatabaseManager.init_db()
    await bot.add_cog(BossBattle(bot))
    await bot.add_cog(SupremoBoss(bot))  # Adicionando o boss supremo
    update_ranking_task.start()  # Inicia a tarefa de atualização a cada minuto, mas atualiza o ranking a cada 10 minutos

@bot.command()
async def ranking(ctx):
    # Exibe o top 10 do ranking de dano com embed e menções aos cargos dos três primeiros
    top_players = await DatabaseManager.get_top_players(10)
    leaderboard = ""
    
    # Mensagens de parabéns para os três primeiros colocados
    messages = [
        "é um verdadeiro sobrevivente da Nova Era!",
        "provou ser digno da glória apocalíptica!",
        "se destaca entre os fortes nesta Nova Era!",
        "mostrou ser indomável diante do caos!",
        "é uma lenda viva do apocalipse!"
    ]
    
    # Organizando o top 3 com cargos e mensagens personalizadas
    for i, (user_id, damage) in enumerate(top_players):
        congrat_message = random.choice(messages)
        
        if i == 0:
            leaderboard += f"**🥇 1º Lugar**\n<@{user_id}> - {damage} dano\n**Cargo:** EXECUTOR BOSS\n_{congrat_message}_\n\n"
        elif i == 1:
            leaderboard += f"**🥈 2º Lugar**\n<@{user_id}> - {damage} dano\n**Cargo:** VICIADO EM MORTES\n_{congrat_message}_\n\n"
        elif i == 2:
            leaderboard += f"**🥉 3º Lugar**\n<@{user_id}> - {damage} dano\n**Cargo:** SNIPER BOSS\n_{congrat_message}_\n\n"
        else:
            leaderboard += f"`{i + 1}º` <@{user_id}> - {damage} dano\n"

    embed = discord.Embed(
        title="📜 **A Nova Era do Poder** 📜",
        description="Esses guerreiros se destacam na luta apocalíptica. A Nova Era os coroou com sangue e glória.",
        color=discord.Color.dark_red()
    )
    embed.add_field(name="**Ranking de dano**", value=leaderboard, inline=False)
    embed.set_image(url="https://i.postimg.cc/662WxfTL/DALL-E-2024-10-30-17-58-02-Three-survivors-in-a-post-apocalyptic-world-standing-together-with-a-d.webp")
    embed.set_footer(text="Somente os mais fortes sobreviverão à Nova Era.")
    
    await ctx.send(embed=embed)

@bot.command()
async def atualizar_ranking(ctx):
    # Força a atualização do ranking e cargos (somente para ID autorizado)
    if ctx.author.id == 470628393272999948:  # Verifica se é o seu ID (substitua pelo seu ID de usuário)
        await RankManager.update_rankings(bot)
        embed = discord.Embed(
            title="⚔️ **O Destino Foi Selado** ⚔️",
            description="O ranking foi atualizado. A Nova Era saúda seus novos campeões.",
            color=discord.Color.dark_red()
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send("Você não tem permissão para executar este comando.")

@bot.command()
async def tempo_para_atualizar(ctx):
    # Mostra o tempo restante para a próxima atualização
    embed = discord.Embed(
        title="⏳ **Tempo para a Próxima Atualização** ⏳",
        description=f"Faltam **{tempo_para_proxima_atualizacao} minutos** para a próxima atualização automática do ranking.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

# Inicia o bot com o token do Railway
bot.run(TOKEN)
