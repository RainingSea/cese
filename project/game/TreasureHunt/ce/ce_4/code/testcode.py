import unittest
import pygame
from game import Game

class TestTreasureHuntGame(unittest.TestCase):

    def setUp(self):
        # Initialize the game
        self.game = Game()
        pygame.init()
        self.screen = pygame.display.set_mode((200, 200))
        self.game.start_game()

    def test_navigate_maze(self):
        # Functionality 1: Navigate the Maze
        initial_position = self.game.player.position
        self.game.player.move('UP')
        self.assertNotEqual(self.game.player.position, initial_position, "Player should move up")
        
        self.game.player.move('DOWN')
        self.assertNotEqual(self.game.player.position, initial_position, "Player should move down")
        
        self.game.player.move('LEFT')
        self.assertNotEqual(self.game.player.position, initial_position, "Player should move left")
        
        self.game.player.move('RIGHT')
        self.assertNotEqual(self.game.player.position, initial_position, "Player should move right")

    def test_find_treasure(self):
        # Functionality 2: Find the Treasure
        self.game.player.position = self.game.maze.treasure_location
        found_treasure = self.game.player.check_treasure(self.game.maze.treasure_location)
        self.assertTrue(found_treasure, "Player should find the treasure")

    def test_score_tracking(self):
        # Functionality 3: Score Tracking
        initial_score = self.game.score.current_score
        self.game.player.position = self.game.maze.treasure_location
        if self.game.player.check_treasure(self.game.maze.treasure_location):
            self.game.score.increase_score()
        self.assertGreater(self.game.score.current_score, initial_score, "Score should increase after finding treasure")

    def test_timer_implementation(self):
        # Functionality 4: Timer Implementation
        self.game.timer.start()
        pygame.time.delay(1000)  # Wait for 1 second
        elapsed_time = self.game.timer.get_time()
        self.assertGreater(elapsed_time, 0, "Timer should count time elapsed")

    def test_level_progression(self):
        # Functionality 5: Level Progression (not implemented in codebase)
        self.fail("Level progression functionality is not implemented in the codebase")

    def test_game_over_condition(self):
        # Functionality 6: Game Over Condition (not implemented in codebase)
        self.fail("Game over condition functionality is not implemented in the codebase")

    def test_best_time_storage(self):
        # Functionality 7: Best Time Storage
        self.game.score.save_best_time(10.0)
        with open('best_time.txt', 'r') as f:
            best_time = float(f.read())
        self.assertEqual(best_time, 10.0, "Best time should be saved correctly")

    def test_restart_game_option(self):
        # Functionality 8: Restart Game Option
        self.game.restart_game()
        self.assertEqual(self.game.player.position, (0, 0), "Game should reset player position on restart")
        self.assertEqual(self.game.score.current_score, 0, "Score should reset on game restart")

if __name__ == '__main__':
    unittest.main()
