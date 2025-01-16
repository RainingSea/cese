from models import TravelTip

class TravelTipManager:
    def __init__(self):
        self.tips = []

    def load_tips(self, file_path: str):
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split('|')
                tip = TravelTip(*data)
                self.tips.append(tip)

    def get_tips(self, destination: str, interests: list) -> list:
        recommended_tips = []
        for tip in self.tips:
            if tip.destination.lower() == destination.lower() and any(interest in tip.interests for interest in interests):
                recommended_tips.append(tip)
        return recommended_tips