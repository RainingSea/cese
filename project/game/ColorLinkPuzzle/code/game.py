import pygame
import json
from typing import List, Tuple, Dict

class Block:
    def __init__(self, color: str, position: Tuple[int, int]) -> None:
        self.color = color
        self.position = position

class Grid:
    def __init__(self) -> None:
        self.blocks: List[List[Block]] = []

    def initialize_grid(self, controlled_colors: List[str] = None) -> None:
        if controlled_colors is None:
            colors = ['red', 'green', 'blue', 'yellow']
        else:
            colors = controlled_colors
        self.blocks = [[Block(colors[(i + j) % len(colors)], (i, j)) for j in range(5)] for i in range(5)]

    def clear_blocks(self, blocks: List[Block]) -> None:
        for block in blocks:
            print(f"Clearing block at {block.position} with color {block.color}")
            self.blocks[block.position[0]][block.position[1]] = None

    def check_path(self, start: Block, end: Block) -> bool:
        return self.is_path_clear(start.position, end.position)

    def is_path_clear(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> bool:
        return self.blocks[start_pos[0]][start_pos[1]].color == self.blocks[end_pos[0]][end_pos[1]].color

    def connect_adjacent_blocks_of_same_color(self, block: Block) -> List[Block]:
        connected_blocks = [block]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor_pos = (block.position[0] + dx, block.position[1] + dy)
            if (0 <= neighbor_pos[0] < 5) and (0 <= neighbor_pos[1] < 5):
                neighbor_block = self.blocks[neighbor_pos[0]][neighbor_pos[1]]
                if neighbor_block and neighbor_block.color == block.color and neighbor_block not in connected_blocks:
                    connected_blocks.extend(self.connect_adjacent_blocks_of_same_color(neighbor_block))
        return connected_blocks

class Score:
    def __init__(self) -> None:
        self.current_score: int = 0

    def update_score(self, points: int) -> None:
        self.current_score += points

    def get_score(self) -> int:
        return self.current_score

class Menu:
    def display_menu(self) -> None:
        print("1. Start New Game")
        print("2. View High Scores")

    def start_new_game(self) -> None:
        print("Starting a new game...")

    def view_high_scores(self) -> None:
        print("Viewing high scores...")

class HighScores:
    def __init__(self) -> None:
        self.scores: List[Dict[str, int]] = []

    def load_scores(self) -> None:
        try:
            with open('high_scores.json', 'r') as f:
                self.scores = json.load(f).get('scores', [])
        except FileNotFoundError:
            self.scores = []

    def save_score(self, name: str, score: int) -> None:
        self.scores.append({"name": name, "score": score})
        self.save_scores()

    def save_scores(self) -> None:
        with open('high_scores.json', 'w') as f:
            json.dump({'scores': self.scores}, f)

    def display_high_scores(self) -> None:
        if not self.scores:
            print("No high scores available.")
            return
        print("High Scores:")
        for entry in sorted(self.scores, key=lambda x: x['score'], reverse=True):
            print(f"{entry['name']} | {entry['score']}")

class LevelData:
    def __init__(self) -> None:
        self.levels: List[Dict[str, int]] = []

    def load_levels(self) -> None:
        try:
            with open('level_data.json', 'r') as f:
                self.levels = json.load(f).get('levels', [])
        except FileNotFoundError:
            self.levels = []

    def save_levels(self) -> None:
        with open('level_data.json', 'w') as f:
            json.dump({'levels': self.levels}, f)

    def next_level(self, current_level: int) -> int:
        if current_level < len(self.levels):
            return current_level + 1
        return current_level

class Game:
    def __init__(self) -> None:
        self.grid = Grid()
        self.score = Score()
        self.menu = Menu()
        self.high_scores = HighScores()
        self.level_data = LevelData()
        self.current_level: int = 1

    def start_game(self) -> None:
        print("Game Started")
        self.grid.initialize_grid(controlled_colors=['red', 'green', 'blue', 'yellow'])
        self.high_scores.load_scores()
        self.level_data.load_levels()
        self.menu.start_new_game()
        self.menu.display_menu()  # Display menu after starting the game

    def update(self) -> None:
        # Update game state
        pass

    def draw(self) -> None:
        # Draw game elements
        pass

    def provide_visual_feedback_on_successful_connections(self, connected_blocks: List[Block]) -> None:
        if connected_blocks:
            print(f"Connected blocks: {[block.position for block in connected_blocks]}")

    def use_bonuses_and_power_ups(self) -> None:
        print("Using bonuses and power-ups...")

    def clear_connected_blocks(self, block: Block) -> None:
        connected_blocks = self.grid.connect_adjacent_blocks_of_same_color(block)
        self.grid.clear_blocks(connected_blocks)
        self.provide_visual_feedback_on_successful_connections(connected_blocks)
        self.score.update_score(len(connected_blocks))  # Update score based on connected blocks