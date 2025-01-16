class TravelTipManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.tips = self.load_tips()

    def get_tips(self, destination: str, interests: list) -> list:
        filtered_tips = [tip for tip in self.tips if tip['destination'] == destination and any(interest in tip['interests'] for interest in interests)]
        return filtered_tips

    def save_favorite(self, user: str, tip: str) -> bool:
        with open('favorites.txt', 'a') as file:
            file.write(f"{user}|{tip}\n")
        return True

    def load_tips(self) -> list:
        tips = []
        try:
            with open(self.filepath, 'r') as file:
                for line in file:
                    destination, interests = line.strip().split('|')
                    tips.append({'destination': destination, 'interests': interests.split(',')})
        except FileNotFoundError:
            pass
        return tips