from game import Game

def main() -> None:
    game = Game()
    game.start()
    while True:
        game.update()
        game.render()

if __name__ == "__main__":
    main()