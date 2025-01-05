class Note:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def create(self, title: str, content: str) -> bool:
        with open('notes.txt', 'a') as f:
            f.write(f"{title}|{content}\n")
        return True

    def edit(self, title: str, content: str) -> bool:
        # Implementation for editing a note
        return True

    def delete(self, title: str) -> bool:
        # Implementation for deleting a note
        return True

    def search(self, title: str) -> list:
        # Implementation for searching a note
        return []