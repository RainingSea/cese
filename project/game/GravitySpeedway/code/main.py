import pygame
from game import Game, Player, Vehicle, ScoreManager, Settings

def main() -> None:
    pygame.init()
    game = Game()
    game.score_manager.load_scores()
    settings = Settings()
    settings.load_settings()

    # Initialize player with a default vehicle
    default_vehicle = Vehicle("Speedster", 0.8, 1.5, 200)
    game.player = Player(default_vehicle)

    # Load track with sample obstacles
    sample_obstacles = [(1.0, 1.0), (2.0, 2.0), (3.0, 3.0)]
    game.track.load_track(sample_obstacles)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic and rendering would go here

    pygame.quit()

if __name__ == "__main__":
    main()