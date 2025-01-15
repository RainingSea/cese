import os
import time

class Note:
    def __init__(self, title: str = '', content: str = ''):
        self.title = title
        self.content = content
        self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    def save(self, username: str) -> None:
        notes_file = f'notes_{username}.txt'
        with open(notes_file, 'a') as file:
            file.write(f"{self.title}|{self.content}|{self.timestamp}\n")

    def edit(self, new_title: str, new_content: str, username: str) -> None:
        self.title = new_title
        self.content = new_content
        self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self.save(username)

    def delete(self, username: str) -> None:
        notes_file = f'notes_{username}.txt'
        lines = []
        with open(notes_file, 'r') as file:
            lines = file.readlines()
        with open(notes_file, 'w') as file:
            for line in lines:
                if not line.startswith(self.title):
                    file.write(line)

    def search(self, title: str, username: str) -> list:
        notes_file = f'notes_{username}.txt'
        found_notes = []
        if os.path.exists(notes_file):
            with open(notes_file, 'r') as file:
                for line in file:
                    note_title, content, timestamp = line.strip().split('|')
                    if note_title == title:
                        found_notes.append(Note(note_title, content))
        return found_notes

    def load_notes(self, username: str) -> list:
        notes_file = f'notes_{username}.txt'
        notes = []
        if os.path.exists(notes_file):
            with open(notes_file, 'r') as file:
                for line in file:
                    title, content, timestamp = line.strip().split('|')
                    notes.append(Note(title, content))
        return notes