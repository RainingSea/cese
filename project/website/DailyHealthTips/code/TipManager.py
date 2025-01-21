class TipManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.tips = self.load_tips()

    def get_current_tip(self, index: int) -> str:
        """Returns the current tip based on the index."""
        return self.tips[index] if 0 <= index < len(self.tips) else "No tips available."

    def get_previous_tip(self, current_index: int) -> str:
        """Returns the previous tip based on the current index."""
        if current_index > 0:
            return self.tips[current_index - 1]
        return "No previous tip."

    def get_next_tip(self, current_index: int) -> str:
        """Returns the next tip based on the current index."""
        if current_index < len(self.tips) - 1:
            return self.tips[current_index + 1]
        return "No next tip."

    def load_tips(self) -> list:
        """Loads tips from the specified file."""
        tips = []
        try:
            with open(self.filename, 'r') as file:
                tips = [line.strip() for line in file]
        except FileNotFoundError:
            pass
        return tips

    def search_tips(self, query: str) -> list:
        """Searches for tips containing the query string."""
        return [tip for tip in self.tips if query.lower() in tip.lower()]

    def get_all_tips(self) -> list:
        """Returns all tips."""
        return self.tips

    def add_tip(self, tip: str) -> bool:
        """Adds a new tip to the list and saves it to the file."""
        self.tips.append(tip)
        with open(self.filename, 'a') as file:
            file.write(f"{tip}\n")
        return True