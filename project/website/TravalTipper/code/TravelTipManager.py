class TravelTip:
    def __init__(self, destination: str, customs: str, safety_tips: str, transportation: str, etiquette: str, attractions: str):
        self.destination = destination
        self.customs = customs
        self.safety_tips = safety_tips
        self.transportation = transportation
        self.etiquette = etiquette
        self.attractions = attractions

class TravelTipManager:
    def __init__(self, tips_file: str):
        self.tips_file = tips_file
        self.tips = self.load_tips()

    def load_tips(self) -> list:
        tips = []
        try:
            with open(self.tips_file, 'r') as f:
                for line in f:
                    data = line.strip().split('|')
                    if len(data) == 6:
                        tip = TravelTip(*data)
                        tips.append(tip)
        except FileNotFoundError:
            pass
        return tips

    def generate_tips(self, destination: str, interests: list) -> list:
        recommended_tips = []
        for tip in self.tips:
            if tip.destination.lower() == destination.lower():
                if any(interest in tip.attractions for interest in interests):
                    recommended_tips.append(tip)
        return recommended_tips

    def get_tip_by_destination(self, destination: str) -> TravelTip:
        for tip in self.tips:
            if tip.destination.lower() == destination.lower():
                return tip
        return None

    def search_tips(self, search_query: str) -> list:
        filtered_tips = []
        for tip in self.tips:
            if search_query.lower() in tip.destination.lower() or any(search_query.lower() in attr.lower() for attr in [tip.customs, tip.safety_tips, tip.transportation, tip.etiquette, tip.attractions]):
                filtered_tips.append(tip)
        return filtered_tips