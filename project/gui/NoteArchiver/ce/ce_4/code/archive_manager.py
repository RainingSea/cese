import os

class ArchiveManager:
    def __init__(self, archived_file='archived_notes.txt', tags_file='tags.txt'):
        self.archived_file = archived_file
        self.tags_file = tags_file

    def archive_note(self, note: str, tags: list):
        with open(self.archived_file, 'a') as archive:
            archive.write(f"{note}\n")
        
        with open(self.tags_file, 'a') as tags_file:
            tags_line = ','.join(tags)
            tags_file.write(f"{note}|{tags_line}\n")

    def restore_note(self, note_id: int) -> str:
        with open(self.archived_file, 'r') as archive:
            notes = archive.readlines()
            if 0 <= note_id < len(notes):
                return notes[note_id].strip()
            return "Note not found."

    def view_archived_notes(self) -> list:
        with open(self.archived_file, 'r') as archive:
            return [note.strip() for note in archive.readlines()]

    def add_tags(self, note_id: int, tags: list):
        notes = self.view_archived_notes()
        if 0 <= note_id < len(notes):
            note = notes[note_id]
            with open(self.tags_file, 'r') as tags_file:
                existing_tags = {line.split('|')[0]: line.split('|')[1].strip() for line in tags_file.readlines()}
            
            existing_tags[note] = ','.join(tags)
            with open(self.tags_file, 'w') as tags_file:
                for note_key, tag_value in existing_tags.items():
                    tags_file.write(f"{note_key}|{tag_value}\n")