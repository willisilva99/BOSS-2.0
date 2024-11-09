import random
import asyncio
from discord.ext import commands, tasks
from database import DatabaseManager
import discord

class BossBattle(commands.Cog):
    BOSSES = {
        "Emberium": {
            "vida": 15000,
            "vida_maxima": 15000,
            "chance_matar_jogador": 0.3,
            "chance_fugir": 0.05,
            "chance_curar": 0.1,
            "chance_furia": 0.2,
            "dano_contra_jogador": 200,
            "cooldown": 3600,
            "images": {
                "appear": "https://i.postimg.cc/3RSGN1ZK/DALL-E-2024-10-29-09-18-46-A-powerful-zombie-boss-named-Emberium-for-a-game-featuring-an-exagge.webp",
                "attack": "https://i.postimg.cc/zfkKZ8bH/DALL-E-2024-10-29-09-21-49-A-powerful-zombie-boss-named-Emberium-inflicting-damage-on-a-player-i.webp",
                "running": "https://i.postimg.cc/k5CKpB4d/DALL-E-2024-10-29-09-40-12-A-dramatic-scene-depicting-a-powerful-zombie-boss-named-Emberium-in-t.webp",
                "defeated": "https://i.postimg.cc/Kvdnt9hj/DALL-E-2024-10-29-09-41-47-A-dramatic-scene-depicting-a-powerful-zombie-boss-named-Emberium-lyin.webp"
            },
            "fala": [
                "🔥 Quem ousa enfrentar Emberium, o soberano das chamas da devastação?",
                "💀 Vocês são apenas cinzas neste mundo em ruínas!",
                "☠️ Eu sou o fim de todos vocês!",
                "😈 Vocês gritam em vão! Eu sou inevitável.",
                "🔥 Queimem, fracos! Vocês são nada!"
            ],
            "insultos": [
                "⚔️ %s, você luta como uma criança!",
                "😨 Eu sinto o medo em você, %s.",
                "💢 Patético, %s! Achei que seria mais difícil."
            ],
            "criticos": [
                "🔥 Emberium enfurecido ataca com fúria!",
                "⚠️ Emberium está furioso e se fortalece!",
                "💀 A chama da destruição consome Emberium!"
            ]
        },
        "Boss das Sombras": {
            "vida": 13000,
            "vida_maxima": 13000,
            "chance_matar_jogador": 0.35,
            "chance_fugir": 0.1,
            "chance_curar": 0.15,
            "chance_furia": 0.25,
            "dano_contra_jogador": 250,
            "cooldown": 3600,
            "images": {
                "appear": "https://i.postimg.cc/zvQTt7Ld/DALL-E-2024-10-29-09-43-23-A-powerful-zombie-boss-known-as-Shadow-Boss-in-a-fantasy-game-setting.webp",
                "attack": "https://i.postimg.cc/m2cYcvqK/DALL-E-2024-10-29-09-44-57-A-dramatic-fantasy-scene-depicting-the-powerful-zombie-boss-named-Shad.webp",
                "running": "https://i.postimg.cc/NGC8jsN1/DALL-E-2024-10-29-09-46-35-A-dramatic-fantasy-scene-depicting-the-powerful-zombie-boss-named-Shad.webp",
                "defeated": "https://i.postimg.cc/x8mLZHKn/DALL-E-2024-10-29-09-47-45-A-dramatic-fantasy-scene-depicting-the-powerful-zombie-boss-named-Shad.webp"
            },
            "fala": [
                "🌑 Das sombras, eu surjo... preparados para a verdadeira escuridão?",
                "👻 Vocês são apenas ecos perdidos neste mundo esquecido.",
                "🖤 Eu sou o pesadelo encarnado!",
                "☠️ A escuridão consome a todos, inclusive vocês!",
                "⚫ Vocês nunca escaparão das sombras!"
            ],
            "insultos": [
                "🌪️ %s, vai desaparecer no vazio como todos os outros!",
                "💀 Eu estou em todos os lugares, %s. Sinta o terror crescer!",
                "🕸️ %s, você parece tão fraco... que decepção."
            ],
            "criticos": [
                "⚫ A sombra se intensifica e o Boss das Sombras absorve força!",
                "🖤 As trevas se movem, cobrindo tudo!",
                "🌑 Um frio aterrorizante consome o campo de batalha!"
            ]
        },
        "Mega Boss": {
            "vida": 16000,
            "vida_maxima": 16000,
            "chance_matar_jogador": 0.4,
            "chance_fugir": 0.05,
            "chance_curar": 0.2,
            "chance_furia": 0.3,
            "dano_contra_jogador": 280,
            "cooldown": 3600,
            "images": {
                "appear": "https://i.postimg.cc/W3CMSSq5/DALL-E-2024-10-29-09-49-34-A-powerful-fantasy-character-design-of-a-zombie-boss-named-Mega-Boss.webp",
                "attack": "https://i.postimg.cc/QMNkMFrJ/DALL-E-2024-10-29-10-11-26-A-dramatic-fantasy-scene-depicting-the-powerful-zombie-boss-named-Mega.webp",
                "running": "https://i.postimg.cc/2S77m4g5/DALL-E-2024-10-29-10-13-34-A-dramatic-fantasy-scene-depicting-the-powerful-zombie-boss-named-Mega.webp",
                "defeated": "https://i.postimg.cc/KvL5pXNB/DALL-E-2024-10-29-10-14-38-A-dramatic-fantasy-scene-depicting-the-powerful-zombie-boss-named-Mega.webp"
            },
            "fala": [
                "💥 Eu sou o colosso, o peso de um mundo destruído!",
                "⚠️ Preparem-se para o colapso absoluto!",
                "👹 Perdidos e fracos... vocês não são nada diante de mim!",
                "🔥 Vocês acham que podem me vencer? Seus esforços são patéticos!",
                "⚔️ Preparem-se para serem esmagados, mortais."
            ],
            "insultos": [
                "💢 Vou esmagar você como uma barata, %s!",
                "😈 %s, você é apenas uma sombra do que poderia ser!",
                "💀 Seu fim está próximo, %s. Apenas aceite a derrota!"
            ],
            "criticos": [
                "💥 Mega Boss emite um grito de fúria, vibrando o solo!",
                "⚠️ A força do Mega Boss aumenta!",
                "🔥 O Mega Boss libera um ataque destruidor!"
            ]
        }
    }

    ARMAS = [
        {
            "nome": "Sniper Boss Rara",
            "imagem": "https://i.postimg.cc/50hC80DG/DALL-E-2024-10-29-10-21-27-A-rugged-survivor-in-an-apocalyptic-setting-holding-the-Emberium-Snip.webp",
            "quebrada": "https://i.postimg.cc/mDz9cMpC/DALL-E-2024-10-29-10-23-18-A-rugged-survivor-in-an-apocalyptic-setting-holding-a-completely-shatt.webp",
            "chance_drop": 0.4,
            "chance_quebrar": 0.3
        },
        {
            "nome": "Sniper Emberium",
            "imagem": "https://i.postimg.cc/nh2BNnQj/DALL-E-2024-10-29-10-24-23-A-rugged-survivor-in-an-apocalyptic-setting-confidently-wielding-the.webp",
            "quebrada": "https://i.postimg.cc/1zzwQbpW/DALL-E-2024-10-29-10-31-58-A-rugged-survivor-in-an-apocalyptic-setting-holding-a-Sniper-Boss-Rar.webp",
            "chance_drop": 0.5,
            "chance_quebrar": 0.2
        },
        {
            "nome": "Sniper Damanty",
            "imagem": "https://i.postimg.cc/qv42mNgH/DALL-E-2024-10-29-10-32-54-A-rugged-survivor-in-an-apocalyptic-setting-confidently-holding-the-S.webp",
            "quebrada": "https://i.postimg.cc/MGrRKt5z/DALL-E-2024-10-29-10-33-40-A-rugged-survivor-in-an-apocalyptic-setting-holding-a-Sniper-Damanty.webp",
            "chance_drop": 0.3,
            "chance_quebrar": 0.25
        },
    ]

    def __init__(self, bot):
        self.bot = bot
        self.current_boss = None
        self.cooldowns = {}
        self.spawn_boss_task.start()
        self.auto_message_task.start()
        self.fugiu = None
        self.derrotado = None

    @tasks.loop(minutes=1)
    async def spawn_boss_task(self):
        if self.current_boss or (self.fugiu and asyncio.get_event_loop().time() < self.fugiu) or (self.derrotado and asyncio.get_event_loop().time() < self.derrotado):
            return

        self.current_boss = random.choice(list(self.BOSSES.keys()))
        boss = self.BOSSES[self.current_boss]
        boss["vida"] = boss["vida_maxima"]
        embed = discord.Embed(
            title=f"⚠️ {self.current_boss} apareceu!",
            description=random.choice(boss["fala"]).replace("%s", "todos os jogadores!"),
            color=discord.Color.red()
        )
        embed.set_image(url=boss["images"]["appear"])
        channel = self.bot.get_channel(1299092242673303552)
        await channel.send(embed=embed)
        await self.atacar_top_jogador()

    @tasks.loop(seconds=30)
    async def auto_message_task(self):
        if not self.current_boss:
            return
        
        boss = self.BOSSES[self.current_boss]
        message = random.choice(boss["fala"])
        embed = discord.Embed(
            title=f"{self.current_boss} fala:",
            description=message,
            color=discord.Color.dark_red()
        )
        await self.bot.get_channel(1299092242673303552).send(embed=embed)

    async def atacar_top_jogador(self):
        top_players = await DatabaseManager.get_top_players(10)
        if top_players:
            user_id, _ = top_players[0]
            boss = self.BOSSES[self.current_boss]
            dano = random.randint(1, 1000)
            await DatabaseManager.subtract_damage(user_id, dano)

            insulto = random.choice(boss["insultos"]).replace("%s", f"<@{user_id}>")
            embed = discord.Embed(
                title=f"{self.current_boss} ataca o Top 1!",
                description=f"{insulto}\n\n<@{user_id}> sofreu **{dano} de dano**!",
                color=discord.Color.red()
            )
            embed.set_image(url=boss["images"]["attack"])
            await self.bot.get_channel(1299092242673303552).send(embed=embed)

    async def curar_boss(self):
        boss = self.BOSSES[self.current_boss]
        if random.random() < boss["chance_curar"]:
            cura = random.randint(500, 1500)
            boss["vida"] = min(boss["vida_maxima"], boss["vida"] + cura)
            embed = discord.Embed(
                title="💉 Cura do Boss!",
                description=f"⚠️ {self.current_boss} se cura e recupera **{cura} de vida**!",
                color=discord.Color.green()
            )
            await self.bot.get_channel(1299092242673303552).send(embed=embed)

    async def ativar_furia(self):
        boss = self.BOSSES[self.current_boss]
        if boss["vida"] <= boss["vida_maxima"] * 0.25 and random.random() < boss["chance_furia"]:
            boss["chance_curar"] += 0.1
            embed = discord.Embed(
                title="💢 Modo Fúria Ativado!",
                description=f"⚠️ {self.current_boss} entrou em MODO FÚRIA! Preparem-se!",
                color=discord.Color.dark_red()
            )
            await self.bot.get_channel(1299092242673303552).send(embed=embed)

    async def dropar_recompensa(self, player):
        arma_selecionada = random.choice(self.ARMAS)
        embed = discord.Embed(
            title="🎉 Recompensa do Boss Derrotado",
            color=discord.Color.green()
        )

        if random.random() <= arma_selecionada["chance_drop"]:
            if random.random() <= arma_selecionada["chance_quebrar"]:
                embed.add_field(name="⚔️ Arma Quebrada!", value=f"Você recebeu uma **{arma_selecionada['nome']}**, mas ela está quebrada!")
                embed.set_image(url=arma_selecionada['quebrada'])
            else:
                embed.add_field(name="🏆 Arma Recebida!", value=f"Você recebeu uma **{arma_selecionada['nome']}** em perfeito estado!")
                embed.set_image(url=arma_selecionada['imagem'])
            await player.send(embed=embed)
        else:
            embed.add_field(name="😢 Sem Recompensa", value="Infelizmente, você não recebeu uma arma desta vez.")
            await player.send(embed=embed)

    @commands.command()
    async def atacar(self, ctx):
        if self.current_boss:
            await self._atacar_boss_normal(ctx)
        else:
            await ctx.send("⚠️ Nenhum boss ativo no momento. Aguarde o próximo surgimento.")

    async def _atacar_boss_normal(self, ctx):
        boss = self.BOSSES[self.current_boss]
        player_id = ctx.author.id
        current_time = asyncio.get_event_loop().time()

        if player_id in self.cooldowns and (self.cooldowns[player_id] + boss["cooldown"]) > current_time:
            time_left = int((self.cooldowns[player_id] + boss["cooldown"] - current_time) / 60)
            await ctx.send(f"⏳ {ctx.author.mention} você está em cooldown! Espere mais {time_left} minutos para atacar novamente.")
            return

        self.cooldowns[player_id] = current_time

        if random.random() < boss["chance_fugir"]:
            embed = discord.Embed(
                title=f"{self.current_boss} fugiu!",
                description=f"O boss escapou das garras de {ctx.author.mention} e se escondeu nas sombras!",
                color=discord.Color.purple()
            )
            embed.set_image(url=boss["images"]["running"])
            await ctx.send(embed=embed)
            self.current_boss = None
            self.fugiu = asyncio.get_event_loop().time() + 600
            return

        dano = random.randint(10, 2000)
        boss["vida"] -= dano
        await self.ativar_furia()

        if boss["vida"] <= 0:
            embed = discord.Embed(
                title=f"{self.current_boss} foi derrotado!",
                description=f"{ctx.author.mention} deu o golpe final! Vocês foram vitoriosos!",
                color=discord.Color.green()
            )
            embed.set_image(url=boss["images"]["defeated"])
            await ctx.send(embed=embed)
            await self.dropar_recompensa(ctx.author)
            self.current_boss = None
            self.derrotado = asyncio.get_event_loop().time() + 600
        else:
            await DatabaseManager.add_damage(player_id, dano)
            insulto = random.choice(boss["insultos"]).replace("%s", ctx.author.mention)
            embed = discord.Embed(
                title=f"{ctx.author.mention} atacou {self.current_boss}!",
                description=f"Causou {dano} de dano. Vida restante de {self.current_boss}: {boss['vida']}\n\n{insulto}",
                color=discord.Color.orange()
            )
            embed.set_image(url=boss["images"]["appear"] if boss["vida"] > boss["vida_maxima"] / 2 else boss["images"]["running"])
            await ctx.send(embed=embed)

        await self.curar_boss()
