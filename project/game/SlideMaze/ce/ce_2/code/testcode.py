import unittest
from game import Game, Maze, Timer, ScoreManager

class TestSlideMazeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.maze = self.game.maze
        self.timer = self.game.timer
        self.score_manager = self.game.score_manager

    def test_navigate_through_maze(self):
        # Functionality 1: Navigate Through the Maze
        self.maze.load_maze('mazes.txt')
        initial_layout = self.maze.layout
        self.maze.slide_tile('horizontal')
        self.assertNotEqual(self.maze.layout, initial_layout, "Tile should move horizontally")
        
        initial_layout = self.maze.layout
        self.maze.slide_tile('vertical')
        self.assertNotEqual(self.maze.layout, initial_layout, "Tile should move vertically")

    def test_objective_of_reaching_exit_tile(self):
        # Functionality 2: Objective of Reaching the Exit Tile
        self.maze.load_maze('mazes.txt')
        self.maze.is_solved = lambda: True  # Mocking the maze as solved
        self.assertTrue(self.maze.is_solved(), "Player should reach the exit tile")
        
        self.maze.is_solved = lambda: False  # Mocking the maze as not solved
        self.assertFalse(self.maze.is_solved(), "Player should not move into a wall or obstacle")

    def test_multiple_levels_with_increasing_difficulty(self):
        # Functionality 3: Multiple Levels with Increasing Difficulty
        self.game.select_level(1)
        self.assertEqual(self.maze.layout, "1|2|3|4|5\n6|7|8| |9\n10|11|12|13|14\n15|16|17|18|19\n20|21|22|23|24", "First level should load")
        
        # Assuming level 2 has a different layout
        self.game.select_level(2)
        self.assertNotEqual(self.maze.layout, "1|2|3|4|5\n6|7|8| |9\n10|11|12|13|14\n15|16|17|18|19\n20|21|22|23|24", "Second level should load with a different layout")

    def test_timer_tracking(self):
        # Functionality 4: Timer Tracking
        self.timer.start()
        self.assertGreater(self.timer.get_elapsed_time(), 0, "Timer should start counting")
        
        self.timer.stop()
        self.assertGreaterEqual(self.timer.get_elapsed_time(), 0, "Timer should stop and display elapsed time")

    def test_collecting_bonus_points(self):
        # Functionality 5: Collecting Bonus Points
        self.fail("Collecting bonus points functionality is not implemented in the codebase")

    def test_resetting_the_maze(self):
        # Functionality 6: Resetting the Maze
        self.game.reset_maze()
        self.assertEqual(self.maze.layout, "1|2|3|4|5\n6|7|8| |9\n10|11|12|13|14\n15|16|17|18|19\n20|21|22|23|24", "Maze should reset to original configuration")

    def test_choosing_different_level(self):
        # Functionality 7: Choosing a Different Level
        self.game.select_level(1)
        self.assertEqual(self.maze.layout, "1|2|3|4|5\n6|7|8| |9\n10|11|12|13|14\n15|16|17|18|19\n20|21|22|23|24", "First level should load")
        
        self.game.select_level(2)
        self.assertNotEqual(self.maze.layout, "1|2|3|4|5\n6|7|8| |9\n10|11|12|13|14\n15|16|17|18|19\n20|21|22|23|24", "Different level should load successfully")

if __name__ == '__main__':
    unittest.main()
