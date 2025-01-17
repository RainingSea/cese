import tkinter as tk
from tkinter import simpledialog, messagebox
from notebooks import Notebooks

class UI:
    def __init__(self, main) -> None:
        self.main = main
        self.window = tk.Tk()
        self.window.title("Notebook Application")
        self.notebooks_listbox = tk.Listbox(self.window)
        self.notebooks_listbox.pack()
        self.load_notebooks()

        self.text_area = tk.Text(self.window)
        self.text_area.pack()

        self.add_button = tk.Button(self.window, text="Add Note", command=self.add_note)
        self.add_button.pack()

        self.window.mainloop()

    def load_notebooks(self) -> None:
        self.notebooks_listbox.delete(0, tk.END)
        for notebook in self.main.notebooks.notebooks:
            self.notebooks_listbox.insert(tk.END, notebook)

    def add_note(self) -> None:
        title = simpledialog.askstring("Input", "Enter note title:")
        content = simpledialog.askstring("Input", "Enter note content:")
        if title and content:
            note = Note(title, content)
            self.main.notebooks.notebooks[self.notebooks_listbox.get(tk.ACTIVE)].append(note.__dict__)
            self.main.notebooks.save_notebook(self.notebooks_listbox.get(tk.ACTIVE))
            self.load_notebooks()
        else:
            messagebox.showwarning("Warning", "Title and content cannot be empty.")