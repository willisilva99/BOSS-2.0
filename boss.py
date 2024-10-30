import random
from discord.ext import commands
from database import DatabaseManager

class BossBattle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def atacar(self, ctx):
        damage = random.randint(10, 100)  # Dano aleatório
        user_id = ctx.author.id
        await DatabaseManager.add_damage(user_id, damage)
        await ctx.send(f'{ctx.author.mention} atacou o boss e causou {damage} de dano!')
