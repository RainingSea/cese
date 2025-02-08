import pygame
import json

class Board:
    def __init__(self, grid):
        self.grid = grid

    def draw(self, screen):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == '#':
                    pygame.draw.rect(screen, (0, 0, 0), (x * 40, y * 40, 40, 40))
                elif cell == '$':
                    pygame.draw.rect(screen, (0, 255, 0), (x * 40, y * 40, 40, 40))
                elif cell == '.':
                    pygame.draw.rect(screen, (255, 255, 0), (x * 40, y * 40, 40, 40))
                elif cell == ' ':
                    pygame.draw.rect(screen, (255, 255, 255), (x * 40, y * 40, 40, 40))

    def update_grid(self, position):
        x, y = position
        self.grid[y][x] = ' '  # Update grid to empty space

class Player:
    def __init__(self, position):
        self.position = position

    def move(self, direction):
        if direction == 'UP':
            self.position = (self.position[0], self.position[1] - 1)
        elif direction == 'DOWN':
            self.position = (self.position[0], self.position[1] + 1)
        elif direction == 'LEFT':
            self.position = (self.position[0] - 1, self.position[1])
        elif direction == 'RIGHT':
            self.position = (self.position[0] + 1, self.position[1])

    def get_position(self):
        return self.position

class GameState:
    def __init__(self):
        self.state_data = {}

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.state_data, file)

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            self.state_data = json.load(file)

class Game:
    def __init__(self):
        self.board = Board([
            ['#', '#', '#', '#', '#'],
            ['#', ' ', ' ', '$', '#'],
            ['#', ' ', '#', ' ', '#'],
            ['#', 'P', ' ', ' ', '#'],
            ['#', '#', '#', '#', '#']
        ])
        self.player = Player((1, 3))  # Starting position of the player
        self.game_state = GameState()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((200, 200))
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_input(event)

            self.update()
            self.render(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.player.move('UP')
            elif event.key == pygame.K_DOWN:
                self.player.move('DOWN')
            elif event.key == pygame.K_LEFT:
                self.player.move('LEFT')
            elif event.key == pygame.K_RIGHT:
                self.player.move('RIGHT')

    def update(self):
        player_pos = self.player.get_position()
        if self.board.grid[player_pos[1]][player_pos[0]] == '$':
            self.board.update_grid(player_pos)

    def render(self, screen):
        screen.fill((255, 255, 255))
        self.board.draw(screen)

    def save_state(self):
        self.game_state.state_data = {
            'player_position': self.player.get_position()
        }
        self.game_state.save_to_file('game_state.txt')

    def load_state(self):
        self.game_state.load_from_file('game_state.txt')
        self.player.position = tuple(self.game_state.state_data['player_position'])