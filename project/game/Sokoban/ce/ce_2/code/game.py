import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction):
        if direction == 'up':
            self.y -= 1
        elif direction == 'down':
            self.y += 1
        elif direction == 'left':
            self.x -= 1
        elif direction == 'right':
            self.x += 1

class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                rect = pygame.Rect(x * 40, y * 40, 40, 40)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)

class Game:
    def __init__(self):
        self.player = Player(1, 1)
        self.boxes = [Box(2, 2), Box(3, 3)]
        self.grid = Grid(10, 10)
        self.screen = pygame.display.set_mode((400, 400))

    def load_game_state(self, file):
        with open(file, 'r') as f:
            data = f.read().strip().split('\n')
            player_pos = data[0].split(',')
            self.player.x = int(player_pos[0])
            self.player.y = int(player_pos[1])
            boxes_data = data[1].split(';')
            self.boxes = [Box(int(box.split(',')[0]), int(box.split(',')[1])) for box in boxes_data]

    def save_game_state(self, file):
        with open(file, 'w') as f:
            f.write(f"{self.player.x},{self.player.y}\n")
            boxes_str = ';'.join([f"{box.x},{box.y}" for box in self.boxes])
            f.write(boxes_str)

    def move_player(self, direction):
        original_x = self.player.x
        original_y = self.player.y
        self.player.move(direction)
        
        # Check for box movement
        for box in self.boxes:
            if box.x == self.player.x and box.y == self.player.y:
                if direction == 'up':
                    box.y -= 1
                elif direction == 'down':
                    box.y += 1
                elif direction == 'left':
                    box.x -= 1
                elif direction == 'right':
                    box.x += 1
        
        # Check boundaries
        if self.player.x < 0 or self.player.x >= self.grid.width or self.player.y < 0 or self.player.y >= self.grid.height:
            self.player.x = original_x
            self.player.y = original_y

    def render(self):
        self.screen.fill((255, 255, 255))
        self.grid.draw(self.screen)
        pygame.draw.rect(self.screen, (0, 0, 255), (self.player.x * 40, self.player.y * 40, 40, 40))
        for box in self.boxes:
            pygame.draw.rect(self.screen, (255, 0, 0), (box.x * 40, box.y * 40, 40, 40))
        pygame.display.flip()