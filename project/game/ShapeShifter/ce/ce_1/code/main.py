from game import Game

def main() -> None:
    game = Game()
    game.load_shapes()
    game.load_patterns()
    game.run()

if __name__ == "__main__":
    main()