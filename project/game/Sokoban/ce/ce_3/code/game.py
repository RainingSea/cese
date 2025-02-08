import pygame
import json

class Game:
    def __init__(self):
        self.board = Board()
        self.player = Player()
        self.game_state = GameState()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.board.width, self.board.height))
        pygame.display.set_caption("Sokoban Game")
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.move("up")
                    elif event.key == pygame.K_DOWN:
                        self.player.move("down")
                    elif event.key == pygame.K_LEFT:
                        self.player.move("left")
                    elif event.key == pygame.K_RIGHT:
                        self.player.move("right")
                    elif event.key == pygame.K_s:
                        self.save_game()
                    elif event.key == pygame.K_l:
                        self.load_game()

            self.board.update(self.player)
            self.board.draw(screen)
            pygame.display.flip()

        pygame.quit()

    def load_game(self):
        self.game_state.load_state("game_state.txt")
        self.player.position = self.game_state.player_position
        self.board.box_positions = self.game_state.box_positions

    def save_game(self):
        self.game_state.save_state("game_state.txt")
        
class Board:
    def __init__(self):
        self.grid = [[0] * 10 for _ in range(10)]  # Example grid
        self.box_positions = [(1, 1), (2, 2)]  # Example box positions
        self.width = 800
        self.height = 600

    def draw(self, screen):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                color = (255, 255, 255) if self.grid[row][col] == 0 else (0, 0, 0)
                pygame.draw.rect(screen, color, (col * 40, row * 40, 40, 40))

    def update(self, player):
        # Update box positions based on player movement
        pass

class Player:
    def __init__(self):
        self.position = (0, 0)

    def move(self, direction: str):
        if direction == "up":
            self.position = (self.position[0] - 1, self.position[1])
        elif direction == "down":
            self.position = (self.position[0] + 1, self.position[1])
        elif direction == "left":
            self.position = (self.position[0], self.position[1] - 1)
        elif direction == "right":
            self.position = (self.position[0], self.position[1] + 1)

class GameState:
    def __init__(self):
        self.player_position = (0, 0)
        self.box_positions = []

    def save_state(self, filename: str):
        state = {
            "player_position": self.player_position,
            "box_positions": self.box_positions
        }
        with open(filename, 'w') as f:
            json.dump(state, f)

    def load_state(self, filename: str):
        with open(filename, 'r') as f:
            state = json.load(f)
            self.player_position = tuple(state["player_position"])
            self.box_positions = [tuple(pos) for pos in state["box_positions"]]