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
                "appear": "https://i.postimg.cc/3RSGN1ZK/DALL-E-2024-10-29-09-18-46-A-powerful-zombie-boss-named-Emberium-for-a-game-featuring-an-exagge.webp",
                "attack": "https://i.postimg.cc/zfkKZ8bH/DALL-E-2024-10-29-09-21-49-A-powerful-zombie-boss-named-Emberium-inflicting-damage-on-a-player-i.webp",
                "defeated": "https://i.postimg.cc/Kvdnt9hj/DALL-E-2024-10-29-09-41-47-A-dramatic-scene-depicting-a-powerful-zombie-boss-named-Emberium-lyin.webp",
            },
            "fala": [
                "Olhem só para vocês! A Nova Era precisa de verdadeiros guerreiros!",
                "Vocês acham que podem me vencer? Patéticos!",
                "Vocês não são nada além de marionetes neste apocalipse!",
            ]
        }
    }

    ARMAS = [
        {
            "nome": "Sniper Boss Rara",
            "imagem": "https://i.postimg.cc/50hC80DG/DALL-E-2024-10-29-10-21-27-A-rugged-survivor-in-an-apocalyptic-setting-holding-the-Emberium-Snip.webp",
            "quebrada": "https://i.postimg.cc/mDz9cMpC/DALL-E-2024-10-29-10-23-18-A-rugged-survivor-in-an-apocalyptic-setting-holding-a-completely-shatt.webp",
        },
        {
            "nome": "Sniper Emberium",
            "imagem": "https://i.postimg.cc/nh2BNnQj/DALL-E-2024-10-29-10-24-23-A-rugged-survivor-in-an-apocalyptic-setting-confidently-wielding-the.webp",
            "quebrada": "https://i.postimg.cc/1zzwQbpW/DALL-E-2024-10-29-10-31-58-A-rugged-survivor-in-an-apocalyptic-setting-holding-a-Sniper-Boss-Rar.webp",
        },
        {
            "nome": "Sniper Damanty",
            "imagem": "https://i.postimg.cc/qv42mNgH/DALL-E-2024-10-29-10-32-54-A-rugged-survivor-in-an-apocalyptic-setting-confidently-holding-the-S.webp",
            "quebrada": "https://i.postimg.cc/MGrRKt5z/DALL-E-2024-10-29-10-33-40-A-rugged-survivor-in-an-apocalyptic-setting-holding-a-Sniper-Damanty.webp",
        },
    ]

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
            embed.set_image(url=boss["images"]["appear"])
            await ctx.send(embed=embed)

    async def dropar_recompensa(self, player):
        # Lógica para dropar recompensas
        arma_selecionada = random.choice(self.ARMAS)
        chance_quebrar = random.random() < 0.3  # 30% de chance de quebrar a arma

        if chance_quebrar:
            await player.send(f"🎁 Você recebeu: **{arma_selecionada['nome']}** (QUEBRADA)!\nImagem: {arma_selecionada['quebrada']}")
            embed = discord.Embed(
                title="⚔️ Arma Quebrada!",
                description=f"Você recebeu uma **{arma_selecionada['nome']}**, mas ela está quebrada!",
                color=discord.Color.red()
            )
            embed.set_image(url=arma_selecionada['quebrada'])
        else:
            await player.send(f"🎁 Você recebeu: **{arma_selecionada['nome']}**!\nImagem: {arma_selecionada['imagem']}")
            embed = discord.Embed(
                title="🏆 Arma Recebida!",
                description=f"Você recebeu uma **{arma_selecionada['nome']}**!",
                color=discord.Color.green()
            )
            embed.set_image(url=arma_selecionada['imagem'])

        await player.send(embed=embed)
