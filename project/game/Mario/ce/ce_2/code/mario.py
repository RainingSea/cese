import pygame

class Mario:
    def __init__(self):
        self.position = pygame.Vector2(100, 500)
        self.score = 0
        self.rect = pygame.Rect(self.position.x, self.position.y, 50, 50)

    def move_left(self):
        self.position.x -= 5

    def move_right(self):
        self.position.x += 5

    def jump(self):
        self.position.y -= 10

    def hit_block(self):
        self.score += 10

    def touch_mushroom(self):
        self.score += 20

    def touch_enemy(self):
        self.score -= 5

    def reach_flagpole(self):
        self.score += 50

    def update(self, event):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_left()
        if keys[pygame.K_RIGHT]:
            self.move_right()
        if keys[pygame.K_SPACE]:
            self.jump()
        self.rect.topleft = (self.position.x, self.position.y)