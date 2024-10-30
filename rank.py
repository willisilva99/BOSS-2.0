from database import DatabaseManager

CARGOS = {
    1: 1300853285858578543,  # ID do cargo para o 1º lugar
    2: 1300850877585690655,  # ID do cargo para o 2º lugar
    3: 1300854639658270761,  # ID do cargo para o 3º lugar
}

class RankManager:
    @staticmethod
    async def update_rankings(bot):
        guild = bot.get_guild(1186390028990025820)  # Insira o Guild ID do servidor
        if not guild:
            print("Guild não encontrado.")
            return

        top_players = await DatabaseManager.get_top_players()  # Obtém o top 3 jogadores

        for i, (user_id, damage) in enumerate(top_players):
            member = guild.get_member(user_id)
            if member:
                cargo_id = CARGOS[i + 1]

                # Remove todos os cargos antigos dos top players que não estão mais no top
                for cargo in CARGOS.values():
                    role = guild.get_role(cargo)
                    if role in member.roles and cargo != cargo_id:
                        await member.remove_roles(role)

                # Adiciona o cargo correto ao jogador na posição do top
                top_role = guild.get_role(cargo_id)
                if top_role not in member.roles:
                    await member.add_roles(top_role)
                    print(f"Cargo {top_role.name} adicionado para {member.display_name}.")
            else:
                print(f"Usuário com ID {user_id} não encontrado no servidor.")
