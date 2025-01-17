import pygame
import time
from memory_game import MemoryGame

def main():
    pygame.init()
    game = MemoryGame()
    game.restart_game()
    
    # Example setup for the game with 8 pairs
    faces = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    game.cards = [Card(face) for face in faces for _ in range(2)]
    game.shuffle_cards()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Memory Game')
    clock = pygame.time.Clock()

    running = True
    first_card_index = None
    second_card_index = None
    start_time = None

    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and game.game_active:
                if start_time is None:
                    start_time = time.time()
                
                mouse_x, mouse_y = event.pos
                card_index = (mouse_y // 100) * 4 + (mouse_x // 100)  # Assuming 4 columns

                if game.flip_card(card_index):
                    if first_card_index is None:
                        first_card_index = card_index
                    elif second_card_index is None:
                        second_card_index = card_index
                        time_taken = time.time() - start_time
                        if not game.check_match(game.cards[first_card_index], game.cards[second_card_index]):
                            pygame.time.delay(1000)  # Show mismatch for a second
                            game.cards[first_card_index].flip()
                            game.cards[second_card_index].flip()
                        else:
                            game.update_score(time_taken)
                        first_card_index = None
                        second_card_index = None
                        start_time = None

        for index, card in enumerate(game.cards):
            color = (0, 0, 0) if card.is_flipped else (200, 200, 200)
            pygame.draw.rect(screen, color, (index % 4 * 100, index // 4 * 100, 100, 100))
            if card.is_flipped:
                font = pygame.font.Font(None, 74)
                text = font.render(card.face, True, (255, 0, 0))
                screen.blit(text, (index % 4 * 100 + 25, index // 4 * 100 + 25))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()