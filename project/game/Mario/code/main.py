from game import Game

def main():
    game = Game()
    game.load_game()  # Load game state at the start
    game.run()

if __name__ == "__main__":
    main()