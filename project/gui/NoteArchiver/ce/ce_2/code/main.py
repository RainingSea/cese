import tkinter as tk
from tkinter import filedialog, messagebox
import os

class Note:
    def __init__(self, content: str, tags: list):
        self.content = content
        self.tags = tags

    def add_tag(self, tag: str):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str):
        if tag in self.tags:
            self.tags.remove(tag)

class NoteArchiver:
    def __init__(self, archive_folder: str):
        self.archive_folder = archive_folder
        self.archived_notes = []

        if not os.path.exists(self.archive_folder):
            os.makedirs(self.archive_folder)

    def archive_notebook(self, notebook_name: str) -> bool:
        try:
            notebook_path = os.path.join(self.archive_folder, f"{notebook_name}.txt")
            with open(notebook_path, 'w') as file:
                for note in self.archived_notes:
                    file.write(f"{note.content}|{'|'.join(note.tags)}\n")
            return True
        except Exception as e:
            print(f"Error archiving notebook: {e}")
            return False

    def archive_note(self, notebook_name: str, note_name: str) -> bool:
        try:
            note_path = os.path.join(self.archive_folder, f"{notebook_name}.txt")
            with open(note_path, 'a') as file:
                note = next((n for n in self.archived_notes if n.content == note_name), None)
                if note:
                    file.write(f"{note.content}|{'|'.join(note.tags)}\n")
            return True
        except Exception as e:
            print(f"Error archiving note: {e}")
            return False

    def restore_note(self, note_name: str) -> bool:
        try:
            for note in self.archived_notes:
                if note.content == note_name:
                    self.archived_notes.remove(note)
                    return True
            return False
        except Exception as e:
            print(f"Error restoring note: {e}")
            return False

    def search_notes(self, tag: str) -> list:
        return [note for note in self.archived_notes if tag in note.tags]

class NoteArchiverApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Note Archiver")
        self.archiver = NoteArchiver("archived_notes")
        
        self.archive_notebook_button = tk.Button(master, text="Archive Notebook", command=self.archive_notebook)
        self.archive_notebook_button.pack()

        self.archive_note_button = tk.Button(master, text="Archive Note", command=self.archive_note)
        self.archive_note_button.pack()

        self.search_entry = tk.Entry(master)
        self.search_entry.pack()

        self.search_button = tk.Button(master, text="Search Notes", command=self.search_notes)
        self.search_button.pack()

        self.display_area = tk.Text(master)
        self.display_area.pack()

    def archive_notebook(self):
        notebook_name = filedialog.askstring("Notebook Name", "Enter the notebook name:")
        if notebook_name:
            success = self.archiver.archive_notebook(notebook_name)
            messagebox.showinfo("Info", "Notebook archived!" if success else "Failed to archive notebook.")

    def archive_note(self):
        notebook_name = filedialog.askstring("Notebook Name", "Enter the notebook name:")
        note_name = filedialog.askstring("Note Name", "Enter the note name:")
        if notebook_name and note_name:
            success = self.archiver.archive_note(notebook_name, note_name)
            messagebox.showinfo("Info", "Note archived!" if success else "Failed to archive note.")

    def search_notes(self):
        tag = self.search_entry.get()
        results = self.archiver.search_notes(tag)
        self.display_area.delete(1.0, tk.END)  # Clear previous results
        for note in results:
            self.display_area.insert(tk.END, f"{note.content} | Tags: {', '.join(note.tags)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteArchiverApp(root)
    root.mainloop()