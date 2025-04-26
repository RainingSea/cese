class TravelTipManager:
    def __init__(self):
        self.tips = self.load_tips()

    def load_tips(self):
        tips = {}
        try:
            with open('travel_tips.txt', 'r') as file:
                for line in file:
                    destination, tip = line.strip().split(',')
                    if destination not in tips:
                        tips[destination] = []
                    tips[destination].append(tip)
        except FileNotFoundError:
            pass
        return tips

    def addTip(self, destination: str, tips: str) -> None:
        if destination not in self.tips:
            self.tips[destination] = []
        self.tips[destination].append(tips)
        with open('travel_tips.txt', 'a') as file:
            file.write(f"{destination},{tips}\n")

    def getTips(self, destination: str) -> str:
        return self.tips.get(destination, [])