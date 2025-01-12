import os
from user import User
from note import Note

class FileManager:
    def save_user_data(self, user: User) -> None:
        """Saves user data to a file."""
        with open('users.txt', 'a') as f:
            f.write(f"{user.username}:{user.password}\n")

    def load_user_data(self) -> list:
        """Loads user data from a file."""
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split(':')
                    users.append(User(username, password))
        return users

    def save_note_data(self, note: Note) -> None:
        """Saves note data to a file."""
        with open('notes.txt', 'a') as f:
            f.write(f"{note.username}:{note.title}:{note.content}\n")

    def load_note_data(self, username: str) -> list:
        """Loads notes for a specific user from a file."""
        notes = []
        if os.path.exists('notes.txt'):
            with open('notes.txt', 'r') as f:
                for line in f:
                    note_username, title, content = line.strip().split(':')
                    if note_username == username:
                        notes.append(Note(note_username, title, content))
        return notes