class Note:
    def __init__(self, title: str, content: str, user: str):
        self.title = title
        self.content = content
        self.user = user

    def save(self):
        """Save the note to the notes.txt file."""
        with open('notes.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}|{self.user}\n")

    def to_string(self) -> str:
        """Return a string representation of the note."""
        return f"{self.title}|{self.content}|{self.user}"