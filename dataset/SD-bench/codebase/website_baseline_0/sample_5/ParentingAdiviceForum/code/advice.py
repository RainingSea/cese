class Advice:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self) -> None:
        """Save the advice to the advice.txt file."""
        with open('advice.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}\n")