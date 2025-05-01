import os
import json
from note import Note
from tag import Tag

class ArchiveManager:
    def __init__(self):
        self.archived_notes = self.load_archived_notes()
        self.tags = self.load_tags()

    def load_archived_notes(self):
        if os.path.exists('archived_notes.txt'):
            with open('archived_notes.txt', 'r') as file:
                notes_data = file.readlines()
                return [self.create_note_from_data(data.strip()) for data in notes_data]
        return []

    def load_tags(self):
        if os.path.exists('tags.txt'):
            with open('tags.txt', 'r') as file:
                tags_data = file.readlines()
                return [Tag(name=data.strip()) for data in tags_data]
        return []

    def create_note_from_data(self, data):
        note_id, content = data.split('|', 1)
        return Note(note_id=note_id, content=content)

    def archive_note(self, content):
        self.backup_data()  # Backup before modifying
        note_id = str(len(self.archived_notes) + 1)
        new_note = Note(note_id=note_id, content=content)
        self.archived_notes.append(new_note)
        self.save_archived_notes()

    def save_archived_notes(self):
        with open('archived_notes.txt', 'w') as file:
            for note in self.archived_notes:
                file.write(f"{note.get_id()}|{note.get_content()}\n")

    def add_tag(self, note_id, tag_name):
        note = next((n for n in self.archived_notes if n.get_id() == note_id), None)
        if note:
            note.add_tag(Tag(name=tag_name))
            self.save_tags()

    def save_tags(self):
        with open('tags.txt', 'w') as file:
            for tag in self.tags:
                file.write(f"{tag.get_name()}\n")

    def search_notes(self, tag_name):
        return [note for note in self.archived_notes if tag_name.lower() in [tag.get_name().lower() for tag in note.tags]]

    def backup_data(self):
        if not os.path.exists('backup'):
            os.makedirs('backup')
        with open('backup/archived_notes_backup.json', 'w') as file:
            json.dump([note.__dict__ for note in self.archived_notes], file)

    def restore_note(self, note_id):
        if 0 <= note_id < len(self.archived_notes):
            return self.archived_notes[note_id]
        else:
            return "Note not found."