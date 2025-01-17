import os
from typing import Dict
from .notebook import Notebook

class NoteKeeper:
    def __init__(self):
        self.notebooks: Dict[str, Notebook] = {}
        self.load_notebooks()

    def create_notebook(self, name: str):
        if name not in self.notebooks:
            self.notebooks[name] = Notebook(name)
            self.save_notebooks()

    def delete_notebook(self, name: str):
        if name in self.notebooks:
            del self.notebooks[name]
            self.save_notebooks()

    def get_notebook(self, name: str) -> Notebook:
        return self.notebooks.get(name)

    def save_notebooks(self):
        with open('notebooks/notebooks_list.json', 'w') as f:
            json.dump(list(self.notebooks.keys()), f)

    def load_notebooks(self):
        if os.path.exists('notebooks/notebooks_list.json'):
            with open('notebooks/notebooks_list.json', 'r') as f:
                notebook_names = json.load(f)
                for name in notebook_names:
                    notebook = Notebook(name)
                    notebook.load_notes()
                    self.notebooks[name] = notebook