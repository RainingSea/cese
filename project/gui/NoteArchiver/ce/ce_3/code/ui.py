import tkinter as tk
from tkinter import messagebox
from archive_manager import ArchiveManager

class UI:
    def __init__(self):
        self.archive_manager = ArchiveManager()
        self.root = tk.Tk()
        self.root.title("Note Archiver")
        self.main_window()

    def main_window(self):
        self.display_notes(self.archive_manager.notes)
        tk.Button(self.root, text="Archive Note", command=self.archive_note).pack()
        tk.Button(self.root, text="Restore Note", command=self.restore_note).pack()
        tk.Button(self.root, text="Search Notes", command=self.search_notes).pack()
        self.root.mainloop()

    def display_notes(self, notes: list):
        for widget in self.root.winfo_children():
            widget.destroy()
        for note in notes:
            tk.Label(self.root, text=f"ID: {note.id}, Content: {note.content}, Tags: {', '.join(note.tags)}").pack()

    def get_user_input(self) -> str:
        return tk.simpledialog.askstring("Input", "Enter your input:")

    def show_message(self, message: str):
        messagebox.showinfo("Information", message)