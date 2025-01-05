import os

class FileManager:
    def read_users(self) -> list:
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as f:
            return [line.strip().split('|') for line in f]

    def write_users(self, users: list) -> None:
        with open('users.txt', 'w') as f:
            for user in users:
                f.write(f"{user[0]}|{user[1]}\n")

    def read_notes(self) -> list:
        if not os.path.exists('notes.txt'):
            return []
        with open('notes.txt', 'r') as f:
            return [dict(zip(['title', 'content'], line.strip().split('|'))) for line in f]

    def write_notes(self, notes: list) -> None:
        with open('notes.txt', 'w') as f:
            for note in notes:
                f.write(f"{note['title']}|{note['content']}\n")