import pygame

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.dictionary = Dictionary()
        self.dictionary.load_words('dictionary.txt')
        self.current_word = ""

    def run(self):
        # Initialize Pygame and start the game loop
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Word Formation Game")
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    start_pos = pygame.mouse.get_pos()
                    self.current_word = self.grid.connect_letters(start_pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.dictionary.is_valid(self.current_word):
                        self.update_score(self.current_word)
                        self.current_word = ""

            screen.fill((255, 255, 255))
            self.grid.display(screen)
            self.display_score(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def update_score(self, word: str):
        points = self.calculate_points(word)  # Calculate points based on word length and complexity
        self.score.add_points(points)

    def calculate_points(self, word: str) -> int:
        base_points = len(word)  # Points based on word length
        bonus_points = 0
        
        # Bonus points for complex words (for example, words longer than 5 letters)
        if len(word) > 5:
            bonus_points = 2  # Example bonus for longer words
        
        return base_points + bonus_points

    def display_score(self, screen):
        font = pygame.font.Font(None, 36)
        score_text = f"Score: {self.score.get_score()}"
        text = font.render(score_text, True, (0, 0, 0))
        screen.blit(text, (10, 10))

class Grid:
    def __init__(self):
        self.letters = [['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H'], ['I', 'J', 'K', 'L'], ['M', 'N', 'O', 'P']]
        self.selected_letters = []

    def display(self, screen):
        # Display the letter grid on the screen
        font = pygame.font.Font(None, 36)
        for row_index, row in enumerate(self.letters):
            for col_index, letter in enumerate(row):
                text = font.render(letter, True, (0, 0, 0))
                screen.blit(text, (col_index * 50 + 100, row_index * 50 + 100))

    def connect_letters(self, start: tuple) -> str:
        # Logic to connect letters based on mouse position
        row = (start[1] - 100) // 50
        col = (start[0] - 100) // 50
        if 0 <= row < len(self.letters) and 0 <= col < len(self.letters[0]):
            letter = self.letters[row][col]
            self.selected_letters.append(letter)
            return ''.join(self.selected_letters)
        return ""

class Score:
    def __init__(self):
        self.total_score = 0

    def add_points(self, points: int):
        self.total_score += points

    def get_score(self) -> int:
        return self.total_score

class Dictionary:
    def __init__(self):
        self.valid_words = set()

    def load_words(self, file_path: str):
        with open(file_path, 'r') as file:
            for line in file:
                self.valid_words.add(line.strip())

    def is_valid(self, word: str) -> bool:
        return word in self.valid_words

    def save_scores(self, file_path: str, scores: dict):
        with open(file_path, 'w') as file:
            for player, score in scores.items():
                file.write(f"{player}|{score}\n")

    def load_scores(self, file_path: str) -> dict:
        scores = {}
        with open(file_path, 'r') as file:
            for line in file:
                player, score = line.strip().split('|')
                scores[player] = int(score)
        return scores