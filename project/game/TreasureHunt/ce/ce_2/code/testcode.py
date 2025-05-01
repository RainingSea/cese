import unittest
from game import Game, Player, Timer, Score

class TestTreasureHuntGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player = self.game.player
        self.timer = self.game.timer
        self.score = self.game.score

    def test_navigate_maze(self):
        # Functionalities 1: Test player movement in the maze
        initial_position = self.player.position
        
        # Move down
        self.player.move('down')
        self.assertEqual(self.player.position, (0, 1), "Player should move down to (0, 1)")

        # Move right
        self.player.move('right')
        self.assertEqual(self.player.position, (1, 1), "Player should move right to (1, 1)")

        # Move up
        self.player.move('up')
        self.assertEqual(self.player.position, (1, 0), "Player should move up to (1, 0)")

        # Move left
        self.player.move('left')
        self.assertEqual(self.player.position, (0, 0), "Player should move left to (0, 0)")

    def test_find_treasure(self):
        # Functionalities 2: Test finding the treasure
        treasure_location = self.game.maze.place_treasure()
        self.player.position = treasure_location  # Simulate reaching the treasure
        self.assertIn(self.player.position, self.game.maze.paths, "Player should be at a valid path location")
        # Here we would normally check for a success message, but it's not implemented

    def test_score_tracking(self):
        # Functionalities 3: Test score increase
        initial_score = self.score.current_score
        self.score.increase_score()
        self.assertEqual(self.score.current_score, initial_score + 1, "Score should increase by 1")

        # Simulate finding treasure again
        self.score.increase_score()
        self.assertEqual(self.score.current_score, initial_score + 2, "Score should increase by 1 again")

    def test_timer_implementation(self):
        # Functionalities 4: Test timer countdown
        self.timer.start_timer(5)  # Start with 5 seconds
        self.assertTrue(self.timer.check_time(), "Timer should be running initially")

        # Simulate time passing
        for _ in range(5):
            self.timer.time_left -= 1
        self.assertFalse(self.timer.check_time(), "Timer should not be running after countdown")

    def test_level_progression(self):
        # Functionalities 5: Test level progression (not implemented in codebase)
        self.fail("Level progression functionality is not implemented in the codebase")

    def test_game_over_condition(self):
        # Functionalities 6: Test game over condition
        self.timer.start_timer(1)  # Start with 1 second
        self.timer.time_left = 0  # Simulate timer running out
        self.assertFalse(self.timer.check_time(), "Game should be over when timer runs out")

    def test_best_time_storage(self):
        # Functionalities 7: Test best time storage
        self.score.save_best_time(30.0)
        self.assertEqual(self.score.best_time, 30.0, "Best time should be 30.0")

        # Simulate a slower time
        self.score.save_best_time(40.0)
        self.assertEqual(self.score.best_time, 30.0, "Best time should remain 30.0")

    def test_restart_game_option(self):
        # Functionalities 8: Test restart game option
        initial_maze = self.game.maze
        self.game.restart()
        self.assertIsNot(initial_maze, self.game.maze, "Maze should be regenerated on restart")

if __name__ == '__main__':
    unittest.main()
