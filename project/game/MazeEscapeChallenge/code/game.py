import pygame
from maze import Maze
from timer import Timer
from player import Player

class Game:
    def __init__(self):
        self.maze = Maze()
        self.timer = Timer()
        self.player = Player()
        self.exit_position = (0, 0)
        self.size = 10
        self.difficulty = "easy"
        self.running = True

    def start_game(self):
        self.maze.generate_maze(self.size, self.difficulty)
        self.timer.start()
        self.player.position = (1, 1)  # Starting position
        self.exit_position = (self.size - 2, self.size - 2)  # Exit position

    def navigate(self, input: str):
        self.player.move(input)
        if self.check_exit():
            self.timer.stop()  # Stop the timer when the game is completed
            elapsed_time = self.timer.get_time()
            self.display_completion_message(elapsed_time)
            self.show_main_menu()  # Return to main menu after completion

    def check_exit(self) -> bool:
        return self.player.check_exit(self.exit_position)

    def display_completion_message(self, elapsed_time: float):
        print(f"Congratulations! You've completed the maze in {elapsed_time:.2f} seconds.")

    def restart_level(self):
        self.start_game()

    def show_main_menu(self):
        print("Main Menu")
        print("1. Start Game")
        print("2. Quit")
        choice = input("Choose an option: ")
        if choice == "1":
            self.start_game()
        elif choice == "2":
            pygame.quit()