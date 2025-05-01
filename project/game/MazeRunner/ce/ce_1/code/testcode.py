import unittest
import pygame
from game import Game, Player, Maze

class TestMazeRunnerGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player = self.game.player
        self.maze = self.game.maze

    def test_player_controls_character(self):
        # Functionalities 1: Test player movement in the maze
        initial_position = self.player.position
        
        # Move up
        self.player.move('UP')
        self.assertEqual(self.player.position, (initial_position[0], initial_position[1] - 1), "Player should move up")

        # Move down
        self.player.move('DOWN')
        self.assertEqual(self.player.position, (initial_position[0], initial_position[1]), "Player should return to original position after moving down")

        # Move left
        self.player.move('LEFT')
        self.assertEqual(self.player.position, (initial_position[0] - 1, initial_position[1]), "Player should move left")

        # Move right
        self.player.move('RIGHT')
        self.assertEqual(self.player.position, (initial_position[0], initial_position[1]), "Player should return to original position after moving right")

    def test_maze_navigation_and_obstacles(self):
        # Functionalities 2: Test navigation through obstacles
        self.maze.generate_maze(1)  # Generate a maze with obstacles
        initial_position = self.player.position
        
        # Attempt to move into an obstacle (assuming obstacles are generated)
        self.player.move('UP')  # This should be blocked by an obstacle
        self.assertEqual(self.player.position, initial_position, "Player should not move into an obstacle")

    def test_collecting_stars(self):
        # Functionalities 3: Test star collection
        self.maze.generate_maze(1)  # Generate a maze with stars
        initial_score = self.player.score
        
        # Simulate collecting a star
        self.player.collect_star()
        self.assertEqual(self.player.score, initial_score + 1, "Player score should increase by 1 after collecting a star")

    def test_multiple_levels_with_increasing_difficulty(self):
        # Functionalities 4: Test level progression
        self.game.start_game()  # Start the game and complete the first level
        self.game.reset_level()  # Reset to start the next level
        self.assertNotEqual(self.maze.obstacles, [], "Next level should have obstacles")

    def test_strategic_movement_and_dead_ends(self):
        # Functionalities 5: Test navigating dead ends
        self.maze.generate_maze(1)  # Generate a maze with known dead ends
        initial_position = self.player.position
        
        # Attempt to navigate towards a dead end
        self.player.move('UP')  # Assuming this leads to a dead end
        self.assertEqual(self.player.position, initial_position, "Player should realize they are at a dead end")

    def test_timer_for_level_completion(self):
        # Functionalities 6: Test timer functionality
        self.game.start_game()  # Start the game
        self.game.timer.stop()  # Stop the timer after completing the level
        self.assertGreater(self.game.timer.time_elapsed, 0, "Timer should track time taken to complete the level")

    def test_progress_tracking(self):
        # Functionalities 7: Test progress tracking (not implemented in codebase)
        self.fail("Progress tracking functionality is not implemented in the codebase")

    def test_scoring_system(self):
        # Functionalities 8: Test scoring system
        time_taken = 5000  # Example time taken in milliseconds
        stars_collected = 3
        moves = 10
        score = self.game.score.calculate_score(time_taken, stars_collected, moves)
        self.assertEqual(score, 300, "Score should be calculated correctly based on stars collected and moves")

if __name__ == '__main__':
    unittest.main()
