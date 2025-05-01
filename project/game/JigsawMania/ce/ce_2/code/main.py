import pygame
from puzzle import Puzzle
from timer import Timer
from data_storage import save_progress, load_progress

class Main:
    def main(self):
        pygame.init()
        game = Game()
        game.start_new_game("puzzle_image.png", 1)  # Example image and difficulty
        pygame.quit()

class Game:
    def __init__(self):
        self.puzzle = None
        self.timer = Timer()

    def start_new_game(self, image: str, difficulty: int):
        self.puzzle = Puzzle(image)
        self.timer.start()

    def save_progress(self, user: str):
        save_progress(user)

    def load_progress(self, user: str):
        load_progress(user)

    def rotate_piece(self, piece_id: int):
        if self.puzzle:
            self.puzzle.pieces[piece_id].rotate()

    def restart_game(self):
        if self.puzzle:
            self.puzzle.shuffle_pieces()
            self.timer.start()

if __name__ == "__main__":
    main = Main()
    main.main()