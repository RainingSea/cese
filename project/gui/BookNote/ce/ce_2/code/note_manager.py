import os
from models import Note

class NoteManager:
    def __init__(self):
        self.notes = []
        self.load_notes()

    def add_note(self, book_title: str, chapter: str, text: str):
        new_note = Note(book_title, chapter, text)
        self.notes.append(new_note)
        self.save_notes()

    def load_notes(self):
        if os.path.exists('notes.txt'):
            with open('notes.txt', 'r') as file:
                for line in file:
                    book_title, chapter, text = line.strip().split('|')
                    self.notes.append(Note(book_title, chapter, text))

    def save_notes(self):
        with open('notes.txt', 'w') as file:
            for note in self.notes:
                file.write(f"{note.book_title}|{note.chapter}|{note.text}\n")

    def search_notes(self, keyword: str):
        return [note for note in self.notes if keyword.lower() in note.text.lower()]