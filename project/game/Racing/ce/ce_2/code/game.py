import pygame
from obstacle import Obstacle

class Game:
    def __init__(self):
        self.speed = 0
        self.distance = 0
        self.lane = 1
        self.obstacles = []
        self.running = True
        self.clock = pygame.time.Clock()

    def run_game(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Racing Game")

        while self.running:
            self.handle_input(pygame.event.get())
            self.update_obstacles()
            self.display_info(screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def update_obstacles(self):
        if len(self.obstacles) < 5:  # Limit the number of obstacles
            new_obstacle = Obstacle(random.randint(1, 3), random.randint(0, 600))
            self.obstacles.append(new_obstacle)

        for obstacle in self.obstacles:
            obstacle.move()

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.lane > 0:
                    self.lane -= 1
                if event.key == pygame.K_RIGHT and self.lane < 2:
                    self.lane += 1

    def check_collision(self):
        # Collision detection logic will go here
        pass

    def display_info(self, screen):
        screen.fill((255, 255, 255))  # Clear the screen
        font = pygame.font.Font(None, 36)
        text_speed = font.render(f'Speed: {self.speed}', True, (0, 0, 0))
        text_distance = font.render(f'Distance: {self.distance}', True, (0, 0, 0))
        screen.blit(text_speed, (600, 10))
        screen.blit(text_distance, (600, 50))