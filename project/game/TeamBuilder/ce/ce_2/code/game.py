import json
import random

class Team:
    def __init__(self, name: str, logo: str):
        self.name = name
        self.logo = logo
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player_id: int):
        self.players = [p for p in self.players if p.id != player_id]

    def assign_position(self, player_id: int, position: str):
        for player in self.players:
            if player.id == player_id:
                player.position = position
                break

    def get_stats(self):
        return {player.name: player.stats for player in self.players}

class Player:
    def __init__(self, player_id: int, name: str, stats: dict):
        self.id = player_id
        self.name = name
        self.stats = stats
        self.position = None

    def train(self, training_type: str):
        if training_type in self.stats:
            self.stats[training_type] += random.randint(1, 5)

class PlayerManager:
    def __init__(self):
        self.available_players = []

    def load_players(self):
        with open('players.txt', 'r') as file:
            data = file.readlines()
            for line in data:
                player_id, name, stats = line.strip().split('|')
                stats_dict = json.loads(stats)
                player = Player(int(player_id), name, stats_dict)
                self.available_players.append(player)

    def get_available_players(self):
        return self.available_players

class MatchManager:
    def __init__(self):
        self.match_history = []

    def record_match(self, result: str, team: Team, opponent: Team):
        match_record = {
            "result": result,
            "team": team.name,
            "opponent": opponent.name
        }
        self.match_history.append(match_record)

    def get_match_history(self):
        return self.match_history

class Game:
    def __init__(self):
        self.team = None
        self.player_manager = PlayerManager()
        self.match_manager = MatchManager()
        self.player_manager.load_players()

    def create_team(self, name: str, logo: str):
        self.team = Team(name, logo)

    def scout_players(self):
        return self.player_manager.get_available_players()

    def train_player(self, player_id: int, training_type: str):
        for player in self.team.players:
            if player.id == player_id:
                player.train(training_type)
                break

    def simulate_match(self, opponent: Team) -> str:
        team_score = random.randint(0, 5)
        opponent_score = random.randint(0, 5)
        result = f"{self.team.name} {team_score} - {opponent.name} {opponent_score}"
        self.match_manager.record_match(result, self.team, opponent)
        return result

    def track_performance(self) -> dict:
        return self.team.get_stats()

    def run(self):
        # Placeholder for game loop
        pass