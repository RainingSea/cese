class TipManager:
    def __init__(self):
        self.tips = []
        self.load_tips()

    def load_tips(self) -> None:
        try:
            with open('tips.txt', 'r') as file:
                self.tips = [line.strip() for line in file]
        except FileNotFoundError:
            pass

    def get_current_tip(self) -> str:
        if self.tips:
            return self.tips[0]
        return "No tips available."

    def get_previous_tip(self) -> str:
        if len(self.tips) > 1:
            return self.tips[1]
        return "No previous tip available."

    def get_next_tip(self) -> str:
        if len(self.tips) > 2:
            return self.tips[2]
        return "No next tip available."

    def search_tips(self, query: str) -> list:
        return [tip for tip in self.tips if query.lower() in tip.lower()]

    def load_feedback(self) -> None:
        pass  # Placeholder for future implementation

    def submit_feedback(self, feedback: str) -> None:
        with open('feedback.txt', 'a') as file:
            file.write(f"{feedback}\n")