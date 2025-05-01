import pygame

class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 5  # Mario's speed
        self.width = 50
        self.height = 50
        self.is_jumping = False
        self.jump_count = 10  # Control jump height
        self.score = 0  # Initialize score

    def move_left(self):
        self.x -= self.velocity  # Move Mario to the left

    def move_right(self):
        self.x += self.velocity  # Move Mario to the right

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True  # Set jumping state

    def update(self):
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1 if self.jump_count >= 0 else -1
                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10  # Reset jump count

    def collect_mushroom(self):
        self.score += 1000  # Increase score by 1000

    def touch_enemy(self):
        self.score -= 5  # Decrease score when touching an enemy

    def hit_block(self):
        self.score += 100  # Increase score by 100

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))