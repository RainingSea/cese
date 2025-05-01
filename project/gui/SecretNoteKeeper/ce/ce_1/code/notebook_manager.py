import os
from note import Note

class NotebookManager:
    def __init__(self):
        self.notebooks = self.load_notebooks()

    def create_notebook(self, name: str) -> None:
        with open('notebooks_list.txt', 'a') as f:
            f.write(name + '\n')
        open(f"{name}.txt", 'w').close()

    def delete_notebook(self, name: str) -> None:
        os.remove(f"{name}.txt")
        self.notebooks.remove(name)
        self.save_notebooks()

    def load_notebooks(self) -> list:
        if os.path.exists('notebooks_list.txt'):
            with open('notebooks_list.txt', 'r') as f:
                return [line.strip() for line in f.readlines()]
        return []

    def save_notebooks(self) -> None:
        with open('notebooks_list.txt', 'w') as f:
            for notebook in self.notebooks:
                f.write(notebook + '\n')

    def load_notebook(self, name: str) -> list:
        notes = []
        if os.path.exists(f"{name}.txt"):
            with open(f"{name}.txt", 'r') as f:
                for line in f:
                    title, content = line.strip().split('|')
                    notes.append(Note(title, content))
        return notes