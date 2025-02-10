class DailyTip:
    def __init__(self, tip: str, date: str):
        self.tip = tip
        self.date = date

    def save(self):
        with open('daily_tips.txt', 'a') as f:
            f.write(f"{self.tip}|{self.date}\n")

    @staticmethod
    def load_all() -> list:
        tips = []
        with open('daily_tips.txt', 'r') as f:
            for line in f:
                tip, date = line.strip().split('|')
                tips.append(DailyTip(tip, date))
        return tips