import os

class FileManager:
    def save_user_data(self, username: str, password: str) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")

    def load_user_data(self) -> dict:
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def save_note_data(self, username: str, title: str, content: str) -> None:
        with open(f'notes_{username}.txt', 'a') as f:
            f.write(f"{title}|{content}\n")

    def load_note_data(self, username: str) -> list:
        notes = []
        if os.path.exists(f'notes_{username}.txt'):
            with open(f'notes_{username}.txt', 'r') as f:
                for line in f:
                    title, content = line.strip().split('|')
                    notes.append({'title': title, 'content': content})
        return notes