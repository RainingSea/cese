import datetime

class TipManager:
    def __init__(self, tips_file='tips.txt'):
        self.tips_file = tips_file
        self._ensure_tips_exist()

    def _ensure_tips_exist(self):
        try:
            with open(self.tips_file, 'r') as f:
                pass
        except FileNotFoundError:
            self._create_sample_tips()

    def _create_sample_tips(self):
        sample_tips = [
            "1|2023-01-01|Drink at least 8 glasses of water daily",
            "2|2023-01-02|Get 7-8 hours of sleep each night",
            "3|2023-01-03|Take a 5-minute break every hour when working",
            "4|2023-01-04|Eat at least 5 servings of fruits and vegetables daily",
            "5|2023-01-05|Exercise for at least 30 minutes daily"
        ]
        with open(self.tips_file, 'w') as f:
            f.write('\n'.join(sample_tips))

    def _load_tips(self):
        with open(self.tips_file, 'r') as f:
            return [line.strip().split('|', 2) for line in f.readlines()]

    def get_current_tip(self):
        tips = self._load_tips()
        today = datetime.date.today().strftime("%Y-%m-%d")
        for tip in tips:
            if tip[1] == today:
                return tip[2]
        return tips[0][2] if tips else "No tips available"

    def get_next_tip(self, current_tip_id):
        tips = self._load_tips()
        if not tips:
            return None
        
        current_index = next((i for i, tip in enumerate(tips) if tip[0] == str(current_tip_id)), -1)
        if current_index == -1 or current_index >= len(tips) - 1:
            return None
        
        return tips[current_index + 1]

    def get_prev_tip(self, current_tip_id):
        tips = self._load_tips()
        if not tips:
            return None
        
        current_index = next((i for i, tip in enumerate(tips) if tip[0] == str(current_tip_id)), -1)
        if current_index <= 0:
            return None
        
        return tips[current_index - 1]

    def get_all_tips(self):
        return self._load_tips()

    def search_tips(self, query):
        if not query:
            return []
        tips = self._load_tips()
        return [tip for tip in tips if query.lower() in tip[2].lower()]