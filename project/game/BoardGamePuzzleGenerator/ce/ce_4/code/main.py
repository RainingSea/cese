import pygame
from puzzle_generator import PuzzleGenerator
from timer import Timer
from scoring import Scoring

class Main:
    def __init__(self):
        self.puzzle_generator = PuzzleGenerator("logic")  # Example category
        self.timer = Timer()
        self.scoring = Scoring()

    def main(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Puzzle Game")
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Game logic
            puzzle = self.puzzle_generator.generate_puzzle()
            print(f"Puzzle: {puzzle}")  # Display the puzzle in the console for testing
            self.timer.start()

            # Simulate player input and solution check
            player_solution = puzzle  # Simulate correct solution for testing
            is_correct = self.puzzle_generator.check_solution(puzzle, player_solution)
            time_taken = self.timer.stop()
            score = self.scoring.calculate_score(time_taken, is_correct)

            print(f"Score: {score}")  # Display the score in the console for testing

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Main()
    game.main()