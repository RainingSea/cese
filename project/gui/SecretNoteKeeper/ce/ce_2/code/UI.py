import tkinter as tk
from tkinter import messagebox
from NotebookManager import NotebookManager

class UserInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Secret Note Keeper")
        self.notebook_manager = NotebookManager()
        self.create_widgets()

    def create_widgets(self):
        self.notebook_listbox = tk.Listbox(self.master)
        self.notebook_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.note_listbox = tk.Listbox(self.master)
        self.note_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.add_note_button = tk.Button(self.master, text="Add Note", command=self.add_note)
        self.add_note_button.pack()

        self.edit_note_button = tk.Button(self.master, text="Edit Note", command=self.edit_note)
        self.edit_note_button.pack()

        self.delete_note_button = tk.Button(self.master, text="Delete Note", command=self.delete_note)
        self.delete_note_button.pack()

    def add_note(self):
        title = "Sample Title"
        content = "Sample Content"
        self.notebook_manager.add_note(title, content)
        self.update_note_listbox()

    def edit_note(self):
        selected_note = self.note_listbox.get(tk.ACTIVE)
        new_content = "Updated Content"
        self.notebook_manager.edit_note(selected_note, new_content)
        self.update_note_listbox()

    def delete_note(self):
        selected_note = self.note_listbox.get(tk.ACTIVE)
        self.notebook_manager.delete_note(selected_note)
        self.update_note_listbox()

    def update_note_listbox(self):
        self.note_listbox.delete(0, tk.END)
        for note in self.notebook_manager.notebooks:
            self.note_listbox.insert(tk.END, note.title)