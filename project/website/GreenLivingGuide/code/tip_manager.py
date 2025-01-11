import os

class TipManager:
    def __init__(self):
        self.tips = self.load_tips()

    def load_tips(self) -> list:
        """Load tips from the tips.txt file."""
        tips = []
        try:
            with open('tips.txt', 'r') as file:
                tips = [line.strip() for line in file]
        except FileNotFoundError:
            pass
        return tips

    def save_tips(self) -> None:
        """Save tips to the tips.txt file."""
        with open('tips.txt', 'w') as file:
            for tip in self.tips:
                file.write(f"{tip}\n")

    def add_tip(self, tip: str) -> None:
        """Add a new tip and save to the file."""
        self.tips.append(tip)
        self.save_tips()

    def get_tips(self) -> list:
        """Retrieve all tips."""
        return self.tips

    def verify_tip_data(self) -> bool:
        """Verify if tip data is correctly saved."""
        current_tips = self.load_tips()
        return current_tips == self.tips