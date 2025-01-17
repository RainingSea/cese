import json

class FileManager:
    @staticmethod
    def save_progress(player: Player) -> None:
        with open('progress.txt', 'a') as f:
            f.write(f"{player.position}|{player.completion_time}\n")

    @staticmethod
    def load_mazes() -> list:
        with open('mazes.txt', 'r') as f:
            return [line.strip() for line in f.readlines()]