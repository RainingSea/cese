import tkinter as tk
from tkinter import messagebox
from secret_note_keeper import SecretNoteKeeper

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secret Note Keeper")
        self.note_keeper = SecretNoteKeeper()
        self.note_keeper.load_notebooks()

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.notebook_listbox = tk.Listbox(self.frame)
        self.notebook_listbox.pack(side=tk.LEFT)

        self.text_area = tk.Text(self.frame)
        self.text_area.pack(side=tk.LEFT)

        self.add_button = tk.Button(self.root, text="Add Note", command=self.add_note)
        self.add_button.pack()

        self.edit_button = tk.Button(self.root, text="Edit Note", command=self.edit_note)
        self.edit_button.pack()

        self.delete_button = tk.Button(self.root, text="Delete Note", command=self.delete_note)
        self.delete_button.pack()

        self.load_notebooks()

    def load_notebooks(self):
        """Load notebooks into the listbox."""
        for notebook_name in self.note_keeper.notebooks.keys():
            self.notebook_listbox.insert(tk.END, notebook_name)

    def add_note(self):
        """Add a new note."""
        selected_notebook = self.notebook_listbox.get(tk.ACTIVE)
        note = self.text_area.get("1.0", tk.END).strip()
        if note:
            self.note_keeper.add_note(selected_notebook, note)
            self.note_keeper.save_notebooks()
            self.text_area.delete("1.0", tk.END)
            messagebox.showinfo("Success", "Note added successfully.")
        else:
            messagebox.showwarning("Warning", "Note cannot be empty.")

    def edit_note(self):
        """Edit an existing note."""
        selected_notebook = self.notebook_listbox.get(tk.ACTIVE)
        note_id = self.notebook_listbox.curselection()[0]
        new_note = self.text_area.get("1.0", tk.END).strip()
        if new_note:
            self.note_keeper.edit_note(selected_notebook, note_id, new_note)
            self.note_keeper.save_notebooks()
            self.text_area.delete("1.0", tk.END)
            messagebox.showinfo("Success", "Note edited successfully.")
        else:
            messagebox.showwarning("Warning", "Note cannot be empty.")

    def delete_note(self):
        """Delete a selected note."""
        selected_notebook = self.notebook_listbox.get(tk.ACTIVE)
        note_id = self.notebook_listbox.curselection()[0]
        self.note_keeper.delete_note(selected_notebook, note_id)
        self.note_keeper.save_notebooks()
        self.text_area.delete("1.0", tk.END)
        messagebox.showinfo("Success", "Note deleted successfully.")