from game import Game

def main() -> None:
    game = Game('shapes.txt', 'patterns.txt')
    game.run()

if __name__ == "__main__":
    main()