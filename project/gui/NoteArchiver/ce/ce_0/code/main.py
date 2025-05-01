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
        self.label = tk.Label(self.root, text="Enter Note:")
        self.label.pack()

        self.note_entry = tk.Entry(self.root, width=50)
        self.note_entry.pack()

        self.tag_label = tk.Label(self.root, text="Enter Tags (comma separated):")
        self.tag_label.pack()

        self.tag_entry = tk.Entry(self.root, width=50)
        self.tag_entry.pack()

        self.archive_button = tk.Button(self.root, text="Archive Note", command=self.archive_note)
        self.archive_button.pack()

        self.restore_button = tk.Button(self.root, text="Restore Note", command=self.restore_note)
        self.restore_button.pack()

        self.search_button = tk.Button(self.root, text="Search Notes", command=self.search_notes)
        self.search_button.pack()

        self.result_display = tk.Text(self.root, height=10, width=50)
        self.result_display.pack()

    def archive_note(self):
        note = self.note_entry.get()
        tags = self.tag_entry.get().split(',')
        if note:
            self.archive_manager.archive_note(note, [tag.strip() for tag in tags])
            messagebox.showinfo("Success", "Note archived successfully!")
        else:
            messagebox.showwarning("Warning", "Please enter a note.")

    def restore_note(self):
        note_id = int(self.note_entry.get())
        restored_note = self.archive_manager.restore_note(note_id)
        self.result_display.delete(1.0, tk.END)
        self.result_display.insert(tk.END, restored_note)

    def search_notes(self):
        query = self.note_entry.get()
        results = self.archive_manager.search_notes(query)
        self.result_display.delete(1.0, tk.END)
        for note in results:
            self.result_display.insert(tk.END, note + "\n")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()