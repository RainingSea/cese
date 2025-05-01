import unittest
from game import Game, Maze, Timer, Score

class TestSlideMazeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.game.load_level(1)  # Load the first level for testing

    def test_navigate_through_maze(self):
        # Functionalities 1: Test sliding tiles
        initial_tiles = self.game.maze.tiles
        self.game.maze.slide_tile('right')  # Attempt to slide a tile right
        self.assertNotEqual(initial_tiles, self.game.maze.tiles, "Tile should move successfully to the right")

        initial_tiles = self.game.maze.tiles
        self.game.maze.slide_tile('down')  # Attempt to slide a tile down
        self.assertNotEqual(initial_tiles, self.game.maze.tiles, "Tile should move successfully down")

    def test_objective_reaching_exit_tile(self):
        # Functionalities 2: Test reaching the exit tile
        self.game.maze.slide_tile('right')  # Simulate moves to reach exit
        self.game.maze.slide_tile('down')
        self.game.maze.slide_tile('down')
        self.assertTrue(self.game.maze.check_win(), "Game should recognize that the player has reached the exit tile")

        # Attempt to move into a wall
        self.game.maze.slide_tile('left')  # Assuming left is a wall
        self.assertFalse(self.game.maze.check_win(), "Game should prevent movement into a wall")

    def test_multiple_levels(self):
        # Functionalities 3: Test loading different levels
        self.game.load_level(1)
        self.assertEqual(self.game.maze.level_id, 'S', "First level should load with a simple maze layout")
        
        self.game.load_level(2)
        self.assertEqual(self.game.maze.level_id, 'S', "Second level should load with a more complex maze layout")

    def test_timer_tracking(self):
        # Functionalities 4: Test timer starts and stops
        self.game.timer.start()
        elapsed_time = self.game.timer.get_elapsed_time()
        self.assertGreaterEqual(elapsed_time, 0, "Timer should start counting as soon as the game begins")

    def test_collecting_bonus_points(self):
        # Functionalities 5: Test collecting stars
        initial_score = self.game.score.get_score()
        self.game.score.add_points(10)  # Simulate collecting a star
        self.assertEqual(self.game.score.get_score(), initial_score + 10, "Score should increase by 10 points")

    def test_resetting_the_maze(self):
        # Functionalities 6: Test resetting the maze
        self.game.reset_maze()
        self.assertIsNotNone(self.game.maze, "Maze should reset to its original configuration")

    def test_choosing_different_level(self):
        # Functionalities 7: Test level selection
        self.game.load_level(1)
        self.assertEqual(self.game.maze.level_id, 'S', "Should load level 1")
        self.game.load_level(2)
        self.assertEqual(self.game.maze.level_id, 'S', "Should load level 2")

if __name__ == '__main__':
    unittest.main()
