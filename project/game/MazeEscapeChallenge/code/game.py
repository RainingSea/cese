import pygame
from maze import Maze
from player import Player
from timer import Timer

class Game:
    def __init__(self):
        self.maze = Maze()
        self.player = Player()
        self.timer = Timer()
        self.running = True
        self.state = "menu"  # Possible states: menu, gameplay, completion

    def start_game(self):
        self.maze.load_maze("mazes.txt")  # Load maze from file
        self.timer.start()
        self.game_loop()

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                self.handle_player_movement(event)

            # Update game state and render
            self.render_game()

            if self.check_exit():
                self.timer.stop()
                self.player.record_time(self.timer.get_time())
                self.state = "completion"
                self.exit_game()

    def handle_player_movement(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.player.move('up', self.maze)
            elif event.key == pygame.K_DOWN:
                self.player.move('down', self.maze)
            elif event.key == pygame.K_LEFT:
                self.player.move('left', self.maze)
            elif event.key == pygame.K_RIGHT:
                self.player.move('right', self.maze)

    def pause_game(self):
        self.state = "paused"

    def resume_game(self):
        self.state = "gameplay"

    def restart_level(self):
        self.player.position_x = 0  # Reset player position
        self.player.position_y = 0
        self.start_game()  # Restart the game

    def return_to_main_menu(self):
        self.state = "menu"
        self.player.position_x = 0
        self.player.position_y = 0
        self.timer.stop()

    def exit_game(self):
        self.running = False

    def render_game(self):
        # Placeholder for rendering logic
        pass

    def check_exit(self):
        if self.player.position_x == self.maze.exit_position[0] and self.player.position_y == self.maze.exit_position[1]:
            return True
        return False