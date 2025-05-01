import pygame
from pygame.locals import *
from typing import List

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Cell:
    def __init__(self, is_wall: bool, is_target: bool):
        self.is_wall = is_wall
        self.is_target = is_target

class Box:
    def __init__(self, position: Position):
        self.position = position

class Player:
    def __init__(self, position: Position):
        self.position = position

    def move(self, direction: str):
        if direction == 'UP':
            self.position.y -= 1
        elif direction == 'DOWN':
            self.position.y += 1
        elif direction == 'LEFT':
            self.position.x -= 1
        elif direction == 'RIGHT':
            self.position.x += 1

class Board:
    def __init__(self, grid: List[List[Cell]]):
        self.grid = grid

    def render(self):
        # Rendering logic for the board
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell.is_wall:
                    pygame.draw.rect(screen, (0, 0, 0), (x * 50, y * 50, 50, 50))
                elif cell.is_target:
                    pygame.draw.rect(screen, (0, 255, 0), (x * 50, y * 50, 50, 50))
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (x * 50, y * 50, 50, 50))
        # Draw player and boxes
        pygame.draw.rect(screen, (0, 0, 255), (self.player.position.x * 50, self.player.position.y * 50, 50, 50))
        for box in self.boxes:
            pygame.draw.rect(screen, (255, 0, 0), (box.position.x * 50, box.position.y * 50, 50, 50))

class Game:
    def __init__(self):
        self.board = None
        self.player = None
        self.boxes = []
        self.initial_state = None

    def load_state(self, file: str):
        with open(file, 'r') as f:
            lines = f.readlines()
            grid = []
            for y, line in enumerate(lines):
                row = []
                for x, char in enumerate(line.strip()):
                    if char == '#':
                        row.append(Cell(is_wall=True, is_target=False))
                    elif char == 'T':
                        row.append(Cell(is_wall=False, is_target=True))
                    elif char == 'B':
                        box_position = Position(x, y)
                        self.boxes.append(Box(box_position))
                        row.append(Cell(is_wall=False, is_target=False))
                    elif char == 'P':
                        self.player = Player(Position(x, y))
                        row.append(Cell(is_wall=False, is_target=False))
                    else:
                        row.append(Cell(is_wall=False, is_target=False))
                grid.append(row)
            self.board = Board(grid)
            self.initial_state = (self.player.position, [box.position for box in self.boxes])

    def save_state(self, file: str):
        with open(file, 'w') as f:
            for y, row in enumerate(self.board.grid):
                line = ''.join(['#' if cell.is_wall else 'T' if cell.is_target else 'B' if any(box.position.x == x and box.position.y == y for box in self.boxes) else 'P' if self.player.position.x == x and self.player.position.y == y else '.' for x, cell in enumerate(row)])
                f.write(line + '\n')

    def check_win(self) -> bool:
        target_positions = [(x, y) for y, row in enumerate(self.board.grid) for x, cell in enumerate(row) if cell.is_target]
        box_positions = [(box.position.x, box.position.y) for box in self.boxes]
        return all(pos in box_positions for pos in target_positions)

    def move_player(self, direction: str):
        original_position = Position(self.player.position.x, self.player.position.y)
        self.player.move(direction)

        # Check for collision with walls
        if self.board.grid[self.player.position.y][self.player.position.x].is_wall:
            self.player.position = original_position
            return

        # Check for box pushing
        for box in self.boxes:
            if box.position.x == self.player.position.x and box.position.y == self.player.position.y:
                box_original_position = Position(box.position.x, box.position.y)
                if direction == 'UP':
                    box.position.y -= 1
                elif direction == 'DOWN':
                    box.position.y += 1
                elif direction == 'LEFT':
                    box.position.x -= 1
                elif direction == 'RIGHT':
                    box.position.x += 1

                # Check if box can be pushed
                if (self.board.grid[box.position.y][box.position.x].is_wall or 
                    any(box.position.x == b.position.x and box.position.y == b.position.y for b in self.boxes if b != box)):
                    box.position = box_original_position
                    self.player.position = original_position
                    return

        # Check win condition after moving
        if self.check_win():
            print("You win!")

    def reset_level(self):
        if self.initial_state:
            self.player.position, box_positions = self.initial_state
            self.boxes = [Box(Position(box.x, box.y)) for box in box_positions]

    def exit_game(self):
        self.save_state('game_state.txt')
        pygame.quit()

    def run(self):
        global screen
        screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption('Game')
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.exit_game()
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.move_player('UP')
                    elif event.key == K_DOWN:
                        self.move_player('DOWN')
                    elif event.key == K_LEFT:
                        self.move_player('LEFT')
                    elif event.key == K_RIGHT:
                        self.move_player('RIGHT')
                    elif event.key == K_r:  # Reset level on 'R' key press
                        self.reset_level()
            self.board.render()
            pygame.display.flip()