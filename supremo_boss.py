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
                "appear": "https://i.postimg.cc/6QptQDLg/DALL-E-2024-10-30-20-19-57-A-powerful-apocalyptic-boss-character-with-intricate-tattoos-inspired-b.webp",
                "attack": "https://i.postimg.cc/Kc6G5px3/DALL-E-2024-10-29-09-21-24-A-powerful-zombie-boss-named-Emberium-inflicting-damage-on-a-player-i.webp",
                "defeated": "https://i.postimg.cc/ZRQg4QV8/DALL-E-2024-10-29-09-41-47-A-dramatic-scene-depicting-a-powerful-zombie-boss-named-Emberium-lyin.webp",
                "laugh": "https://i.postimg.cc/Sxrmky8c/DALL-E-2024-10-30-20-20-35-A-powerful-apocalyptic-boss-character-with-intricate-tattoos-inspired-b.webp",
                "mock": "https://i.postimg.cc/hGSNrTXd/DALL-E-2024-10-30-20-34-15-A-colossal-apocalyptic-boss-character-with-intricate-tattoos-inspired-b.webp",
                "mutate": "https://i.postimg.cc/DfJfL3kK/DALL-E-2024-10-30-20-26-29-A-colossal-apocalyptic-boss-character-with-intricate-tattoos-inspired-b.webp",
                "fight": "https://i.postimg.cc/vZMGJ11Q/DALL-E-2024-10-30-20-22-02-A-powerful-apocalyptic-boss-character-with-intricate-tattoos-inspired-b.webp",
                "drop": "https://i.postimg.cc/KzjwXbrc/DALL-E-2024-10-30-20-31-14-A-colossal-apocalyptic-boss-character-with-intricate-tattoos-inspired-b.webp",
            },
            "fala": [
                "Riam enquanto podem, logo vocês não existirão mais!",
                "Patéticos! Vocês acham que podem me vencer?",
                "Nada além de poeira e cinzas. Onde estão seus famosos títulos agora?",
                "Meus olhos veem a sua fraqueza! A Nova Era é minha!",
                "Ah, os guerreiros caídos! São tão... divertidos!",
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
        await ctx.send(embed=embed)

    @commands.command()
    async def atacar_admin(self, ctx):
        if not self.current_boss:
            await ctx.send("⚠️ Nenhum boss supremo ativo no momento.")
            return

        boss = self.SUPREMO_BOSS[self.current_boss]
        player_id = ctx.author.id

        # Dano ao boss
        dano = random.randint(1, 400)  # Dano que o jogador pode causar ao boss supremo
        boss["vida"] -= dano

        # Mensagem do boss
        if boss["vida"] > 0:
            await ctx.send(f"{self.current_boss} grita: 'Vocês realmente acham que podem me derrotar?'")
            await ctx.send(f"{self.current_boss} ri: 'Vocês são tão fracos!'")

        if boss["vida"] <= 0:
            await self.dropar_recompensa(ctx.author)  # Chama a função de recompensas
            embed = discord.Embed(
                title=f"{self.current_boss} foi derrotado!",
                description=f"{ctx.author.mention} deu o golpe final! Vocês foram vitoriosos!",
                color=discord.Color.green()
            )
            embed.set_image(url=boss["images"]["defeated"])
            await ctx.send(embed=embed)
            self.current_boss = None  # Reset para o próximo boss
            # Reinicia o spawn dos bosses normais
            await self.bot.get_cog('BossBattle').spawn_boss_task.restart()
        else:
            await DatabaseManager.add_damage(player_id, dano)
            embed = discord.Embed(
                title=f"{ctx.author.mention} atacou {self.current_boss}!",
                description=f"Causou {dano} de dano. Vida restante de {self.current_boss}: {boss['vida']}",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)

    async def dropar_recompensa(self, player):
        # Lógica para dropar recompensas
        arma_selecionada = random.choice(self.ARMAS)
        chance_quebrar = random.random() < 0.3  # 30% de chance de quebrar a arma

        if chance_quebrar:
            embed = discord.Embed(
                title="⚔️ Arma Quebrada!",
                description=f"Você recebeu uma **{arma_selecionada['nome']}**, mas ela está quebrada!",
                color=discord.Color.red()
            )
            embed.set_image(url=arma_selecionada['quebrada'])
        else:
            embed = discord.Embed(
                title="🏆 Arma Recebida!",
                description=f"Você recebeu uma **{arma_selecionada['nome']}**!",
                color=discord.Color.green()
            )
            embed.set_image(url=arma_selecionada['imagem'])

        await player.send(embed=embed)
