import unittest
from game import Game, Player, Stats

class TestTeamBuilderGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()
        self.game.create_team("Dream Team", "logo.png")
        self.players = self.game.scout_players()

    def test_create_and_manage_virtual_sports_team(self):
        # Functionalities 1: Test team creation
        self.assertIsNotNone(self.game.team, "Team should be created successfully")
        self.assertEqual(self.game.team.name, "Dream Team", "Team name should match")
        self.assertEqual(self.game.team.logo, "logo.png", "Team logo should match")

    def test_scout_for_new_talent(self):
        # Functionalities 2: Test scouting players
        self.assertEqual(len(self.players), 4, "There should be 4 players scouted")
        for player in self.players:
            self.assertIsInstance(player, Player, "Scouted talent should be a Player instance")

    def test_assign_athletes_to_positions(self):
        # Functionalities 3: Test assigning players to positions
        player = self.players[0]
        self.game.assign_player("Forward", player)
        self.assertIn(player, self.game.team.players, "Player should be added to the team")
        self.assertEqual(player.stats.position, "Forward", "Player position should be set to Forward")

    def test_train_athletes(self):
        # Functionalities 4: Test training athletes
        player = self.players[0]
        initial_skill = player.stats.skill_level
        self.game.train_player(player, "speed")
        self.assertGreater(player.stats.skill_level, initial_skill, "Player's skill level should increase after training")

    def test_develop_tactics_and_plans(self):
        # Functionalities 5: Test developing strategy
        self.game.develop_strategy("Offensive")  # No assertion, just checking if it runs without error

    def test_track_team_performance(self):
        # Functionalities 6: Test tracking performance
        self.game.performance.update_record("Win")
        self.assertIn("Win", self.game.track_performance().win_loss_record, "Performance record should include the latest result")

    def test_career_progression_system(self):
        # Functionalities 7: Test career progression (not implemented in codebase)
        self.fail("Career progression system is not implemented in the codebase")

if __name__ == '__main__':
    unittest.main()
