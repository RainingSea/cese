class Note:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def save(self, username: str) -> bool:
        with open(f'notes_{username}.txt', 'a') as file:
            file.write(f'{self.title}:{self.content}\n')
        return True

    def delete(self, username: str) -> bool:
        notes = []
        with open(f'notes_{username}.txt', 'r') as file:
            notes = [line.strip() for line in file]
        notes.pop(self.title)  # Assuming title is unique
        with open(f'notes_{username}.txt', 'w') as file:
            for note in notes:
                file.write(note + '\n')
        return True

    def edit(self, new_title: str, new_content: str) -> bool:
        self.title = new_title
        self.content = new_content
        return True