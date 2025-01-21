class Tip:
    """Represents an eco-friendly tip."""
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self):
        """Saves the tip to a file."""
        with open('tips.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}\n")

    @staticmethod
    def load_all():
        """Loads all tips from the file."""
        tips = []
        with open('tips.txt', 'r') as file:
            for line in file:
                title, content = line.strip().split('|')
                tips.append(Tip(title, content))
        return tips