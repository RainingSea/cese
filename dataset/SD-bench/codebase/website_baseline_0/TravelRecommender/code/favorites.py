class Favorites:
    def __init__(self, user: str):
        self.user = user
        self.destinations = self.load_favorites()

    def load_favorites(self):
        favorites = []
        try:
            with open('favorites.txt', 'r') as file:
                for line in file:
                    user, destination = line.strip().split('|')
                    if user == self.user:
                        favorites.append(destination)
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return favorites

    def save(self):
        with open('favorites.txt', 'a') as file:
            for destination in self.destinations:
                file.write(f"{self.user}|{destination}\n")