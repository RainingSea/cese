import tkinter as tk
from tkinter import messagebox
from NoteArchiver import NoteArchiver
from Note import Note

class NoteArchiverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Archiver")
        self.archiver = NoteArchiver()

        self.create_widgets()

    def create_widgets(self):
        self.note_listbox = tk.Listbox(self.root)
        self.note_listbox.pack(fill=tk.BOTH, expand=True)

        self.archive_button = tk.Button(self.root, text="Archive Note", command=self.archive_note)
        self.archive_button.pack()

        self.restore_button = tk.Button(self.root, text="Restore Note", command=self.restore_note)
        self.restore_button.pack()

        self.tag_entry = tk.Entry(self.root)
        self.tag_entry.pack()

        self.add_tag_button = tk.Button(self.root, text="Add Tag", command=self.add_tag)
        self.add_tag_button.pack()

        self.load_notes()

    def load_notes(self):
        for note in self.archiver.notes:
            self.note_listbox.insert(tk.END, note.content)

    def archive_note(self):
        selected_index = self.note_listbox.curselection()
        if selected_index:
            note = self.archiver.notes[selected_index[0]]
            self.archiver.archive_note(note)
            self.note_listbox.delete(selected_index)

    def restore_note(self):
        note_id = self.note_listbox.get(tk.ACTIVE)
        if note_id:
            self.archiver.restore_note(note_id)
            self.load_notes()

    def add_tag(self):
        selected_index = self.note_listbox.curselection()
        if selected_index:
            note = self.archiver.notes[selected_index[0]]
            tag = self.tag_entry.get()
            if tag:
                self.archiver.add_tag(note.id, tag)
                messagebox.showinfo("Tag Added", f"Tag '{tag}' added to note.")
            else:
                messagebox.showwarning("Input Error", "Please enter a tag.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteArchiverApp(root)
    root.mainloop()