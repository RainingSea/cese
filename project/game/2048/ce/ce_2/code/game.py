import pygame
from game_board import GameBoard
from score import Score
from ui import UI

class Game:
    def __init__(self):
        self.board = GameBoard()
        self.score = Score()
        self.ui = UI()

    def start_game(self):
        self.board.initialize_board()
        self.ui.render_board(self.board.tiles)
        self.ui.display_score(self.score.get_score())
        self.game_loop()

    def game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move('up')
                    elif event.key == pygame.K_DOWN:
                        self.move('down')
                    elif event.key == pygame.K_LEFT:
                        self.move('left')
                    elif event.key == pygame.K_RIGHT:
                        self.move('right')
                    elif event.key == pygame.K_s:  # Save game
                        self.save_game()
                    elif event.key == pygame.K_l:  # Load game
                        self.load_game()

            if self.game_over():
                self.ui.show_game_over()
                running = False

    def move(self, direction: str):
        previous_tiles = [row[:] for row in self.board.tiles]  # Copy current state
        self.board.move_tiles(direction)
        if previous_tiles != self.board.tiles:  # Only update score if tiles changed
            self.score.update_score(self.board.get_score_increment())
            self.ui.render_board(self.board.tiles)
            self.ui.display_score(self.score.get_score())
            self.board.generate_new_tile()

    def game_over(self) -> bool:
        return self.board.check_game_over()

    def save_game(self):
        try:
            with open('game_state.txt', 'w') as file:
                file.write(','.join(map(str, [tile for row in self.board.tiles for tile in row])) + '\n')
                file.write(f'Score: {self.score.get_score()}')
        except Exception as e:
            print(f"Error saving game: {e}")

    def load_game(self):
        try:
            with open('game_state.txt', 'r') as file:
                lines = file.readlines()
                tiles = list(map(int, lines[0].strip().split(',')))
                self.board.tiles = [tiles[i:i + 4] for i in range(0, len(tiles), 4)]
                self.score.current_score = int(lines[1].strip().split('Score: ')[1])
                self.ui.render_board(self.board.tiles)  # Update UI after loading
                self.ui.display_score(self.score.get_score())
        except Exception as e:
            print(f"Error loading game: {e}")