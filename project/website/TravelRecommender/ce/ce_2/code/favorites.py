class Favorites:
    def __init__(self, username: str):
        self.username = username
        self.destinations = []

    def add(self, destination: str) -> None:
        with open('favorites.txt', 'a') as file:
            file.write(f"{self.username}|{destination}\n")

    def remove(self, destination: str) -> None:
        lines = []
        with open('favorites.txt', 'r') as file:
            lines = file.readlines()

        with open('favorites.txt', 'w') as file:
            for line in lines:
                if not (line.startswith(self.username) and destination in line):
                    file.write(line)

    def load(self, username: str) -> list:
        favorites = []
        with open('favorites.txt', 'r') as file:
            for line in file:
                fav_data = line.strip().split('|')
                if fav_data[0] == username:
                    favorites.append(fav_data[1])
        return favorites