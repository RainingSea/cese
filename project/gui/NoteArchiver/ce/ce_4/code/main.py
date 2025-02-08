import tkinter as tk
from tkinter import messagebox
from archive_manager import ArchiveManager

class Main:
    def __init__(self, master):
        self.master = master
        self.archive_manager = ArchiveManager()

        self.master.title("Notes Archiver")
        self.master.geometry("400x300")

        self.note_text = tk.Text(master, height=10)
        self.note_text.pack()

        self.tag_entry = tk.Entry(master)
        self.tag_entry.pack()

        self.archive_button = tk.Button(master, text="Archive Note", command=self.archive_note)
        self.archive_button.pack()

        self.restore_button = tk.Button(master, text="Restore Note", command=self.restore_note)
        self.restore_button.pack()

        self.view_button = tk.Button(master, text="View Archived Notes", command=self.view_archived_notes)
        self.view_button.pack()

    def archive_note(self):
        note = self.note_text.get("1.0", tk.END).strip()
        tags = self.tag_entry.get().strip().split(',')
        if note:
            self.archive_manager.archive_note(note, tags)
            messagebox.showinfo("Success", "Note archived successfully.")
            self.note_text.delete("1.0", tk.END)
            self.tag_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a note.")

    def restore_note(self):
        note_id = int(self.tag_entry.get())
        restored_note = self.archive_manager.restore_note(note_id)
        messagebox.showinfo("Restored Note", restored_note)

    def view_archived_notes(self):
        archived_notes = self.archive_manager.view_archived_notes()
        notes_display = "\n".join(f"{i}: {note}" for i, note in enumerate(archived_notes))
        messagebox.showinfo("Archived Notes", notes_display)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()