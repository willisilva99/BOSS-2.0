import random
import asyncio
from discord.ext import commands, tasks
from database import DatabaseManager
import discord

class BossBattle(commands.Cog):
    BOSSES = {
        "Emberium": {
            "vida": 15000,
            "chance_matar_jogador": 0.3,
            "chance_fugir": 0.05,
            "dano_contra_jogador": 200,
            "cooldown": 3600,
            "images": {
                "appear": "https://i.postimg.cc/3RSGN1ZK/DALL-E-2024-10-29-09-18-46-A-powerful-zombie-boss-named-Emberium-for-a-game-featuring-an-exagge.webp",
                "attack": "https://i.postimg.cc/zfkKZ8bH/DALL-E-2024-10-29-09-21-49-A-powerful-zombie-boss-named-Emberium-inflicting-damage-on-a-player-i.webp",
                "running": "https://i.postimg.cc/k5CKpB4d/DALL-E-2024-10-29-09-40-12-A-dramatic-scene-depicting-a-powerful-zombie-boss-named-Emberium-in-t.webp",
                "defeated": "https://i.postimg.cc/Kvdnt9hj/DALL-E-2024-10-29-09-41-47-A-dramatic-scene-depicting-a-powerful-zombie-boss-named-Emberium-lyin.webp"
            },
            "fala": [
                "Quem ousa enfrentar Emberium, o soberano das chamas da devastação?",
                "Vocês são apenas cinzas neste mundo em ruínas!",
                "Venham, tolos! Eu já vi o fim dos tempos, e não é nada comparado ao que vos espera!",
                "Olhem para vocês, guerreiros! Nossos 'campeões' não passam de cinzas!",
                "Quantos títulos vocês têm, mas a verdade é que nenhum deles os salvará de mim!"
            ]
        },
        "Boss das Sombras": {
            "vida": 13000,
            "chance_matar_jogador": 0.35,
            "chance_fugir": 0.1,
            "dano_contra_jogador": 250,
            "cooldown": 3600,
            "images": {
                "appear": "https://i.postimg.cc/zvQTt7Ld/DALL-E-2024-10-29-09-43-23-A-powerful-zombie-boss-known-as-Shadow-Boss-in-a-fantasy-game-setting.webp",
                "attack": "https://i.postimg.cc/m2cYcvqK/DALL-E-2024-10-29-09-44-57-A-dramatic-fantasy-scene-depicting-the-powerful-zombie-boss-named-Shad.webp",
                "running": "https://i.postimg.cc/NGC8jsN1/DALL-E-2024-10-29-09-46-35-A-dramatic-fantasy-scene-depicting-the-powerful-zombie-boss-named-Shad.webp",
                "defeated": "https://i.postimg.cc/x8mLZHKn/DALL-E-2024-10-29-09-47-45-A-dramatic-fantasy-scene-depicting-the-powerful-zombie-boss-named-Shad.webp"
            },
            "fala": [
                "Das sombras, eu surjo... preparados para a verdadeira escuridão?",
                "Vocês não passam de sombras em meu reino!",
                "Apenas ecos... vocês são os últimos suspiros deste mundo perdido!",
                "Onde estão seus famosos títulos? Eles não têm poder contra mim!",
                "Seus esforços são tão frágeis quanto o próprio mundo que vocês tentam salvar!"
            ]
        },
        "Mega Boss": {
            "vida": 16000,
            "chance_matar_jogador": 0.4,
            "chance_fugir": 0.05,
            "dano_contra_jogador": 280,
            "cooldown": 3600,
            "images": {
                "appear": "https://i.postimg.cc/W3CMSSq5/DALL-E-2024-10-29-09-49-34-A-powerful-fantasy-character-design-of-a-zombie-boss-named-Mega-Boss.webp",
                "attack": "https://i.postimg.cc/QMNkMFrJ/DALL-E-2024-10-29-10-11-26-A-dramatic-fantasy-scene-depicting-the-powerful-zombie-boss-named-Mega.webp",
                "running": "https://i.postimg.cc/2S77m4g5/DALL-E-2024-10-29-10-13-34-A-dramatic-fantasy-scene-depicting-the-powerful-zombie-boss-named-Mega.webp",
                "defeated": "https://i.postimg.cc/KvL5pXNB/DALL-E-2024-10-29-10-14-38-A-dramatic-fantasy-scene-depicting-the-powerful-zombie-boss-named-Mega.webp"
            },
            "fala": [
                "Eu sou o colosso, o peso de um mundo destruído!",
                "O último som que ouvirão é o meu riso!",
                "Perdidos e fracos... vocês não são nada diante de mim!",
                "Títulos e conquistas não têm valor aqui. Preparem-se para serem obliterados!",
                "Vocês acham que podem me vencer? Seus esforços são patéticos!"
            ]
        }
    }

    def __init__(self, bot):
        self.bot = bot
        self.current_boss = None
        self.cooldowns = {}
        self.spawn_boss_task.start()
        self.fugiu = None
        self.derrotado = None

    @tasks.loop(minutes=1)
    async def spawn_boss_task(self):
        if self.current_boss:
            return  # Se já existir um boss, espera até ser derrotado ou fugir

        if self.fugiu is not None and asyncio.get_event_loop().time() < self.fugiu:
            return  # Espera até o tempo de reaparecimento após fuga

        if self.derrotado is not None and asyncio.get_event_loop().time() < self.derrotado:
            return  # Espera até o tempo de reaparecimento após derrota

        self.current_boss = random.choice(list(self.BOSSES.keys()))
        boss = self.BOSSES[self.current_boss]
        embed = discord.Embed(
            title=f"⚠️ {self.current_boss} apareceu!",
            description=random.choice(boss["fala"]) + "\n" + self.zombar_jogadores(),
            color=discord.Color.red()
        )
        embed.set_image(url=boss["images"]["appear"])
        channel = self.bot.get_channel(1299092242673303552)  # ID do canal onde o boss aparece
        await channel.send(embed=embed)

    def zombar_jogadores(self):
        return "Olhem para vocês, criaturas frágeis! Não merecem nem o título de 'guerreiro'!"

    @commands.command()
    async def atacar(self, ctx):
        boss_battle_cog = self.bot.get_cog('BossBattle')
        supremo_boss_cog = self.bot.get_cog('SupremoBoss')

        if boss_battle_cog and boss_battle_cog.current_boss:
            await self._atacar_boss_normal(ctx, boss_battle_cog)
        elif supremo_boss_cog and supremo_boss_cog.current_boss:
            await supremo_boss_cog.atacar_admin(ctx)
        else:
            await ctx.send("⚠️ Nenhum boss ativo no momento. Aguarde o próximo surgimento.")

    async def _atacar_boss_normal(self, ctx, boss_battle_cog):
        boss = boss_battle_cog.BOSSES[boss_battle_cog.current_boss]
        player_id = ctx.author.id
        current_time = asyncio.get_event_loop().time()

        # Verifica o cooldown do jogador
        if player_id in boss_battle_cog.cooldowns and (boss_battle_cog.cooldowns[player_id] + boss["cooldown"]) > current_time:
            time_left = int((boss_battle_cog.cooldowns[player_id] + boss["cooldown"] - current_time) / 60)
            await ctx.send(f"⏳ {ctx.author.mention} você está em cooldown! Espere mais {time_left} minutos para atacar novamente.")
            return

        # Atualiza o cooldown do jogador
        boss_battle_cog.cooldowns[player_id] = current_time

        # Chance do boss fugir
        if random.random() < boss["chance_fugir"]:
            embed = discord.Embed(
                title=f"{boss_battle_cog.current_boss} fugiu!",
                description=f"O boss escapou das garras de {ctx.author.mention} e se escondeu nas sombras!",
                color=discord.Color.purple()
            )
            embed.set_image(url=boss["images"]["running"])
            await ctx.send(embed=embed)
            boss_battle_cog.current_boss = None
            boss_battle_cog.fugiu = asyncio.get_event_loop().time() + 600  # 10 minutos de espera
            return

        # Chance de o boss matar o jogador
        if random.random() < boss["chance_matar_jogador"]:
            await DatabaseManager.subtract_damage(player_id, boss["dano_contra_jogador"])
            embed = discord.Embed(
                title=f"{boss_battle_cog.current_boss} contra-atacou!",
                description=f"{ctx.author.mention} foi derrotado e perdeu {boss['dano_contra_jogador']} pontos de dano acumulado!",
                color=discord.Color.red()
            )
            embed.set_image(url=boss["images"]["attack"])
            await ctx.send(embed=embed)
            return

        # Dano ao boss
        dano = random.randint(10, 2000)
        boss["vida"] -= dano

        # Verifica se o boss foi derrotado
        if boss["vida"] <= 0:
            embed = discord.Embed(
                title=f"{boss_battle_cog.current_boss} foi derrotado!",
                description=f"{ctx.author.mention} deu o golpe final! Preparem-se para o Supremo Boss!",
                color=discord.Color.green()
            )
            embed.set_image(url=boss["images"]["defeated"])
            await ctx.send(embed=embed)
            
            # Reseta o boss normal e invoca o Supremo Boss
            boss_battle_cog.current_boss = None
            await self.bot.get_cog('SupremoBoss').aparecer(ctx)  # Invoca o Supremo Boss
        else:
            # Atualiza o dano do jogador
            await DatabaseManager.add_damage(player_id, dano)
            embed = discord.Embed(
                title=f"{ctx.author.mention} atacou {boss_battle_cog.current_boss}!",
                description=f"Causou {dano} de dano. Vida restante de {boss_battle_cog.current_boss}: {boss['vida']}",
                color=discord.Color.orange()
            )
            embed.set_image(url=boss["images"]["running"] if boss["vida"] < boss["vida"] / 2 else boss["images"]["appear"])
            await ctx.send(embed=embed)
