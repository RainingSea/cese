class Tip:
    def __init__(self, content: str) -> None:
        self.content = content

    def save(self) -> None:
        with open('tips.txt', 'a') as file:
            file.write(f"{self.content}\n")

    @staticmethod
    def load_tips() -> list:
        tips = []
        try:
            with open('tips.txt', 'r') as file:
                for line in file:
                    tips.append(line.strip())
        except FileNotFoundError:
            pass
        return tips