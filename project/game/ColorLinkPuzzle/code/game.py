import pygame
from grid import Grid
from score import Score
from powerup import PowerUp

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.level_data = self.load_levels()
        self.current_level = None
        self.powerups = []

    def load_levels(self):
        levels = []
        with open('levels.txt', 'r') as file:
            for line in file:
                levels.append(line.strip().split('|'))
        return levels

    def start_game(self):
        self.reset_game()
        self.current_level = self.get_next_level()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Additional event handling can be added here
            self.grid.display()
            self.clear_blocks()
            self.check_for_powerups()
            pygame.display.flip()

    def reset_game(self):
        self.score = Score()
        self.grid.reset()
        self.level_data = self.load_levels()

    def clear_blocks(self):
        cleared = self.grid.clear_connected_blocks()
        if cleared:
            points_earned = cleared * 10  # Example: 10 points per block cleared
            self.update_score(points_earned)

    def check_for_powerups(self):
        for powerup in self.powerups:
            if powerup.is_active():
                powerup.apply_effect(self)

    def update_score(self, points: int):
        self.score.update_score(points)

    def get_next_level(self):
        if self.level_data:
            level_info = self.level_data.pop(0)
            print(f"Advancing to {level_info[0]}")
            return level_info
        return None

    def connect_adjacent_blocks(self, start: tuple, end: tuple):
        start_block = self.grid.get_block(start)
        end_block = self.grid.get_block(end)
        if start_block and end_block and start_block.is_adjacent(end_block) and start_block.color == end_block.color:
            cleared = self.grid.clear_connected_blocks(start_block)
            if cleared:
                points_earned = cleared * 10  # Example: 10 points per block cleared
                self.update_score(points_earned)
            print(f"Connected blocks at {start} and {end}")
        else:
            print("Blocks cannot be connected.")

    def increase_difficulty(self):
        self.grid.width += 1
        self.grid.height += 1
        self.grid.reset()
        print("Increased difficulty: New grid size is {}x{}".format(self.grid.width, self.grid.height))