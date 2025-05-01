import tkinter as tk
from tkinter import messagebox
from archive_manager import ArchiveManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Archiver")
        self.archive_manager = ArchiveManager()
        self.setup_ui()

    def setup_ui(self):
        self.note_entry = tk.Entry(self.root, width=50)
        self.note_entry.pack(pady=10)

        self.archive_button = tk.Button(self.root, text="Archive Note", command=self.archive_note)
        self.archive_button.pack(pady=5)

        self.tag_entry = tk.Entry(self.root, width=50)
        self.tag_entry.pack(pady=10)

        self.add_tag_button = tk.Button(self.root, text="Add Tag", command=self.add_tag)
        self.add_tag_button.pack(pady=5)

        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack(pady=10)

        self.search_button = tk.Button(self.root, text="Search Notes", command=self.search_notes)
        self.search_button.pack(pady=5)

        self.result_text = tk.Text(self.root, width=60, height=15)
        self.result_text.pack(pady=10)

    def archive_note(self):
        note_content = self.note_entry.get()
        if note_content:
            self.archive_manager.archive_note(note_content)
            messagebox.showinfo("Success", "Note archived successfully!")
            self.note_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a note.")

    def add_tag(self):
        tag_name = self.tag_entry.get()
        if tag_name:
            if self.archive_manager.archived_notes:
                self.archive_manager.add_tag(self.archive_manager.archived_notes[-1].get_id(), tag_name)
                messagebox.showinfo("Success", "Tag added successfully!")
                self.tag_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Warning", "No notes available to tag.")
        else:
            messagebox.showwarning("Warning", "Please enter a tag.")

    def search_notes(self):
        tag_name = self.search_entry.get()
        if tag_name:
            notes = self.archive_manager.search_notes(tag_name)
            self.result_text.delete(1.0, tk.END)
            if notes:
                for note in notes:
                    self.result_text.insert(tk.END, f"{note.get_content()}\n")
            else:
                self.result_text.insert(tk.END, "No notes found with this tag.\n")
        else:
            messagebox.showwarning("Warning", "Please enter a tag to search.")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()