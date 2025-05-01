import tkinter as tk
from tkinter import messagebox
from notebook_manager import NotebookManager
from user_auth import UserAuth
from error_handling import ErrorHandling

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Note Management Application")
        self.notebook_manager = NotebookManager()
        self.user_auth = UserAuth()
        self.create_widgets()

    def create_widgets(self):
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        self.password_entry = tk.Entry(self.master, show='*')
        self.password_entry.pack()

        self.login_button = tk.Button(self.master, text="Login", command=self.login)
        self.login_button.pack()

        self.add_notebook_button = tk.Button(self.master, text="Add Notebook", command=self.add_notebook)
        self.add_notebook_button.pack()

        self.add_note_button = tk.Button(self.master, text="Add Note", command=self.add_note)
        self.add_note_button.pack()

        self.edit_note_button = tk.Button(self.master, text="Edit Note", command=self.edit_note)
        self.edit_note_button.pack()

        self.delete_note_button = tk.Button(self.master, text="Delete Note", command=self.delete_note)
        self.delete_note_button.pack()

        self.search_bar = tk.Entry(self.master)
        self.search_bar.pack()

        self.search_button = tk.Button(self.master, text="Search Notes", command=self.search_notes)
        self.search_button.pack()

        self.sort_button = tk.Button(self.master, text="Sort Notes", command=self.sort_notes)
        self.sort_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_auth.login_user(username, password):
            messagebox.showinfo("Login", "Login successful!")
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    def add_notebook(self):
        notebook_name = self.username_entry.get()  # Placeholder for user input
        try:
            self.notebook_manager.create_notebook(notebook_name)
            messagebox.showinfo("Notebook", f"Notebook '{notebook_name}' created.")
        except ValueError as e:
            ErrorHandling.handle_file_error(e)

    def add_note(self):
        notebook_name = self.username_entry.get()  # Placeholder for user input
        title = "Sample Note"  # Placeholder for user input
        content = "This is a sample note."  # Placeholder for user input
        try:
            self.notebook_manager.add_note(notebook_name, title, content)
            messagebox.showinfo("Note", f"Note '{title}' added to '{notebook_name}'.")
        except ValueError as e:
            ErrorHandling.handle_file_error(e)

    def edit_note(self):
        notebook_name = self.username_entry.get()  # Placeholder for user input
        title = "Sample Note"  # Placeholder for user input
        new_content = "This is the edited content."  # Placeholder for user input
        try:
            self.notebook_manager.edit_note(notebook_name, title, new_content)
            messagebox.showinfo("Note", f"Note '{title}' edited.")
        except ValueError as e:
            ErrorHandling.handle_file_error(e)

    def delete_note(self):
        notebook_name = self.username_entry.get()  # Placeholder for user input
        title = "Sample Note"  # Placeholder for user input
        try:
            self.notebook_manager.delete_note(notebook_name, title)
            messagebox.showinfo("Note", f"Note '{title}' deleted.")
        except ValueError as e:
            ErrorHandling.handle_file_error(e)

    def search_notes(self):
        notebook_name = self.username_entry.get()  # Placeholder for user input
        query = self.search_bar.get()
        try:
            results = self.notebook_manager.search_notes(notebook_name, query)
            messagebox.showinfo("Search Results", str(results))
        except ValueError as e:
            ErrorHandling.handle_file_error(e)

    def sort_notes(self):
        notebook_name = self.username_entry.get()  # Placeholder for user input
        try:
            sorted_notes = self.notebook_manager.sort_notes(notebook_name)
            messagebox.showinfo("Sorted Notes", str(sorted_notes))
        except ValueError as e:
            ErrorHandling.handle_file_error(e)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()