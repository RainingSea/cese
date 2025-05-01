import tkinter as tk
from tkinter import messagebox
from notebook_manager import NotebookManager

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Notebook Manager")
        self.notebook_manager = NotebookManager()

        self.notebooks_listbox = tk.Listbox(self.master)
        self.notebooks_listbox.pack()

        self.archive_button = tk.Button(self.master, text="Archive Notebook", command=self.archive_notebook)
        self.archive_button.pack()

        self.restore_button = tk.Button(self.master, text="Restore Notebook", command=self.restore_notebook)
        self.restore_button.pack()

        self.search_entry = tk.Entry(self.master)
        self.search_entry.pack()

        self.search_button = tk.Button(self.master, text="Search Notes", command=self.search_notes)
        self.search_button.pack()

        self.load_notebooks()

    def load_notebooks(self):
        try:
            with open("notebooks.txt", "r") as file:
                notebooks = file.readlines()
                for notebook in notebooks:
                    self.notebooks_listbox.insert(tk.END, notebook.strip())
        except FileNotFoundError:
            messagebox.showerror("Error", "Notebooks file not found.")

    def archive_notebook(self):
        selected_notebook = self.notebooks_listbox.get(tk.ACTIVE)
        if selected_notebook:
            self.notebook_manager.archive_notebook(selected_notebook)
            self.notebooks_listbox.delete(tk.ACTIVE)
        else:
            messagebox.showwarning("Warning", "Please select a notebook to archive.")

    def restore_notebook(self):
        selected_notebook = self.notebooks_listbox.get(tk.ACTIVE)
        if selected_notebook:
            self.notebook_manager.restore_notebook(selected_notebook)
            self.load_notebooks()
        else:
            messagebox.showwarning("Warning", "Please select a notebook to restore.")

    def search_notes(self):
        query = self.search_entry.get()
        results = self.notebook_manager.search_notes(query)
        messagebox.showinfo("Search Results", "\n".join(results) if results else "No notes found.")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()