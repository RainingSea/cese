class TravelTipManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.tips = self.load_tips()

    def load_tips(self) -> dict:
        tips = {}
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    destination, tip = line.strip().split('|')
                    if destination not in tips:
                        tips[destination] = []
                    tips[destination].append(tip)
        except FileNotFoundError:
            pass
        return tips

    def add_tip(self, destination: str, tips: str) -> None:
        if destination not in self.tips:
            self.tips[destination] = []
        self.tips[destination].append(tips)
        with open(self.file_path, 'a') as file:
            file.write(f"{destination}|{tips}\n")

    def get_tips(self, destination: str) -> list:
        return self.tips.get(destination, [])

    def search_tips(self, query: str) -> list:
        results = []
        for destination, tips in self.tips.items():
            for tip in tips:
                if query.lower() in tip.lower():
                    results.append((destination, tip))
        return results