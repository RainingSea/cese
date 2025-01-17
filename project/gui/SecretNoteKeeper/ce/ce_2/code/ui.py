import tkinter as tk
from tkinter import simpledialog, messagebox
from notebook_manager import NotebookManager

class UI:
    def __init__(self, notebook_manager: NotebookManager):
        self.notebook_manager = notebook_manager
        self.root = tk.Tk()
        self.root.title("Note Manager")
        self.notebook_listbox = tk.Listbox(self.root)
        self.note_listbox = tk.Listbox(self.root)
        self.search_entry = tk.Entry(self.root)
        self.setup_ui()

    def setup_ui(self):
        self.notebook_listbox.pack()
        self.note_listbox.pack()
        self.search_entry.pack()
        self.display_notebooks()
        tk.Button(self.root, text="Create Notebook", command=self.create_notebook).pack()
        tk.Button(self.root, text="Add Note", command=self.add_note).pack()
        tk.Button(self.root, text="Edit Note", command=self.edit_note).pack()
        tk.Button(self.root, text="Delete Note", command=self.delete_note).pack()
        tk.Button(self.root, text="Search Notes", command=self.search_notes).pack()
        self.root.mainloop()

    def display_notebooks(self) -> None:
        self.notebook_listbox.delete(0, tk.END)
        for notebook in self.notebook_manager.notebooks.keys():
            self.notebook_listbox.insert(tk.END, notebook)

    def display_notes(self, notebook_name: str) -> None:
        self.note_listbox.delete(0, tk.END)
        for note in self.notebook_manager.notebooks[notebook_name]:
            decrypted_note = self.notebook_manager.cipher.decrypt(note.encode()).decode()
            self.note_listbox.insert(tk.END, decrypted_note)

    def create_notebook(self) -> None:
        name = simpledialog.askstring("Notebook Name", "Enter notebook name:")
        if name:
            self.notebook_manager.create_notebook(name)
            self.display_notebooks()

    def add_note(self) -> None:
        selected_notebook = self.notebook_listbox.get(tk.ACTIVE)
        note = simpledialog.askstring("Add Note", "Enter note:")
        if selected_notebook and note:
            self.notebook_manager.add_note(selected_notebook, note)
            self.display_notes(selected_notebook)

    def edit_note(self) -> None:
        selected_notebook = self.notebook_listbox.get(tk.ACTIVE)
        selected_note_index = self.note_listbox.curselection()
        if selected_notebook and selected_note_index:
            note = simpledialog.askstring("Edit Note", "Enter new note:")
            if note:
                self.notebook_manager.edit_note(selected_notebook, selected_note_index[0], note)
                self.display_notes(selected_notebook)

    def delete_note(self) -> None:
        selected_notebook = self.notebook_listbox.get(tk.ACTIVE)
        selected_note_index = self.note_listbox.curselection()
        if selected_notebook and selected_note_index:
            self.notebook_manager.delete_note(selected_notebook, selected_note_index[0])
            self.display_notes(selected_notebook)

    def search_notes(self) -> None:
        selected_notebook = self.notebook_listbox.get(tk.ACTIVE)
        query = self.search_entry.get()
        if selected_notebook and query:
            results = self.notebook_manager.search_notes(selected_notebook, query)
            self.note_listbox.delete(0, tk.END)
            for note in results:
                self.note_listbox.insert(tk.END, self.notebook_manager.cipher.decrypt(note.encode()).decode())