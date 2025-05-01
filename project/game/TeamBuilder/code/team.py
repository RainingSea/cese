class Team:
    def __init__(self, name: str, logo: str):
        self.name = name
        self.logo = logo
        self.players = []

    def add_player(self, player: Player) -> None:
        self.players.append(player)

    def assign_player_to_position(self, player_id: int, position: str) -> None:
        for player in self.players:
            if player.id == player_id:
                player.position = position
                break