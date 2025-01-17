import pygame
from obstacle import Obstacle

class Game:
    def __init__(self):
        self.speed = 0
        self.distance = 0
        self.obstacles = []
        self.lane_position = 0
        self.running = True
        self.load_game_state()

    def run_game(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Racing Game")
        clock = pygame.time.Clock()

        while self.running:
            self.handle_input()
            self.update_obstacles()
            self.draw_elements(screen)
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

    def update_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.move()
            if obstacle.position > 600:  # Remove off-screen obstacles
                self.obstacles.remove(obstacle)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.speed += 5
                elif event.key == pygame.K_DOWN:
                    self.speed -= 5
                self.distance += self.speed // 30  # Update distance based on speed

    def draw_elements(self, screen):
        screen.fill((255, 255, 255))  # Clear the screen
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, (255, 0, 0), (obstacle.lane_position, obstacle.position, 50, 50))  # Draw obstacles
        # Draw the car (stationary)
        pygame.draw.rect(screen, (0, 0, 255), (self.lane_position, 500, 50, 100))  # Draw the car
        # Display speed and distance
        font = pygame.font.Font(None, 36)
        text = font.render(f'Speed: {self.speed} Distance: {self.distance}', True, (0, 0, 0))
        screen.blit(text, (600, 10))

    def save_game_state(self):
        with open('game_data.txt', 'w') as f:
            f.write(f"{self.speed}|{self.distance}|{len(self.obstacles)}\n")
            for obstacle in self.obstacles:
                f.write(f"{obstacle.type}|{obstacle.position}\n")

    def load_game_state(self):
        try:
            with open('game_data.txt', 'r') as f:
                lines = f.readlines()
                if lines:
                    first_line = lines[0].strip().split('|')
                    self.speed = int(first_line[0])
                    self.distance = int(first_line[1])
                    num_obstacles = int(first_line[2])
                    for line in lines[1:num_obstacles + 1]:
                        type, position = map(int, line.strip().split('|'))
                        self.obstacles.append(Obstacle(type, position))
        except FileNotFoundError:
            pass  # If file doesn't exist, start with default values