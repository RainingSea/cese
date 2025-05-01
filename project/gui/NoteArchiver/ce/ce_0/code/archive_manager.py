import os

class ArchiveManager:
    def __init__(self):
        self.archived_notes = self.load_archived_notes()
        self.tags = self.load_tags()

    def load_archived_notes(self):
        if not os.path.exists('archived_notes.txt'):
            return []
        with open('archived_notes.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

    def load_tags(self):
        if not os.path.exists('tags.txt'):
            return []
        with open('tags.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

    def archive_note(self, note: str, tags: list):
        self.archived_notes.append(note)
        self.tags.extend(tags)
        self.save_archived_notes()
        self.save_tags()

    def restore_note(self, note_id: int) -> str:
        if 0 <= note_id < len(self.archived_notes):
            return self.archived_notes[note_id]
        return "Note not found."

    def search_notes(self, query: str) -> list:
        return [note for note in self.archived_notes if query.lower() in note.lower()]

    def save_archived_notes(self):
        with open('archived_notes.txt', 'w') as file:
            for note in self.archived_notes:
                file.write(note + '\n')

    def save_tags(self):
        with open('tags.txt', 'w') as file:
            for tag in set(self.tags):  # Save unique tags
                file.write(tag + '\n')