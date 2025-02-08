import pygame

class Board:
    def __init__(self):
        self.grid = []

    def draw(self, screen):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                color = (255, 255, 255) if cell == 0 else (0, 0, 0)
                pygame.draw.rect(screen, color, (x * 40, y * 40, 40, 40))

    def update(self):
        pass  # Logic for updating the board can be implemented here.

    def load_from_file(self, file_path: str):
        with open(file_path, 'r') as file:
            self.grid = [list(map(int, line.strip().split())) for line in file]

class Player:
    def __init__(self, start_position):
        self.position = start_position

    def move(self, direction: str):
        if direction == 'up':
            self.position = (self.position[0], self.position[1] - 1)
        elif direction == 'down':
            self.position = (self.position[0], self.position[1] + 1)
        elif direction == 'left':
            self.position = (self.position[0] - 1, self.position[1])
        elif direction == 'right':
            self.position = (self.position[0] + 1, self.position[1])

    def get_position(self) -> tuple:
        return self.position

class ScoreManager:
    def __init__(self):
        self.high_scores = []

    def load_scores(self, file_path: str):
        with open(file_path, 'r') as file:
            self.high_scores = [int(line.strip()) for line in file]

    def save_scores(self, file_path: str):
        with open(file_path, 'w') as file:
            for score in self.high_scores:
                file.write(f"{score}\n")

    def add_score(self, score: int):
        self.high_scores.append(score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:10]  # Keep only top 10 scores

class Game:
    def __init__(self):
        self.board = Board()
        self.player = Player((1, 1))
        self.score_manager = ScoreManager()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Sokoban Game")

        self.load_game_state()

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

            screen.fill((0, 0, 0))
            self.board.draw(screen)
            pygame.display.flip()

        self.save_game_state()
        pygame.quit()

    def load_game_state(self):
        self.board.load_from_file('game_state.txt')
        self.score_manager.load_scores('high_scores.txt')

    def save_game_state(self):
        with open('game_state.txt', 'w') as file:
            for row in self.board.grid:
                file.write(' '.join(map(str, row)) + '\n')