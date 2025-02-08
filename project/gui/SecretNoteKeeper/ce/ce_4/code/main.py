import tkinter as tk
from tkinter import messagebox
from notebook import Notebook
from note import Note
from encryption import EncryptionManager
import os

class NoteKeeperApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Note Keeper")
        self.notebooks = {}
        self.current_notebook = None
        self.encryption_manager = EncryptionManager(b'YOUR_KEY_HERE')

        self.create_widgets()

    def create_widgets(self):
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New Notebook", command=self.create_notebook)
        file_menu.add_command(label="Open Notebook", command=self.open_notebook)
        file_menu.add_command(label="Save Notebook", command=self.save_notebook)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        self.sidebar = tk.Listbox(self.master)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.note_area = tk.Text(self.master)
        self.note_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.sidebar.bind('<<ListboxSelect>>', self.load_note)

    def create_notebook(self):
        name = tk.simpledialog.askstring("Notebook Name", "Enter notebook name:")
        if name:
            self.notebooks[name] = Notebook(name)
            self.sidebar.insert(tk.END, name)

    def open_notebook(self):
        selected = self.sidebar.curselection()
        if selected:
            notebook_name = self.sidebar.get(selected)
            self.current_notebook = self.notebooks[notebook_name]
            self.current_notebook.load_from_file()
            self.load_notes()

    def save_notebook(self):
        if self.current_notebook:
            self.current_notebook.save_to_file()
            messagebox.showinfo("Save", "Notebook saved successfully.")

    def load_notes(self):
        self.note_area.delete(1.0, tk.END)
        for note in self.current_notebook.notes:
            self.note_area.insert(tk.END, f"{note.title}\n{note.content}\n\n")

    def load_note(self, event):
        selected = self.sidebar.curselection()
        if selected:
            notebook_name = self.sidebar.get(selected)
            self.current_notebook = self.notebooks[notebook_name]
            self.load_notes()

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteKeeperApp(root)
    root.mainloop()