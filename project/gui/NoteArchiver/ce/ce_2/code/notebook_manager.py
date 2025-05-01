import os
import json
from note import Note

class NotebookManager:
    def __init__(self):
        self.notebooks = self.load_notebooks()
        self.archived_notes = self.load_archived_notes()

    def load_notebooks(self):
        if not os.path.exists("notebooks.txt"):
            return []
        with open("notebooks.txt", "r") as file:
            return [line.strip() for line in file.readlines()]

    def load_archived_notes(self):
        if not os.path.exists("archived_notes.txt"):
            return {}
        with open("archived_notes.txt", "r") as file:
            return json.load(file)

    def archive_notebook(self, notebook_name: str) -> None:
        if notebook_name in self.notebooks:
            self.notebooks.remove(notebook_name)
            self.archived_notes[notebook_name] = []
            self.save_archived_notes()

    def restore_notebook(self, notebook_name: str) -> None:
        if notebook_name in self.archived_notes:
            self.notebooks.append(notebook_name)
            del self.archived_notes[notebook_name]
            self.save_archived_notes()
            self.save_notebooks()

    def add_tag(self, note_id: str, tag: str) -> None:
        for notebook in self.archived_notes:
            for note in self.archived_notes[notebook]:
                if note['id'] == note_id:
                    note['tags'].append(tag)
                    self.save_archived_notes()
                    return

    def search_notes(self, query: str) -> list:
        results = []
        for notebook in self.archived_notes:
            for note in self.archived_notes[notebook]:
                if query.lower() in note['content'].lower():
                    results.append(note['content'])
        return results

    def save_notebooks(self) -> None:
        with open("notebooks.txt", "w") as file:
            for notebook in self.notebooks:
                file.write(notebook + "\n")

    def save_archived_notes(self) -> None:
        with open("archived_notes.txt", "w") as file:
            json.dump(self.archived_notes, file)