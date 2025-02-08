import os

class ArchiveManager:
    def __init__(self, notes_file: str = 'archived_notes.txt', tags_file: str = 'tags.txt'):
        self.notes_file = notes_file
        self.tags_file = tags_file

    def archive_note(self, title: str, content: str, tags: list) -> None:
        with open(self.notes_file, 'a') as nf:
            nf.write(f"{title}|{content}|{','.join(tags)}\n")

    def restore_note(self, title: str) -> str:
        with open(self.notes_file, 'r') as nf:
            for line in nf:
                if line.startswith(title + '|'):
                    return line.strip()
        return "Note not found."

    def add_tag(self, title: str, tag: str) -> None:
        notes = []
        found = False
        with open(self.notes_file, 'r') as nf:
            for line in nf:
                if line.startswith(title + '|'):
                    found = True
                    parts = line.strip().split('|')
                    tags = parts[2].split(',')
                    if tag not in tags:
                        tags.append(tag)
                    parts[2] = ','.join(tags)
                    notes.append('|'.join(parts))
                else:
                    notes.append(line.strip())
        
        if found:
            with open(self.notes_file, 'w') as nf:
                for note in notes:
                    nf.write(note + '\n')

    def search_notes(self, tag: str) -> list:
        found_notes = []
        with open(self.notes_file, 'r') as nf:
            for line in nf:
                if tag in line.strip().split('|')[2]:
                    found_notes.append(line.strip())
        return found_notes

    def backup_data(self) -> None:
        if os.path.exists(self.notes_file):
            os.rename(self.notes_file, f"{self.notes_file}.bak")
        if os.path.exists(self.tags_file):
            os.rename(self.tags_file, f"{self.tags_file}.bak")