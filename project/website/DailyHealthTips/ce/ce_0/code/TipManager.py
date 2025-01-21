class TipManager:
    def __init__(self, tips_file: str, feedback_file: str):
        self.tips_file = tips_file
        self.feedback_file = feedback_file
        self.load_tips()
        self.load_feedback()

    def load_tips(self):
        self.tips = []
        try:
            with open(self.tips_file, 'r') as file:
                self.tips = [line.strip() for line in file]
        except FileNotFoundError:
            pass

    def load_feedback(self):
        self.feedback = []
        try:
            with open(self.feedback_file, 'r') as file:
                self.feedback = [line.strip() for line in file]
        except FileNotFoundError:
            pass

    def get_daily_tip(self) -> str:
        return self.tips[0] if self.tips else "No tips available."

    def get_previous_tip(self, current_index: int) -> str:
        if current_index > 0:
            return self.tips[current_index - 1]
        return "No previous tip."

    def get_next_tip(self, current_index: int) -> str:
        if current_index < len(self.tips) - 1:
            return self.tips[current_index + 1]
        return "No next tip."

    def get_all_tips(self) -> list:
        return self.tips

    def search_tips(self, query: str) -> list:
        return [tip for tip in self.tips if query.lower() in tip.lower()]

    def submit_feedback(self, feedback: str) -> None:
        with open(self.feedback_file, 'a') as file:
            file.write(f"{feedback}\n")