class TipManager:
    def __init__(self, filename):
        self.tips = self.load_tips(filename)

    def load_tips(self, filename):
        with open(filename, 'r') as file:
            return [line.strip() for line in file]

    def get_current_tip(self):
        return self.tips[0] if self.tips else "No tips available."

    def get_previous_tip(self, current_index):
        if current_index > 0:
            return self.tips[current_index - 1]
        return None

    def get_next_tip(self, current_index):
        if current_index < len(self.tips) - 1:
            return self.tips[current_index + 1]
        return None

    def search_tips(self, query):
        return [tip for tip in self.tips if query.lower() in tip.lower()]