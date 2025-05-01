import pygame
from mario import Mario
from block import Block
from mushroom import Mushroom
from enemy import Enemy
from score import Score

class Game:
    def __init__(self):
        self.mario = Mario()
        self.block = Block()
        self.mushroom = Mushroom()
        self.enemy = Enemy()
        self.score = Score()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True

    def start_game(self):
        while self.running:
            self.update()
            self.check_collisions()
            self.render()
            self.clock.tick(60)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.mario.update(event)

    def check_collisions(self):
        if self.mario.rect.colliderect(self.block.rect):
            self.mario.hit_block()
            self.block.release_mushroom()

        if self.mario.rect.colliderect(self.enemy.rect):
            self.mario.touch_enemy()

        if self.mario.rect.colliderect(self.mushroom.rect):
            self.mario.touch_mushroom()

        if self.mario.rect.colliderect(self.flagpole.rect):
            self.mario.reach_flagpole()