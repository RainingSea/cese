import pygame
import os

class Cell:
    def __init__(self, is_target=False, is_wall=False):
        self.is_target = is_target
        self.is_wall = is_wall

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Box:
    def __init__(self, position):
        self.position = position

    def move(self, direction):
        if direction == 'up':
            self.position.y -= 1
        elif direction == 'down':
            self.position.y += 1
        elif direction == 'left':
            self.position.x -= 1
        elif direction == 'right':
            self.position.x += 1

class Player:
    def __init__(self, position):
        self.position = position

    def move(self, direction):
        if direction == 'up':
            self.position.y -= 1
        elif direction == 'down':
            self.position.y += 1
        elif direction == 'left':
            self.position.x -= 1
        elif direction == 'right':
            self.position.x += 1

class Board:
    def __init__(self, width, height):
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]

    def render(self, screen):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                color = (255, 255, 255)  # Default color for empty cell
                if cell.is_wall:
                    color = (0, 0, 0)  # Black for walls
                elif cell.is_target:
                    color = (0, 255, 0)  # Green for targets
                pygame.draw.rect(screen, color, (x * 40, y * 40, 40, 40))

class Game:
    def __init__(self):
        self.board = Board(10, 10)
        self.player = Player(Position(1, 1))
        self.boxes = [Box(Position(2, 2)), Box(Position(3, 3))]
        self.load_state()

    def run(self):
        screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Sokoban")
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.move('up')
                    elif event.key == pygame.K_DOWN:
                        self.player.move('down')
                    elif event.key == pygame.K_LEFT:
                        self.player.move('left')
                    elif event.key == pygame.K_RIGHT:
                        self.player.move('right')

            screen.fill((255, 255, 255))
            self.board.render(screen)
            pygame.display.flip()
            clock.tick(60)

        self.save_state()

    def load_state(self):
        if os.path.exists('game_state.txt'):
            with open('game_state.txt', 'r') as file:
                data = file.readlines()
                player_data = data[0].strip().split(': ')[1].split(',')
                self.player.position = Position(int(player_data[0]), int(player_data[1]))
                box_data = data[1].strip().split(': ')[1].split('; ')
                self.boxes = [Box(Position(int(pos.split(',')[0]), int(pos.split(',')[1]))) for pos in box_data]

    def save_state(self):
        with open('game_state.txt', 'w') as file:
            file.write(f'player: {self.player.position.x},{self.player.position.y}\n')
            file.write('boxes: ' + '; '.join([f'{box.position.x},{box.position.y}' for box in self.boxes]))