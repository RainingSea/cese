import json
import os
from note import Note

class Notebooks:
    def __init__(self) -> None:
        self.notebooks = {}

    def create_notebook(self, name: str) -> None:
        self.notebooks[name] = []
        self.save_notebook(name)

    def load_notebook(self, name: str) -> dict:
        if os.path.exists(f"{name}.json"):
            with open(f"{name}.json", "r") as file:
                self.notebooks[name] = json.load(file)
        return self.notebooks[name]

    def save_notebook(self, name: str) -> None:
        with open(f"{name}.json", "w") as file:
            json.dump(self.notebooks[name], file)

    def delete_notebook(self, name: str) -> None:
        if name in self.notebooks:
            del self.notebooks[name]
            os.remove(f"{name}.json")