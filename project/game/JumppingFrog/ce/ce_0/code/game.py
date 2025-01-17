import pygame
import random

class Frog:
    def __init__(self, x: int, y: int, jump_height: int):
        self.x = x
        self.y = y
        self.jump_height = jump_height
        self.velocity = 0
        self.on_ground = True

    def move_left(self) -> None:
        self.x -= 5

    def move_right(self) -> None:
        self.x += 5

    def jump(self) -> None:
        if self.on_ground:
            self.velocity = -self.jump_height
            self.on_ground = False

    def update_position(self) -> None:
        self.y += self.velocity
        self.velocity += 0.5  # Gravity effect
        if self.y >= 400:  # Assuming ground level
            self.y = 400
            self.on_ground = True
            self.velocity = 0

class Platform:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def is_colliding(self, frog: Frog) -> bool:
        return (frog.x > self.x and frog.x < self.x + self.width and
                frog.y + 20 > self.y and frog.y < self.y + self.height)

class Game:
    def __init__(self):
        self.frog = Frog(100, 400, 15)
        self.platforms = [Platform(random.randint(0, 400), random.randint(100, 300), 100, 10) for _ in range(5)]
        self.score = 0
        self.timer = 0

    def start(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Jumping Frog")
        self.clock = pygame.time.Clock()
        self.run_game()

    def run_game(self) -> None:
        running = True
        while running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.frog.move_left()
        if keys[pygame.K_RIGHT]:
            self.frog.move_right()
        if keys[pygame.K_SPACE]:
            self.frog.jump()

    def update(self) -> None:
        self.frog.update_position()
        for platform in self.platforms:
            if platform.is_colliding(self.frog):
                self.frog.y = platform.y - 20  # Place frog on top of the platform
                self.frog.on_ground = True
                self.frog.velocity = 0

    def draw(self) -> None:
        self.screen.fill((0, 0, 255))  # Fill with water color
        for platform in self.platforms:
            pygame.draw.rect(self.screen, (139, 69, 19), (platform.x, platform.y, platform.width, platform.height))
        pygame.draw.rect(self.screen, (0, 255, 0), (self.frog.x, self.frog.y, 20, 20))  # Draw frog
        pygame.display.flip()

    def save_data(self) -> None:
        with open('game_data.txt', 'a') as file:
            file.write(f"{self.score},{self.timer}\n")