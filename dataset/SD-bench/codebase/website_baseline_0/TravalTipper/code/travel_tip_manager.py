class TravelTip:
    def __init__(self, destination: str, duration: str, interests: list):
        self.destination = destination
        self.duration = duration
        self.interests = interests

    def generate_tips(self):
        return [f"Tip for {self.destination}: Explore for {self.duration} days focusing on {', '.join(self.interests)}."]


class TravelTipManager:
    def load_tips(self):
        tips = []
        try:
            with open('tips.txt', 'r') as file:
                for line in file:
                    destination, duration, interests = line.strip().split('|')
                    tips.append(TravelTip(destination, duration, interests.split(',')))
        except FileNotFoundError:
            pass
        return tips

    def save_tip(self, tip: TravelTip):
        with open('tips.txt', 'a') as file:
            file.write(f"{tip.destination}|{tip.duration}|{','.join(tip.interests)}\n")