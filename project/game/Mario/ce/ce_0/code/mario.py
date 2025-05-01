import pygame

class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
        self.width = 50
        self.height = 50
        self.velocity = 5
        self.jump_height = 10
        self.is_jumping = False
        self.jump_count = self.jump_height

    def move_left(self):
        self.x -= self.velocity

    def move_right(self):
        self.x += self.velocity

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True

    def update(self):
        if self.is_jumping:
            if self.jump_count >= -self.jump_height:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = self.jump_height

    def hit_block(self):
        # Logic for hitting a block
        pass

    def collect_mushroom(self):
        self.score += 1

    def touch_flagpole(self):
        # Logic for touching the flagpole
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))  # Draw Mario