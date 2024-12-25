from grid import Grid
from score import Score
from timer import Timer
from wordlist import WordList
from gamestate import GameState
import pygame

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.timer = Timer()
        self.word_list = WordList()
        self.game_state = GameState()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Word Formation Game")
        self.font = pygame.font.Font(None, 36)
        self.sound_success = pygame.mixer.Sound("success.wav")
        self.sound_bonus = pygame.mixer.Sound("bonus.wav")
        self.sound_timer_warning = pygame.mixer.Sound("timer_warning.wav")

    def start_game(self):
        self.word_list.load_words('dictionary.txt')
        self.grid.generate_grid(4)  # Example grid size
        self.timer.start_timer(300)  # 5 minutes timer
        self.game_loop()

    def game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_event(event)
            if self.timer.check_time():
                print("Time's up!")
                running = False
            if self.timer.time_left <= 30 and self.timer.running:  # Timer warning at 30 seconds
                self.sound_timer_warning.play()
            self.update_display()
            pygame.display.flip()

    def handle_key_event(self, event):
        if event.key == pygame.K_p:  # Pause game
            self.pause_game()
        elif event.key == pygame.K_s:  # Save progress
            self.save_progress()
        elif event.key == pygame.K_l:  # Load progress
            self.load_progress()
        elif event.key == pygame.K_RETURN:  # Validate word
            word = self.get_word_from_input()  # Assume this function gets the word from input
            if self.validate_word(word):
                self.score.update_score(word)
                self.game_state.formed_words.append(word)
                self.sound_success.play()  # Play success sound
            else:
                print("Invalid word!")

    def update_display(self):
        self.screen.fill((255, 255, 255))  # Clear screen with white background
        self.draw_grid()
        self.draw_score()
        self.draw_timer()
        self.draw_formed_words()

    def draw_grid(self):
        for row_index, row in enumerate(self.grid.letters):
            for col_index, letter in enumerate(row):
                letter_surface = self.font.render(letter, True, (0, 0, 0))
                self.screen.blit(letter_surface, (col_index * 50 + 50, row_index * 50 + 50))

    def draw_score(self):
        score_surface = self.font.render(f"Score: {self.score.get_score()}", True, (0, 0, 0))
        self.screen.blit(score_surface, (50, 10))

    def draw_timer(self):
        timer_surface = self.font.render(f"Time Left: {self.timer.time_left}", True, (0, 0, 0))
        self.screen.blit(timer_surface, (650, 10))

    def draw_formed_words(self):
        words_surface = self.font.render("Formed Words: " + ", ".join(self.game_state.formed_words), True, (0, 0, 0))
        self.screen.blit(words_surface, (50, 550))

    def pause_game(self):
        self.timer.pause_timer()

    def save_progress(self):
        self.game_state.current_grid = self.grid.letters
        self.game_state.current_score = self.score.get_score()
        self.game_state.save_state('save_game.txt')

    def load_progress(self):
        self.game_state.load_state('save_game.txt')
        self.grid.letters = self.game_state.current_grid
        self.score.points = self.game_state.current_score

    def validate_word(self, word: str) -> bool:
        return self.word_list.is_valid_word(word)

    def get_word_from_input(self) -> str:
        # Placeholder for actual input handling
        return "example"  # Replace with actual input handling logic