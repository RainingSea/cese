class GameState:
    def __init__(self):
        self.current_grid = []
        self.current_score = 0
        self.formed_words = []

    def save_state(self, file_path: str):
        """Saves the current game state to a file."""
        with open(file_path, 'w') as file:
            file.write(f"{self.current_grid}\n{self.current_score}\n{self.formed_words}")

    def load_state(self, file_path: str):
        """Loads the game state from a file."""
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.current_grid = eval(lines[0].strip())
            self.current_score = int(lines[1].strip())
            self.formed_words = eval(lines[2].strip())