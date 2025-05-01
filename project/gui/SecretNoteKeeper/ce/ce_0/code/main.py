import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from cryptography.fernet import Fernet
import os

class Main:
    def __init__(self):
        self.notebook_manager = NotebookManager()
        self.notebook_manager.load_notebooks()
        self.root = tk.Tk()
        self.root.title("Secret Note Keeper")
        self.create_menu()
        self.root.mainloop()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        notebook_menu = tk.Menu(menu)
        menu.add_cascade(label="Notebooks", menu=notebook_menu)
        notebook_menu.add_command(label="Create", command=self.create_notebook)
        notebook_menu.add_command(label="Delete", command=self.delete_notebook)

    def create_notebook(self):
        name = simpledialog.askstring("Notebook Name", "Enter the name of the notebook:")
        if name:
            self.notebook_manager.create_notebook(name)
            messagebox.showinfo("Success", f"Notebook '{name}' created.")

    def delete_notebook(self):
        name = simpledialog.askstring("Notebook Name", "Enter the name of the notebook to delete:")
        if name:
            self.notebook_manager.delete_notebook(name)
            messagebox.showinfo("Success", f"Notebook '{name}' deleted.")

def main():
    Main()

if __name__ == "__main__":
    main()