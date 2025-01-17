from game import Game

def main() -> str:
    game = Game()
    game.start_game()
    return "Game started"

if __name__ == "__main__":
    main()