import pygame
import random

class Player:
    def __init__(self):
        self.size = self.load_player_size()
        self.position = [400, 300]  # Initialize player position at the center of the screen

    def load_player_size(self) -> int:
        try:
            with open('player_data.txt', 'r') as file:
                return int(file.readline().strip())
        except FileNotFoundError:
            return 20  # Default size if file not found

    def move(self, direction: str):
        keys = pygame.key.get_pressed()
        if direction == "UP" and self.position[1] - self.size > 0:
            self.position[1] -= 5
        elif direction == "DOWN" and self.position[1] + self.size < 600:
            self.position[1] += 5
        elif direction == "LEFT" and self.position[0] - self.size > 0:
            self.position[0] -= 5
        elif direction == "RIGHT" and self.position[0] + self.size < 800:
            self.position[0] += 5

    def grow(self):
        self.size += 5  # Increase size when consuming an enemy ball

class Enemy:
    def __init__(self, size: int, position: tuple):
        self.size = size
        self.position = list(position)

    @staticmethod
    def load_enemies() -> list:
        enemies = []
        try:
            with open('enemy_data.txt', 'r') as file:
                for line in file:
                    size, x, y = map(int, line.strip().split('|'))
                    enemies.append(Enemy(size, (x, y)))
        except FileNotFoundError:
            # Default enemies if file not found
            for _ in range(5):
                size = random.randint(10, 30)
                position = (random.randint(0, 800), random.randint(0, 600))
                enemies.append(Enemy(size, position))
        return enemies

    def move(self):
        # Randomly choose direction for movement
        direction_x = random.choice([-1, 1])
        direction_y = random.choice([-1, 1])
        self.position[0] += direction_x * random.randint(1, 3)
        self.position[1] += direction_y * random.randint(1, 3)
        # Ensure position stays within bounds
        self.position[0] = max(0, min(self.position[0], 800))
        self.position[1] = max(0, min(self.position[1], 600))

class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = Enemy.load_enemies()  # Load enemies from file
        self.running = True

    def start(self):
        while self.running:
            self.update()
            self.check_collisions()
            self.end_game()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.move("UP")
                elif event.key == pygame.K_DOWN:
                    self.player.move("DOWN")
                elif event.key == pygame.K_LEFT:
                    self.player.move("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.player.move("RIGHT")
        for enemy in self.enemies:
            enemy.move()  # Update enemy positions

    def check_collisions(self):
        for enemy in self.enemies:
            if self.check_collision(self.player, enemy):
                if self.player.size > enemy.size:
                    self.player.grow()
                    self.enemies.remove(enemy)

    def check_collision(self, player: Player, enemy: Enemy) -> bool:
        return (player.position[0] < enemy.position[0] + enemy.size and
                player.position[0] + player.size > enemy.position[0] and
                player.position[1] < enemy.position[1] + enemy.size and
                player.position[1] + player.size > enemy.position[1])

    def end_game(self):
        # Logic to end the game
        self.running = False  # For demonstration purposes, end the game immediately
        self.save_game_state()

    def save_game_state(self):
        with open("game_data.txt", "w") as file:
            file.write(f"Player Size: {self.player.size}\n")
            file.write(f"Player Position: {self.player.position}\n")
            file.write(f"Enemies Remaining: {len(self.enemies)}\n")