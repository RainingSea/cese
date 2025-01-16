from TravelTipManager import TravelTip

class FavoritesManager:
    def __init__(self, favorites_file: str):
        self.favorites_file = favorites_file

    def save_favorite(self, username: str, tip: TravelTip):
        with open(self.favorites_file, 'a') as f:
            f.write(f"{username}|{tip.destination}|{tip.customs}|{tip.safety_tips}|{tip.transportation}|{tip.etiquette}|{tip.attractions}\n")

    def load_favorites(self, username: str) -> list:
        favorites = []
        try:
            with open(self.favorites_file, 'r') as f:
                for line in f:
                    data = line.strip().split('|')
                    if data[0] == username:
                        favorites.append(data[1:])  # Exclude username
        except FileNotFoundError:
            pass
        return favorites