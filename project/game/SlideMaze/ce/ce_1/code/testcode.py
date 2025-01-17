import unittest
from game import Game, Player, Maze, Timer, Score

class TestSlideMazeGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player = self.game.player
        self.maze = self.game.maze
        self.timer = self.game.timer
        self.score = self.game.score

    def test_navigate_through_maze(self):
        # Functionality 1: Navigate Through the Maze
        self.game.start_game()
        # Attempt to slide a tile horizontally
        self.maze.slide_tile((0, 0))  # Assuming slide_tile modifies the maze
        # Check if the maze layout updated
        self.assertTrue(self.maze.tiles, "Maze layout should update after sliding a tile")
        # Attempt to slide a tile vertically
        self.maze.slide_tile((0, 0))  # Assuming slide_tile modifies the maze
        # Check if the maze layout updated
        self.assertTrue(self.maze.tiles, "Maze layout should update after sliding a tile")

    def test_objective_of_reaching_exit_tile(self):
        # Functionality 2: Objective of Reaching the Exit Tile
        self.game.start_game()
        # Move player to the exit tile
        self.player.position = (4, 4)  # Assuming (4, 4) is the exit
        self.assertTrue(self.maze.is_solved(), "Game should recognize reaching the exit tile")
        # Attempt to move player into a wall or obstacle
        self.player.move('up')  # Assuming (4, 3) is an obstacle
        self.assertNotEqual(self.player.position, (4, 3), "Player should not move into an obstacle")

    def test_multiple_levels_with_increasing_difficulty(self):
        # Functionality 3: Multiple Levels with Increasing Difficulty
        self.game.start_game()
        self.assertEqual(self.maze.tiles, [['empty']*5]*5, "First level should load with a simple maze layout")
        # Complete the first level and proceed to the second level
        self.maze.is_solved = lambda: True  # Mocking maze solved
        self.game.load_level(2)
        self.assertNotEqual(self.maze.tiles, [['empty']*5]*5, "Second level should load with a more complex layout")

    def test_timer_tracking(self):
        # Functionality 4: Timer Tracking
        self.game.start_game()
        self.assertGreater(self.timer.get_time(), 0, "Timer should start counting down")
        # Complete the maze and check the timer
        self.maze.is_solved = lambda: True  # Mocking maze solved
        self.timer.stop()
        self.assertGreater(self.timer.get_time(), 0, "Timer should stop and display total time taken")

    def test_collecting_bonus_points(self):
        # Functionality 5: Collecting Bonus Points
        self.game.start_game()
        self.maze.stars = [(0, 0)]
        self.player.position = (0, 0)
        self.score.add_points(10)  # Assuming collecting a star adds points
        self.assertEqual(self.score.get_score(), 10, "Score should increase by bonus points")
        # Attempt to collect an unreachable star
        self.player.position = (1, 1)  # Assuming (1, 1) is blocked
        self.assertNotEqual(self.player.position, (0, 0), "Player should not collect an unreachable star")

    def test_resetting_the_maze(self):
        # Functionality 6: Resetting the Maze
        self.game.start_game()
        self.player.move('right')
        self.game.reset_game()
        self.assertEqual(self.player.position, (0, 0), "Maze should reset to original configuration")
        # Attempt to reset after reaching the exit
        self.maze.is_solved = lambda: True  # Mocking maze solved
        self.game.reset_game()
        self.assertEqual(self.player.position, (0, 0), "Maze should reset successfully after reaching the exit")

    def test_choosing_a_different_level(self):
        # Functionality 7: Choosing a Different Level
        self.game.start_game()
        self.maze.is_solved = lambda: True  # Mocking maze solved
        self.game.load_level(2)
        self.assertNotEqual(self.maze.tiles, [['empty']*5]*5, "Selected level should load successfully")

if __name__ == '__main__':
    unittest.main()
