import pygame
from maze import Maze
from player import Player
from timer import Timer

class Main:
    def main(self) -> str:
        pygame.init()
        game = Game()
        game.start()
        pygame.quit()
        return "Game exited"

class Game:
    def __init__(self):
        self.maze = Maze()
        self.player = Player()
        self.timer = Timer()

    def start(self) -> None:
        self.maze.load_maze("mazes.txt")
        self.timer.start()
        self.run_game_loop()

    def reset(self) -> None:
        self.maze.load_maze("mazes.txt")
        self.player.reset()

    def run_game_loop(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_event(event.key)

            self.update_display()
            pygame.display.flip()

    def handle_key_event(self, key) -> None:
        if key == pygame.K_UP:
            self.player.move("up")
        elif key == pygame.K_DOWN:
            self.player.move("down")
        elif key == pygame.K_LEFT:
            self.player.move("left")
        elif key == pygame.K_RIGHT:
            self.player.move("right")
        if self.maze.check_win():
            self.reset()

    def update_display(self) -> None:
        # Update the display with the current state of the maze and player
        pass

if __name__ == "__main__":
    main = Main()
    main.main()