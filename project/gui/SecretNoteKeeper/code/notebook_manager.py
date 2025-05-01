import os
from note import Note
from cryptography.fernet import Fernet

class NotebookManager:
    def __init__(self):
        self.notebooks = {}
        self.load_notebooks()

    def load_notebooks(self):
        if not os.path.exists('notebooks'):
            os.makedirs('notebooks')
        for filename in os.listdir('notebooks'):
            if filename.endswith('.txt'):
                notebook_name = filename[:-4]
                self.notebooks[notebook_name] = []
                with open(f'notebooks/{filename}', 'r') as f:
                    for line in f:
                        title, content = line.strip().split('|')
                        note = Note(title, content)
                        self.notebooks[notebook_name].append(note)

    def create_notebook(self, name: str) -> None:
        if name not in self.notebooks:
            self.notebooks[name] = []
            with open(f'notebooks/{name}.txt', 'w') as f:
                f.write('')
        else:
            raise ValueError("Notebook already exists.")

    def add_note(self, notebook_name: str, title: str, content: str) -> None:
        if notebook_name in self.notebooks:
            if not any(note.get_title() == title for note in self.notebooks[notebook_name]):
                note = Note(title, self.encrypt_content(content))
                self.notebooks[notebook_name].append(note)
                self.save_notes(notebook_name)
            else:
                raise ValueError("Note title already exists.")
        else:
            raise ValueError("Notebook does not exist.")

    def edit_note(self, notebook_name: str, title: str, new_content: str) -> None:
        if notebook_name in self.notebooks:
            for note in self.notebooks[notebook_name]:
                if note.get_title() == title:
                    note.content = self.encrypt_content(new_content)
                    self.save_notes(notebook_name)
                    return
            raise ValueError("Note not found.")
        else:
            raise ValueError("Notebook does not exist.")

    def delete_note(self, notebook_name: str, title: str) -> None:
        if notebook_name in self.notebooks:
            self.notebooks[notebook_name] = [note for note in self.notebooks[notebook_name] if note.get_title() != title]
            self.save_notes(notebook_name)
        else:
            raise ValueError("Notebook does not exist.")

    def search_notes(self, notebook_name: str, query: str) -> list:
        if notebook_name in self.notebooks:
            return [note.get_title() for note in self.notebooks[notebook_name] if query in self.decrypt_content(note.get_content())]
        else:
            raise ValueError("Notebook does not exist.")

    def sort_notes(self, notebook_name: str) -> list:
        if notebook_name in self.notebooks:
            return sorted(self.notebooks[notebook_name], key=lambda note: note.get_title())
        else:
            raise ValueError("Notebook does not exist.")

    def save_notes(self, notebook_name: str) -> None:
        with open(f'notebooks/{notebook_name}.txt', 'w') as f:
            for note in self.notebooks[notebook_name]:
                f.write(f"{note.get_title()}|{note.get_content()}\n")

    def encrypt_content(self, content: str) -> str:
        key = Fernet.generate_key()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(content.encode())
        return encrypted.decode()

    def decrypt_content(self, encrypted_content: str) -> str:
        key = Fernet.generate_key()
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_content.encode())
        return decrypted.decode()