import json
from note import Note
from tag import Tag

class NoteManager:
    def __init__(self):
        self.notes = self.load_notes()
        self.tags = self.load_tags()

    def load_notes(self):
        notes = []
        try:
            with open('archived_notes.txt', 'r') as file:
                for line in file:
                    content, *tags = line.strip().split('|')
                    note = Note(content, tags)
                    notes.append(note)
        except FileNotFoundError:
            pass
        return notes

    def load_tags(self):
        tags = []
        try:
            with open('tags.txt', 'r') as file:
                for line in file:
                    tag_name = line.strip()
                    tags.append(Tag(tag_name))
        except FileNotFoundError:
            pass
        return tags

    def archive(self, note_id):
        note = self.find_note_by_id(note_id)
        if note:
            with open('archived_notes.txt', 'a') as file:
                file.write(f"{note.get_content()}|{'|'.join(note.tags)}\n")
            self.notes.remove(note)

    def restore(self, note_id):
        note = self.find_note_by_id(note_id)
        if note:
            self.notes.append(note)
            return note
        return None

    def search_by_tag(self, tag):
        return [note for note in self.notes if tag in note.tags]

    def find_note_by_id(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                return note
        return None