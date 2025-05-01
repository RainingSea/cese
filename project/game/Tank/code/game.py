import pygame
import random

class Player:
    def __init__(self) -> None:
        self.health = 100
        self.position_x = 0
        self.position_y = 0

    def move(self, direction: str) -> None:
        if direction == 'UP' and self.position_y > 0:
            self.position_y -= 1
        elif direction == 'DOWN' and self.position_y < 19:
            self.position_y += 1
        elif direction == 'LEFT' and self.position_x > 0:
            self.position_x -= 1
        elif direction == 'RIGHT' and self.position_x < 19:
            self.position_x += 1

    def fire(self) -> 'Bullet':
        return Bullet(self.position_x, self.position_y, -1)  # Example direction

class Enemy:
    def __init__(self) -> None:
        self.health = 100
        self.position_x = random.randint(0, 19)
        self.position_y = random.randint(0, 19)

    def shoot(self) -> 'Bullet':
        return Bullet(self.position_x, self.position_y, 1)  # Example direction

class Bullet:
    def __init__(self, position_x: int, position_y: int, direction: int) -> None:
        self.position_x = position_x
        self.position_y = position_y
        self.direction = direction

    def move(self) -> None:
        self.position_y += self.direction

class Game:
    def __init__(self) -> None:
        self.player = Player()
        self.enemies = [Enemy() for _ in range(5)]
        self.bullets = []
        self.score = 0
        self.player_health = self.player.health

    def start_game(self) -> None:
        self.load_game_data()
        self.game_loop()

    def game_loop(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        bullet = self.player.fire()
                        self.bullets.append(bullet)
                    elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                        direction = pygame.key.name(event.key).upper()
                        self.player.move(direction)

            self.update()
            self.check_collisions()
            self.render()
            self.check_game_end_conditions()

        self.save_game_data()

    def update(self) -> None:
        for bullet in self.bullets:
            bullet.move()

    def render(self) -> None:
        # Placeholder for rendering logic
        pass

    def check_collisions(self) -> None:
        for bullet in self.bullets[:]:  # Iterate over a copy of the list
            for enemy in self.enemies[:]:  # Iterate over a copy of the list
                if bullet.position_x == enemy.position_x and bullet.position_y == enemy.position_y:
                    enemy.health -= 100  # Assuming bullet destroys enemy
                    self.calculate_score(enemy)
                    self.bullets.remove(bullet)
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)

        # Check for player getting hit by enemy bullets
        for enemy in self.enemies:
            if enemy.health > 0:  # Only check for active enemies
                enemy_bullet = enemy.shoot()
                if enemy_bullet.position_x == self.player.position_x and enemy_bullet.position_y == self.player.position_y:
                    self.player.health -= 10  # Damage to player
                    if self.player.health <= 0:
                        self.end_game()  # End game if player health is zero

    def check_game_end_conditions(self) -> None:
        if all(enemy.health <= 0 for enemy in self.enemies) or self.player.health <= 0:
            self.end_game()  # Call game ending process

    def calculate_score(self, enemy: Enemy) -> None:
        if enemy.health <= 0:
            self.score += 200  # Increase score for destroyed enemy tank

    def load_game_data(self) -> None:
        try:
            with open('game_data.txt', 'r') as f:
                data = f.read().splitlines()
                self.player.position_x, self.player.position_y = map(int, data[0].split('|'))
                self.score = int(data[1].split(': ')[1])  # Load score
                self.player.health = int(data[2].split(': ')[1])  # Load player health
                enemy_count = int(data[3])  # Load enemies count
                self.enemies = [Enemy() for _ in range(enemy_count)]
        except FileNotFoundError:
            self.score = 0
            self.player.health = 100
            self.enemies = [Enemy() for _ in range(5)]  # Default enemies if file not found

    def save_game_data(self) -> None:
        with open('game_data.txt', 'w') as f:
            f.write(f"{self.player.position_x}|{self.player.position_y}\n")
            f.write(f"Score: {self.score}\n")
            f.write(f"Health: {self.player.health}\n")
            f.write(f"{len(self.enemies)}\n")

    def end_game(self) -> None:
        # Placeholder for game ending logic
        pass