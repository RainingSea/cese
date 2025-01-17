import pygame

class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
        self.is_jumping = False
        self.jump_height = 10
        self.gravity = 1
        self.jump_velocity = 0

    def move_left(self):
        self.x -= 5  # Move left by 5 pixels

    def move_right(self):
        self.x += 5  # Move right by 5 pixels

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = self.jump_height

    def update(self):
        if self.is_jumping:
            self.y -= self.jump_velocity
            self.jump_velocity -= self.gravity
            if self.jump_velocity < 0:
                self.is_jumping = False
                self.jump_velocity = 0

    def hit_block(self):
        # Logic for hitting a block
        pass

    def touch_mushroom(self):
        self.score += 100  # Increment score by 100

    def touch_enemy(self):
        self.score -= 50  # Decrement score by 50

    def reach_flagpole(self):
        # Logic for reaching the flagpole
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 50, 50))  # Draw Mario as a red square