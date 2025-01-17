import pygame
from menu import Menu
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Color Link Puzzle')
    
    menu = Menu(screen)
    game = Game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game.start_game()
                    # Placeholder for game loop logic

        menu.show_main_menu()

    pygame.quit()

if __name__ == "__main__":
    main()