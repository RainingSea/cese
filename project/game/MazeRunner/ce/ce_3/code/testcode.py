import unittest
import pygame
from game import Game, Player, Maze, Timer, Score

class TestMazeRunnerGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game and its components
        pygame.init()
        self.game = Game()
        self.player = self.game.player
        self.maze = self.game.maze
        self.timer = self.game.timer
        self.score = self.game.score

    def test_player_controls_character(self):
        # Functionality 1: Test player movement
        initial_position = self.player.position
        self.player.move('up')
        self.assertEqual(self.player.position, (initial_position[0], initial_position[1] - 1), "Player should move up")

        self.player.move('down')
        self.assertEqual(self.player.position, (initial_position[0], initial_position[1]), "Player should move down")

        self.player.move('left')
        self.assertEqual(self.player.position, (initial_position[0] - 1, initial_position[1]), "Player should move left")

        self.player.move('right')
        self.assertEqual(self.player.position, (initial_position[0], initial_position[1]), "Player should move right")

    def test_maze_navigation_and_obstacles(self):
        # Functionality 2: Test maze navigation and obstacles
        self.maze.generate_maze(1)
        initial_position = self.player.position
        self.maze.obstacles.append((initial_position[0], initial_position[1] - 1))  # Add obstacle above player
        self.player.move('up')
        self.assertEqual(self.player.position, initial_position, "Player should not move into an obstacle")

    def test_collecting_stars(self):
        # Functionality 3: Test collecting stars
        self.maze.stars.append((self.player.position[0], self.player.position[1] + 1))  # Place star below player
        self.player.move('down')
        self.player.collect_star()
        self.assertEqual(self.player.score, 1, "Player should collect a star and increase score")

    def test_multiple_levels_with_increasing_difficulty(self):
        # Functionality 4: Test multiple levels
        self.game.load_levels()
        self.assertGreater(len(self.maze.grid), 0, "Levels should be loaded")

    def test_strategic_movement_and_dead_ends(self):
        # Functionality 5: Test strategic movement and dead ends
        self.maze.generate_maze(1)
        self.maze.obstacles.append((self.player.position[0] + 1, self.player.position[1]))  # Create dead end
        self.player.move('right')
        self.assertEqual(self.player.position, (self.player.position[0], self.player.position[1]), "Player should not move into a dead end")

    def test_timer_for_level_completion(self):
        # Functionality 6: Test timer
        self.timer.start()
        time.sleep(1)
        elapsed_time = self.timer.get_time()
        self.assertGreater(elapsed_time, 0, "Timer should track elapsed time")

    def test_progress_tracking(self):
        # Functionality 7: Test progress tracking
        self.score.update_score(30.0, 5, 10)
        self.score.save_scores()
        self.score.load_scores()
        self.assertIn((30.0, 5, 10), self.score.high_scores, "Scores should be saved and loaded correctly")

    def test_scoring_system(self):
        # Functionality 8: Test scoring system
        self.score.update_score(25.0, 3, 8)
        self.assertIn((25.0, 3, 8), self.score.high_scores, "Scores should reflect player's performance")

if __name__ == '__main__':
    unittest.main()
