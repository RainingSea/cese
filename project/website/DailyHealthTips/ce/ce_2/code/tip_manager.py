class TipManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.tips = self.load_tips()

    def get_current_tip(self) -> str:
        return self.tips[0] if self.tips else "No tips available."

    def get_previous_tip(self, current_index: int) -> str:
        if current_index > 0:
            return self.tips[current_index - 1]
        return "No previous tip."

    def get_next_tip(self, current_index: int) -> str:
        if current_index < len(self.tips) - 1:
            return self.tips[current_index + 1]
        return "No next tip."

    def load_tips(self) -> list:
        tips = []
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    tips.append(line.strip())
        except FileNotFoundError:
            pass
        return tips