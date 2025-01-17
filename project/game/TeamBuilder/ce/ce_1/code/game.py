import random
import json

class Team:
    def __init__(self, name: str, logo: str):
        self.name = name
        self.logo = logo
        self.players = []

    def add_player(self, athlete):
        self.players.append(athlete)

    def get_stats(self):
        stats = {}
        for player in self.players:
            stats[player.name] = player.stats
        return stats

class Athlete:
    def __init__(self, name: str, position: str, stats: dict):
        self.name = name
        self.position = position
        self.stats = stats

    def train(self, exercise: str):
        if exercise in self.stats:
            self.stats[exercise] += random.randint(1, 5)  # Simulate training improvement

class Game:
    def __init__(self):
        self.team = None
        self.athletes = self.load_athletes()

    def create_team(self, name: str, logo: str):
        self.team = Team(name, logo)

    def scout_athletes(self):
        return random.sample(self.athletes, 3)  # Scout 3 random athletes

    def assign_player(self, position: str, athlete: Athlete):
        if self.team:
            athlete.position = position
            self.team.add_player(athlete)

    def train_player(self, athlete: Athlete, exercise: str):
        athlete.train(exercise)

    def simulate_match(self, opponent: Team):
        return f"{self.team.name} vs {opponent.name}: {random.choice(['Win', 'Lose', 'Draw'])}"

    def track_performance(self):
        return self.team.get_stats()

    def load_athletes(self):
        with open('data/athletes.txt', 'r') as file:
            athletes = []
            for line in file:
                name, position, stats = line.strip().split('|')
                stats_dict = json.loads(stats)
                athletes.append(Athlete(name, position, stats_dict))
            return athletes