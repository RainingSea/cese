import pygame
from game import Game

def main():
    game = Game()
    game.run()
    high_scores = game.high_score_manager.load_high_scores()
    print("High Scores:", high_scores)

if __name__ == "__main__":
    main()