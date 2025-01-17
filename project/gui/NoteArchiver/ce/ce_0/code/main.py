import tkinter as tk
from tkinter import messagebox, simpledialog
from ArchiveManager import ArchiveManager

class Main:
    def __init__(self):
        self.archive_manager = ArchiveManager()
        self.root = tk.Tk()
        self.create_ui()

    def create_ui(self) -> None:
        self.root.title("Note Archiver")
        
        self.archive_button = tk.Button(self.root, text="Archive Note", command=self.archive_note)
        self.archive_button.pack(pady=10)

        self.view_button = tk.Button(self.root, text="View Archived Notes", command=self.view_archived_notes)
        self.view_button.pack(pady=10)

        self.tag_button = tk.Button(self.root, text="Add Tag to Note", command=self.add_tag)
        self.tag_button.pack(pady=10)

        self.backup_button = tk.Button(self.root, text="Backup Data", command=self.backup_data)
        self.backup_button.pack(pady=10)

        self.root.mainloop()

    def archive_note(self) -> None:
        title = simpledialog.askstring("Input", "Enter note title:")
        content = simpledialog.askstring("Input", "Enter note content:")
        tags = simpledialog.askstring("Input", "Enter tags (comma-separated):").split(',')
        if title and content:
            self.archive_manager.archive_note(title, content, tags)
            messagebox.showinfo("Success", "Note archived successfully!")

    def view_archived_notes(self) -> None:
        with open(self.archive_manager.notes_file, 'r') as nf:
            notes = nf.readlines()
            notes_display = ''.join(notes)
            messagebox.showinfo("Archived Notes", notes_display)

    def add_tag(self) -> None:
        title = simpledialog.askstring("Input", "Enter note title to tag:")
        tag = simpledialog.askstring("Input", "Enter tag to add:")
        if title and tag:
            self.archive_manager.add_tag(title, tag)
            messagebox.showinfo("Success", "Tag added successfully!")

    def backup_data(self) -> None:
        self.archive_manager.backup_data()
        messagebox.showinfo("Success", "Backup completed successfully!")

if __name__ == "__main__":
    Main()