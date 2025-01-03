class Tip:
    def __init__(self, content: str):
        self.content = content

    def save(self) -> None:
        with open('tips.txt', 'a') as file:
            file.write(f"{self.content}\n")

    @staticmethod
    def load_tips() -> list:
        tips = []
        with open('tips.txt', 'r') as file:
            for line in file:
                content = line.strip()
                tips.append(Tip(content))
        return tips