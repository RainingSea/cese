import pygame
from maze import Maze
from player import Player
from timer import Timer

class Game:
    def __init__(self):
        self.maze = Maze()
        self.player = Player()
        self.timer = Timer()

    def start_game(self):
        self.maze.generate_maze(10, 'easy')
        self.timer.start()
        self.run_game_loop()

    def run_game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.move('up')
                    elif event.key == pygame.K_DOWN:
                        self.player.move('down')
                    elif event.key == pygame.K_LEFT:
                        self.player.move('left')
                    elif event.key == pygame.K_RIGHT:
                        self.player.move('right')

            self.maze.display_maze()
            if self.player.check_exit():
                self.timer.stop()
                self.display_completion_message()
                running = False

            pygame.display.flip()

    def display_completion_message(self):
        print("Congratulations! You've completed the maze.")

    def restart_level(self):
        self.start_game()

    def exit_game(self):
        pygame.quit()