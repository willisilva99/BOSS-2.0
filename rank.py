from database import DatabaseManager

CARGOS = {
    1: 1300853285858578543,  # Cargo para o 1º lugar
    2: 1300850877585690655,  # Cargo para o 2º lugar
    3: 1300854639658270761,  # Cargo para o 3º lugar
}

class RankManager:
    @staticmethod
    async def update_rankings(bot):
        guild = bot.get_guild(1186390028990025820)  # Guild ID do seu servidor
        top_players = await DatabaseManager.get_top_players()

        for i, (user_id, damage) in enumerate(top_players):
            member = guild.get_member(user_id)
            cargo_id = CARGOS[i + 1]

            # Remove cargos de jogadores fora do top 3
            for cargo in CARGOS.values():
                role = guild.get_role(cargo)
                if role in member.roles and cargo != cargo_id:
                    await member.remove_roles(role)

            # Adiciona cargo ao top player da posição correta
            top_role = guild.get_role(cargo_id)
            if top_role not in member.roles:
                await member.add_roles(top_role)
