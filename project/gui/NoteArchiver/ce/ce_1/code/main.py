import tkinter as tk
from tkinter import messagebox
from note_manager import NoteManager

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("NoteArchiver")
        self.note_manager = NoteManager()
        
        self.setup_ui()

    def setup_ui(self):
        self.sidebar = tk.Frame(self.master)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.archive_button = tk.Button(self.sidebar, text="Archive Note", command=self.archive_note)
        self.archive_button.pack()

        self.restore_button = tk.Button(self.sidebar, text="Restore Note", command=self.restore_note)
        self.restore_button.pack()

        self.tag_button = tk.Button(self.sidebar, text="Add Tag", command=self.add_tag)
        self.tag_button.pack()

        self.search_entry = tk.Entry(self.sidebar)
        self.search_entry.pack()

        self.search_button = tk.Button(self.sidebar, text="Search by Tag", command=self.search_by_tag)
        self.search_button.pack()

        self.notes_display = tk.Text(self.master)
        self.notes_display.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def main(self):
        self.master.mainloop()

    def archive_note(self):
        note_id = self.get_selected_note_id()
        if note_id:
            self.note_manager.archive(note_id)
            messagebox.showinfo("Success", "Note archived successfully.")

    def restore_note(self):
        note_id = self.get_selected_note_id()
        if note_id:
            note = self.note_manager.restore(note_id)
            if note:
                self.notes_display.insert(tk.END, note.get_content())
                messagebox.showinfo("Success", "Note restored successfully.")
            else:
                messagebox.showerror("Error", "Note not found.")

    def add_tag(self):
        note_id = self.get_selected_note_id()
        tag = self.get_tag_from_user()
        if note_id and tag:
            self.note_manager.add_tag(note_id, tag)
            messagebox.showinfo("Success", "Tag added successfully.")

    def search_by_tag(self):
        tag = self.search_entry.get()
        notes = self.note_manager.search_by_tag(tag)
        self.notes_display.delete(1.0, tk.END)
        for note in notes:
            self.notes_display.insert(tk.END, note.get_content() + "\n")

    def get_selected_note_id(self):
        # Placeholder for getting the selected note ID from the UI
        return "example_note_id"

    def get_tag_from_user(self):
        # Placeholder for getting a tag from the user
        return "example_tag"

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.main()