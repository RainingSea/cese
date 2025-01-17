import unittest
import pygame
from game import Game, Player, Maze, Timer, Score

class TestMazeRunnerGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        self.game = Game()
        self.player = self.game.player
        self.maze = self.game.maze
        self.timer = self.game.timer
        self.score = self.game.score

    def test_player_controls_character(self):
        # Functionalities 1: Test player movement
        initial_position = self.player.position
        self.player.move('UP')
        self.assertEqual(self.player.position, (initial_position[0], initial_position[1] - 1), "Player should move up")

        self.player.move('DOWN')
        self.assertEqual(self.player.position, (initial_position[0], initial_position[1]), "Player should move down")

        self.player.move('LEFT')
        self.assertEqual(self.player.position, (initial_position[0] - 1, initial_position[1]), "Player should move left")

        self.player.move('RIGHT')
        self.assertEqual(self.player.position, (initial_position[0], initial_position[1]), "Player should move right")

    def test_maze_navigation_and_obstacles(self):
        # Functionalities 2: Test maze navigation and obstacles
        self.maze.generate_maze(1)
        self.player.position = (0, 0)
        self.maze.layout[0][1] = 1  # Place an obstacle
        self.player.move('RIGHT')
        self.assertTrue(self.maze.check_collision(self.player), "Player should not move into an obstacle")

    def test_collecting_stars(self):
        # Functionalities 3: Test collecting stars
        initial_score = self.player.score
        self.player.collect_star()
        self.assertEqual(self.player.score, initial_score + 1, "Score should increase by 1 when a star is collected")

    def test_multiple_levels_with_increasing_difficulty(self):
        # Functionalities 4: Test multiple levels
        self.game.load_level(1)
        initial_obstacles = len(self.maze.obstacles)
        self.game.load_level(2)
        self.assertGreater(len(self.maze.obstacles), initial_obstacles, "Level 2 should have more obstacles than Level 1")

    def test_strategic_movement_and_dead_ends(self):
        # Functionalities 5: Test strategic movement and dead ends
        self.maze.generate_maze(1)
        self.maze.layout[0][1] = 1  # Create a dead end
        self.player.position = (0, 0)
        self.player.move('RIGHT')
        self.assertTrue(self.maze.check_collision(self.player), "Player should realize they are at a dead end")

    def test_timer_for_level_completion(self):
        # Functionalities 6: Test timer for level completion
        self.timer.start()
        time.sleep(1)
        elapsed_time = self.timer.stop()
        self.assertGreater(elapsed_time, 0, "Timer should track the time taken to complete the level")

    def test_progress_tracking(self):
        # Functionalities 7: Test progress tracking (not implemented in codebase)
        self.fail("Progress tracking functionality is not implemented in the codebase")

    def test_scoring_system(self):
        # Functionalities 8: Test scoring system
        time_taken = 10
        stars_collected = 3
        moves = 5
        calculated_score = self.score.calculate_score(time_taken, stars_collected, moves)
        expected_score = stars_collected * 10 - time_taken - moves
        self.assertEqual(calculated_score, expected_score, "Score should be calculated based on time, stars, and moves")

if __name__ == '__main__':
    unittest.main()
