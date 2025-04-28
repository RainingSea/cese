class TipGenerator:
    def __init__(self):
        self.tips = {}

    def generate_tips(self, destination: str, interests: list) -> str:
        relevant_tips = []
        for interest in interests:
            if destination in self.tips and interest in self.tips[destination]:
                relevant_tips.append(self.tips[destination][interest])
        return relevant_tips if relevant_tips else ["No tips available for this destination and interests."]

    def load_tips(self) -> None:
        try:
            with open('tips.txt', 'r') as file:
                for line in file:
                    destination, tip = line.strip().split(':')
                    if destination not in self.tips:
                        self.tips[destination] = {}
                    self.tips[destination][tip] = tip
        except FileNotFoundError:
            pass