import json
from player import Player

class PlayerScout:
    def __init__(self):
        self.available_players = []
        self.load_players()

    def load_players(self) -> None:
        with open('players.txt', 'r') as file:
            for line in file:
                player_data = line.strip().split('|')
                player_id = int(player_data[0])
                name = player_data[1]
                stats = json.loads(player_data[2])
                player = Player(player_id, name, stats)
                self.available_players.append(player)

    def browse_players(self) -> list:
        return self.available_players

    def get_player_by_id(self, player_id: int) -> Player:
        for player in self.available_players:
            if player.id == player_id:
                return player
        return None