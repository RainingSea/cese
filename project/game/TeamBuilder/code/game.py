import os
import json
from player import Player
from team import Team
from player_scout import PlayerScout
from training import Training
from performance_tracker import PerformanceTracker
from team_manager import TeamManager
from tactics_manager import TacticsManager

class Game:
    def __init__(self):
        self.team_manager = TeamManager()
        self.player_scout = PlayerScout()
        self.training = Training()
        self.performance_tracker = PerformanceTracker()
        self.tactics_manager = TacticsManager()
        self.load_data()

    def load_data(self):
        self.team_manager.load_teams()
        self.player_scout.load_players()
        self.tactics_manager.load_tactics()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def create_team(self, name: str, logo: str) -> None:
        team = Team(name, logo)
        self.team_manager.add_team(team)

    def scout_players(self) -> list:
        return self.player_scout.browse_players()

    def assign_player_to_position(self, player_id: int, position: str) -> None:
        player = self.player_scout.get_player_by_id(player_id)
        if player:
            player.position = position
            self.team_manager.assign_player_to_position(player_id, position)

    def train_player(self, player_id: int, training_type: str) -> None:
        self.training.train(player_id, training_type)

    def track_performance(self, player_id: int) -> str:
        return self.performance_tracker.track(player_id)

    def develop_strategy(self, strategy_name: str, strategy_details: dict) -> None:
        self.tactics_manager.create_tactic(strategy_name, strategy_details)

    def track_team_performance(self) -> PerformanceTracker:
        return self.performance_tracker

    def progress_career(self, player_id: int) -> None:
        player = self.player_scout.get_player_by_id(player_id)
        if player:
            player.update_stats({"skill": player.stats["skill"] + 1})
            print(f"Player {player.name} has progressed in their career.")