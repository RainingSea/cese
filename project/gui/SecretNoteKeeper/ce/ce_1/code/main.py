import tkinter as tk
from tkinter import messagebox
from notebooks.note_keeper import NoteKeeper

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Keeper")
        self.note_keeper = NoteKeeper()
        self.create_widgets()

    def create_widgets(self):
        self.notebook_listbox = tk.Listbox(self.root)
        self.notebook_listbox.pack()

        self.add_notebook_button = tk.Button(self.root, text="Add Notebook", command=self.add_notebook)
        self.add_notebook_button.pack()

        self.delete_notebook_button = tk.Button(self.root, text="Delete Notebook", command=self.delete_notebook)
        self.delete_notebook_button.pack()

        self.load_notebooks()

    def load_notebooks(self):
        for notebook_name in self.note_keeper.notebooks.keys():
            self.notebook_listbox.insert(tk.END, notebook_name)

    def add_notebook(self):
        notebook_name = "New Notebook"  # Placeholder for user input
        self.note_keeper.create_notebook(notebook_name)
        self.notebook_listbox.insert(tk.END, notebook_name)

    def delete_notebook(self):
        selected_index = self.notebook_listbox.curselection()
        if selected_index:
            notebook_name = self.notebook_listbox.get(selected_index)
            self.note_keeper.delete_notebook(notebook_name)
            self.notebook_listbox.delete(selected_index)

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()