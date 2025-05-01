import tkinter as tk
from tkinter import messagebox
from notebook_manager import NotebookManager
from search_engine import SearchEngine

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Secret Note Keeper")
        self.notebook_manager = NotebookManager()
        self.search_engine = SearchEngine()
        self.create_widgets()
        self.load_notebooks()

    def create_widgets(self):
        self.notebook_listbox = tk.Listbox(self.master)
        self.notebook_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.note_text = tk.Text(self.master)
        self.note_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_button = tk.Button(self.master, text="Create Notebook", command=self.create_notebook)
        self.create_button.pack(side=tk.BOTTOM)

        self.delete_button = tk.Button(self.master, text="Delete Notebook", command=self.delete_notebook)
        self.delete_button.pack(side=tk.BOTTOM)

        self.search_entry = tk.Entry(self.master)
        self.search_entry.pack(side=tk.BOTTOM, fill=tk.X)
        self.search_entry.bind("<Return>", self.search_notes)

    def load_notebooks(self):
        notebooks = self.notebook_manager.load_notebooks()
        for notebook in notebooks:
            self.notebook_listbox.insert(tk.END, notebook)

    def create_notebook(self):
        notebook_name = tk.simpledialog.askstring("Notebook Name", "Enter notebook name:")
        if notebook_name:
            self.notebook_manager.create_notebook(notebook_name)
            self.load_notebooks()

    def delete_notebook(self):
        selected_notebook = self.notebook_listbox.get(tk.ACTIVE)
        if selected_notebook:
            self.notebook_manager.delete_notebook(selected_notebook)
            self.load_notebooks()

    def search_notes(self, event):
        query = self.search_entry.get()
        notes = self.notebook_manager.load_notebook(self.notebook_listbox.get(tk.ACTIVE))
        results = self.search_engine.search(query, notes)
        self.note_text.delete(1.0, tk.END)
        for note in results:
            self.note_text.insert(tk.END, f"{note.title}: {note.decrypt_content()}\n")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()