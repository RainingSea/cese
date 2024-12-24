import pygame
from grid import Grid
from score import Score
from timer import Timer
from wordlist import WordList

class Game:
    def __init__(self):
        self.grid = Grid()
        self.score = Score()
        self.timer = Timer()
        self.formed_words = WordList()
        # self.alert_sound = pygame.mixer.Sound(
        #     "D:\\02-Project\\02-Align\models\RTADev\Altdev\project\decide.wav"
        # )  # Load alert sound
        # self.success_sound = pygame.mixer.Sound(
        #     "D:\\02-Project\\02-Align\models\RTADev\Altdev\project\decide.wav"
        # )  # Load success sound

    def start_game(self, difficulty: str):
        self.grid.generate_grid(difficulty)
        self.timer.start_timer(60)  # Default timer set to 60 seconds
        self.run_game_loop()

    def run_game_loop(self):
        running = True
        while running:
            self.timer.update_timer()  # Update timer each loop iteration
            if self.timer.alert_time():
                self.play_alert_sound()  # Play alert sound if time is low

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    word = self.get_word_from_input()  # Assume this function gets the word input from the player
                    if self.validate_word(word):
                        self.formed_words.add_word(word)
                        points = self.score.calculate_score(word)
                        self.score.add_points(points)
                        self.play_success_sound()  # Play success sound for valid word

            self.grid.display_grid()
            pygame.display.flip()

    def play_alert_sound(self):
        self.alert_sound.play()  # Play alert sound

    def play_success_sound(self):
        self.success_sound.play()  # Play success sound

    def save_progress(self):
        with open('game_state.txt', 'w') as f:
            f.write(f"Score: {self.score.get_score()}\n")
            f.write(f"Words: {'|'.join(self.formed_words.get_words())}\n")
            f.write(f"Time Left: {self.timer.time_left}\n")

    def load_progress(self):
        try:
            with open('game_state.txt', 'r') as f:
                lines = f.readlines()
                self.score.points = int(lines[0].split(": ")[1])
                self.formed_words.words = lines[1].split(": ")[1].split("|") if lines[1].split(": ")[1] else []
                self.timer.time_left = int(lines[2].split(": ")[1])
        except FileNotFoundError:
            print("No saved game found.")

    def pause_game(self):
        self.timer.pause_timer()

    def validate_word(self, word: str) -> bool:
        with open('dictionary.txt', 'r') as f:
            valid_words = f.read().splitlines()
        return word in valid_words

    def get_word_from_input(self) -> str:
        # This function should implement the logic to get the word input from the player
        # For now, we will return a placeholder word for demonstration
        return "APPLE"  # Placeholder
