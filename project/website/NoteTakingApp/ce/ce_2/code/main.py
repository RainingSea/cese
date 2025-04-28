import os
import json

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.note_manager = NoteManager()

    def main(self):
        # Load existing users and notes
        self.user_manager.load_users()
        self.note_manager.load_notes()
        # Here you can set up the web framework and routing
        print("Application started. Routes set up.")

class UserManager:
    def __init__(self):
        self.users = {}

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class NoteManager:
    def __init__(self):
        self.notes = []

    def load_notes(self):
        if os.path.exists('notes.txt'):
            with open('notes.txt', 'r') as file:
                for line in file:
                    title, content = line.strip().split('|')
                    self.notes.append({'title': title, 'content': content})

    def add_note(self, title: str, content: str) -> bool:
        self.notes.append({'title': title, 'content': content})
        with open('notes.txt', 'a') as file:
            file.write(f"{title}|{content}\n")
        return True

    def get_notes(self) -> list:
        return self.notes

    def get_note_details(self, note_id: int) -> str:
        if 0 <= note_id < len(self.notes):
            note = self.notes[note_id]
            return f"Title: {note['title']}\nContent: {note['content']}"
        return "Note not found."

    def edit_note(self, note_id: int, title: str, content: str) -> bool:
        if 0 <= note_id < len(self.notes):
            self.notes[note_id] = {'title': title, 'content': content}
            self.save_notes()
            return True
        return False

    def delete_note(self, note_id: int) -> bool:
        if 0 <= note_id < len(self.notes):
            del self.notes[note_id]
            self.save_notes()
            return True
        return False

    def search_notes(self, title: str) -> list:
        return [note for note in self.notes if title.lower() in note['title'].lower()]

    def save_notes(self):
        with open('notes.txt', 'w') as file:
            for note in self.notes:
                file.write(f"{note['title']}|{note['content']}\n")

if __name__ == "__main__":
    app = Main()
    app.main()