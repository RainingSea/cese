import pygame
import json
import random
from typing import List, Tuple, Dict

class PlayerBall:
    """Class representing the player's ball."""
    
    def __init__(self, size: int, position_x: int, position_y: int):
        self.size = size
        self.position_x = position_x
        self.position_y = position_y

    def move(self, direction: str):
        """Move the player ball in the specified direction."""
        if direction == 'up':
            self.position_y -= 5
        elif direction == 'down':
            self.position_y += 5
        elif direction == 'left':
            self.position_x -= 5
        elif direction == 'right':
            self.position_x += 5

    def grow(self, size_increase: int):
        """Increase the size of the player ball."""
        self.size += size_increase

class EnemyBall:
    """Class representing an enemy ball."""
    
    def __init__(self, size: int, position_x: int, position_y: int):
        self.size = size
        self.position_x = position_x
        self.position_y = position_y

    def move(self):
        """Randomly move the enemy ball."""
        self.position_x += random.choice([-1, 1])
        self.position_y += random.choice([-1, 1])

class DataStorage:
    """Class for handling game data storage."""
    
    def save_game_state(self, data: Dict):
        """Save the current game state to a JSON file."""
        with open('game_data.json', 'w') as file:
            json.dump(data, file)

    def load_game_state(self) -> Dict:
        """Load the game state from a JSON file."""
        try:
            with open('game_data.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_high_scores(self, scores: List[int]):
        """Save high scores to a JSON file."""
        with open('high_scores.json', 'w') as file:
            json.dump(scores, file)

    def load_high_scores(self) -> List[int]:
        """Load high scores from a JSON file."""
        try:
            with open('high_scores.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

class Game:
    """Main game class to manage the game logic and flow."""
    
    def __init__(self):
        self.player_ball = PlayerBall(size=20, position_x=400, position_y=300)
        self.enemy_balls: List[EnemyBall] = []
        self.is_game_over = False
        self.data_storage = DataStorage()
        self.initialize_balls()
        self.load_game_state()

    def initialize_balls(self):
        """Initialize enemy balls."""
        for _ in range(5):
            self.spawn_enemy_ball()

    def spawn_enemy_ball(self):
        """Spawn a single enemy ball at a random position."""
        size = random.randint(5, 15)
        position_x = random.randint(0, 800)
        position_y = random.randint(0, 600)
        new_enemy_ball = EnemyBall(size=size, position_x=position_x, position_y=position_y)
        self.enemy_balls.append(new_enemy_ball)

    def run(self):
        """Run the main game loop."""
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Battle of Balls")
        clock = pygame.time.Clock()

        while not self.is_game_over:
            self.handle_input()
            self.update()
            self.render(screen)
            clock.tick(60)

        pygame.quit()

    def handle_input(self):
        """Handle user input for player movement."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player_ball.move('up')
        if keys[pygame.K_DOWN]:
            self.player_ball.move('down')
        if keys[pygame.K_LEFT]:
            self.player_ball.move('left')
        if keys[pygame.K_RIGHT]:
            self.player_ball.move('right')

    def update(self):
        """Update the game state."""
        for enemy in self.enemy_balls:
            enemy.move()
        self.check_collisions()

    def render(self, screen):
        """Render the game objects on the screen."""
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (0, 255, 0), (self.player_ball.position_x, self.player_ball.position_y), self.player_ball.size)

        for enemy in self.enemy_balls:
            pygame.draw.circle(screen, (255, 0, 0), (enemy.position_x, enemy.position_y), enemy.size)

        pygame.display.flip()

    def check_collisions(self):
        """Check for collisions between the player ball and enemy balls."""
        for enemy in self.enemy_balls[:]:  # Iterate over a copy to avoid modification during iteration
            if self.is_colliding(self.player_ball.position_x, self.player_ball.size, enemy.position_x, enemy.size):
                if self.player_ball.size > enemy.size:
                    self.player_ball.grow(enemy.size)
                    self.enemy_balls.remove(enemy)
                else:
                    self.end_game()

    def is_colliding(self, pos1_x: int, size1: int, pos2_x: int, size2: int) -> bool:
        """Check if two balls are colliding."""
        distance = abs(pos1_x - pos2_x)
        return distance < (size1 + size2)

    def end_game(self):
        """End the game and save the game state."""
        self.is_game_over = True
        self.save_game_state()

    def save_game_state(self):
        """Save the current game state."""
        game_state = {
            "player_size": self.player_ball.size,
            "player_position": (self.player_ball.position_x, self.player_ball.position_y),
            "enemy_positions": [(enemy.position_x, enemy.position_y) for enemy in self.enemy_balls],
            "is_game_over": self.is_game_over
        }
        self.data_storage.save_game_state(game_state)

    def load_game_state(self):
        """Load the game state from a file."""
        game_state = self.data_storage.load_game_state()
        if game_state:
            self.player_ball.size = game_state.get("player_size", self.player_ball.size)
            self.player_ball.position_x, self.player_ball.position_y = game_state.get("player_position", (self.player_ball.position_x, self.player_ball.position_y))
            self.enemy_balls = [EnemyBall(size=5, position_x=x, position_y=y) for x, y in game_state.get("enemy_positions", [])]
            self.is_game_over = game_state.get("is_game_over", self.is_game_over)