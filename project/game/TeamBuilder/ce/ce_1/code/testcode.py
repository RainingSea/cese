import unittest
import json
import os
from main import Main, TeamManager, PlayerScout, PerformanceTracker, Player, Match

class TestTeamBuilderGame(unittest.TestCase):

    def setUp(self):
        # Initialize the main game class
        self.game = Main()
        self.team_manager = self.game.team_manager
        self.player_scout = self.game.player_scout
        self.performance_tracker = self.game.performance_tracker

    def test_create_team(self):
        # Functionality 1: Create and Manage a Virtual Sports Team
        self.team_manager.create_team("Team A", "team_logo.png")
        self.assertEqual(self.team_manager.team_name, "Team A", "Team name should be set correctly")
        self.assertEqual(self.team_manager.team_logo, "team_logo.png", "Team logo should be set correctly")
        
        # Check if team data is saved correctly
        with open('team.txt', 'r') as file:
            data = file.read().strip()
            self.assertEqual(data, "Team A|team_logo.png", "Team data should be saved correctly")

    def test_browse_players(self):
        # Functionality 2: Scout for New Talent
        players = self.player_scout.browse_players()
        self.assertGreater(len(players), 0, "There should be available players to scout")
        self.assertIsInstance(players[0], Player, "Players should be instances of Player class")

    def test_assign_athletes_to_positions(self):
        # Functionality 3: Assign Athletes to Positions (not implemented in codebase)
        self.fail("Assigning athletes to positions functionality is not implemented in the codebase")

    def test_train_athletes(self):
        # Functionality 4: Train Athletes
        player = Player("Player1", {"speed": 80, "strength": 75})
        initial_speed = player.stats["speed"]
        player.train("speed", 5)
        self.assertEqual(player.stats["speed"], initial_speed + 5, "Player's speed should improve after training")

    def test_develop_tactics_and_plans(self):
        # Functionality 5: Develop Tactics and Plans (not implemented in codebase)
        self.fail("Developing tactics and plans functionality is not implemented in the codebase")

    def test_track_team_performance(self):
        # Functionality 6: Track Team Performance
        matches = self.performance_tracker.match_history
        self.assertGreater(len(matches), 0, "There should be match history to track")
        self.assertIsInstance(matches[0], Match, "Match history should contain instances of Match class")

    def test_career_progression_system(self):
        # Functionality 7: Career Progression System (not implemented in codebase)
        self.fail("Career progression system functionality is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
