class FileManager:
    def read_users(self) -> list:
        try:
            with open('users.txt', 'r') as f:
                return f.read().strip().split('\n')
        except FileNotFoundError:
            return []

    def write_users(self, users: list) -> None:
        with open('users.txt', 'w') as f:
            for user in users:
                f.write(f"{user}\n")

    def read_notes(self) -> list:
        try:
            with open('notes.txt', 'r') as f:
                return [line.strip().split('|') for line in f.readlines()]
        except FileNotFoundError:
            return []

    def write_notes(self, notes: list) -> None:
        with open('notes.txt', 'w') as f:
            for title, content in notes:
                f.write(f"{title}|{content}\n")