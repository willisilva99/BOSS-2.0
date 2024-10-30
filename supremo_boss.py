import random
import asyncio
from discord.ext import commands
from database import DatabaseManager
import discord

class SupremoBoss(commands.Cog):
    SUPREMO_BOSS = {
        "Admin": {
            "vida": 20000,
            "chance_matar_jogador": 0.5,
            "chance_fugir": 0.0,  # Não pode fugir
            "dano_contra_jogador": 2000,
            "images": {
                "appear": "LINK_IMAGEM_ADMIN",  # Coloque o link da imagem
                "attack": "LINK_IMAGEM_ADMIN_ATACANDO",  # Coloque o link da imagem
                "defeated": "LINK_IMAGEM_ADMIN_DEFEAT",  # Coloque o link da imagem
            },
            "fala": [
                "Eu sou o verdadeiro poder por trás deste apocalipse!",
                "Vocês realmente acham que podem me derrotar?",
                "Vamos ver o quanto vocês são realmente fortes!",
            ]
        }
    }

    def __init__(self, bot):
        self.bot = bot
        self.current_boss = None

    async def aparecer(self, ctx):
        self.current_boss = "Admin"
        boss = self.SUPREMO_BOSS[self.current_boss]
        embed = discord.Embed(
            title=f"⚠️ {self.current_boss} apareceu!",
            description=random.choice(boss["fala"]),
            color=discord.Color.red()
        )
        embed.set_image(url=boss["images"]["appear"])
        channel = self.bot.get_channel(1299092242673303552)  # ID do canal onde o boss aparece
        await channel.send(embed=embed)

    @commands.command()
    async def atacar_admin(self, ctx):
        if not self.current_boss:
            await ctx.send("⚠️ Nenhum boss supremo ativo no momento.")
            return

        boss = self.SUPREMO_BOSS[self.current_boss]
        player_id = ctx.author.id
        current_time = asyncio.get_event_loop().time()

        # Verifica o cooldown do jogador
        if player_id in self.cooldowns and (self.cooldowns[player_id] + boss["cooldown"]) > current_time:
            time_left = int((self.cooldowns[player_id] + boss["cooldown"] - current_time) / 60)
            await ctx.send(f"⏳ {ctx.author.mention} você está em cooldown! Espere mais {time_left} minutos para atacar novamente.")
            return

        # Atualiza o cooldown do jogador
        self.cooldowns[player_id] = current_time

        # Dano ao boss
        dano = random.randint(1, 400)  # Dano que o jogador pode causar ao boss supremo
        boss["vida"] -= dano

        # Verifica se o boss supremo foi derrotado
        if boss["vida"] <= 0:
            await self.dropar_recompensa(ctx.author)  # Chama a função de recompensas
            embed = discord.Embed(
                title=f"{boss['name']} foi derrotado!",
                description=f"{ctx.author.mention} deu o golpe final! Vocês foram vitoriosos!",
                color=discord.Color.green()
            )
            embed.set_image(url=boss["images"]["defeated"])
            await ctx.send(embed=embed)
            self.current_boss = None  # Reset para o próximo boss
        else:
            # Atualiza o dano do jogador
            await DatabaseManager.add_damage(player_id, dano)
            embed = discord.Embed(
                title=f"{ctx.author.mention} atacou {boss['name']}!",
                description=f"Causou {dano} de dano. Vida restante de {boss['name']}: {boss['vida']}",
                color=discord.Color.orange()
            )
            embed.set_image(url=boss["images"]["running"])
            await ctx.send(embed=embed)

    async def dropar_recompensa(self, player):
        # Lógica para dropar recompensas
        recompensas = [
            "Item raro",
            "100 moedas",
            "Armadura épica"
        ]
        recompensa = random.choice(recompensas)
        await player.send(f"🎁 Você recebeu: {recompensa} ao derrotar o boss supremo!")
